"""
Input handling for the Translation Power.

This module handles processing of text and file inputs, including validation,
file reading with encoding handling, and error management for file system operations.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from .models import TranslationError
except ImportError:
    from models import TranslationError


class InputHandler:
    """Handles input processing for translation requests."""
    
    def __init__(self, max_input_length: int = 10000):
        """
        Initialize the input handler.
        
        Args:
            max_input_length: Maximum allowed input length in characters
        """
        self.max_input_length = max_input_length
    
    def process_input(self, input_data: str, is_file: bool = False) -> str:
        """
        Process input data - either return as-is or read from file.
        
        Args:
            input_data: Either plain text or a file path
            is_file: If True, treat input_data as a file path
        
        Returns:
            The text content to be translated
        
        Raises:
            ValueError: If input is invalid (empty, too long, etc.)
            FileNotFoundError: If file path doesn't exist
            PermissionError: If file cannot be read due to permissions
            UnicodeDecodeError: If file encoding cannot be handled
        """
        if is_file:
            # Read from file
            return self.read_file(input_data)
        else:
            # Validate plain text input
            if not self.validate_input(input_data):
                raise ValueError("Input is empty or contains only whitespace")
            
            if len(input_data) > self.max_input_length:
                raise ValueError(
                    f"Input exceeds maximum length of {self.max_input_length} characters"
                )
            
            return input_data
    
    def read_file(self, file_path: str) -> str:
        """
        Read and return file contents with encoding handling.
        
        Args:
            file_path: Path to the file to read
        
        Returns:
            File contents as a string
        
        Raises:
            ValueError: If file_path is empty or invalid
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be read
            UnicodeDecodeError: If file encoding cannot be handled
        """
        if not file_path or not file_path.strip():
            raise ValueError("File path is empty")
        
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if it's a file (not a directory)
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Try to read with different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                
                # Validate the content
                if not self.validate_input(content):
                    raise ValueError(f"File is empty or contains only whitespace: {file_path}")
                
                if len(content) > self.max_input_length:
                    raise ValueError(
                        f"File content exceeds maximum length of {self.max_input_length} characters"
                    )
                
                return content
            
            except UnicodeDecodeError:
                # Try next encoding
                if encoding == encodings[-1]:
                    # Last encoding failed, raise error
                    raise UnicodeDecodeError(
                        encoding,
                        b'',
                        0,
                        1,
                        f"Unable to decode file with supported encodings: {file_path}"
                    )
                continue
            
            except PermissionError:
                raise PermissionError(f"Permission denied reading file: {file_path}")
            
            except OSError as e:
                raise OSError(f"Error reading file {file_path}: {str(e)}")
        
        # Should not reach here, but just in case
        raise UnicodeDecodeError(
            'utf-8',
            b'',
            0,
            1,
            f"Unable to decode file: {file_path}"
        )
    
    def validate_input(self, text: str) -> bool:
        """
        Validate that input is not empty and is properly formatted.
        
        Args:
            text: The text to validate
        
        Returns:
            True if input is valid, False otherwise
        """
        if text is None:
            return False
        
        if not isinstance(text, str):
            return False
        
        # Check if text is empty or only whitespace
        if not text or not text.strip():
            return False
        
        return True
