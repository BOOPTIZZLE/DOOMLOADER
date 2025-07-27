"""
Advanced example demonstrating NAM file processing and amp simulation.
Shows how to work with multiple models and batch processing.
"""

import numpy as np
import json
import pickle
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from doomloader import NAMLoader, AmpSimulator, FileHandler


def create_sample_nam_files():
    """Create sample NAM files for testing."""
    sample_dir = Path("./sample_nam_models")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample models directory structure
    models_dir = sample_dir / "models"
    metadata_dir = sample_dir / "metadata"
    models_dir.mkdir(exist_ok=True)
    metadata_dir.mkdir(exist_ok=True)
    
    # Sample model data (simplified)
    sample_models = [
        {
            "name": "vintage_tube",
            "type": "tube_amp",
            "description": "Vintage tube amplifier with warm overdrive",
            "gain_range": [0.0, 1.0],
            "recommended_settings": {"gain": 0.6, "tone": 0.7, "volume": 0.8}
        },
        {
            "name": "modern_high_gain",
            "type": "solid_state",
            "description": "High-gain modern amplifier for metal tones",
            "gain_range": [0.0, 1.0],
            "recommended_settings": {"gain": 0.9, "tone": 0.4, "volume": 0.7}
        },
        {
            "name": "clean_jazz",
            "type": "tube_amp",
            "description": "Clean jazz amplifier with crystal clarity",
            "gain_range": [0.0, 0.3],
            "recommended_settings": {"gain": 0.1, "tone": 0.8, "volume": 0.9}
        }
    ]
    
    created_files = []
    
    for model_info in sample_models:
        model_name = model_info["name"]
        
        # Create metadata file
        metadata_file = metadata_dir / f"{model_name}.json"
        with open(metadata_file, 'w') as f:
            json.dump(model_info, f, indent=2)
        created_files.append(metadata_file)
        
        # Create sample NAM model file (simplified binary data)
        model_file = models_dir / f"{model_name}.nam"
        sample_model_data = {
            "model_type": "nam",
            "name": model_info["name"],
            "weights": np.random.random((10, 10)).tolist(),  # Simplified model weights
            "architecture": "feedforward",
            "input_size": 1,
            "output_size": 1,
            "sample_rate": 44100
        }
        
        with open(model_file, 'wb') as f:
            pickle.dump(sample_model_data, f)
        created_files.append(model_file)
    
    return sample_dir, created_files


def demonstrate_file_operations():
    """Demonstrate file handling operations."""
    print("=== File Operations Demo ===")
    
    # Create sample files
    sample_dir, created_files = create_sample_nam_files()
    print(f"Created sample directory: {sample_dir}")
    print(f"Created {len(created_files)} sample files")
    
    # Initialize file handler
    handler = FileHandler()
    
    # Scan directory
    print(f"\nScanning directory: {sample_dir}")
    scan_results = handler.scan_directory(sample_dir)
    
    for category, files in scan_results.items():
        if files:
            print(f"  {category}: {len(files)} files")
            for file_path in files[:3]:  # Show first 3 files
                file_info = handler.get_file_info(file_path)
                print(f"    - {file_info['name']} ({file_info['size_human']})")
    
    # Validate structure
    validation = handler.validate_file_structure(sample_dir)
    print(f"\nValidation results:")
    print(f"  Valid structure: {validation['is_valid']}")
    print(f"  File counts: {validation['file_counts']}")
    
    if validation['warnings']:
        print(f"  Warnings: {validation['warnings']}")
    if validation['errors']:
        print(f"  Errors: {validation['errors']}")
    
    # Create manifest
    manifest = handler.create_file_manifest(sample_dir)
    print(f"\nManifest summary: {manifest['summary']}")
    
    return sample_dir


def demonstrate_nam_loading():
    """Demonstrate NAM file loading and model information."""
    print("\n=== NAM Loading Demo ===")
    
    sample_dir = Path("./sample_nam_models")
    if not sample_dir.exists():
        print("Sample directory not found. Running file operations demo first...")
        sample_dir = demonstrate_file_operations()
    
    loader = NAMLoader()
    
    # Find all NAM files
    handler = FileHandler()
    nam_files = handler.find_nam_files(sample_dir, recursive=True)
    
    loaded_models = {}
    
    print(f"Found {len(nam_files)} NAM files")
    
    for nam_file in nam_files:
        try:
            print(f"\nLoading: {nam_file.name}")
            
            if nam_file.suffix == '.nam':
                model_data = loader.load_nam_file(nam_file)
                model_info = loader.get_model_info(model_data)
                
                print(f"  Model type: {model_info['model_type']}")
                print(f"  File size: {model_info['file_size']} bytes")
                print(f"  Valid: {model_info['is_valid']}")
                
                # Store for later use
                loaded_models[nam_file.stem] = model_data
                
                # Show model details if available
                if 'name' in model_data:
                    print(f"  Name: {model_data['name']}")
                if 'architecture' in model_data:
                    print(f"  Architecture: {model_data['architecture']}")
                    
            elif nam_file.suffix == '.json':
                metadata = loader.load_nam_file(nam_file)
                print(f"  Metadata for: {metadata.get('name', 'Unknown')}")
                print(f"  Type: {metadata.get('type', 'Unknown')}")
                print(f"  Description: {metadata.get('description', 'No description')}")
                
        except Exception as e:
            print(f"  Error loading {nam_file}: {e}")
    
    return loaded_models


def demonstrate_amp_simulation():
    """Demonstrate amp simulation with loaded models."""
    print("\n=== Amp Simulation Demo ===")
    
    sample_dir = Path("./sample_nam_models")
    if not sample_dir.exists():
        print("Creating sample files first...")
        demonstrate_file_operations()
    
    # Initialize amp simulator
    amp_sim = AmpSimulator(sample_rate=44100)
    
    # Load models
    handler = FileHandler()
    nam_files = [f for f in handler.find_nam_files(sample_dir) if f.suffix == '.nam']
    
    print(f"Loading {len(nam_files)} NAM models...")
    
    for nam_file in nam_files:
        try:
            model_name = amp_sim.load_nam_model(nam_file, nam_file.stem)
            print(f"  Loaded: {model_name}")
        except Exception as e:
            print(f"  Error loading {nam_file.name}: {e}")
    
    loaded_models = amp_sim.get_loaded_models()
    print(f"\nTotal loaded models: {len(loaded_models)}")
    
    # Test each model with different settings
    for model_name in loaded_models:
        print(f"\n--- Testing model: {model_name} ---")
        
        # Set current model
        amp_sim.set_current_model(model_name)
        
        # Get model info
        model_info = amp_sim.get_model_info()
        print(f"Model info: {model_info}")
        
        # Load corresponding metadata for recommended settings
        metadata_file = sample_dir / "metadata" / f"{model_name}.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                
            if 'recommended_settings' in metadata:
                settings = metadata['recommended_settings']
                amp_sim.set_parameters(**settings)
                print(f"Applied recommended settings: {settings}")
        
        # Generate test signal
        duration = 0.5  # seconds
        sample_rate = amp_sim.sample_rate
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Create different test signals for different amp types
        if 'clean' in model_name.lower():
            # Clean signal - single tone
            test_signal = 0.2 * np.sin(2 * np.pi * 220 * t)  # A3
        elif 'high_gain' in model_name.lower():
            # Aggressive signal for high gain
            test_signal = 0.5 * np.sin(2 * np.pi * 110 * t)  # A2
            # Add some harmonics
            test_signal += 0.2 * np.sin(2 * np.pi * 220 * t)
        else:
            # Medium complexity signal
            test_signal = 0.3 * np.sin(2 * np.pi * 146.8 * t)  # D3
            test_signal += 0.2 * np.sin(2 * np.pi * 196 * t)   # G3
        
        # Process through amp
        processed = amp_sim.process_audio(test_signal)
        
        # Calculate statistics
        input_rms = np.sqrt(np.mean(test_signal**2))
        output_rms = np.sqrt(np.mean(processed**2))
        gain_change = output_rms / input_rms if input_rms > 0 else 0
        
        print(f"Audio processing results:")
        print(f"  Input RMS: {input_rms:.4f}")
        print(f"  Output RMS: {output_rms:.4f}")
        print(f"  Gain change: {gain_change:.2f}x")
        
        # Check for clipping
        if np.max(np.abs(processed)) > 0.95:
            print(f"  Warning: Output signal may be clipping!")


def demonstrate_batch_processing():
    """Demonstrate batch processing of multiple NAM files."""
    print("\n=== Batch Processing Demo ===")
    
    sample_dir = Path("./sample_nam_models")
    if not sample_dir.exists():
        print("Creating sample files first...")
        demonstrate_file_operations()
    
    # Initialize components
    loader = NAMLoader()
    handler = FileHandler()
    
    # Find all files
    scan_results = handler.scan_directory(sample_dir)
    
    # Process results
    results = {
        'successful_loads': 0,
        'failed_loads': 0,
        'total_size': 0,
        'model_types': {},
        'errors': []
    }
    
    print("Processing all NAM files...")
    
    for nam_file in scan_results['nam_files']:
        try:
            model_data = loader.load_nam_file(nam_file)
            model_info = loader.get_model_info(model_data)
            
            results['successful_loads'] += 1
            results['total_size'] += model_info.get('file_size', 0)
            
            model_type = model_info.get('model_type', 'unknown')
            results['model_types'][model_type] = results['model_types'].get(model_type, 0) + 1
            
            print(f"  ✓ {nam_file.name}: {model_type}")
            
        except Exception as e:
            results['failed_loads'] += 1
            results['errors'].append(f"{nam_file.name}: {str(e)}")
            print(f"  ✗ {nam_file.name}: {str(e)}")
    
    # Print summary
    print(f"\nBatch Processing Summary:")
    print(f"  Successful loads: {results['successful_loads']}")
    print(f"  Failed loads: {results['failed_loads']}")
    print(f"  Total size: {results['total_size']} bytes")
    print(f"  Model types: {results['model_types']}")
    
    if results['errors']:
        print(f"  Errors:")
        for error in results['errors']:
            print(f"    - {error}")


def main():
    """Run all demonstrations."""
    print("DOOMLOADER Advanced NAM File Processing Demo")
    print("=" * 50)
    
    try:
        # Run demonstrations
        demonstrate_file_operations()
        demonstrate_nam_loading()
        demonstrate_amp_simulation()
        demonstrate_batch_processing()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed successfully!")
        print("Check the 'sample_nam_models' directory for created files.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())