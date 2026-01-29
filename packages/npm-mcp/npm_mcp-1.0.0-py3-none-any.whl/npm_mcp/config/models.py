"""Configuration models for NPM MCP Server.

This module defines Pydantic models for:
- InstanceConfig: Configuration for a single NPM instance
- GlobalSettings: Global MCP server settings
- Config: Complete configuration combining instances and settings

All models use Pydantic v2 for validation and serialization.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class InstanceConfig(BaseModel):
    """Configuration for a single NPM instance.

    Attributes:
        name: Unique identifier for the instance.
        host: Hostname or IP address of the NPM instance.
        port: Port number for NPM API (default: 81).
        use_https: Whether to use HTTPS for connections (default: False).
        verify_ssl: Whether to verify SSL certificates (default: True).
                    Set to False for self-signed certificates.
        username: Username for authentication (mutually exclusive with api_token).
        password: Password for authentication (required if username is provided).
        api_token: Pre-generated JWT token (alternative to username/password).
        default: Whether this is the default instance (default: False).
    """

    name: str = Field(..., min_length=1, description="Unique instance identifier")
    host: str = Field(..., min_length=1, description="NPM instance hostname or IP")
    port: int = Field(default=81, ge=1, le=65535, description="NPM API port")
    use_https: bool = Field(default=False, description="Use HTTPS for connections")
    verify_ssl: bool = Field(default=True, description="Verify SSL certs (False for self-signed)")
    username: str | None = Field(default=None, description="Authentication username")
    password: str | None = Field(default=None, description="Authentication password")
    api_token: str | None = Field(default=None, description="Pre-generated JWT token")
    default: bool = Field(default=False, description="Default instance flag")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "production",
                    "host": "npm.example.com",
                    "port": 81,
                    "use_https": True,
                    "verify_ssl": True,
                    "username": "admin@example.com",
                    "password": "secretpassword",
                    "default": True,
                },
                {
                    "name": "homelab",
                    "host": "192.168.1.100",
                    "port": 81,
                    "use_https": True,
                    "verify_ssl": False,
                    "api_token": "eyJhbGc...",
                },
            ]
        }
    }


class GlobalSettings(BaseModel):
    """Global MCP server settings.

    Attributes:
        default_timeout: Default timeout in seconds for HTTP requests.
        retry_attempts: Number of retry attempts for failed requests.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        cache_tokens: Whether to cache JWT tokens.
        token_cache_dir: Directory for storing cached tokens.
    """

    default_timeout: int = Field(
        default=30,
        ge=1,
        description="Default timeout in seconds for HTTP requests",
    )
    retry_attempts: int = Field(
        default=3,
        ge=0,
        description="Number of retry attempts for failed requests",
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    cache_tokens: bool = Field(
        default=True,
        description="Whether to cache JWT tokens",
    )
    token_cache_dir: Path = Field(
        default_factory=lambda: Path.home() / ".npm-mcp" / "tokens",
        description="Directory for storing cached tokens",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "default_timeout": 30,
                    "retry_attempts": 3,
                    "log_level": "INFO",
                    "cache_tokens": True,
                    "token_cache_dir": "~/.npm-mcp/tokens",
                }
            ]
        }
    }


class Config(BaseModel):
    """Complete configuration for NPM MCP Server.

    Attributes:
        instances: List of NPM instance configurations.
        settings: Global server settings.
    """

    instances: list[InstanceConfig] = Field(
        ...,
        min_length=1,
        description="List of NPM instance configurations",
    )
    settings: GlobalSettings = Field(
        default_factory=GlobalSettings,
        description="Global server settings",
    )

    @model_validator(mode="after")
    def validate_unique_instance_names(self) -> "Config":
        """Validate that all instance names are unique."""
        names = [instance.name for instance in self.instances]
        if len(names) != len(set(names)):
            msg = "Instance names must be unique. Found duplicate names."
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_single_default_instance(self) -> "Config":
        """Validate that at most one instance is marked as default."""
        default_instances = [instance for instance in self.instances if instance.default]
        if len(default_instances) > 1:
            msg = f"Only one instance can be marked as default. Found {len(default_instances)}."
            raise ValueError(msg)
        return self

    def get_default_instance(self) -> InstanceConfig | None:
        """Get the default instance.

        Returns:
            The instance marked as default, or the first instance if none is marked.
            Returns None if no instances are configured (shouldn't happen due to validation).
        """
        # Find instance marked as default
        for instance in self.instances:
            if instance.default:
                return instance

        # Fall back to first instance if none marked as default
        return self.instances[0] if self.instances else None

    def get_instance(self, name: str) -> InstanceConfig | None:
        """Get an instance by name.

        Args:
            name: The instance name to retrieve.

        Returns:
            The instance with the given name, or None if not found.
        """
        for instance in self.instances:
            if instance.name == name:
                return instance
        return None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "instances": [
                        {
                            "name": "production",
                            "host": "npm.example.com",
                            "port": 81,
                            "use_https": True,
                            "username": "admin@example.com",
                            "password": "secret",
                            "default": True,
                        }
                    ],
                    "settings": {
                        "default_timeout": 30,
                        "retry_attempts": 3,
                        "log_level": "INFO",
                        "cache_tokens": True,
                    },
                }
            ]
        }
    }
