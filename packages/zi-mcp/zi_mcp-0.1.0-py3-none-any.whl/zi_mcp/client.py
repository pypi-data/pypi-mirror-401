"""HTTP client for Zi API."""

import httpx
from typing import Optional


class ZiClient:
    """HTTP client for interacting with Zi API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.ziai.chat",
        timeout: float = 120.0,  # Zi responses can take time
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    async def chat(
        self,
        message: str,
        thread_id: Optional[str] = None,
        language: str = "EN",
    ) -> dict:
        """Send a message to Zi and get a response.

        Args:
            message: The message to send to Zi
            thread_id: Optional thread ID for conversation continuity
            language: "EN" or "VN"

        Returns:
            dict with thread_id, response, and usage
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "message": message,
                "language": language,
            }
            if thread_id:
                payload["thread_id"] = thread_id

            resp = await client.post(
                f"{self.base_url}/chat/message",
                headers=self.headers,
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()

    async def list_threads(self) -> list[dict]:
        """List all conversation threads.

        Returns:
            List of threads with id, title, updated_at
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}/chat/threads",
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("threads", [])

    async def get_thread(self, thread_id: str) -> dict:
        """Get conversation history for a thread.

        Args:
            thread_id: The thread ID

        Returns:
            dict with messages list
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}/chat/history/{thread_id}",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a conversation thread.

        Args:
            thread_id: The thread ID

        Returns:
            True if deleted successfully
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.delete(
                f"{self.base_url}/chat/history/{thread_id}",
                headers=self.headers,
            )
            return resp.status_code == 200
