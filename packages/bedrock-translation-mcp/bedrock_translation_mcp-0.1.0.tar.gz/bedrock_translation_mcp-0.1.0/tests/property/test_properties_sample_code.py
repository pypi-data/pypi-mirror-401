"""
Property-based tests for sample code generation.

Feature: translation-power, Property 8: Sample Code Comment Inclusion
Feature: translation-power, Property 9: Unsupported Language Error
Validates: Requirements 3.4, 3.5
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from hypothesis import given, strategies as st, settings
from sample_code_gen import SampleCodeGenerator
from models import TranslationError
import pytest


# Feature: translation-power, Property 8: Sample Code Comment Inclusion
# Validates: Requirements 3.4
@settings(max_examples=100)
@given(
    language=st.sampled_from(['java', 'python', 'nodejs'])
)
def test_sample_code_contains_comments(language):
    """
    Property: For any supported language, when sample code is generated,
    the code should contain comment markers and explanatory text about
    key integration points.
    
    Feature: translation-power, Property 8: Sample Code Comment Inclusion
    Validates: Requirements 3.4
    """
    generator = SampleCodeGenerator()
    result = generator.generate_sample(language)
    
    # Verify the result contains code
    assert result.code is not None
    assert len(result.code) > 0
    
    # Define comment markers for each language
    comment_markers = {
        'java': ['//', '/*', '*/', '*'],
        'python': ['#', '"""', "'''"],
        'nodejs': ['//', '/*', '*/', '*']
    }
    
    # Check that at least one comment marker exists in the code
    markers = comment_markers[language]
    has_comments = any(marker in result.code for marker in markers)
    assert has_comments, f"Generated {language} code should contain comment markers"
    
    # Check for key integration point explanations
    # These terms should appear in comments explaining the integration
    integration_keywords = [
        'MCP',
        'server',
        'translate',
        'request',
        'response'
    ]
    
    # At least some integration keywords should be present
    code_lower = result.code.lower()
    keywords_found = sum(1 for keyword in integration_keywords if keyword.lower() in code_lower)
    assert keywords_found >= 3, f"Generated code should explain key integration points (found {keywords_found} keywords)"
    
    # Verify language and description are set correctly
    assert result.language == language
    assert result.description is not None
    assert len(result.description) > 0


# Feature: translation-power, Property 9: Unsupported Language Error
# Validates: Requirements 3.5
@settings(max_examples=100)
@given(
    language=st.text(min_size=1, max_size=20).filter(
        lambda x: x.lower() not in ['java', 'python', 'nodejs']
    )
)
def test_unsupported_language_error(language):
    """
    Property: For any unsupported language name, when requesting sample code,
    the Sample_Code_Generator should return an error message listing the
    supported languages.
    
    Feature: translation-power, Property 9: Unsupported Language Error
    Validates: Requirements 3.5
    """
    generator = SampleCodeGenerator()
    
    # Attempt to generate code for unsupported language
    with pytest.raises(TranslationError) as exc_info:
        generator.generate_sample(language)
    
    error = exc_info.value
    
    # Verify error type is validation
    assert error.error_type == "validation"
    
    # Verify error message mentions the unsupported language
    assert language.lower() in error.message.lower() or "unsupported" in error.message.lower()
    
    # Verify error message lists supported languages
    supported_languages = ['java', 'python', 'nodejs']
    message_lower = error.message.lower()
    
    # At least mention some supported languages
    languages_mentioned = sum(1 for lang in supported_languages if lang in message_lower)
    assert languages_mentioned >= 2, "Error message should list supported languages"
    
    # Verify error details contain useful information
    assert error.details is not None
    assert 'requested_language' in error.details or 'supported_languages' in error.details
