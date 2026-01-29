from __future__ import annotations

import os
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import httpx as httpx_types

try:
    import httpx
except ImportError:
    httpx = None

logger = logging.getLogger(__name__)


class CNSDispatchError(Exception):
    """Raised when a CNS dispatch fails."""

    def __init__(
        self,
        message: str,
        intent: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        response: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.intent = intent
        self.status_code = status_code
        self.error_code = error_code
        self.response = response

    def __str__(self):
        return f"CNSDispatchError({self.intent}): {self.args[0]}"


class CNSClient:
    """
    Base client for dispatching intents via CNS Bus HTTP.

    All inter-organ communication goes through CNS Bus.
    This ensures:
    - Centralized routing and load balancing
    - Schema validation
    - Audit logging
    - Circuit breaking

    Example:
        cns = CNSClient()
        result = await cns.dispatch("vy.memory.remember.v1", {"content": "hello"})
        await cns.close()
    """

    def __init__(
        self,
        cns_bus_url: Optional[str] = None,
        timeout: float = 120.0,
    ):
        """
        Initialize CNS Client.

        Args:
            cns_bus_url: CNS Bus HTTP endpoint. Defaults to CNS_BUS_URL env var
                        or http://cns-bus:8081
            timeout: Default timeout for requests in seconds
        """
        if httpx is None:
            raise ImportError(
                "httpx is required for CNSClient. Install with: pip install httpx"
            )

        self.cns_bus_url = cns_bus_url or os.getenv(
            "CNS_BUS_URL", "https://cns-bus:8081"
        )
        self.default_timeout = timeout
        self._http: Optional[httpx_types.AsyncClient] = None
        self._closed = False

    async def _get_client(self) -> httpx_types.AsyncClient:
        """Get or create HTTP client (lazy initialization)."""
        if self._http is None or self._closed:
            self._http = httpx.AsyncClient(
                timeout=httpx.Timeout(self.default_timeout),
                headers={"Content-Type": "application/json"},
            )
            self._closed = False
        return self._http

    async def dispatch(
        self,
        intent: str,
        payload: Dict[str, Any],
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Dispatch an intent via CNS Bus.

        Args:
            intent: Intent to dispatch (e.g., "vy.memory.remember.v1")
            payload: Request payload
            timeout: Optional timeout override in seconds

        Returns:
            Response payload from the target organ

        Raises:
            CNSDispatchError: If dispatch fails
        """
        client = await self._get_client()
        url = f"{self.cns_bus_url}/dispatch"

        request_body = {
            "intent": intent,
            "payload": payload,
        }

        logger.debug(f"Dispatching intent: {intent}")

        try:
            response = await client.post(
                url,
                json=request_body,
                timeout=timeout or self.default_timeout,
            )

            # Parse response
            try:
                result = response.json()
            except Exception:
                raise CNSDispatchError(
                    f"Invalid JSON response: {response.text[:200]}",
                    intent=intent,
                    status_code=response.status_code,
                )

            # Check for HTTP errors
            if response.status_code >= 400:
                error_msg = result.get("error", result.get("message", "Unknown error"))
                raise CNSDispatchError(
                    error_msg,
                    intent=intent,
                    status_code=response.status_code,
                    error_code=result.get("code"),
                    response=result,
                )

            # Check for application-level errors in response
            if not result.get("ok", True) and "error" in result:
                raise CNSDispatchError(
                    result.get("error", "Dispatch failed"),
                    intent=intent,
                    error_code=result.get("code"),
                    response=result,
                )

            logger.debug(f"Dispatch successful: {intent}")
            return result

        except httpx.TimeoutException as e:
            raise CNSDispatchError(
                f"Timeout after {timeout or self.default_timeout}s",
                intent=intent,
            ) from e

        except httpx.ConnectError as e:
            logger.error(f"Connection failed to CNS Bus: {e}")
            raise CNSDispatchError(
                "Connection failed to CNS Bus",
                intent=intent,
            ) from e

        except CNSDispatchError:
            raise

        except Exception as e:
            logger.error(f"Unexpected error during dispatch: {e}")
            raise CNSDispatchError(
                "Unexpected error during dispatch",
                intent=intent,
            ) from e

    async def health(self) -> Dict[str, Any]:
        """
        Check CNS Bus health.

        Returns:
            Health status from CNS Bus
        """
        client = await self._get_client()
        url = f"{self.cns_bus_url}/health"

        try:
            response = await client.get(url, timeout=5.0)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def list_organs(self) -> Dict[str, Any]:
        """
        List registered organs in CNS Bus.

        Returns:
            List of registered organs with their intents
        """
        client = await self._get_client()
        url = f"{self.cns_bus_url}/organs"

        try:
            response = await client.get(url, timeout=10.0)
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e), "organs": []}

    async def close(self):
        """Close the HTTP client."""
        if self._http is not None and not self._closed:
            await self._http.aclose()
            self._closed = True
            self._http = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
