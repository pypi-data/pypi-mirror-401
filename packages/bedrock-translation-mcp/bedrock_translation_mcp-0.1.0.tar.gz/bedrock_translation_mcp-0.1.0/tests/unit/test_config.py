"""
Unit tests for configuration loading.

Tests environment variable configuration, config file loading, and default values.
Requirements: 7.2, 7.3
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from config import ConfigLoader, load_config
from models import ServerConfig, TranslationConfig


class TestConfigLoader:
    """Test suite for ConfigLoader class."""
    
    def test_default_server_config(self):
        """Test that default server configuration values are used when no config is provided."""
        loader = ConfigLoader()
        config = loader.load_server_config()
        
        assert config.host == "localhost"
        assert config.port == 8080
        assert config.log_level == "INFO"
        assert config.aws_region == "us-east-1"
        assert config.model_id == "amazon.nova-pro-v1:0"
        assert config.max_retries == 3
        assert config.timeout == 30
    
    def test_default_translation_config(self):
        """Test that default translation configuration values are used when no config is provided."""
        loader = ConfigLoader()
        config = loader.load_translation_config()
        
        assert config.default_source_lang == "auto"
        assert config.default_target_lang == "en"
        assert config.max_input_length == 10000
        assert config.temperature == 0.3
        assert config.max_tokens == 2000
    
    def test_server_config_from_env(self, monkeypatch):
        """Test loading server configuration from environment variables."""
        # Set environment variables
        monkeypatch.setenv("MCP_HOST", "0.0.0.0")
        monkeypatch.setenv("MCP_PORT", "9090")
        monkeypatch.setenv("MCP_LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("AWS_REGION", "us-west-2")
        monkeypatch.setenv("BEDROCK_MODEL_ID", "custom-model-id")
        monkeypatch.setenv("MCP_MAX_RETRIES", "5")
        monkeypatch.setenv("MCP_TIMEOUT", "60")
        
        loader = ConfigLoader()
        config = loader.load_server_config()
        
        assert config.host == "0.0.0.0"
        assert config.port == 9090
        assert config.log_level == "DEBUG"
        assert config.aws_region == "us-west-2"
        assert config.model_id == "custom-model-id"
        assert config.max_retries == 5
        assert config.timeout == 60
    
    def test_translation_config_from_env(self, monkeypatch):
        """Test loading translation configuration from environment variables."""
        # Set environment variables
        monkeypatch.setenv("TRANSLATION_SOURCE_LANG", "es")
        monkeypatch.setenv("TRANSLATION_TARGET_LANG", "fr")
        monkeypatch.setenv("TRANSLATION_MAX_INPUT_LENGTH", "5000")
        monkeypatch.setenv("TRANSLATION_TEMPERATURE", "0.7")
        monkeypatch.setenv("TRANSLATION_MAX_TOKENS", "3000")
        
        loader = ConfigLoader()
        config = loader.load_translation_config()
        
        assert config.default_source_lang == "es"
        assert config.default_target_lang == "fr"
        assert config.max_input_length == 5000
        assert config.temperature == 0.7
        assert config.max_tokens == 3000
    
    def test_config_from_file(self):
        """Test loading configuration from a JSON file."""
        # Create a temporary config file
        config_data = {
            "server": {
                "host": "192.168.1.1",
                "port": 7070,
                "log_level": "WARNING",
                "aws_region": "eu-west-1"
            },
            "translation": {
                "default_source_lang": "de",
                "default_target_lang": "it",
                "max_input_length": 8000,
                "temperature": 0.5
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            loader = ConfigLoader(config_file=config_file)
            
            server_config = loader.load_server_config()
            assert server_config.host == "192.168.1.1"
            assert server_config.port == 7070
            assert server_config.log_level == "WARNING"
            assert server_config.aws_region == "eu-west-1"
            # Values not in file should use defaults
            assert server_config.model_id == "amazon.nova-pro-v1:0"
            assert server_config.max_retries == 3
            
            translation_config = loader.load_translation_config()
            assert translation_config.default_source_lang == "de"
            assert translation_config.default_target_lang == "it"
            assert translation_config.max_input_length == 8000
            assert translation_config.temperature == 0.5
            # Values not in file should use defaults
            assert translation_config.max_tokens == 2000
        finally:
            # Clean up temp file
            os.unlink(config_file)
    
    def test_env_overrides_file(self, monkeypatch):
        """Test that environment variables override config file values."""
        # Create a temporary config file
        config_data = {
            "server": {
                "host": "file-host",
                "port": 5000
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            # Set environment variable that should override file
            monkeypatch.setenv("MCP_HOST", "env-host")
            
            loader = ConfigLoader(config_file=config_file)
            config = loader.load_server_config()
            
            # Environment variable should win
            assert config.host == "env-host"
            # File value should be used for port
            assert config.port == 5000
        finally:
            os.unlink(config_file)
    
    def test_invalid_env_values_ignored(self, monkeypatch):
        """Test that invalid environment variable values are ignored and defaults are used."""
        # Set invalid environment variables
        monkeypatch.setenv("MCP_PORT", "not-a-number")
        monkeypatch.setenv("MCP_MAX_RETRIES", "invalid")
        monkeypatch.setenv("TRANSLATION_TEMPERATURE", "not-a-float")
        
        loader = ConfigLoader()
        server_config = loader.load_server_config()
        translation_config = loader.load_translation_config()
        
        # Should fall back to defaults for invalid values
        assert server_config.port == 8080
        assert server_config.max_retries == 3
        assert translation_config.temperature == 0.3
    
    def test_nonexistent_config_file(self):
        """Test that nonexistent config file falls back to defaults."""
        loader = ConfigLoader(config_file="/nonexistent/path/config.json")
        config = loader.load_server_config()
        
        # Should use defaults
        assert config.host == "localhost"
        assert config.port == 8080
    
    def test_load_config_convenience_function(self):
        """Test the convenience function that loads both configs."""
        server_config, translation_config = load_config()
        
        assert isinstance(server_config, ServerConfig)
        assert isinstance(translation_config, TranslationConfig)
        
        # Should have default values
        assert server_config.host == "localhost"
        assert translation_config.default_target_lang == "en"
