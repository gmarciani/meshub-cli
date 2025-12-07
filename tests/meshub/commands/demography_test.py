# Copyright (c) 2025, Meshub
# Licensed under the MIT License

"""Tests for demography commands."""

import json
from click.testing import CliRunner
from unittest.mock import patch
from meshub.commands.demography import demography


def test_demography_help():
    """Test demography command help."""
    runner = CliRunner()
    result = runner.invoke(demography, ["--help"])
    assert result.exit_code == 0
    assert "Demography data commands" in result.output


def test_list_entities_with_api_key():
    """Test list_entities with API key option."""
    runner = CliRunner()
    result = runner.invoke(demography, ["list-entities", "--api-key", "test-key"])
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output == []


def test_list_entities_with_config_api_key():
    """Test list_entities with API key from config."""
    runner = CliRunner()
    with patch("meshub.commands.common.load_config") as mock_load:
        mock_load.return_value = {"ApiKey": "config-key"}
        result = runner.invoke(demography, ["list-entities"])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output == []


def test_list_entities_no_api_key():
    """Test list_entities fails without API key."""
    runner = CliRunner()
    with patch("meshub.commands.common.load_config") as mock_load:
        mock_load.return_value = {}
        result = runner.invoke(demography, ["list-entities"])
        assert result.exit_code == 1


def test_list_entities_debug():
    """Test list_entities with debug flag."""
    runner = CliRunner()
    result = runner.invoke(
        demography, ["list-entities", "--api-key", "test-key", "--debug"]
    )
    assert result.exit_code == 0
