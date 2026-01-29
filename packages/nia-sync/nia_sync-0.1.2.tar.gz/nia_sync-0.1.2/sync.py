"""
Sync engine for Nia Local Sync CLI.

Handles:
- Extracting data from local sources (databases, folders)
- Uploading to cloud API
- Cursor management for incremental sync
"""
import os
import logging
import random
import time
from pathlib import Path
from typing import Any
import httpx

from config import API_BASE_URL, get_api_key
from extractor import extract_incremental, detect_source_type

logger = logging.getLogger(__name__)

SYNC_TIMEOUT = 60  # 1 minute per sync request (reduced from 2 min)
CONNECT_TIMEOUT = 10  # 10 second connection timeout
MAX_FILES_PER_BATCH = 500  # Keep below backend limit (1000)
MAX_RETRIES = 4
RETRY_BASE_DELAY = 1.5
RETRY_MAX_DELAY = 15.0

# Reusable client for connection pooling
_http_client: httpx.Client | None = None

def get_http_client() -> httpx.Client:
    """Get or create HTTP client with connection pooling."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client(
            timeout=httpx.Timeout(SYNC_TIMEOUT, connect=CONNECT_TIMEOUT),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )
    return _http_client


def sync_all_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Sync all configured sources.

    Args:
        sources: List of source configs from cloud API

    Returns:
        List of results for each source
    """
    results = []

    for source in sources:
        result = sync_source(source)
        results.append(result)

    return results


def sync_source(source: dict[str, Any]) -> dict[str, Any]:
    """
    Sync a single source.

    Args:
        source: Source config from cloud API with:
            - local_folder_id: UUID of the local folder
            - path: Local path to sync
            - detected_type: Type of source
            - cursor: Current sync cursor

    Returns:
        Result dict with status, path, and stats
    """
    local_folder_id = source.get("local_folder_id")
    path = source.get("path", "")
    detected_type = source.get("detected_type")
    cursor = source.get("cursor", {})

    # Expand ~ in path
    path = os.path.expanduser(path)

    # Validate path exists
    if not os.path.exists(path):
        error_message = f"Path does not exist: {path}"
        report_sync_error(local_folder_id, error_message, path)
        return {
            "path": path,
            "status": "error",
            "error": error_message,
        }

    # Auto-detect type if not specified
    if not detected_type:
        detected_type = detect_source_type(path)

    logger.info(f"Syncing {path} (type={detected_type})")

    try:
        # Extract data incrementally
        extraction_result = extract_incremental(
            path=path,
            source_type=detected_type,
            cursor=cursor,
        )

        files = extraction_result.get("files", [])
        new_cursor = extraction_result.get("cursor", {})
        stats = extraction_result.get("stats", {})

        if not files:
            logger.info(f"No new data to sync for {path}")
            return {
                "path": path,
                "status": "success",
                "added": 0,
                "message": "No new data",
            }

        # Upload to backend in batches
        upload_result = upload_sync_batches(
            local_folder_id=local_folder_id,
            files=files,
            cursor=new_cursor,
            stats=stats,
        )

        if upload_result.get("status") == "ok":
            # Update source cursor in-place so subsequent syncs use it
            source["cursor"] = new_cursor
            return {
                "path": path,
                "status": "success",
                "added": len(files),
                "chunks_indexed": upload_result.get("chunks_indexed", 0),
                "new_cursor": new_cursor,
            }
        else:
            report_sync_error(local_folder_id, upload_result.get("message", "Upload failed"), path)
            return {
                "path": path,
                "status": "error",
                "error": upload_result.get("message", "Upload failed"),
            }

    except PermissionError:
        error_message = "Permission denied. Grant Full Disk Access in System Settings > Privacy & Security."
        report_sync_error(local_folder_id, error_message, path)
        return {
            "path": path,
            "status": "error",
            "error": error_message,
        }
    except Exception as e:
        logger.error(f"Error syncing {path}: {e}", exc_info=True)
        report_sync_error(local_folder_id, str(e), path)
        return {
            "path": path,
            "status": "error",
            "error": str(e),
        }


def upload_sync_data(
    local_folder_id: str,
    files: list[dict[str, Any]],
    cursor: dict[str, Any],
    stats: dict[str, Any],
    is_final_batch: bool = True,
) -> dict[str, Any]:
    """
    Upload extracted data to the cloud API.

    Args:
        local_folder_id: UUID of the local folder
        files: List of extracted files with path, content, metadata
        cursor: New cursor after extraction
        stats: Extraction stats

    Returns:
        API response dict
    """
    api_key = get_api_key()
    if not api_key:
        return {"status": "error", "message": "Not authenticated"}

    try:
        client = get_http_client()
        response = _post_with_retries(
            client=client,
            url=f"{API_BASE_URL}/v2/daemon/sync",
            headers={"Authorization": f"Bearer {api_key}"},
            payload={
                "local_folder_id": local_folder_id,
                "files": files,
                "cursor": cursor,
                "stats": stats,
                "is_final_batch": is_final_batch,
            },
        )

        if response is None:
            return {"status": "error", "message": "Request failed after retries"}

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"status": "error", "message": "Authentication failed"}
        elif response.status_code == 404:
            return {"status": "error", "message": "Local folder not found"}
        else:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text or f"HTTP {response.status_code}"
            return {"status": "error", "message": f"API error: {detail}"}

    except httpx.TimeoutException:
        return {"status": "error", "message": "Request timeout"}
    except httpx.RequestError as e:
        return {"status": "error", "message": f"Network error: {e}"}


def upload_sync_batches(
    local_folder_id: str,
    files: list[dict[str, Any]],
    cursor: dict[str, Any],
    stats: dict[str, Any],
) -> dict[str, Any]:
    """Upload files in batches and only advance cursor after all succeed."""
    if not files:
        return {"status": "ok", "chunks_indexed": 0}

    total_batches = max(1, (len(files) + MAX_FILES_PER_BATCH - 1) // MAX_FILES_PER_BATCH)
    chunks_indexed = 0

    for batch_index, batch in enumerate(_iter_batches(files, MAX_FILES_PER_BATCH), start=1):
        is_last_batch = batch_index == total_batches
        result = upload_sync_data(
            local_folder_id=local_folder_id,
            files=batch,
            cursor=cursor if is_last_batch else {},
            stats=stats if is_last_batch else {},
            is_final_batch=is_last_batch,
        )

        if result.get("status") != "ok":
            return result

        chunks_indexed += result.get("chunks_indexed", 0)

    return {"status": "ok", "chunks_indexed": chunks_indexed}


def report_sync_error(local_folder_id: str | None, error: str, path: str | None = None) -> None:
    """Report local sync errors to backend for UI visibility."""
    if not local_folder_id:
        return
    api_key = get_api_key()
    if not api_key:
        return

    try:
        client = get_http_client()
        _post_with_retries(
            client=client,
            url=f"{API_BASE_URL}/v2/daemon/sources/{local_folder_id}/error",
            headers={"Authorization": f"Bearer {api_key}"},
            payload={"error": error, "path": path},
        )
    except Exception:
        logger.debug("Failed to report sync error", exc_info=True)


def _iter_batches(items: list[dict[str, Any]], size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def _post_with_retries(
    client: httpx.Client,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> httpx.Response | None:
    delay = RETRY_BASE_DELAY
    for attempt in range(MAX_RETRIES):
        try:
            response = client.post(url, headers=headers, json=payload)
            if response.status_code in {429} or response.status_code >= 500:
                raise httpx.HTTPStatusError(
                    f"Retryable status {response.status_code}",
                    request=response.request,
                    response=response,
                )
            return response
        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as e:
            is_last_attempt = attempt >= MAX_RETRIES - 1
            if is_last_attempt:
                logger.warning(f"POST failed after retries: {e}")
                return None
            jitter = random.uniform(0.8, 1.2)
            time.sleep(min(RETRY_MAX_DELAY, delay) * jitter)
            delay *= 2
