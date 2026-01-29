"""HTTP Client with retry logic and connection pooling.

This module provides an async HTTP client wrapper around httpx with:
- Automatic retry logic using tenacity
- Connection pooling
- Timeout handling
- Error response handling

Usage:
    from npm_mcp.client.http_client import HTTPClient

    async with HTTPClient(timeout=30, max_retries=3) as client:
        response = await client.get("https://api.example.com/data")
        print(response.json())
"""

from typing import Any

import httpx
import structlog
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = structlog.get_logger(__name__)


def _should_retry_on_http_error(exception: BaseException) -> bool:
    """Determine if an HTTP error should be retried.

    Args:
        exception: The exception to check.

    Returns:
        True if the exception is retryable, False otherwise.
    """
    # Retry on connection errors, timeouts, and network errors
    if isinstance(exception, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
        return True

    # Retry on 5xx server errors (500, 502, 503, 504)
    if isinstance(exception, httpx.HTTPStatusError):
        status_code = exception.response.status_code
        return status_code >= 500

    return False


def _log_http_error(
    exc: httpx.HTTPStatusError,
    method: str,
    url: str,
    max_retries: int,
) -> None:
    """Log HTTP error based on status code."""
    status_code = exc.response.status_code
    if status_code < 500:
        logger.warning(
            "http_request_client_error",
            method=method,
            url=url,
            status_code=status_code,
        )
    else:
        logger.error(
            "http_request_server_error_after_retries",
            method=method,
            url=url,
            status_code=status_code,
            max_retries=max_retries,
        )


def _log_network_error(
    exc: httpx.ConnectError | httpx.TimeoutException | httpx.NetworkError,
    method: str,
    url: str,
    max_retries: int,
) -> None:
    """Log network error after retries exhausted."""
    logger.error(
        "http_request_failed_after_retries",
        method=method,
        url=url,
        error=str(exc),
        max_retries=max_retries,
    )


def _handle_retry_failure(
    retry_error: RetryError,
    method: str,
    url: str,
    max_retries: int,
) -> None:
    """Handle retry failure by extracting and re-raising original exception."""
    if not retry_error.last_attempt.failed:
        raise retry_error

    original = retry_error.last_attempt.exception()
    if not isinstance(original, BaseException):
        raise retry_error

    if isinstance(original, httpx.HTTPStatusError):
        _log_http_error(original, method, url, max_retries)
        raise original from retry_error

    if isinstance(original, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
        _log_network_error(original, method, url, max_retries)
        raise original from retry_error

    raise original from retry_error


class HTTPClient:
    """Async HTTP client with retry logic and connection pooling.

    Provides a wrapper around httpx.AsyncClient with automatic retry logic
    for transient failures, configurable timeouts, and connection pooling.

    Attributes:
        timeout: Default timeout for requests in seconds.
        max_retries: Maximum number of retry attempts for transient failures.
        retry_min_wait: Minimum wait time between retries in seconds.
        retry_max_wait: Maximum wait time between retries in seconds.
        max_connections: Maximum number of connections in the pool.
        max_keepalive_connections: Maximum number of keep-alive connections.
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_min_wait: int = 1,
        retry_max_wait: int = 10,
        max_connections: int = 100,
        max_keepalive_connections: int = 20,
        verify: bool = True,
    ) -> None:
        """Initialize HTTP client with retry and connection pool settings.

        Args:
            timeout: Default request timeout in seconds. Default: 30.
            max_retries: Maximum retry attempts for transient failures. Default: 3.
            retry_min_wait: Minimum wait time between retries in seconds. Default: 1.
            retry_max_wait: Maximum wait time between retries in seconds. Default: 10.
            max_connections: Maximum connections in pool. Default: 100.
            max_keepalive_connections: Max keep-alive connections. Default: 20.
            verify: Whether to verify SSL certificates. Default: True.
                    Set to False for self-signed certificates.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_min_wait = retry_min_wait
        self.retry_max_wait = retry_max_wait
        self.max_connections = max_connections
        self.max_keepalive_connections = max_keepalive_connections
        self._verify = verify

        # Configure connection limits for the client
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
        )

        # Create the underlying httpx client
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=limits,
            verify=verify,
        )

        logger.debug(
            "http_client_initialized",
            timeout=timeout,
            max_retries=max_retries,
            max_connections=max_connections,
            verify=verify,
        )

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make an HTTP request with automatic retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            url: The URL to request.
            **kwargs: Additional arguments to pass to httpx request.

        Returns:
            httpx.Response object.

        Raises:
            httpx.HTTPStatusError: For non-retryable HTTP errors (4xx).
            httpx.ConnectError: If connection fails after all retries.
            httpx.TimeoutException: If request times out after all retries.
            RetryError: If max retries exceeded for retryable errors.
        """
        if "timeout" in kwargs:
            kwargs["timeout"] = httpx.Timeout(kwargs["timeout"])

        retry_logic = AsyncRetrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(min=self.retry_min_wait, max=self.retry_max_wait),
            retry=retry_if_exception(_should_retry_on_http_error),
        )

        try:
            async for attempt in retry_logic:
                with attempt:
                    logger.debug(
                        "http_request_attempt",
                        method=method,
                        url=url,
                        attempt=attempt.retry_state.attempt_number,
                    )
                    response = await self._client.request(method, url, **kwargs)
                    response.raise_for_status()
                    logger.debug(
                        "http_request_success",
                        method=method,
                        url=url,
                        status_code=response.status_code,
                    )
                    return response

        except RetryError as e:
            _handle_retry_failure(e, method, url, self.max_retries)

        except httpx.HTTPStatusError as e:
            if e.response.status_code < 500:
                _log_http_error(e, method, url, self.max_retries)
            raise

        # Unreachable but satisfies mypy
        msg = "Unreachable code"
        raise RuntimeError(msg)  # pragma: no cover

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a GET request.

        Args:
            url: The URL to request.
            params: Query parameters to include.
            headers: HTTP headers to include.
            **kwargs: Additional arguments to pass to httpx (including timeout).

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if params is not None:
            request_kwargs["params"] = params
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_retry("GET", url, **request_kwargs)

    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a POST request.

        Args:
            url: The URL to request.
            json: JSON data to send in request body.
            headers: HTTP headers to include.
            **kwargs: Additional arguments to pass to httpx (including timeout).

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_retry("POST", url, **request_kwargs)

    async def put(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a PUT request.

        Args:
            url: The URL to request.
            json: JSON data to send in request body.
            headers: HTTP headers to include.
            **kwargs: Additional arguments to pass to httpx (including timeout).

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_retry("PUT", url, **request_kwargs)

    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a DELETE request.

        Args:
            url: The URL to request.
            headers: HTTP headers to include.
            **kwargs: Additional arguments to pass to httpx (including timeout).

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_retry("DELETE", url, **request_kwargs)

    async def patch(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:
        """Make a PATCH request.

        Args:
            url: The URL to request.
            json: JSON data to send in request body.
            headers: HTTP headers to include.
            **kwargs: Additional arguments to pass to httpx (including timeout).

        Returns:
            httpx.Response object.
        """
        request_kwargs = kwargs.copy()
        if json is not None:
            request_kwargs["json"] = json
        if headers is not None:
            request_kwargs["headers"] = headers

        return await self._request_with_retry("PATCH", url, **request_kwargs)

    async def close(self) -> None:
        """Close the HTTP client and cleanup resources."""
        logger.debug("http_client_closing")
        await self._client.aclose()
        logger.debug("http_client_closed")

    async def __aenter__(self) -> "HTTPClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:  # noqa: ANN401
        """Async context manager exit - cleanup resources."""
        await self.close()
