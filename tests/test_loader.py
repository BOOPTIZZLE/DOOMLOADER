"""
Tests for the AudioLoader module
"""

import pytest
import os
import tempfile
from doomloader.loader import AudioLoader


class TestAudioLoader:
    """Test cases for AudioLoader class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.loader = AudioLoader()
    
    def test_initialization(self):
        """Test AudioLoader initialization."""
        assert self.loader is not None
        assert len(self.loader.supported_formats) > 0
        assert '.wav' in self.loader.supported_formats
        assert '.mp3' in self.loader.supported_formats
    
    def test_get_supported_formats(self):
        """Test getting supported formats."""
        formats = self.loader.get_supported_formats()
        assert isinstance(formats, list)
        assert len(formats) > 0
        assert '.wav' in formats
    
    def test_is_supported(self):
        """Test format support checking."""
        assert self.loader.is_supported('test.wav') is True
        assert self.loader.is_supported('test.mp3') is True
        assert self.loader.is_supported('test.xyz') is False
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.loader.load('/nonexistent/file.wav')
    
    def test_load_unsupported_format(self):
        """Test loading an unsupported format."""
        # Create a temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as tmp:
            tmp.write(b'dummy content')
            temp_path = tmp.name
        
        try:
            with pytest.raises(ValueError):
                self.loader.load(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_supported_format(self):
        """Test loading a supported format file (placeholder implementation)."""
        # Create a temporary file with supported extension
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(b'dummy wav content')
            temp_path = tmp.name
        
        try:
            audio_data = self.loader.load(temp_path)
            assert isinstance(audio_data, dict)
            assert audio_data['file_path'] == temp_path
            assert audio_data['format'] == '.wav'
            assert 'sample_rate' in audio_data
            assert 'channels' in audio_data
        finally:
            os.unlink(temp_path)