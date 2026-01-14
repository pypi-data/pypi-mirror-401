"""
Kurral Platform API Client

Client for sending captured sessions to the Kurral platform API.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

logger = logging.getLogger("kurral.mcp.platform_client")


@dataclass
class PlatformConfig:
    """Configuration for Kurral Platform API"""
    api_url: str = "https://api.kurral.dev"
    api_key: Optional[str] = None
    auto_send: bool = True
    auto_scan: bool = True  # Auto-trigger security scan after upload
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0


class KurralPlatformClient:
    """
    Client for communicating with Kurral Platform API.

    Handles:
    - Session upload (POST /api/sessions)
    - Auto-triggering security scans
    - Retry logic for reliability
    """

    def __init__(self, config: PlatformConfig):
        if not HTTPX_AVAILABLE:
            raise ImportError(
                "httpx not installed. Install with: pip install httpx"
            )

        self.config = config
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return bool(self.config.api_key)

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.config.api_url,
                timeout=self.config.timeout,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "kurral-mcp-proxy/1.0"
                }
            )
        return self._client

    async def close(self):
        """Close the HTTP client"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def upload_session(
        self,
        artifact: Dict[str, Any],
        agent_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Upload a session artifact to the Kurral platform.

        Args:
            artifact: The .kurral format session data
            agent_name: Optional agent name override

        Returns:
            Session response from platform, or None if failed
        """
        if not self.is_configured:
            logger.warning("Platform API key not configured, skipping upload")
            return None

        if not self.config.auto_send:
            logger.debug("Auto-send disabled, skipping upload")
            return None

        payload = {
            "artifact": artifact,
            "agent_name": agent_name
        }

        for attempt in range(self.config.retry_count):
            try:
                client = await self._get_client()
                response = await client.post("/api/sessions", json=payload)

                if response.status_code == 200 or response.status_code == 201:
                    session_data = response.json()
                    logger.info(
                        f"Session uploaded to platform: {session_data.get('id')} "
                        f"(kurral_id: {session_data.get('kurral_id')})"
                    )

                    # Auto-trigger security scan if enabled
                    if self.config.auto_scan:
                        await self._trigger_security_scan(session_data.get('id'))

                    return session_data

                elif response.status_code == 401:
                    logger.error("Platform API key invalid or expired")
                    return None

                elif response.status_code == 429:
                    # Rate limited, wait and retry
                    retry_after = int(response.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limited, waiting {retry_after}s")
                    await asyncio.sleep(retry_after)
                    continue

                else:
                    logger.error(
                        f"Failed to upload session: {response.status_code} - {response.text}"
                    )

            except httpx.TimeoutException:
                logger.warning(f"Upload timeout (attempt {attempt + 1}/{self.config.retry_count})")
                if attempt < self.config.retry_count - 1:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))

            except httpx.RequestError as e:
                logger.error(f"Upload request failed: {e}")
                if attempt < self.config.retry_count - 1:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))

        logger.error("Failed to upload session after all retries")
        return None

    async def _trigger_security_scan(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Trigger a security scan for the uploaded session.

        Args:
            session_id: The platform session ID

        Returns:
            Scan response from platform, or None if failed
        """
        if not session_id:
            return None

        try:
            client = await self._get_client()
            response = await client.post(
                "/api/security/scan",
                json={"session_id": session_id}
            )

            if response.status_code == 200 or response.status_code == 201:
                scan_data = response.json()
                logger.info(
                    f"Security scan triggered: {scan_data.get('id')} "
                    f"(status: {scan_data.get('status')})"
                )
                return scan_data
            else:
                logger.warning(
                    f"Failed to trigger security scan: {response.status_code}"
                )

        except Exception as e:
            logger.error(f"Error triggering security scan: {e}")

        return None

    async def get_scan_status(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a security scan.

        Args:
            scan_id: The scan ID

        Returns:
            Scan status response, or None if failed
        """
        if not self.is_configured:
            return None

        try:
            client = await self._get_client()
            response = await client.get(f"/api/security/{scan_id}")

            if response.status_code == 200:
                return response.json()

        except Exception as e:
            logger.error(f"Error getting scan status: {e}")

        return None


def create_platform_client(
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    auto_send: bool = True,
    auto_scan: bool = True
) -> KurralPlatformClient:
    """
    Factory function to create a platform client.

    Args:
        api_url: Platform API URL (default: https://api.kurral.dev)
        api_key: Platform API key
        auto_send: Whether to auto-send sessions
        auto_scan: Whether to auto-trigger security scans

    Returns:
        Configured KurralPlatformClient
    """
    import os

    config = PlatformConfig(
        api_url=api_url or os.environ.get("KURRAL_API_URL", "https://api.kurral.dev"),
        api_key=api_key or os.environ.get("KURRAL_API_KEY"),
        auto_send=auto_send,
        auto_scan=auto_scan
    )

    return KurralPlatformClient(config)
