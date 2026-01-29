"""
Centralized logging configuration for NPM MCP Server.

This module provides structured logging using structlog with features:
- Context-aware logging with instance/user binding
- Automatic credential redaction
- Performance timing decorators
- JSON output for production
- Configurable log levels
"""

import logging
import sys
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar

import structlog


def configure_logging(
    log_level: str = "INFO",
    json_output: bool = False,
) -> None:
    """
    Configure structlog for the application.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: If True, output logs as JSON; otherwise use console format

    Example:
        >>> # Development mode
        >>> configure_logging(log_level="DEBUG", json_output=False)

        >>> # Production mode
        >>> configure_logging(log_level="INFO", json_output=True)
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Configure processors for structlog
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Add JSON or console renderer based on config
    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    # Configure structlog
    structlog.configure(
        processors=processors,  # type: ignore[arg-type]
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def setup_logging(
    log_level: str = "INFO", json_output: bool = False
) -> structlog.stdlib.BoundLogger:
    """
    Set up logging configuration and return a root logger.

    This is a convenience function that combines configure_logging and get_logger.
    It configures structlog for the application and returns a logger instance.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: If True, output logs as JSON; otherwise use console format

    Returns:
        Configured structlog BoundLogger for the root logger

    Example:
        >>> logger = setup_logging(log_level="INFO")
        >>> logger.info("application started")
    """
    configure_logging(log_level=log_level, json_output=json_output)
    return get_logger("npm_mcp")


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structlog logger for the given module name.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured structlog BoundLogger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("message", key="value")
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]


def bind_context(
    logger: structlog.stdlib.BoundLogger,
    **kwargs: Any,  # noqa: ANN401
) -> structlog.stdlib.BoundLogger:
    """
    Bind context variables to a logger.

    Args:
        logger: Logger to bind context to
        **kwargs: Context key-value pairs to bind

    Returns:
        New logger with bound context

    Example:
        >>> logger = get_logger(__name__)
        >>> bound = bind_context(
        ...     logger,
        ...     instance_name="prod-npm",
        ...     user_id=123,
        ... )
        >>> bound.info("user action")  # Will include instance_name and user_id
    """
    return logger.bind(**kwargs)


class CredentialRedactor:
    """
    Redacts sensitive information from log data.

    Automatically removes or masks:
    - Passwords
    - Tokens
    - API keys
    - Secrets
    - Authorization headers

    Example:
        >>> redactor = CredentialRedactor()
        >>> data = {"username": "admin", "password": "secret"}
        >>> redacted = redactor.redact(data)
        >>> print(redacted)
        {'username': 'admin', 'password': '***REDACTED***'}
    """

    SENSITIVE_KEYS: ClassVar[set[str]] = {
        "password",
        "passwd",
        "pwd",
        "secret",
        "token",
        "api_key",
        "apikey",
        "access_token",
        "refresh_token",
        "authorization",
        "auth",
        "credentials",
        "credential",
    }

    REDACTED_VALUE: ClassVar[str] = "***REDACTED***"

    def redact(self, data: Any) -> Any:  # noqa: ANN401
        """
        Redact sensitive information from data.

        Args:
            data: Data to redact (typically dict, but handles any type)

        Returns:
            Data with sensitive values redacted
        """
        if isinstance(data, dict):
            return self._redact_dict(data)
        return data

    def _redact_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Redact sensitive keys in a dictionary recursively.

        Args:
            data: Dictionary to redact

        Returns:
            Dictionary with sensitive values redacted
        """
        redacted: dict[str, Any] = {}
        for key, value in data.items():
            # Always recurse into nested dicts first
            if isinstance(value, dict):
                redacted[key] = self._redact_dict(value)
            # Then check if key is sensitive (for leaf values)
            elif key.lower() in self.SENSITIVE_KEYS:
                redacted[key] = self.REDACTED_VALUE
            else:
                redacted[key] = value
        return redacted


def performance_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to log function execution time.

    Args:
        func: Function to time

    Returns:
        Wrapped function that logs execution time

    Example:
        >>> @performance_timer
        ... def slow_function():
        ...     time.sleep(1)
        ...     return "done"
        >>> result = slow_function()  # Logs execution time
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        logger = get_logger(func.__module__)
        start_time = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            logger.debug(
                "function_performance",
                function=func.__name__,
                elapsed_seconds=round(elapsed, 4),
            )

    return wrapper
