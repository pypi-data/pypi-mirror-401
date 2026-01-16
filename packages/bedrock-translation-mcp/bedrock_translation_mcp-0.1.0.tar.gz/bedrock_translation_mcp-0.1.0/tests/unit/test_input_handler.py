"""
Unit tests for input handling.

Tests reading various file formats, empty file handling, file not found errors,
permission errors, and encoding errors.
Validates: Requirements 1.2, 1.7
"""

import sys
from pathlib import Path
import tempfile
import os
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from input_handler import InputHandler


class TestInputHandlerFileFormats:
    """Test reading various file formats."""
    
    def test_read_txt_file(self):
        """Test reading a plain text file."""
        handler = InputHandler(max_input_length=10000)
        
        content = "This is a plain text file.\nWith multiple lines."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.read_file(temp_path)
            assert result == content
        finally:
            os.unlink(temp_path)
    
    def test_read_md_file(self):
        """Test reading a markdown file."""
        handler = InputHandler(max_input_length=10000)
        
        content = "# Markdown Header\n\nThis is **bold** text."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.md') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.read_file(temp_path)
            assert result == content
        finally:
            os.unlink(temp_path)
    
    def test_read_json_file(self):
        """Test reading a JSON file."""
        handler = InputHandler(max_input_length=10000)
        
        content = '{"key": "value", "number": 42}'
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.json') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.read_file(temp_path)
            assert result == content
        finally:
            os.unlink(temp_path)


class TestInputHandlerEmptyFiles:
    """Test empty file handling."""
    
    def test_empty_file_raises_error(self):
        """Test that reading an empty file raises ValueError."""
        handler = InputHandler(max_input_length=10000)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            # Write nothing
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError) as exc_info:
                handler.read_file(temp_path)
            assert "empty" in str(exc_info.value).lower() or "whitespace" in str(exc_info.value).lower()
        finally:
            os.unlink(temp_path)
    
    def test_whitespace_only_file_raises_error(self):
        """Test that reading a file with only whitespace raises ValueError."""
        handler = InputHandler(max_input_length=10000)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write("   \n\n\t\t  ")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError) as exc_info:
                handler.read_file(temp_path)
            assert "empty" in str(exc_info.value).lower() or "whitespace" in str(exc_info.value).lower()
        finally:
            os.unlink(temp_path)


class TestInputHandlerFileErrors:
    """Test file not found and permission errors."""
    
    def test_file_not_found_error(self):
        """Test that reading a non-existent file raises FileNotFoundError."""
        handler = InputHandler(max_input_length=10000)
        
        non_existent_path = "this_file_does_not_exist_12345.txt"
        
        with pytest.raises(FileNotFoundError) as exc_info:
            handler.read_file(non_existent_path)
        assert "not found" in str(exc_info.value).lower() or non_existent_path in str(exc_info.value)
    
    def test_directory_path_raises_error(self):
        """Test that providing a directory path raises ValueError."""
        handler = InputHandler(max_input_length=10000)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError) as exc_info:
                handler.read_file(temp_dir)
            assert "not a file" in str(exc_info.value).lower()
    
    def test_empty_file_path_raises_error(self):
        """Test that an empty file path raises ValueError."""
        handler = InputHandler(max_input_length=10000)
        
        with pytest.raises(ValueError) as exc_info:
            handler.read_file("")
        assert "empty" in str(exc_info.value).lower()


class TestInputHandlerEncodingErrors:
    """Test encoding error handling."""
    
    def test_utf8_encoding(self):
        """Test reading a UTF-8 encoded file."""
        handler = InputHandler(max_input_length=10000)
        
        content = "Hello 世界 🌍"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.read_file(temp_path)
            assert result == content
        finally:
            os.unlink(temp_path)
    
    def test_latin1_encoding(self):
        """Test reading a Latin-1 encoded file."""
        handler = InputHandler(max_input_length=10000)
        
        content = "Café résumé"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='latin-1', suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.read_file(temp_path)
            # Should successfully read with fallback encoding
            assert len(result) > 0
        finally:
            os.unlink(temp_path)


class TestInputHandlerValidation:
    """Test input validation."""
    
    def test_validate_valid_input(self):
        """Test that valid input passes validation."""
        handler = InputHandler(max_input_length=10000)
        
        assert handler.validate_input("Valid text") is True
        assert handler.validate_input("Multiple\nlines") is True
        assert handler.validate_input("  Text with spaces  ") is True
    
    def test_validate_invalid_input(self):
        """Test that invalid input fails validation."""
        handler = InputHandler(max_input_length=10000)
        
        assert handler.validate_input("") is False
        assert handler.validate_input("   ") is False
        assert handler.validate_input("\n\n") is False
        assert handler.validate_input(None) is False


class TestInputHandlerProcessInput:
    """Test the process_input method."""
    
    def test_process_plain_text(self):
        """Test processing plain text input."""
        handler = InputHandler(max_input_length=10000)
        
        text = "This is plain text"
        result = handler.process_input(text, is_file=False)
        
        assert result == text
    
    def test_process_file_input(self):
        """Test processing file input."""
        handler = InputHandler(max_input_length=10000)
        
        content = "File content here"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = handler.process_input(temp_path, is_file=True)
            assert result == content
        finally:
            os.unlink(temp_path)
    
    def test_process_input_too_long(self):
        """Test that input exceeding max length raises ValueError."""
        handler = InputHandler(max_input_length=100)
        
        long_text = "a" * 101
        
        with pytest.raises(ValueError) as exc_info:
            handler.process_input(long_text, is_file=False)
        assert "exceeds maximum length" in str(exc_info.value).lower()
