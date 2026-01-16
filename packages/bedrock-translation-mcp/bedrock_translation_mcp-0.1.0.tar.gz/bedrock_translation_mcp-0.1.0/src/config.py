"""
Configuration management for Translation Power.

This module handles loading configuration from environment variables,
configuration files, and provides default values.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

try:
    from .models import ServerConfig, TranslationConfig
except ImportError:
    from models import ServerConfig, TranslationConfig


class ConfigLoader:
    """Loads configuration from multiple sources with priority order."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_file: Optional path to a JSON configuration file
        """
        self.config_file = config_file
        # Load environment variables from .env file if present
        load_dotenv()
    
    def load_server_config(self) -> ServerConfig:
        """
        Load server configuration with the following priority:
        1. Environment variables (highest priority)
        2. Configuration file
        3. Default values (lowest priority)
        
        Returns:
            ServerConfig instance with loaded configuration
        """
        # Start with defaults
        config_dict = {
            "host": "localhost",
            "port": 8080,
            "log_level": "INFO",
            "aws_region": "us-east-1",
            "model_id": "amazon.nova-pro-v1:0",
            "max_retries": 3,
            "timeout": 30
        }
        
        # Override with config file if provided
        if self.config_file:
            file_config = self._load_from_file()
            if file_config and "server" in file_config:
                config_dict.update(file_config["server"])
        
        # Override with environment variables (highest priority)
        env_config = self._load_server_from_env()
        config_dict.update(env_config)
        
        return ServerConfig(**config_dict)
    
    def load_translation_config(self) -> TranslationConfig:
        """
        Load translation configuration with the following priority:
        1. Environment variables (highest priority)
        2. Configuration file
        3. Default values (lowest priority)
        
        Returns:
            TranslationConfig instance with loaded configuration
        """
        # Start with defaults
        config_dict = {
            "default_source_lang": "auto",
            "default_target_lang": "en",
            "max_input_length": 10000,
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        # Override with config file if provided
        if self.config_file:
            file_config = self._load_from_file()
            if file_config and "translation" in file_config:
                config_dict.update(file_config["translation"])
        
        # Override with environment variables (highest priority)
        env_config = self._load_translation_from_env()
        config_dict.update(env_config)
        
        return TranslationConfig(**config_dict)
    
    def _load_from_file(self) -> Optional[Dict[str, Any]]:
        """
        Load configuration from JSON file.
        
        Returns:
            Dictionary with configuration or None if file doesn't exist
        """
        if not self.config_file:
            return None
        
        config_path = Path(self.config_file)
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Log error but don't fail - fall back to defaults
            print(f"Warning: Failed to load config file {self.config_file}: {e}")
            return None
    
    def _load_server_from_env(self) -> Dict[str, Any]:
        """
        Load server configuration from environment variables.
        
        Environment variables:
        - MCP_HOST: Server host
        - MCP_PORT: Server port
        - MCP_LOG_LEVEL: Logging level
        - AWS_REGION: AWS region for Bedrock
        - BEDROCK_MODEL_ID: Model ID for translation
        - MCP_MAX_RETRIES: Maximum retry attempts
        - MCP_TIMEOUT: Request timeout in seconds
        
        Returns:
            Dictionary with configuration values from environment
        """
        config = {}
        
        if os.getenv("MCP_HOST"):
            config["host"] = os.getenv("MCP_HOST")
        
        if os.getenv("MCP_PORT"):
            try:
                config["port"] = int(os.getenv("MCP_PORT"))
            except ValueError:
                pass
        
        if os.getenv("MCP_LOG_LEVEL"):
            config["log_level"] = os.getenv("MCP_LOG_LEVEL")
        
        if os.getenv("AWS_REGION"):
            config["aws_region"] = os.getenv("AWS_REGION")
        
        if os.getenv("BEDROCK_MODEL_ID"):
            config["model_id"] = os.getenv("BEDROCK_MODEL_ID")
        
        if os.getenv("MCP_MAX_RETRIES"):
            try:
                config["max_retries"] = int(os.getenv("MCP_MAX_RETRIES"))
            except ValueError:
                pass
        
        if os.getenv("MCP_TIMEOUT"):
            try:
                config["timeout"] = int(os.getenv("MCP_TIMEOUT"))
            except ValueError:
                pass
        
        return config
    
    def _load_translation_from_env(self) -> Dict[str, Any]:
        """
        Load translation configuration from environment variables.
        
        Environment variables:
        - TRANSLATION_SOURCE_LANG: Default source language
        - TRANSLATION_TARGET_LANG: Default target language
        - TRANSLATION_MAX_INPUT_LENGTH: Maximum input length
        - TRANSLATION_TEMPERATURE: LLM temperature
        - TRANSLATION_MAX_TOKENS: Maximum tokens in response
        
        Returns:
            Dictionary with configuration values from environment
        """
        config = {}
        
        if os.getenv("TRANSLATION_SOURCE_LANG"):
            config["default_source_lang"] = os.getenv("TRANSLATION_SOURCE_LANG")
        
        if os.getenv("TRANSLATION_TARGET_LANG"):
            config["default_target_lang"] = os.getenv("TRANSLATION_TARGET_LANG")
        
        if os.getenv("TRANSLATION_MAX_INPUT_LENGTH"):
            try:
                config["max_input_length"] = int(os.getenv("TRANSLATION_MAX_INPUT_LENGTH"))
            except ValueError:
                pass
        
        if os.getenv("TRANSLATION_TEMPERATURE"):
            try:
                config["temperature"] = float(os.getenv("TRANSLATION_TEMPERATURE"))
            except ValueError:
                pass
        
        if os.getenv("TRANSLATION_MAX_TOKENS"):
            try:
                config["max_tokens"] = int(os.getenv("TRANSLATION_MAX_TOKENS"))
            except ValueError:
                pass
        
        return config


def load_config(config_file: Optional[str] = None) -> tuple[ServerConfig, TranslationConfig]:
    """
    Convenience function to load both server and translation configurations.
    
    Args:
        config_file: Optional path to a JSON configuration file
    
    Returns:
        Tuple of (ServerConfig, TranslationConfig)
    """
    loader = ConfigLoader(config_file)
    return loader.load_server_config(), loader.load_translation_config()
