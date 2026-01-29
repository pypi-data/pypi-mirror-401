"""
Configuration management for Cercalia SDK.

Supports both environment variables and manual configuration.
"""

import os
from typing import Any, Optional, Union

from pydantic import BaseModel, Field

from .utils.logger import logger


class CercaliaConfig(BaseModel):
    """Configuration for Cercalia API connection."""

    api_key: str = Field(..., description="Cercalia API key")
    base_url: str = Field(
        default="https://lb.cercalia.com/services/v2/json",
        description="Base URL for Cercalia API",
    )


class SDKConfig(BaseModel):
    """SDK configuration including Cercalia API settings and debug options."""

    cercalia: CercaliaConfig
    debug: bool = Field(default=False, description="Enable debug logging")


# Global configuration instance
_config: Optional[SDKConfig] = None


def get_config() -> SDKConfig:
    """
    Get the current SDK configuration.

    If no configuration has been set, creates one from environment variables.

    Returns:
        Current SDKConfig instance

    Example:
        >>> config = get_config()
        >>> print(config.cercalia.api_key)
    """
    global _config

    if _config is None:
        # Create default config from environment variables
        _config = SDKConfig(
            cercalia=CercaliaConfig(
                api_key=os.environ.get("CERCALIA_API_KEY", ""),
                base_url=os.environ.get(
                    "CERCALIA_BASE_URL", "https://lb.cercalia.com/services/v2/json"
                ),
            ),
            debug=os.environ.get("CERCALIA_DEBUG", "").lower() in ("true", "1", "yes"),
        )

        if _config.debug:
            logger.set_debug(True)

    return _config


def set_config(
    cercalia: Optional[Union[CercaliaConfig, dict[str, Any]]] = None,
    debug: Optional[bool] = None,
) -> None:
    """
    Update the SDK configuration.

    Can be used both in backend and application environments.

    Args:
        cercalia: Cercalia API configuration (CercaliaConfig or dict)
        debug: Enable or disable debug logging

    Example:
        >>> set_config(
        ...     cercalia={"api_key": "your-api-key", "base_url": "https://..."},
        ...     debug=True
        ... )
    """
    global _config

    current = get_config()

    # Update cercalia config
    if cercalia is not None:
        if isinstance(cercalia, dict):
            # Merge with existing config
            new_cercalia = CercaliaConfig(
                api_key=cercalia.get("api_key", current.cercalia.api_key),
                base_url=cercalia.get("base_url", current.cercalia.base_url),
            )
        else:
            new_cercalia = cercalia
    else:
        new_cercalia = current.cercalia

    # Update debug setting
    new_debug = debug if debug is not None else current.debug

    _config = SDKConfig(cercalia=new_cercalia, debug=new_debug)

    if new_debug:
        logger.set_debug(True)
    else:
        logger.set_debug(False)


def validate_config() -> None:
    """
    Validate the current configuration.

    Logs warnings if configuration is incomplete.
    """
    config = get_config()

    if config.debug:
        logger.set_debug(True)

    if not config.cercalia.api_key:
        logger.warn("Warning: CERCALIA_API_KEY is not set")


def reset_config() -> None:
    """
    Reset configuration to default (from environment variables).

    Useful for testing or reinitializing the SDK.
    """
    global _config
    _config = None
