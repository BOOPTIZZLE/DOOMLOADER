# DOOMLOADER

A Neural Amp Modeler (NAM) file support tool for guitar amp simulation. DOOMLOADER provides a comprehensive framework for loading, processing, and integrating NAM files into amp simulation workflows.

*A place where good tone goes to die. And probably not get improved.*

## Features

- **NAM File Support**: Load and parse Neural Amp Modeler files (.nam, .json metadata)
- **Amp Simulation**: Real-time guitar amp simulation using NAM models
- **File Management**: Scan, organize, and validate NAM file collections
- **Audio Processing**: Process audio through NAM-based amp simulations
- **CLI Tools**: Command-line interface for batch operations
- **Python API**: Full programmatic access to all functionality

## Installation

### From Source

```bash
git clone https://github.com/BOOPTIZZLE/DOOMLOADER.git
cd DOOMLOADER
pip install -r requirements.txt
pip install -e .
```

### Dependencies

- Python 3.7+
- NumPy >= 1.21.0
- SciPy >= 1.7.0

## Quick Start

### Basic Usage

```python
from doomloader import NAMLoader, AmpSimulator, FileHandler

# Initialize components
nam_loader = NAMLoader()
amp_sim = AmpSimulator(sample_rate=44100)
file_handler = FileHandler()

# Load a NAM model
model_data = nam_loader.load_nam_file("path/to/amp_model.nam")
model_name = amp_sim.load_nam_model("path/to/amp_model.nam")

# Set amp parameters
amp_sim.set_parameters(gain=0.7, tone=0.6, volume=0.8)

# Process audio
import numpy as np
test_audio = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))  # 1 second 440Hz tone
processed_audio = amp_sim.process_audio(test_audio)
```

### Command Line Interface

```bash
# Scan directory for NAM files
doomloader scan ./nam_models --validate

# Get information about a NAM file
doomloader info ./amp_model.nam --detailed

# Run amp simulation
doomloader simulate ./amp_model.nam --gain 0.7 --tone 0.6 --volume 0.8
```

## NAM File Support

### Supported Formats

- **.nam files**: Neural network model files (binary format)
- **.json files**: Metadata and configuration files
- **Audio files**: .wav, .mp3, .flac (for impulse responses and training data)

### File Structure

DOOMLOADER expects NAM files to follow this organization:

```
nam_models/
├── models/
│   ├── vintage_tube.nam
│   ├── modern_high_gain.nam
│   └── clean_jazz.nam
├── metadata/
│   ├── vintage_tube.json
│   ├── modern_high_gain.json
│   └── clean_jazz.json
└── audio/
    ├── impulse_responses/
    └── training_data/
```

### Metadata Format

JSON metadata files should include:

```json
{
  "name": "Vintage Tube Amp",
  "type": "tube_amp",
  "gain_range": [0.0, 1.0],
  "description": "Classic vintage tube amplifier model",
  "author": "ModelCreator",
  "version": "1.0",
  "sample_rate": 44100,
  "parameters": {
    "gain": 0.5,
    "tone": 0.5,
    "volume": 0.8
  }
}
```

## API Reference

### NAMLoader

The `NAMLoader` class handles loading and parsing of NAM files.

```python
loader = NAMLoader()

# Load NAM file
model_data = loader.load_nam_file("amp_model.nam")

# Validate model
is_valid = loader.validate_nam_file(model_data)

# Get model information
info = loader.get_model_info(model_data)
```

### AmpSimulator

The `AmpSimulator` class provides amp simulation functionality.

```python
amp_sim = AmpSimulator(sample_rate=44100)

# Load NAM model
model_name = amp_sim.load_nam_model("amp_model.nam")

# Set current model
amp_sim.set_current_model(model_name)

# Configure parameters
amp_sim.set_parameters(gain=0.7, tone=0.6, volume=0.8)

# Process audio
processed = amp_sim.process_audio(audio_data)

# Get simulation info
info = amp_sim.get_simulation_info()
```

### FileHandler

The `FileHandler` class manages NAM file operations.

```python
handler = FileHandler()

# Find NAM files
nam_files = handler.find_nam_files("./models", recursive=True)

# Scan directory
scan_results = handler.scan_directory("./models")

# Validate file structure
validation = handler.validate_file_structure("./models")

# Create file manifest
manifest = handler.create_file_manifest("./models", "manifest.json")
```

## Examples

### Loading and Processing NAM Files

```python
import numpy as np
from doomloader import NAMLoader, AmpSimulator

# Initialize
nam_loader = NAMLoader()
amp_sim = AmpSimulator()

# Load model
model_data = nam_loader.load_nam_file("vintage_amp.nam")
print(f"Loaded model: {model_data.get('name', 'Unknown')}")

# Load into simulator
model_name = amp_sim.load_nam_model("vintage_amp.nam")
amp_sim.set_current_model(model_name)

# Set amp parameters for vintage tone
amp_sim.set_parameters(
    gain=0.6,    # Moderate drive
    tone=0.7,    # Warm tone
    volume=0.8   # Good output level
)

# Generate test signal (guitar-like)
sample_rate = 44100
duration = 2.0
t = np.linspace(0, duration, int(sample_rate * duration))

# Simulate guitar chord (multiple frequencies)
frequencies = [82.4, 110.0, 146.8, 196.0]  # E2, A2, D3, G3
guitar_signal = sum(0.25 * np.sin(2 * np.pi * f * t) for f in frequencies)

# Add some pick attack transient
envelope = np.exp(-t * 2)
guitar_signal *= envelope

# Process through amp
processed = amp_sim.process_audio(guitar_signal)

print(f"Processed {len(processed)} samples")
print(f"RMS change: {np.sqrt(np.mean(guitar_signal**2)):.3f} -> {np.sqrt(np.mean(processed**2)):.3f}")
```

### Batch Processing NAM Files

```python
from pathlib import Path
from doomloader import FileHandler, NAMLoader

# Scan for NAM files
handler = FileHandler()
loader = NAMLoader()

nam_directory = Path("./nam_collection")
nam_files = handler.find_nam_files(nam_directory)

print(f"Found {len(nam_files)} NAM files")

# Process each file
for nam_file in nam_files:
    try:
        model_data = loader.load_nam_file(nam_file)
        info = loader.get_model_info(model_data)
        
        print(f"Model: {nam_file.name}")
        print(f"  Type: {info['model_type']}")
        print(f"  Size: {info['file_size']} bytes")
        print(f"  Valid: {info['is_valid']}")
        
    except Exception as e:
        print(f"Error processing {nam_file}: {e}")
```

### Directory Organization

```python
from doomloader import FileHandler

handler = FileHandler()

# Organize scattered NAM files
source_dir = "./unorganized_nam_files"
target_dir = "./organized_nam_models"

# Organize with subdirectories
results = handler.organize_nam_files(
    source_dir=source_dir,
    target_dir=target_dir,
    create_subdirs=True
)

print(f"Organization complete:")
print(f"  Files moved: {results['moved_files']}")
print(f"  Directories created: {len(results['created_directories'])}")
print(f"  Errors: {len(results['errors'])}")

# Validate the organized structure
validation = handler.validate_file_structure(target_dir)
print(f"Structure is valid: {validation['is_valid']}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Neural Amp Modeler (NAM) project for the amp modeling technology
- The guitar and audio processing community for inspiration and feedback
