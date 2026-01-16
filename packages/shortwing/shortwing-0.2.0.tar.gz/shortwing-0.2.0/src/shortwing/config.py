"""Configuration and credential resolution."""

import configparser
import os
from typing import Optional

import dimcli

from shortwing.exceptions import ConfigurationError

DEFAULT_ENDPOINT = "https://app.dimensions.ai/api/dsl/v2"
USER_CONFIG_FILE_PATH = os.path.expanduser("~/.dimensions/dsl.ini")


def read_dsl_ini(instance: str = "live") -> tuple[Optional[str], Optional[str]]:
    """
    Read credentials from dsl.ini file.

    Checks:
    1. ./dsl.ini in current working directory
    2. ~/.dimensions/dsl.ini

    Args:
        instance: The instance name to read (default: "live")

    Returns:
        Tuple of (api_key, endpoint) or (None, None) if not found
    """
    # Check current directory first, then user directory
    config_paths = [
        os.path.join(os.getcwd(), "dsl.ini"),
        USER_CONFIG_FILE_PATH,
    ]

    config = configparser.ConfigParser()
    for path in config_paths:
        if os.path.exists(path):
            config.read(path)
            break
    else:
        return None, None

    section_name = f"instance.{instance}"
    if section_name not in config:
        return None, None

    section = config[section_name]
    api_key = section.get("key", "").strip() or None
    api_endpoint = section.get("url", "").strip() or None

    return api_key, api_endpoint


def resolve_credentials(
    key: Optional[str] = None,
    endpoint: Optional[str] = None,
    instance: str = "live",
) -> tuple[str, str]:
    """
    Resolve API credentials from flags, environment, or dsl.ini.

    Priority order:
    1. CLI flags (--key, --endpoint)
    2. Environment variables (DIMENSIONS_KEY, DIMENSIONS_ENDPOINT)
    3. dsl.ini file (~/.dimensions/dsl.ini)

    Args:
        key: API key from CLI flag
        endpoint: API endpoint from CLI flag
        instance: Instance name for dsl.ini (default: "live")

    Returns:
        Tuple of (api_key, endpoint)

    Raises:
        ConfigurationError: If no API key is found
    """
    # Priority 1: CLI flags
    api_key = key
    api_endpoint = endpoint

    # Priority 2: Environment variables
    if not api_key:
        api_key = os.environ.get("DIMENSIONS_KEY")
    if not api_endpoint:
        api_endpoint = os.environ.get("DIMENSIONS_ENDPOINT")

    # Priority 3: dsl.ini file
    if not api_key or not api_endpoint:
        ini_key, ini_endpoint = read_dsl_ini(instance)
        if not api_key:
            api_key = ini_key
        if not api_endpoint:
            api_endpoint = ini_endpoint

    # Final fallback for endpoint
    if not api_endpoint:
        api_endpoint = DEFAULT_ENDPOINT

    if not api_key:
        raise ConfigurationError(
            "Missing API key. Set DIMENSIONS_KEY environment variable, "
            "use --key flag, or configure ~/.dimensions/dsl.ini"
        )

    return api_key, api_endpoint


def initialize_client(key: str, endpoint: str) -> None:
    """Initialize dimcli with credentials."""
    dimcli.login(key=key, endpoint=endpoint)
