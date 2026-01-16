"""
Data models for the Translation Power.

This module defines all data structures used throughout the translation service,
including configuration models, request/response models, and error models.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class ServerConfig:
    """MCP Server configuration"""
    host: str = "localhost"
    port: int = 8080
    log_level: str = "INFO"
    aws_region: str = "us-east-1"
    model_id: str = "amazon.nova-pro-v1:0"
    max_retries: int = 3
    timeout: int = 30


@dataclass
class TranslationConfig:
    """Translation engine configuration"""
    default_source_lang: str = "auto"
    default_target_lang: str = "en"
    max_input_length: int = 10000
    temperature: float = 0.3
    max_tokens: int = 2000


@dataclass
class TranslationRequest:
    """Translation request model"""
    input: str
    is_file: bool = False
    source_lang: Optional[str] = None
    target_lang: str = "en"
    stream: bool = False


@dataclass
class TranslationResult:
    """Translation result model"""
    translated_text: str
    source_language: str
    target_language: str
    model_used: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class TranslationChunk:
    """Streaming translation chunk"""
    chunk: str
    is_complete: bool = False


@dataclass
class SampleCodeRequest:
    """Sample code request model"""
    language: str
    include_comments: bool = True


@dataclass
class SampleCodeResult:
    """Sample code result model"""
    code: str
    language: str
    description: str


class TranslationError(Exception):
    """Error information for translation operations"""
    
    def __init__(self, error_type: str, message: str, details: Optional[dict] = None):
        """
        Initialize a translation error.
        
        Args:
            error_type: Type of error ("validation", "aws", "file", "network")
            message: Human-readable error message
            details: Optional additional error details
        """
        self.error_type = error_type
        self.message = message
        self.details = details
        super().__init__(message)
