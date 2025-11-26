# Copyright (c) 2024 Meshub Team
# Licensed under the MIT License

"""Tests for configuration utilities."""

import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from meshub.config.configuration import (
    load_config,
    save_config,
    get_config_path,
    load_default_config,
)


def test_load_config_empty():
    """Test loading config when file doesn't exist."""
    with patch("meshub.config.configuration.get_config_path") as mock_path:
        mock_path.return_value = Path("/nonexistent/config.yaml")
        with patch("meshub.config.configuration.load_default_config") as mock_default:
            mock_default.return_value = {"apikey": None}
            config = load_config()
            assert config == {"apikey": None}


def test_save_and_load_config():
    """Test saving and loading configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config.yaml"

        with patch("meshub.config.configuration.get_config_path") as mock_path:
            with patch(
                "meshub.config.configuration.load_default_config"
            ) as mock_default:
                mock_path.return_value = config_path
                mock_default.return_value = {"apikey": None}

                test_config = {"apikey": "test-token"}
                save_config(test_config)

                loaded_config = load_config()
                assert loaded_config == test_config


def test_get_config_path():
    """Test config path generation."""
    path = get_config_path()
    assert path.name == "config.yaml"
    assert ".meshub" in str(path)


def test_load_default_config():
    """Test loading default configuration."""
    mock_yaml_content = "apikey: null\n"
    with patch("importlib.resources.open_text", mock_open(read_data=mock_yaml_content)):
        config = load_default_config()
        assert config == {"apikey": None}


def test_load_default_config_error():
    """Test loading default config with error."""
    with patch("importlib.resources.open_text", side_effect=FileNotFoundError):
        config = load_default_config()
        assert config == {}


def test_load_config_yaml_error():
    """Test loading config with YAML error."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "config.yaml"
        config_path.write_text("invalid: yaml: content:")

        with patch("meshub.config.configuration.get_config_path") as mock_path:
            with patch(
                "meshub.config.configuration.load_default_config"
            ) as mock_default:
                mock_path.return_value = config_path
                mock_default.return_value = {"apikey": None}

                config = load_config()
                assert config == {"apikey": None}
