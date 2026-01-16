"""Translation Power - Kiro Power for text translation using AWS Bedrock Nova Pro"""

__version__ = "0.1.0"

# Make imports available at package level
from .models import (
    ServerConfig,
    TranslationConfig,
    TranslationResult,
    TranslationChunk,
    TranslationError,
    SampleCodeRequest,
    SampleCodeResult
)

from .config import ConfigLoader, load_config
from .bedrock_client import BedrockClient, BedrockClientError
from .translation_engine import TranslationEngine, TranslationEngineError
from .input_handler import InputHandler
from .sample_code_gen import SampleCodeGenerator

__all__ = [
    'ServerConfig',
    'TranslationConfig',
    'TranslationResult',
    'TranslationChunk',
    'TranslationError',
    'SampleCodeRequest',
    'SampleCodeResult',
    'ConfigLoader',
    'load_config',
    'BedrockClient',
    'BedrockClientError',
    'TranslationEngine',
    'TranslationEngineError',
    'InputHandler',
    'SampleCodeGenerator',
]
