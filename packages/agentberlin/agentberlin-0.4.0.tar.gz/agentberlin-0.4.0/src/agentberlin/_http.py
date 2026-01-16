"""Internal HTTP client for Agent Berlin SDK."""

from typing import Any, Dict, Optional

import requests

from .exceptions import (
    AgentBerlinAPIError,
    AgentBerlinAuthenticationError,
    AgentBerlinConnectionError,
    AgentBerlinNotFoundError,
    AgentBerlinRateLimitError,
    AgentBerlinServerError,
)

__version__ = "0.1.0"


class HTTPClient:
    """Internal HTTP client with authentication and error handling."""

    def __init__(
        self,
        token: str,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        self._token = token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": f"agentberlin-python/{__version__}",
            }
        )

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request.

        Args:
            path: API endpoint path.
            json: Request body as dict.

        Returns:
            Response data as dict.

        Raises:
            AgentBerlinAPIError: On API errors.
            AgentBerlinConnectionError: On network errors.
        """
        url = f"{self._base_url}{path}"

        try:
            response = self._session.post(
                url,
                json=json,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout:
            raise AgentBerlinConnectionError(f"Request timed out after {self._timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise AgentBerlinConnectionError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise AgentBerlinConnectionError(f"Request failed: {e}")

        return self._handle_response(response)

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request.

        Args:
            path: API endpoint path.
            params: Query parameters.

        Returns:
            Response data as dict.

        Raises:
            AgentBerlinAPIError: On API errors.
            AgentBerlinConnectionError: On network errors.
        """
        url = f"{self._base_url}{path}"

        try:
            response = self._session.get(
                url,
                params=params,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout:
            raise AgentBerlinConnectionError(f"Request timed out after {self._timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise AgentBerlinConnectionError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise AgentBerlinConnectionError(f"Request failed: {e}")

        return self._handle_response(response)

    def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PATCH request.

        Args:
            path: API endpoint path.
            json: Request body as dict.

        Returns:
            Response data as dict.

        Raises:
            AgentBerlinAPIError: On API errors.
            AgentBerlinConnectionError: On network errors.
        """
        url = f"{self._base_url}{path}"

        try:
            response = self._session.patch(
                url,
                json=json,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout:
            raise AgentBerlinConnectionError(f"Request timed out after {self._timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise AgentBerlinConnectionError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise AgentBerlinConnectionError(f"Request failed: {e}")

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle response and raise appropriate exceptions."""
        # Success
        if response.ok:
            if response.content:
                return response.json()  # type: ignore[no-any-return]
            return {}

        # Parse error response
        try:
            error_data = response.json()
            message = error_data.get("message", error_data.get("error", "Unknown error"))
            error_code = error_data.get("code")
        except Exception:
            message = response.text or f"HTTP {response.status_code}"
            error_code = None
            error_data = {}

        # Map status codes to exceptions
        if response.status_code == 401:
            raise AgentBerlinAuthenticationError(message, details=error_data)
        elif response.status_code == 404:
            raise AgentBerlinNotFoundError(
                message,
                status_code=404,
                error_code=error_code,
                details=error_data,
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise AgentBerlinRateLimitError(
                message,
                retry_after=int(retry_after) if retry_after else None,
                details=error_data,
            )
        elif response.status_code >= 500:
            raise AgentBerlinServerError(
                message,
                status_code=response.status_code,
                error_code=error_code,
                details=error_data,
            )
        else:
            raise AgentBerlinAPIError(
                message,
                status_code=response.status_code,
                error_code=error_code,
                details=error_data,
            )
