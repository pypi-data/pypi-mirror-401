"""Configuration loading and management for integrations."""

from pathlib import Path
from typing import Any
import os
import re

import yaml
from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    """Authentication configuration."""

    api_key: str | None = None
    username: str | None = None
    password: str | None = None
    token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


class IntegrationConfig(BaseModel):
    """Standard configuration for integrations."""

    name: str
    vendor: str | None = None
    field_mappings: dict[str, Any] = Field(default_factory=dict)
    auth: AuthConfig | None = None
    batch_size: int = 100
    timeout_seconds: int = 30
    retry_attempts: int = 3
    custom: dict[str, Any] = Field(default_factory=dict)


def substitute_env_vars(data: Any) -> Any:
    """Recursively substitute environment variable references.

    Supports ${VAR_NAME} syntax.

    Args:
        data: Configuration data (dict, list, str, etc.)

    Returns:
        Data with environment variables substituted
    """
    if isinstance(data, dict):
        return {k: substitute_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [substitute_env_vars(item) for item in data]
    elif isinstance(data, str):
        # Match ${VAR_NAME} pattern
        pattern = r"\$\{([^}]+)\}"
        matches = re.findall(pattern, data)
        for var_name in matches:
            env_value = os.getenv(var_name, "")
            data = data.replace(f"${{{var_name}}}", env_value)
        return data
    else:
        return data


def load_config(path: Path | str) -> IntegrationConfig:
    """Load integration configuration from YAML file.

    Supports environment variable substitution with ${VAR_NAME} syntax.

    Args:
        path: Path to configuration file

    Returns:
        IntegrationConfig instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        raw_data = yaml.safe_load(f)

    # Substitute environment variables
    data = substitute_env_vars(raw_data)

    # Extract integration section if present
    if "integration" in data:
        config_data = data["integration"]
        
        # Move auth if at root level
        if "auth" in data and "auth" not in config_data:
            config_data["auth"] = data["auth"]
            
        # Move field_mappings if at root level
        if "field_mappings" in data and "field_mappings" not in config_data:
            config_data["field_mappings"] = data["field_mappings"]
    else:
        config_data = data

    return IntegrationConfig.model_validate(config_data)
