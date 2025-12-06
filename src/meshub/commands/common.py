# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Common utilities for Meshub CLI commands."""

import click
import logging
from typing import Optional
from meshub.config.configuration import load_config

logger = logging.getLogger(__name__)


def get_api_key(api_key_option: Optional[str]) -> Optional[str]:
    """Get API key from option or config.

    Args:
        api_key_option: API key passed via --api-key option

    Returns:
        API key from option (if provided) or from config
    """
    if api_key_option:
        return api_key_option
    cfg = load_config()
    return cfg.get("ApiKey")


def configure_logging(debug: bool = False) -> None:
    """Configure logging with UTC timestamps.

    Args:
        debug: Whether to enable debug level logging
    """
    import time

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    logging.Formatter.converter = time.gmtime


def require_api_key(api_key_option: Optional[str], debug: bool = False) -> str:
    """Get API key, raising error if not available.

    Args:
        api_key_option: API key passed via --api-key option
        debug: Whether to log debug information

    Returns:
        API key

    Raises:
        SystemExit: If no API key is available
    """
    configure_logging(debug)
    api_key = get_api_key(api_key_option)
    if not api_key:
        logger.error(
            "An API key is required to execute the command. Unable to locate your API key."
        )
        raise SystemExit(1)
    if debug:
        masked_key = "***" + api_key[-3:]
        logger.debug(f"Using API key: {masked_key}")
    return api_key


api_key_option = click.option(
    "--api-key",
    type=str,
    default=None,
    help="API key (overrides configured key)",
)

debug_option = click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Enable debug output",
)
