"""
Audio processor module for DOOMLOADER

Handles audio processing and effects application.
"""

from typing import Dict, Any, Optional, List


class AudioProcessor:
    """Process audio data with various effects and transformations."""
    
    def __init__(self):
        """Initialize the AudioProcessor."""
        self.available_effects = [
            'reverb', 'delay', 'distortion', 'equalizer', 'compressor'
        ]
        self.effect_chain = []
    
    def add_effect(self, effect_name: str, parameters: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an effect to the processing chain.
        
        Args:
            effect_name: Name of the effect to add
            parameters: Effect parameters (optional)
            
        Raises:
            ValueError: If effect is not supported
        """
        if effect_name not in self.available_effects:
            raise ValueError(f"Unsupported effect: {effect_name}")
        
        effect_config = {
            'name': effect_name,
            'parameters': parameters or {}
        }
        self.effect_chain.append(effect_config)
    
    def remove_effect(self, effect_name: str) -> bool:
        """
        Remove an effect from the processing chain.
        
        Args:
            effect_name: Name of the effect to remove
            
        Returns:
            True if effect was removed, False if not found
        """
        for i, effect in enumerate(self.effect_chain):
            if effect['name'] == effect_name:
                self.effect_chain.pop(i)
                return True
        return False
    
    def process(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process audio data through the effect chain.
        
        Args:
            audio_data: Audio data dictionary from AudioLoader
            
        Returns:
            Processed audio data dictionary
        """
        # TODO: Implement actual audio processing logic
        # For now, return the input data with processing metadata
        processed_data = audio_data.copy()
        processed_data['effects_applied'] = [effect['name'] for effect in self.effect_chain]
        processed_data['processing_chain'] = self.effect_chain.copy()
        
        return processed_data
    
    def get_available_effects(self) -> List[str]:
        """Get list of available effects."""
        return self.available_effects.copy()
    
    def clear_effects(self) -> None:
        """Clear all effects from the processing chain."""
        self.effect_chain.clear()
    
    def get_effect_chain(self) -> List[Dict[str, Any]]:
        """Get the current effect chain."""
        return self.effect_chain.copy()