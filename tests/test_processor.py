"""
Tests for the AudioProcessor module
"""

import pytest
from doomloader.processor import AudioProcessor


class TestAudioProcessor:
    """Test cases for AudioProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = AudioProcessor()
    
    def test_initialization(self):
        """Test AudioProcessor initialization."""
        assert self.processor is not None
        assert len(self.processor.available_effects) > 0
        assert 'reverb' in self.processor.available_effects
        assert len(self.processor.effect_chain) == 0
    
    def test_get_available_effects(self):
        """Test getting available effects."""
        effects = self.processor.get_available_effects()
        assert isinstance(effects, list)
        assert len(effects) > 0
        assert 'reverb' in effects
        assert 'delay' in effects
    
    def test_add_effect(self):
        """Test adding effects to the chain."""
        self.processor.add_effect('reverb')
        assert len(self.processor.effect_chain) == 1
        assert self.processor.effect_chain[0]['name'] == 'reverb'
        
        # Add with parameters
        self.processor.add_effect('delay', {'time': 0.5})
        assert len(self.processor.effect_chain) == 2
        assert self.processor.effect_chain[1]['parameters']['time'] == 0.5
    
    def test_add_unsupported_effect(self):
        """Test adding an unsupported effect."""
        with pytest.raises(ValueError):
            self.processor.add_effect('unsupported_effect')
    
    def test_remove_effect(self):
        """Test removing effects from the chain."""
        self.processor.add_effect('reverb')
        self.processor.add_effect('delay')
        
        result = self.processor.remove_effect('reverb')
        assert result is True
        assert len(self.processor.effect_chain) == 1
        assert self.processor.effect_chain[0]['name'] == 'delay'
        
        # Try to remove non-existent effect
        result = self.processor.remove_effect('nonexistent')
        assert result is False
    
    def test_clear_effects(self):
        """Test clearing all effects."""
        self.processor.add_effect('reverb')
        self.processor.add_effect('delay')
        assert len(self.processor.effect_chain) == 2
        
        self.processor.clear_effects()
        assert len(self.processor.effect_chain) == 0
    
    def test_get_effect_chain(self):
        """Test getting the effect chain."""
        self.processor.add_effect('reverb')
        self.processor.add_effect('delay', {'time': 0.3})
        
        chain = self.processor.get_effect_chain()
        assert len(chain) == 2
        assert chain[0]['name'] == 'reverb'
        assert chain[1]['name'] == 'delay'
        assert chain[1]['parameters']['time'] == 0.3
    
    def test_process_audio(self):
        """Test processing audio data."""
        # Mock audio data
        audio_data = {
            'file_path': 'test.wav',
            'format': '.wav',
            'sample_rate': 44100,
            'channels': 2,
            'data': 'mock_audio_data'
        }
        
        self.processor.add_effect('reverb')
        self.processor.add_effect('delay')
        
        processed = self.processor.process(audio_data)
        
        assert processed is not None
        assert 'effects_applied' in processed
        assert 'processing_chain' in processed
        assert 'reverb' in processed['effects_applied']
        assert 'delay' in processed['effects_applied']
        assert len(processed['processing_chain']) == 2