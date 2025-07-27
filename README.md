# DOOMLOADER

**A powerful, cross-platform amp simulator with neural modeling capabilities**

DOOMLOADER is a standalone amp simulator that brings together the best of neural amp modeling, impulse response convolution, and modern audio processing. Built with mobile and desktop compatibility in mind, it integrates NeuralAmpModelerCore, JUCE framework, and Tone3000 API for a comprehensive guitar tone solution.

## 🚀 Features

- **Neural Amp Modeling**: Load and process NAM (Neural Amp Modeler) models for authentic amp simulation
- **Impulse Response Support**: Full IR loading and convolution for cabinet simulation
- **Cross-Platform**: Runs on Windows, macOS, Linux, iOS, and Android
- **Plugin Formats**: Available as VST3, AU, and standalone application
- **Cloud Integration**: Sync presets and models with Tone3000 API
- **Modern UI**: Responsive interface built with JUCE
- **GitHub Codespaces**: Full development environment in the cloud

## 📦 Installation

### From Releases
Download the latest release for your platform from the [Releases](https://github.com/BOOPTIZZLE/DOOMLOADER/releases) page.

### Building from Source
```bash
git clone https://github.com/BOOPTIZZLE/DOOMLOADER.git
cd DOOMLOADER
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

## 🛠 Development

### Prerequisites
- CMake 3.20+
- Modern C++ compiler (C++17 support)
- Git

### Quick Start with GitHub Codespaces
1. Click "Code" → "Open with Codespaces" on this repository
2. Wait for the environment to initialize
3. Run `cmake --build build --config Debug`
4. Start developing!

### Local Development Setup

#### Dependencies
The build system automatically handles these dependencies:
- **JUCE Framework**: Cross-platform audio framework
- **NeuralAmpModelerCore**: Neural amp modeling engine  
- **nlohmann/json**: JSON parsing for presets and configuration
- **cURL**: HTTP client for Tone3000 API integration

#### Build Configuration
```bash
# Configure build with options
cmake -B build \
  -DDOOMLOADER_BUILD_PLUGIN=ON \
  -DDOOMLOADER_BUILD_STANDALONE=ON \
  -DDOOMLOADER_BUILD_EXAMPLES=ON \
  -DDOOMLOADER_ENABLE_TESTING=ON

# Build
cmake --build build --config Release

# Install
cmake --install build
```

## 📖 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Impulse Response Loading](docs/ir-loading.md) 
- [Amp Modeling Guide](docs/amp-modeling.md)
- [Preset Management](docs/preset-management.md)
- [API Reference](docs/api-reference.md)
- [Mobile Development](docs/mobile-development.md)
- [Plugin Development](docs/plugin-development.md)

## 🎸 Usage

### Basic Audio Processing
```cpp
#include "DoomloaderEngine.h"

doomloader::DoomloaderEngine engine;
engine.initialize(44100.0, 512);

// Load an amp model
engine.loadAmpModel("path/to/model.nam");

// Load impulse response
engine.loadImpulseResponse("path/to/cabinet.wav");

// Process audio
engine.processAudio(audioBuffer);
```

### Preset Management
```cpp
#include "PresetManager.h"

doomloader::PresetManager presets;
presets.initialize("./presets");

// Load a preset
auto preset = presets.loadPreset("clean-twin.json");

// Search presets
auto metalPresets = presets.getPresetsByCategory("Metal");
```

## 🏗 Project Structure

```
DOOMLOADER/
├── src/                    # Core source code
│   ├── Core/              # Main engine and processing
│   ├── NAM/               # Neural Amp Modeler integration
│   ├── Tone3000/          # Cloud API integration
│   ├── Audio/             # Audio processing utilities
│   ├── Plugin/            # Audio plugin implementation
│   └── Standalone/        # Standalone application
├── include/               # Public headers
├── docs/                  # Documentation
├── examples/              # Example projects
├── presets/               # Default presets
├── impulse_responses/     # Sample IR files
├── cmake/                 # Build configuration
├── platforms/             # Platform-specific code
└── .devcontainer/         # Codespaces configuration
```

## 🔌 Plugin Usage

### As VST3/AU Plugin
1. Install DOOMLOADER plugin to your DAW's plugin directory
2. Load in your DAW as an audio effect
3. Load presets or create your own tone
4. Adjust amp and IR parameters in real-time

### Standalone Application
1. Launch DOOMLOADER standalone
2. Configure audio input/output devices
3. Load guitar signal and start playing
4. Use built-in preset browser and editor

## 🌍 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows  | ✅ | VST3, Standalone |
| macOS    | ✅ | VST3, AU, Standalone |
| Linux    | ✅ | VST3, Standalone |
| iOS      | 🚧 | In development |
| Android  | 🚧 | In development |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Neural Amp Modeler](https://github.com/sdatkinson/NeuralAmpModeler) for neural modeling technology
- [JUCE Framework](https://juce.com/) for cross-platform audio development
- Tone3000 for cloud-based preset and model sharing
- The open-source audio development community

## 🆘 Support

- 📖 Check the [documentation](docs/)
- 🐛 Report bugs via [GitHub Issues](https://github.com/BOOPTIZZLE/DOOMLOADER/issues)
- 💬 Join discussions in [GitHub Discussions](https://github.com/BOOPTIZZLE/DOOMLOADER/discussions)
- ✉️ Contact: [support@doomloader.com](mailto:support@doomloader.com)

---

**DOOMLOADER**: Where tone goes to live, thrive, and get dramatically improved! 🎸🔥
