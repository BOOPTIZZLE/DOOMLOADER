"""
NAM (Neural Amp Modeler) file loader and parser.
Handles loading of .nam files and associated metadata.
"""

import json
import os
import pickle
from pathlib import Path
from typing import Dict, Any, Optional, Union
import warnings


class NAMLoader:
    """
    Handles loading and parsing of NAM (Neural Amp Modeler) files.
    
    Supports:
    - .nam files (neural network models)
    - .json metadata files
    - Model validation and preprocessing
    """
    
    def __init__(self):
        self.supported_formats = ['.nam', '.json']
        self.loaded_models = {}
        
    def load_nam_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load a NAM file and return the model data.
        
        Args:
            file_path: Path to the NAM file
            
        Returns:
            Dictionary containing model data and metadata
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"NAM file not found: {file_path}")
            
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        try:
            if file_path.suffix.lower() == '.nam':
                return self._load_nam_model(file_path)
            elif file_path.suffix.lower() == '.json':
                return self._load_json_metadata(file_path)
        except Exception as e:
            raise ValueError(f"Error loading NAM file {file_path}: {str(e)}")
    
    def _load_nam_model(self, file_path: Path) -> Dict[str, Any]:
        """
        Load a .nam model file.
        
        Args:
            file_path: Path to the .nam file
            
        Returns:
            Dictionary containing model data
        """
        try:
            # NAM files are typically pickled or custom binary format
            # This is a simplified implementation - real NAM files might use
            # different formats (PyTorch, ONNX, etc.)
            with open(file_path, 'rb') as f:
                model_data = pickle.load(f)
                
            # Basic validation
            if not isinstance(model_data, dict):
                warnings.warn("NAM file format may not be standard")
                model_data = {'raw_data': model_data}
                
            # Add metadata
            model_data['file_path'] = str(file_path)
            model_data['file_size'] = file_path.stat().st_size
            model_data['model_type'] = 'nam'
            
            return model_data
            
        except pickle.UnpicklingError:
            # Try alternative loading methods
            return self._load_alternative_format(file_path)
    
    def _load_alternative_format(self, file_path: Path) -> Dict[str, Any]:
        """
        Handle alternative NAM file formats.
        
        Args:
            file_path: Path to the NAM file
            
        Returns:
            Dictionary containing model data
        """
        # For now, read as binary data
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            
        return {
            'raw_data': raw_data,
            'file_path': str(file_path),
            'file_size': len(raw_data),
            'model_type': 'nam_binary',
            'needs_processing': True
        }
    
    def _load_json_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Load JSON metadata file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dictionary containing metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        metadata['file_path'] = str(file_path)
        metadata['metadata_type'] = 'nam_config'
        
        return metadata
    
    def validate_nam_file(self, model_data: Dict[str, Any]) -> bool:
        """
        Validate NAM model data.
        
        Args:
            model_data: Model data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ['file_path', 'model_type']
        
        for key in required_keys:
            if key not in model_data:
                return False
                
        return True
    
    def get_model_info(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract model information and statistics.
        
        Args:
            model_data: Model data dictionary
            
        Returns:
            Dictionary with model information
        """
        info = {
            'file_path': model_data.get('file_path', 'unknown'),
            'model_type': model_data.get('model_type', 'unknown'),
            'file_size': model_data.get('file_size', 0),
            'is_valid': self.validate_nam_file(model_data)
        }
        
        # Add additional info if available
        if 'raw_data' in model_data:
            info['has_raw_data'] = True
            info['data_size'] = len(model_data['raw_data']) if isinstance(model_data['raw_data'], bytes) else 'unknown'
        
        return info