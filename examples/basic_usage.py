"""
Basic example of using DOOMLOADER to load and process NAM files.
"""

import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from doomloader import NAMLoader, AmpSimulator, FileHandler


def main():
    """
    Demonstrate basic DOOMLOADER functionality.
    """
    print("DOOMLOADER - NAM File Support Example")
    print("=" * 40)
    
    # Initialize components
    nam_loader = NAMLoader()
    amp_sim = AmpSimulator(sample_rate=44100)
    file_handler = FileHandler()
    
    print(f"Supported NAM formats: {nam_loader.supported_formats}")
    print(f"Sample rate: {amp_sim.sample_rate} Hz")
    
    # Example: Create a sample NAM file for testing
    example_dir = Path("./example_nam_files")
    example_dir.mkdir(exist_ok=True)
    
    # Create a sample metadata file
    sample_metadata = {
        "name": "Example Amp Model",
        "type": "tube_amp",
        "gain_range": [0.0, 1.0],
        "description": "A sample NAM amp model for testing",
        "author": "DOOMLOADER",
        "version": "1.0"
    }
    
    metadata_file = example_dir / "example_amp.json"
    import json
    with open(metadata_file, 'w') as f:
        json.dump(sample_metadata, f, indent=2)
    
    print(f"\nCreated sample metadata file: {metadata_file}")
    
    # Load the metadata file
    try:
        metadata = nam_loader.load_nam_file(metadata_file)
        print(f"Loaded metadata: {metadata.get('name', 'Unknown')}")
        
        model_info = nam_loader.get_model_info(metadata)
        print(f"Model info: {model_info}")
        
    except Exception as e:
        print(f"Error loading metadata: {e}")
    
    # Example: Scan directory for NAM files
    print(f"\nScanning directory: {example_dir}")
    try:
        scan_results = file_handler.scan_directory(example_dir)
        for category, files in scan_results.items():
            if files:
                print(f"  {category}: {len(files)} files")
                for file_path in files:
                    file_info = file_handler.get_file_info(file_path)
                    print(f"    - {file_info['name']} ({file_info['size_human']})")
    except Exception as e:
        print(f"Error scanning directory: {e}")
    
    # Example: Audio processing simulation
    print(f"\nAudio Processing Example:")
    print("Generating test audio signal...")
    
    # Generate a simple test signal (1 second of sine wave)
    duration = 1.0  # seconds
    frequency = 440.0  # Hz (A4 note)
    sample_rate = amp_sim.sample_rate
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    test_audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    print(f"Test signal: {len(test_audio)} samples, {duration}s duration")
    
    # Set amp parameters
    amp_sim.set_parameters(gain=0.7, tone=0.6, volume=0.8)
    params = amp_sim.get_parameters()
    print(f"Amp parameters: {params}")
    
    # Process audio (this will use the simplified simulation since no real NAM model is loaded)
    try:
        # For demonstration, we'll simulate having a model loaded
        amp_sim.loaded_models['demo_model'] = {
            'file_path': 'demo',
            'model_type': 'nam',
            'file_size': 1024
        }
        amp_sim.current_model = 'demo_model'
        
        processed_audio = amp_sim.process_audio(test_audio)
        print(f"Processed audio: {len(processed_audio)} samples")
        print(f"Input RMS: {np.sqrt(np.mean(test_audio**2)):.4f}")
        print(f"Output RMS: {np.sqrt(np.mean(processed_audio**2)):.4f}")
        
        # Get simulation info
        sim_info = amp_sim.get_simulation_info()
        print(f"Simulation info: {sim_info}")
        
    except Exception as e:
        print(f"Error processing audio: {e}")
    
    print(f"\nExample completed successfully!")
    print(f"Check the '{example_dir}' directory for sample files.")


if __name__ == "__main__":
    main()