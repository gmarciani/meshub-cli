# Copyright (c) 2024 Meshub Team
# Licensed under the MIT License

"""Tests for configuration commands."""

import json
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from meshub.commands.config import config


def test_config_get():
    """Test config get command."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_config") as mock_load:
        mock_load.return_value = {"apikey": "test-value"}
        result = runner.invoke(config, ["get", "apikey"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["key"] == "apikey"
        assert output["value"] == "test-value"


def test_config_get_unknown_key():
    """Test config get with unknown key."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_config") as mock_load:
        mock_load.return_value = {"apikey": None}
        result = runner.invoke(config, ["get", "unknown"])

        assert result.exit_code == 0


def test_config_set():
    """Test config set command."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_default_config") as mock_default:
        with patch("meshub.commands.config.load_config") as mock_load:
            with patch("meshub.commands.config.save_config") as mock_save:
                mock_default.return_value = {"apikey": None}
                mock_load.return_value = {"apikey": None}

                result = runner.invoke(config, ["set", "apikey", "new-value"])

                assert result.exit_code == 0
                output = json.loads(result.output)
                assert output["key"] == "apikey"
                assert output["value"] == "new-value"
                assert output["oldValue"] is None
                mock_save.assert_called_once()


def test_config_set_unknown_key():
    """Test config set with unknown key."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_default_config") as mock_default:
        mock_default.return_value = {"apikey": None}
        result = runner.invoke(config, ["set", "unknown", "value"])

        assert result.exit_code == 0


def test_config_show():
    """Test config show command."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_config") as mock_load:
        mock_load.return_value = {"apikey": "test-value"}
        result = runner.invoke(config, ["show"])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["apikey"] == "test-value"


def test_config_reset():
    """Test config reset command."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_config") as mock_load:
        with patch("meshub.commands.config.get_config_path") as mock_path:
            mock_config_path = MagicMock()
            mock_config_path.exists.return_value = True
            mock_path.return_value = mock_config_path
            mock_load.return_value = {"apikey": "test-value"}

            result = runner.invoke(config, ["reset"])

            assert result.exit_code == 0
            output = json.loads(result.output)
            assert output["apikey"] == "test-value"
            mock_config_path.unlink.assert_called_once()


def test_config_reset_no_file():
    """Test config reset when no config file exists."""
    runner = CliRunner()

    with patch("meshub.commands.config.load_config") as mock_load:
        with patch("meshub.commands.config.get_config_path") as mock_path:
            mock_config_path = MagicMock()
            mock_config_path.exists.return_value = False
            mock_path.return_value = mock_config_path
            mock_load.return_value = {"apikey": None}

            result = runner.invoke(config, ["reset"])

            assert result.exit_code == 0
            mock_config_path.unlink.assert_not_called()
