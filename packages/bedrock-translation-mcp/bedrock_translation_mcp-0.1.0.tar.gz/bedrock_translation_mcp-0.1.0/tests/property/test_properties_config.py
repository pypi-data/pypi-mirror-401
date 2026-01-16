"""
Property-based tests for configuration models.

Feature: translation-power, Property 15: Configuration Application
Validates: Requirements 7.1
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from hypothesis import given, strategies as st, settings, HealthCheck
from models import ServerConfig, TranslationConfig


# Feature: translation-power, Property 15: Configuration Application
# Validates: Requirements 7.1
@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=20)
@given(
    host=st.text(min_size=1, max_size=100),
    port=st.integers(min_value=1, max_value=65535),
    log_level=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    aws_region=st.sampled_from(["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]),
    model_id=st.text(min_size=1, max_size=100),
    max_retries=st.integers(min_value=0, max_value=10),
    timeout=st.integers(min_value=1, max_value=300)
)
def test_server_config_application(host, port, log_level, aws_region, model_id, max_retries, timeout):
    """
    Property: For any configuration options provided, the ServerConfig should
    store and apply those settings correctly.
    
    Feature: translation-power, Property 15: Configuration Application
    Validates: Requirements 7.1
    """
    config = ServerConfig(
        host=host,
        port=port,
        log_level=log_level,
        aws_region=aws_region,
        model_id=model_id,
        max_retries=max_retries,
        timeout=timeout
    )
    
    # Verify all configuration values are applied correctly
    assert config.host == host
    assert config.port == port
    assert config.log_level == log_level
    assert config.aws_region == aws_region
    assert config.model_id == model_id
    assert config.max_retries == max_retries
    assert config.timeout == timeout


# Feature: translation-power, Property 15: Configuration Application
# Validates: Requirements 7.1
@settings(max_examples=20)
@given(
    default_source_lang=st.text(min_size=2, max_size=10),
    default_target_lang=st.text(min_size=2, max_size=10),
    max_input_length=st.integers(min_value=100, max_value=100000),
    temperature=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    max_tokens=st.integers(min_value=100, max_value=10000)
)
def test_translation_config_application(default_source_lang, default_target_lang, 
                                       max_input_length, temperature, max_tokens):
    """
    Property: For any translation configuration options provided, the TranslationConfig
    should store and apply those settings correctly.
    
    Feature: translation-power, Property 15: Configuration Application
    Validates: Requirements 7.1
    """
    config = TranslationConfig(
        default_source_lang=default_source_lang,
        default_target_lang=default_target_lang,
        max_input_length=max_input_length,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Verify all configuration values are applied correctly
    assert config.default_source_lang == default_source_lang
    assert config.default_target_lang == default_target_lang
    assert config.max_input_length == max_input_length
    assert config.temperature == temperature
    assert config.max_tokens == max_tokens


# Feature: translation-power, Property 15: Configuration Application
# Validates: Requirements 7.1
def test_server_config_defaults():
    """
    Property: When no configuration is provided, ServerConfig should use sensible defaults.
    
    Feature: translation-power, Property 15: Configuration Application
    Validates: Requirements 7.1
    """
    config = ServerConfig()
    
    # Verify default values are set
    assert config.host == "localhost"
    assert config.port == 8080
    assert config.log_level == "INFO"
    assert config.aws_region == "us-east-1"
    assert config.model_id == "amazon.nova-pro-v1:0"
    assert config.max_retries == 3
    assert config.timeout == 30


# Feature: translation-power, Property 15: Configuration Application
# Validates: Requirements 7.1
def test_translation_config_defaults():
    """
    Property: When no configuration is provided, TranslationConfig should use sensible defaults.
    
    Feature: translation-power, Property 15: Configuration Application
    Validates: Requirements 7.1
    """
    config = TranslationConfig()
    
    # Verify default values are set
    assert config.default_source_lang == "auto"
    assert config.default_target_lang == "en"
    assert config.max_input_length == 10000
    assert config.temperature == 0.3
    assert config.max_tokens == 2000
