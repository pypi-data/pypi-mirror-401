"""
Property-based tests for input handling.

Feature: translation-power, Property 1: Input Processing Consistency
Feature: translation-power, Property 4: Invalid Input Error Handling
Feature: translation-power, Property 11: File Path Detection
Validates: Requirements 1.1, 1.2, 1.5, 1.7, 5.4, 6.1
"""

import sys
from pathlib import Path
import tempfile
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from hypothesis import given, strategies as st, settings, assume
from input_handler import InputHandler


# Feature: translation-power, Property 1: Input Processing Consistency
# Validates: Requirements 1.1, 1.2
@settings(max_examples=20)
@given(
    text=st.text(min_size=1, max_size=1000).filter(lambda x: x.strip())
)
def test_input_processing_consistency_plain_text(text):
    """
    Property: For any valid plain text input, when processed by the InputHandler,
    the handler should return the same text content.
    
    Feature: translation-power, Property 1: Input Processing Consistency
    Validates: Requirements 1.1, 1.2
    """
    handler = InputHandler(max_input_length=10000)
    
    # Process plain text (is_file=False)
    result = handler.process_input(text, is_file=False)
    
    # The result should match the input
    assert result == text


# Feature: translation-power, Property 1: Input Processing Consistency
# Validates: Requirements 1.1, 1.2
@settings(max_examples=20)
@given(
    text=st.text(min_size=1, max_size=1000).filter(lambda x: x.strip())
)
def test_input_processing_consistency_file_input(text):
    """
    Property: For any valid text written to a file, when processed by the InputHandler
    with a file path, the handler should return the file contents matching the original text.
    
    Feature: translation-power, Property 1: Input Processing Consistency
    Validates: Requirements 1.1, 1.2
    """
    handler = InputHandler(max_input_length=10000)
    
    # Create a temporary file with the text
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt', newline='') as f:
        f.write(text)
        temp_path = f.name
    
    try:
        # Process file input (is_file=True)
        result = handler.process_input(temp_path, is_file=True)
        
        # The result should match the original text
        # Note: Python may normalize line endings when reading in text mode
        # We normalize both to handle platform differences
        assert result.replace('\r\n', '\n').replace('\r', '\n') == text.replace('\r\n', '\n').replace('\r', '\n')
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


# Feature: translation-power, Property 4: Invalid Input Error Handling
# Validates: Requirements 1.5, 1.7, 6.1
@settings(max_examples=20)
@given(
    invalid_text=st.one_of(
        st.just(""),
        st.just("   "),
        st.just("\n\n\n"),
        st.just("\t\t"),
        st.text(max_size=0)
    )
)
def test_invalid_input_error_handling_empty(invalid_text):
    """
    Property: For any invalid input (empty, whitespace-only), the InputHandler
    should raise a ValueError with a descriptive error message.
    
    Feature: translation-power, Property 4: Invalid Input Error Handling
    Validates: Requirements 1.5, 1.7, 6.1
    """
    handler = InputHandler(max_input_length=10000)
    
    try:
        handler.process_input(invalid_text, is_file=False)
        # Should not reach here
        assert False, "Expected ValueError for invalid input"
    except ValueError as e:
        # Verify error message is descriptive
        assert "empty" in str(e).lower() or "whitespace" in str(e).lower()


# Feature: translation-power, Property 4: Invalid Input Error Handling
# Validates: Requirements 1.5, 1.7, 6.1
@settings(max_examples=20)
@given(
    file_path=st.text(min_size=1, max_size=100).filter(
        lambda x: not os.path.exists(x) and '/' not in x and '\\' not in x and x.strip()  # Exclude whitespace-only strings
    )
)
def test_invalid_input_error_handling_nonexistent_file(file_path):
    """
    Property: For any non-existent file path, the InputHandler should raise
    a FileNotFoundError with a descriptive error message.
    
    Feature: translation-power, Property 4: Invalid Input Error Handling
    Validates: Requirements 1.5, 1.7, 6.1
    """
    handler = InputHandler(max_input_length=10000)
    
    # Ensure the file doesn't exist
    assume(not os.path.exists(file_path))
    
    try:
        handler.process_input(file_path, is_file=True)
        # Should not reach here
        assert False, "Expected FileNotFoundError for non-existent file"
    except FileNotFoundError as e:
        # Verify error message mentions the file
        assert file_path in str(e) or "not found" in str(e).lower()


# Feature: translation-power, Property 11: File Path Detection
# Validates: Requirements 5.4
@settings(max_examples=20)
@given(
    text=st.text(min_size=1, max_size=1000).filter(lambda x: x.strip())
)
def test_file_path_detection_plain_text(text):
    """
    Property: For any input with is_file=False, the InputHandler should treat
    it as plain text and not attempt to read it as a file.
    
    Feature: translation-power, Property 11: File Path Detection
    Validates: Requirements 5.4
    """
    handler = InputHandler(max_input_length=10000)
    
    # Process as plain text
    result = handler.process_input(text, is_file=False)
    
    # Should return the text as-is (not try to read as file)
    assert result == text


# Feature: translation-power, Property 11: File Path Detection
# Validates: Requirements 5.4
@settings(max_examples=20)
@given(
    text=st.text(min_size=1, max_size=1000).filter(lambda x: x.strip())
)
def test_file_path_detection_file_input(text):
    """
    Property: For any input with is_file=True, the InputHandler should treat
    it as a file path and attempt to read the file contents.
    
    Feature: translation-power, Property 11: File Path Detection
    Validates: Requirements 5.4
    """
    handler = InputHandler(max_input_length=10000)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt', newline='') as f:
        f.write(text)
        temp_path = f.name
    
    try:
        # Process as file
        result = handler.process_input(temp_path, is_file=True)
        
        # Should read from file and return file contents
        # Note: Python may normalize line endings when reading in text mode
        # We normalize both to handle platform differences
        assert result.replace('\r\n', '\n').replace('\r', '\n') == text.replace('\r\n', '\n').replace('\r', '\n')
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
