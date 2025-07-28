"""
Audio file loader module for DOOMLOADER

Handles loading various audio file formats.
"""

import os
from typing import Optional, Union, Dict, Any


class AudioLoader:
    """Load and manage audio files in various formats."""
    
    def __init__(self):
        """Initialize the AudioLoader."""
        self.supported_formats = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
        self.loaded_files = {}
    
    def load(self, file_path: str) -> Dict[str, Any]:
        """
        Load an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio data and metadata
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported audio format: {file_ext}")
        
        # TODO: Implement actual audio loading logic
        # For now, return placeholder data
        audio_data = {
            'file_path': file_path,
            'format': file_ext,
            'sample_rate': 44100,  # Placeholder
            'channels': 2,  # Placeholder
            'duration': 0.0,  # Placeholder
            'data': None  # Placeholder for actual audio data
        }
        
        self.loaded_files[file_path] = audio_data
        return audio_data
    
    def get_supported_formats(self) -> list:
        """Get list of supported audio formats."""
        return self.supported_formats.copy()
    
    def is_supported(self, file_path: str) -> bool:
        """Check if a file format is supported."""
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.supported_formats