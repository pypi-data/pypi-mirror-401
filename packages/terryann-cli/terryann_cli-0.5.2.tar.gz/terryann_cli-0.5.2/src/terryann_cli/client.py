"""HTTP client for TerryAnn Gateway."""

from typing import Optional

import httpx

from terryann_cli.config import Config


class GatewayClient:
    """Async HTTP client for TerryAnn Gateway."""

    def __init__(self, config: Config, auth_token: Optional[str] = None):
        self.config = config
        self.base_url = config.gateway_url.rstrip("/")
        self.auth_token = auth_token

    def _get_headers(self) -> dict:
        """Build request headers including auth if available."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    async def health_check(self) -> dict:
        """Check gateway health status."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/health",
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return response.json()

    async def send_message(
        self, session_id: str, message: str, surface: str = "cli"
    ) -> dict:
        """Send a message to the gateway.

        Args:
            session_id: Conversation session ID
            message: User message text
            surface: Client surface identifier (default: "cli")

        Returns:
            Gateway response dict
        """
        async with httpx.AsyncClient(timeout=180.0) as client:  # 3 min for full pipeline
            response = await client.post(
                f"{self.base_url}/gateway/message",
                headers=self._get_headers(),
                json={"session_id": session_id, "message": message, "surface": surface},
            )
            response.raise_for_status()
            return response.json()
