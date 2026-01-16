"""HTTP client for Zi API."""

import asyncio
import httpx
from typing import Optional

__all__ = ["ZiClient"]

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
        timezone: str = "Asia/Ho_Chi_Minh",
        timezone_offset: int = -420,  # UTC+7
    ) -> dict:
        """Send a message to Zi and get a response.

        Args:
            message: The message to send to Zi
            thread_id: Optional thread ID for conversation continuity
            language: "EN" or "VN"
            timezone: IANA timezone name (e.g., "Asia/Ho_Chi_Minh")
            timezone_offset: Offset in minutes from UTC (e.g., -420 for UTC+7)

        Returns:
            dict with thread_id, response, and usage
        """
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
