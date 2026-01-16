"""HTTP client for Zi API."""

import asyncio
import httpx
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

__all__ = ["ZiClient", "get_system_timezone"]


def get_system_timezone() -> Tuple[str, int]:
    """Get the system's timezone name and offset.

    Returns:
        Tuple of (timezone_name, offset_minutes)
        - timezone_name: IANA name like "Asia/Ho_Chi_Minh" or fallback to UTC offset
        - offset_minutes: Offset from UTC in minutes (e.g., -420 for UTC+7)
    """
    # Get offset in minutes (negative because time.timezone is seconds WEST of UTC)
    if time.daylight and time.localtime().tm_isdst > 0:
        offset_seconds = -time.altzone
    else:
        offset_seconds = -time.timezone
    offset_minutes = offset_seconds // 60

    # Try to get IANA timezone name
    tz_name = None

    # Method 1: Try /etc/timezone (Debian/Ubuntu)
    try:
        tz_file = Path("/etc/timezone")
        if tz_file.exists():
            tz_name = tz_file.read_text().strip()
    except Exception:
        pass

    # Method 2: Try to read /etc/localtime symlink (macOS, some Linux)
    if not tz_name:
        try:
            localtime = Path("/etc/localtime")
            if localtime.is_symlink():
                target = str(localtime.resolve())
                # Extract timezone from path like /usr/share/zoneinfo/Asia/Ho_Chi_Minh
                if "zoneinfo/" in target:
                    tz_name = target.split("zoneinfo/")[-1]
        except Exception:
            pass

    # Method 3: Try TZ environment variable
    if not tz_name:
        import os
        tz_name = os.environ.get("TZ")

    # Fallback: Use UTC offset format
    if not tz_name:
        hours = abs(offset_minutes) // 60
        mins = abs(offset_minutes) % 60
        sign = "+" if offset_minutes >= 0 else "-"
        tz_name = f"UTC{sign}{hours:02d}:{mins:02d}"

    return tz_name, offset_minutes

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds
RETRYABLE_STATUS_CODES = {502, 503, 504}  # Gateway errors


class ZiClient:
    """HTTP client for interacting with Zi API.

    Uses connection pooling for efficient HTTP requests.
    Includes retry logic for transient network errors.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.ziai.chat",
        timeout: float = 120.0,  # Zi responses can take time
    ):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )

    async def close(self):
        """Close the HTTP client and release connections."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        """Make HTTP request with retry logic for transient errors."""
        last_exception = None

        for attempt in range(MAX_RETRIES):
            try:
                resp = await self._client.request(method, url, **kwargs)

                # Retry on gateway errors
                if resp.status_code in RETRYABLE_STATUS_CODES:
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                        continue

                resp.raise_for_status()
                return resp

            except (httpx.ConnectError, httpx.ReadTimeout) as e:
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise

        if last_exception:
            raise last_exception
        raise RuntimeError("Request failed after retries")

    async def chat(
        self,
        message: str,
        thread_id: Optional[str] = None,
        language: str = "EN",
        timezone: Optional[str] = None,
        timezone_offset: Optional[int] = None,
    ) -> dict:
        """Send a message to Zi and get a response.

        Args:
            message: The message to send to Zi
            thread_id: Optional thread ID for conversation continuity
            language: "EN" or "VN"
            timezone: IANA timezone name (auto-detected from system if not provided)
            timezone_offset: Offset in minutes from UTC (auto-detected if not provided)

        Returns:
            dict with thread_id, response, and usage
        """
        # Auto-detect timezone from system if not provided
        if timezone is None or timezone_offset is None:
            sys_tz, sys_offset = get_system_timezone()
            if timezone is None:
                timezone = sys_tz
            if timezone_offset is None:
                timezone_offset = sys_offset

        payload = {
            "message": message,
            "language": language,
            "timezone": timezone,
            "timezone_offset": timezone_offset,
        }
        if thread_id:
            payload["thread_id"] = thread_id

        resp = await self._request_with_retry(
            "POST",
            f"{self.base_url}/chat/message",
            json=payload,
        )
        return resp.json()

    async def list_threads(self) -> list[dict]:
        """List all conversation threads.

        Returns:
            List of threads with id, title, updated_at
        """
        resp = await self._request_with_retry(
            "GET",
            f"{self.base_url}/chat/threads",
        )
        data = resp.json()
        return data.get("threads", [])

    async def get_thread(self, thread_id: str) -> dict:
        """Get conversation history for a thread.

        Args:
            thread_id: The thread ID

        Returns:
            dict with messages list
        """
        resp = await self._request_with_retry(
            "GET",
            f"{self.base_url}/chat/history/{thread_id}",
        )
        return resp.json()

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a conversation thread.

        Args:
            thread_id: The thread ID

        Returns:
            True if deleted successfully
        """
        try:
            resp = await self._request_with_retry(
                "DELETE",
                f"{self.base_url}/chat/history/{thread_id}",
            )
            return resp.status_code == 200
        except httpx.HTTPStatusError:
            return False
