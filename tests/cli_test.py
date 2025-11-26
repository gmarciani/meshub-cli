# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Tests for the main CLI module."""

import logging
from click.testing import CliRunner
from unittest.mock import patch
from meshub.cli import main


def test_main_help():
    """Test main command help."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Meshub CLI" in result.output


def test_version():
    """Test version option."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.0.1" in result.output


def test_verbose_flag():
    """Test verbose flag."""
    runner = CliRunner()
    with patch("meshub.cli.logging.basicConfig") as mock_logging:
        with patch("meshub.commands.config.load_config") as mock_load:
            mock_load.return_value = {"apikey": None}
            result = runner.invoke(main, ["--verbose", "config", "show"])
            assert result.exit_code == 0
            mock_logging.assert_called_once()
            args, kwargs = mock_logging.call_args
            assert kwargs["level"] == logging.DEBUG


def test_no_verbose_flag():
    """Test without verbose flag."""
    runner = CliRunner()
    with patch("meshub.cli.logging.basicConfig") as mock_logging:
        with patch("meshub.commands.config.load_config") as mock_load:
            mock_load.return_value = {"apikey": None}
            result = runner.invoke(main, ["config", "show"])
            assert result.exit_code == 0
            mock_logging.assert_called_once()
            args, kwargs = mock_logging.call_args
            assert kwargs["level"] == logging.INFO
