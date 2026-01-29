"""NPM API Client with automatic authentication.

This module provides an NPM-specific API client that:
- Automatically injects authentication headers
- Integrates with AuthManager
- Provides convenience methods for NPM API operations
- Handles 401 errors with automatic re-authentication

Usage:
    from npm_mcp.client.npm_client import NPMClient
    from npm_mcp.auth.manager import AuthManager
    from npm_mcp.config.models import InstanceConfig, Config, GlobalSettings

    instance = InstanceConfig(name="prod", host="npm.example.com", ...)
    config = Config(instances=[instance], settings=GlobalSettings())
    auth_manager = AuthManager(config)

    async with NPMClient(instance, auth_manager) as client:
        response = await client.get("/api/nginx/proxy-hosts")
        proxy_hosts = response.json()
"""

from typing import Any

import httpx
import structlog

from npm_mcp.auth.manager import AuthManager
from npm_mcp.client.http_client import HTTPClient
from npm_mcp.config.models import InstanceConfig

logger = structlog.get_logger(__name__)


class NPMClient:
    """NPM API client with automatic authentication and header injection.

    Wraps HTTPClient with NPM-specific functionality including automatic
    authentication header injection, base URL handling, and 401 retry logic.

    Attributes:
        instance_config: The NPM instance configuration.
        auth_manager: The authentication manager for token management.
        base_url: The base URL for the NPM instance API.
    """

    def __init__(
        self,
        instance_config: InstanceConfig,
        auth_manager: AuthManager,
    ) -> None:
        """Initialize NPM client.

        Args:
            instance_config: Configuration for the NPM instance.
            auth_manager: Authentication manager for token handling.
        """
        self.instance_config = instance_config
        self.auth_manager = auth_manager

        # Build base URL from instance config
        scheme = "https" if instance_config.use_https else "http"
        self.base_url = f"{scheme}://{instance_config.host}:{instance_config.port}"

        # Create underlying HTTP client
        self._http_client = HTTPClient(
            timeout=30,  # Default timeout
            max_retries=3,  # Default retries
            verify=instance_config.verify_ssl,
        )

        logger.debug(
            "npm_client_initialized",
            instance_name=instance_config.name,
            base_url=self.base_url,
            verify_ssl=instance_config.verify_ssl,
        )

    async def _get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers with valid token.

        Returns:
            Dictionary with Authorization header.
        """
        # Get valid token from auth manager
        token = await self.auth_manager.get_valid_token(self.instance_config.name)

        return {"Authorization": f"Bearer {token}"}

    async def _dispatch_request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Dispatch HTTP request to appropriate client method."""
        if method == "GET":
            return await self._http_client.get(url, headers=headers, **kwargs)
        if method == "POST":
            return await self._http_client.post(url, headers=headers, **kwargs)
        if method == "PUT":
            return await self._http_client.put(url, headers=headers, **kwargs)
        if method == "DELETE":
            return await self._http_client.delete(url, headers=headers, **kwargs)
        if method == "PATCH":
            return await self._http_client.patch(url, headers=headers, **kwargs)
        msg = f"Unsupported HTTP method: {method}"
        raise ValueError(msg)

    async def _handle_401_retry(
        self,
        method: str,
        url: str,
        endpoint: str,
        headers: dict[str, str],
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Handle 401 by re-authenticating and retrying once."""
        logger.info(
            "npm_client_401_reauthenticating",
            instance_name=self.instance_config.name,
            endpoint=endpoint,
        )
        await self.auth_manager.authenticate(self.instance_config.name)
        auth_headers = await self._get_auth_headers()
        headers.update(auth_headers)
        return await self._dispatch_request(method, url, headers, **kwargs)

    async def _request_with_auth(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make an authenticated request to the NPM API.

        Automatically injects authentication headers and handles 401 errors
        by re-authenticating and retrying the request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            endpoint: API endpoint path (e.g., "/api/nginx/proxy-hosts").
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.

        Raises:
            httpx.HTTPStatusError: For HTTP errors.
            httpx.ConnectError: For connection errors.
            httpx.TimeoutException: For timeout errors.
        """
        url = f"{self.base_url}{endpoint}"
        auth_headers = await self._get_auth_headers()
        headers = kwargs.pop("headers", {})
        headers.update(auth_headers)

        try:
            return await self._dispatch_request(method, url, headers, **kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return await self._handle_401_retry(method, url, endpoint, headers, **kwargs)
            raise

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a GET request to the NPM API.

        Args:
            endpoint: API endpoint path (e.g., "/api/nginx/proxy-hosts").
            params: Query parameters to include.
            headers: Additional HTTP headers (auth header added automatically).
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if params is not None:
            request_kwargs["params"] = params
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_auth("GET", endpoint, **request_kwargs)

    async def post(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a POST request to the NPM API.

        Args:
            endpoint: API endpoint path.
            json: JSON data to send in request body.
            headers: Additional HTTP headers (auth header added automatically).
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_auth("POST", endpoint, **request_kwargs)

    async def put(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a PUT request to the NPM API.

        Args:
            endpoint: API endpoint path.
            json: JSON data to send in request body.
            headers: Additional HTTP headers (auth header added automatically).
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_auth("PUT", endpoint, **request_kwargs)

    async def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a DELETE request to the NPM API.

        Args:
            endpoint: API endpoint path.
            headers: Additional HTTP headers (auth header added automatically).
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_auth("DELETE", endpoint, **request_kwargs)

    async def patch(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a PATCH request to the NPM API.

        Args:
            endpoint: API endpoint path.
            json: JSON data to send in request body.
            headers: Additional HTTP headers (auth header added automatically).
            **kwargs: Additional arguments to pass to HTTP client.

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_auth("PATCH", endpoint, **request_kwargs)

    async def close(self) -> None:
        """Close the NPM client and cleanup resources."""
        logger.debug(
            "npm_client_closing",
            instance_name=self.instance_config.name,
        )
        await self._http_client.close()
        logger.debug(
            "npm_client_closed",
            instance_name=self.instance_config.name,
        )

    async def __aenter__(self) -> "NPMClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:  # noqa: ANN401
        """Async context manager exit - cleanup resources."""
        await self.close()
