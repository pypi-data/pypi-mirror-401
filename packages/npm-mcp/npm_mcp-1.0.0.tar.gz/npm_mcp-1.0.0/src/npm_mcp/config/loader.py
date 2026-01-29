"""Configuration loader for NPM MCP Server.

This module provides functionality to load configuration from:
- YAML files
- Environment variables (JSON format)
- With environment variable substitution support (${VAR_NAME})

The loader validates all configuration using Pydantic models.
"""

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml

from npm_mcp.config.models import Config


class ConfigLoader:
    """Loads and validates NPM MCP Server configuration.

    Supports loading from:
    - YAML files (with env var substitution)
    - Environment variables (JSON format)
    - Default configuration paths
    """

    @staticmethod
    def get_default_path() -> Path:
        """Get the default configuration file path.

        Returns:
            Path to default config file: ~/.npm-mcp/instances.yaml
        """
        return Path.home() / ".npm-mcp" / "instances.yaml"

    def load_from_file(
        self,
        config_path: Path,
        substitute_env: bool = False,
    ) -> Config:
        """Load configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file.
            substitute_env: Whether to substitute environment variables.

        Returns:
            Validated Config object.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            yaml.YAMLError: If the YAML is malformed.
            ValidationError: If the config structure is invalid.
        """
        if not config_path.exists():
            msg = f"Configuration file not found: {config_path}"
            raise FileNotFoundError(msg)

        # Load YAML file
        with config_path.open("r") as f:
            config_data = yaml.safe_load(f)

        # Substitute environment variables if requested
        if substitute_env:
            config_data = self._substitute_env_vars(config_data)

        # Validate and return Config object
        return Config(**config_data)

    def load_from_env(self) -> Config:
        """Load configuration from NPM_MCP_CONFIG environment variable.

        The environment variable should contain a JSON string with the
        complete configuration structure.

        Returns:
            Validated Config object.

        Raises:
            ValueError: If NPM_MCP_CONFIG is not set.
            JSONDecodeError: If the JSON is malformed.
            ValidationError: If the config structure is invalid.
        """
        config_json = os.getenv("NPM_MCP_CONFIG")
        if not config_json:
            msg = "NPM_MCP_CONFIG environment variable is not set"
            raise ValueError(msg)

        # Parse JSON
        config_data = json.loads(config_json)

        # Validate and return Config object
        return Config(**config_data)

    def _substitute_env_vars(self, data: Any) -> Any:  # noqa: ANN401
        """Recursively substitute environment variables in config data.

        Supports two formats:
        - ${VAR_NAME} - Required variable (raises error if not set)
        - ${VAR_NAME:-default_value} - Optional with default

        Args:
            data: Configuration data (dict, list, str, or primitive).
                Uses Any to handle recursive dict/list/str/primitive types.

        Returns:
            Data with environment variables substituted.

        Raises:
            ValueError: If a required environment variable is not set.
        """
        if isinstance(data, dict):
            return {key: self._substitute_env_vars(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        if isinstance(data, str):
            return self._substitute_string(data)
        return data

    def _substitute_string(self, value: str) -> str:
        """Substitute environment variables in a string value.

        Args:
            value: String that may contain ${VAR_NAME} or ${VAR_NAME:-default}.

        Returns:
            String with environment variables substituted.

        Raises:
            ValueError: If a required environment variable is not set.
        """
        # Pattern matches ${VAR_NAME} or ${VAR_NAME:-default_value}
        pattern = r"\$\{([A-Z_][A-Z0-9_]*)(:-([^}]*))?\}"

        def replacer(match: re.Match[str]) -> str:
            var_name = match.group(1)
            has_default = match.group(2) is not None
            default_value = match.group(3) if has_default else None

            env_value = os.getenv(var_name)

            if env_value is None:
                if has_default:
                    return default_value or ""
                msg = f"Environment variable '{var_name}' is not set"
                raise ValueError(msg)

            return env_value

        return re.sub(pattern, replacer, value)


def load_config(
    config_path: Path | None = None,
    from_env: bool = False,
    substitute_env: bool = False,
) -> Config:
    """Helper function to load configuration.

    Args:
        config_path: Optional path to config file. Uses default if not provided.
        from_env: If True, load from NPM_MCP_CONFIG environment variable.
        substitute_env: If True, substitute environment variables in config.

    Returns:
        Validated Config object.

    Raises:
        FileNotFoundError: If config file not found.
        ValueError: If environment variable not set (when from_env=True).
        ValidationError: If config structure is invalid.
    """
    loader = ConfigLoader()

    if from_env:
        return loader.load_from_env()

    if config_path is None:
        config_path = loader.get_default_path()

    return loader.load_from_file(config_path, substitute_env=substitute_env)
