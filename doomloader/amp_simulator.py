"""
Amp simulation workflow that integrates NAM models.
Handles the processing pipeline for guitar amp simulation using NAM files.
"""

import numpy as np
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import warnings

from .nam_loader import NAMLoader


class AmpSimulator:
    """
    Handles amp simulation workflow using NAM (Neural Amp Modeler) files.
    
    Provides:
    - NAM model integration
    - Audio processing pipeline
    - Amp simulation parameters
    - Tone shaping controls
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the amp simulator.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.nam_loader = NAMLoader()
        self.loaded_models = {}
        self.current_model = None
        self.processing_parameters = {
            'gain': 1.0,
            'tone': 0.5,
            'volume': 0.8,
            'bias': 0.0
        }
        
    def load_nam_model(self, model_path: Union[str, Path], model_name: Optional[str] = None) -> str:
        """
        Load a NAM model for amp simulation.
        
        Args:
            model_path: Path to the NAM file
            model_name: Optional name for the model (uses filename if not provided)
            
        Returns:
            Model identifier string
            
        Raises:
            ValueError: If model loading fails
        """
        model_path = Path(model_path)
        
        if model_name is None:
            model_name = model_path.stem
            
        try:
            model_data = self.nam_loader.load_nam_file(model_path)
            
            # Validate the model
            if not self.nam_loader.validate_nam_file(model_data):
                raise ValueError(f"Invalid NAM model: {model_path}")
                
            # Store the model
            self.loaded_models[model_name] = model_data
            
            # Set as current model if it's the first one loaded
            if self.current_model is None:
                self.current_model = model_name
                
            return model_name
            
        except Exception as e:
            raise ValueError(f"Failed to load NAM model {model_path}: {str(e)}")
    
    def set_current_model(self, model_name: str) -> None:
        """
        Set the current active NAM model.
        
        Args:
            model_name: Name of the loaded model to activate
            
        Raises:
            ValueError: If model is not loaded
        """
        if model_name not in self.loaded_models:
            raise ValueError(f"Model '{model_name}' not loaded. Available models: {list(self.loaded_models.keys())}")
            
        self.current_model = model_name
    
    def get_loaded_models(self) -> List[str]:
        """
        Get list of loaded model names.
        
        Returns:
            List of model names
        """
        return list(self.loaded_models.keys())
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a loaded model.
        
        Args:
            model_name: Model name (uses current model if not specified)
            
        Returns:
            Dictionary containing model information
        """
        if model_name is None:
            model_name = self.current_model
            
        if model_name is None or model_name not in self.loaded_models:
            return {'error': 'No model specified or model not found'}
            
        model_data = self.loaded_models[model_name]
        return self.nam_loader.get_model_info(model_data)
    
    def set_parameters(self, **params) -> None:
        """
        Set amp simulation parameters.
        
        Args:
            **params: Parameter key-value pairs (gain, tone, volume, bias)
        """
        for param, value in params.items():
            if param in self.processing_parameters:
                # Clamp values to reasonable ranges
                if param in ['gain', 'tone', 'volume']:
                    value = max(0.0, min(1.0, float(value)))
                elif param == 'bias':
                    value = max(-1.0, min(1.0, float(value)))
                    
                self.processing_parameters[param] = value
            else:
                warnings.warn(f"Unknown parameter: {param}")
    
    def get_parameters(self) -> Dict[str, float]:
        """
        Get current amp simulation parameters.
        
        Returns:
            Dictionary of current parameters
        """
        return self.processing_parameters.copy()
    
    def process_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Process audio through the NAM amp simulation.
        
        Args:
            audio_data: Input audio data (numpy array)
            
        Returns:
            Processed audio data
            
        Raises:
            ValueError: If no model is loaded or audio format is invalid
        """
        if self.current_model is None:
            raise ValueError("No NAM model loaded for processing")
            
        if not isinstance(audio_data, np.ndarray):
            raise ValueError("Audio data must be a numpy array")
            
        # Get current model
        model_data = self.loaded_models[self.current_model]
        
        # Apply pre-processing
        processed_audio = self._apply_preprocessing(audio_data)
        
        # Apply NAM model simulation (simplified implementation)
        processed_audio = self._apply_nam_simulation(processed_audio, model_data)
        
        # Apply post-processing
        processed_audio = self._apply_postprocessing(processed_audio)
        
        return processed_audio
    
    def _apply_preprocessing(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Apply pre-processing to audio data.
        
        Args:
            audio_data: Input audio data
            
        Returns:
            Pre-processed audio data
        """
        # Apply gain
        gain_factor = self.processing_parameters['gain']
        processed = audio_data * gain_factor
        
        # Apply bias (DC offset)
        bias = self.processing_parameters['bias']
        processed = processed + bias
        
        # Clamp to prevent clipping
        processed = np.clip(processed, -1.0, 1.0)
        
        return processed
    
    def _apply_nam_simulation(self, audio_data: np.ndarray, model_data: Dict[str, Any]) -> np.ndarray:
        """
        Apply NAM model simulation (simplified implementation).
        
        Args:
            audio_data: Pre-processed audio data
            model_data: NAM model data
            
        Returns:
            NAM-processed audio data
        """
        # This is a simplified simulation - real NAM processing would involve
        # running the neural network model on the audio data
        
        # For now, apply basic non-linear transformation to simulate amp behavior
        tone = self.processing_parameters['tone']
        
        # Simple saturation curve that mimics tube amp behavior
        drive = 1.0 + tone * 4.0  # Map tone to drive amount
        processed = np.tanh(audio_data * drive) / drive
        
        # Add some harmonic content
        harmonic_content = np.sin(audio_data * np.pi) * tone * 0.1
        processed = processed + harmonic_content
        
        # Clamp output
        processed = np.clip(processed, -1.0, 1.0)
        
        return processed
    
    def _apply_postprocessing(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Apply post-processing to audio data.
        
        Args:
            audio_data: NAM-processed audio data
            
        Returns:
            Final processed audio data
        """
        # Apply volume
        volume = self.processing_parameters['volume']
        processed = audio_data * volume
        
        # Final clamp
        processed = np.clip(processed, -1.0, 1.0)
        
        return processed
    
    def get_simulation_info(self) -> Dict[str, Any]:
        """
        Get information about current simulation setup.
        
        Returns:
            Dictionary with simulation information
        """
        return {
            'sample_rate': self.sample_rate,
            'current_model': self.current_model,
            'loaded_models': list(self.loaded_models.keys()),
            'parameters': self.processing_parameters.copy(),
            'models_count': len(self.loaded_models)
        }