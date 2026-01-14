"""
Configuration utilities for Cindergrace applications.

Provides type-safe environment variable helpers and a base configuration class.

Usage:
    from cindergrace_common import BaseConfig, env_bool, env_int, env_str

    class Config(BaseConfig):
        APP_PREFIX = "MYAPP"

        # Using class-level env helpers
        PORT = env_int("MYAPP_PORT", 7865)
        DEBUG = env_bool("MYAPP_DEBUG", False)
        NAME = env_str("MYAPP_NAME", "My Application")

        # Or using inherited methods
        @classmethod
        def get_custom_setting(cls):
            return cls.env_int("MYAPP_CUSTOM", 100)
"""

import os
from typing import TypeVar

T = TypeVar("T")


def env_str(key: str, default: str = "") -> str:
    """Get string from environment variable.

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default)


def env_int(key: str, default: int = 0) -> int:
    """Get integer from environment variable.

    Args:
        key: Environment variable name
        default: Default value if not set or invalid

    Returns:
        Parsed integer or default
    """
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def env_bool(key: str, default: bool = False) -> bool:
    """Get boolean from environment variable.

    Truthy values: "1", "true", "yes", "on" (case-insensitive)
    Falsy values: "0", "false", "no", "off", "" (case-insensitive)

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        Parsed boolean or default
    """
    value = os.environ.get(key)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


class BaseConfig:
    """Base configuration class for Cindergrace applications.

    Provides common patterns for environment-based configuration.
    Subclass this and define your app-specific settings.

    Class attributes:
        APP_PREFIX: Prefix for all environment variables (e.g., "SYSMON")

    Example:
        class Config(BaseConfig):
            APP_PREFIX = "SYSMON"

            # Define settings using env helpers
            PORT = env_int("SYSMON_PORT", 7865)
            ALLOW_REMOTE = env_bool("SYSMON_ALLOW_REMOTE", False)

            # Or use prefixed helpers
            @classmethod
            def get_port(cls):
                return cls.prefixed_int("PORT", 7865)
    """

    APP_PREFIX: str = "CINDERGRACE"

    @classmethod
    def prefixed_key(cls, key: str) -> str:
        """Get full environment variable name with prefix.

        Args:
            key: Short key name (e.g., "PORT")

        Returns:
            Full key with prefix (e.g., "SYSMON_PORT")
        """
        return f"{cls.APP_PREFIX}_{key}"

    @classmethod
    def prefixed_str(cls, key: str, default: str = "") -> str:
        """Get prefixed string environment variable."""
        return env_str(cls.prefixed_key(key), default)

    @classmethod
    def prefixed_int(cls, key: str, default: int = 0) -> int:
        """Get prefixed integer environment variable."""
        return env_int(cls.prefixed_key(key), default)

    @classmethod
    def prefixed_bool(cls, key: str, default: bool = False) -> bool:
        """Get prefixed boolean environment variable."""
        return env_bool(cls.prefixed_key(key), default)

    @classmethod
    def get_env_docs(cls) -> dict[str, str]:
        """Get documentation for all environment variables.

        Override this in subclasses to document available settings.

        Returns:
            Dict mapping env var names to descriptions
        """
        return {}
