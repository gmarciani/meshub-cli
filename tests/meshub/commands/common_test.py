# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Tests for common command utilities."""

import logging
from unittest.mock import patch
from meshub.commands.common import (
    get_api_key,
    configure_logging,
    require_api_key,
)


def test_get_api_key_from_option():
    """Test get_api_key returns option value when provided."""
    result = get_api_key("my-api-key")
    assert result == "my-api-key"


def test_get_api_key_from_config():
    """Test get_api_key returns config value when option is None."""
    with patch("meshub.commands.common.load_config") as mock_load:
        mock_load.return_value = {"ApiKey": "config-api-key"}
        result = get_api_key(None)
        assert result == "config-api-key"


def test_get_api_key_none():
    """Test get_api_key returns None when no key available."""
    with patch("meshub.commands.common.load_config") as mock_load:
        mock_load.return_value = {}
        result = get_api_key(None)
        assert result is None


def test_configure_logging_debug():
    """Test configure_logging with debug=True."""
    with patch("logging.basicConfig") as mock_config:
        configure_logging(debug=True)
        mock_config.assert_called_once()
        _, kwargs = mock_config.call_args
        assert kwargs["level"] == logging.DEBUG


def test_configure_logging_info():
    """Test configure_logging with debug=False."""
    with patch("logging.basicConfig") as mock_config:
        configure_logging(debug=False)
        mock_config.assert_called_once()
        _, kwargs = mock_config.call_args
        assert kwargs["level"] == logging.INFO


def test_require_api_key_success():
    """Test require_api_key returns key when available."""
    with patch("meshub.commands.common.get_api_key") as mock_get:
        mock_get.return_value = "test-key"
        result = require_api_key("test-key")
        assert result == "test-key"


def test_require_api_key_from_config():
    """Test require_api_key gets key from config."""
    with patch("meshub.commands.common.get_api_key") as mock_get:
        mock_get.return_value = "config-key"
        result = require_api_key(None)
        assert result == "config-key"


def test_require_api_key_missing():
    """Test require_api_key raises SystemExit when no key."""
    with patch("meshub.commands.common.get_api_key") as mock_get:
        mock_get.return_value = None
        try:
            require_api_key(None)
            assert False, "Should have raised SystemExit"
        except SystemExit as e:
            assert e.code == 1


def test_require_api_key_debug_logging():
    """Test require_api_key logs masked key in debug mode."""
    with patch("meshub.commands.common.get_api_key") as mock_get:
        with patch("meshub.commands.common.logger") as mock_logger:
            mock_get.return_value = "my-secret-key"
            result = require_api_key(None, debug=True)
            assert result == "my-secret-key"
            mock_logger.debug.assert_called_once()
            call_args = mock_logger.debug.call_args[0][0]
            assert "***key" in call_args
