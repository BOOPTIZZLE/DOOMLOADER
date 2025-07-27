# Getting Started with DOOMLOADER

Welcome to DOOMLOADER! This guide will help you get up and running with the amp simulator, whether you're a user looking to get great guitar tone or a developer wanting to contribute to the project.

## For Users

### Installation

#### Download Pre-built Binaries
1. Visit the [Releases page](https://github.com/BOOPTIZZLE/DOOMLOADER/releases)
2. Download the appropriate version for your platform:
   - **Windows**: `DOOMLOADER-Windows-x64.zip`
   - **macOS**: `DOOMLOADER-macOS.dmg`
   - **Linux**: `DOOMLOADER-Linux-x64.tar.gz`

#### Plugin Installation
- **VST3**: Copy to your VST3 plugins folder
  - Windows: `C:\Program Files\Common Files\VST3\`
  - macOS: `~/Library/Audio/Plug-Ins/VST3/`
  - Linux: `~/.vst3/`
- **AU (macOS only)**: Copy to `~/Library/Audio/Plug-Ins/Components/`

### First Time Setup

1. **Launch DOOMLOADER** (standalone or in your DAW)
2. **Configure Audio Settings**:
   - Select your audio interface
   - Set buffer size (128-512 samples recommended)
   - Choose sample rate (44.1kHz or 48kHz)
3. **Load Your First Preset**:
   - Click "Presets" button
   - Browse to "Clean" category
   - Select "Clean Twin" preset

### Basic Workflow

1. **Connect Your Guitar**:
   - Use an audio interface with instrument input
   - Set input gain appropriately (avoid clipping)

2. **Choose an Amp Model**:
   - Click "Amp" section
   - Browse built-in models or load NAM files
   - Adjust gain, bass, mid, treble controls

3. **Add Cabinet Simulation**:
   - Click "IR" section  
   - Load impulse response files (.wav)
   - Adjust wet/dry mix

4. **Add Effects**:
   - Use built-in reverb, delay, chorus
   - Chain multiple effects as needed

5. **Save Your Settings**:
   - Click "Save Preset"
   - Give it a descriptive name
   - Choose appropriate category

## For Developers

### Development Environment Setup

#### Option 1: GitHub Codespaces (Recommended)
1. Click "Code" → "Open with Codespaces" on the repository
2. Wait for environment to initialize (includes all dependencies)
3. Run: `cmake --build build --config Debug`
4. Start developing!

#### Option 2: Local Development

##### Prerequisites
- CMake 3.20+
- C++17 compatible compiler
- Git

##### Clone and Build
```bash
git clone https://github.com/BOOPTIZZLE/DOOMLOADER.git
cd DOOMLOADER

# Create build directory
mkdir build && cd build

# Configure
cmake .. -DCMAKE_BUILD_TYPE=Debug \
         -DDOOMLOADER_BUILD_EXAMPLES=ON \
         -DDOOMLOADER_ENABLE_TESTING=ON

# Build
cmake --build . --config Debug

# Run tests
ctest
```

### Project Architecture

```
DoomloaderEngine
├── AmpModeler (NAM integration)
├── ConvolutionEngine (IR processing)
├── PresetManager (save/load)
├── EffectChain (reverb, delay, etc.)
└── Tone3000Client (cloud sync)
```

### Key Components

#### DoomloaderEngine
Main processing engine that orchestrates all components:
```cpp
doomloader::DoomloaderEngine engine;
engine.initialize(44100.0, 512);
engine.loadPreset("my-preset.json");
engine.processAudio(buffer);
```

#### AmpModeler  
Neural amp modeling with NAM support:
```cpp
doomloader::AmpModeler amp;
amp.loadModel("marshall-jcm800.nam");
amp.setParameters(ampParams);
```

#### IRLoader & ConvolutionEngine
Impulse response loading and convolution:
```cpp
doomloader::IRLoader ir;
ir.loadIR("4x12-cabinet.wav");

doomloader::ConvolutionEngine conv;
conv.loadIR(ir.getIRSamples(), ir.getIRSampleRate());
```

#### PresetManager
Preset save/load with cloud sync:
```cpp
doomloader::PresetManager presets;
auto preset = presets.loadPreset("clean-twin.json");
presets.savePreset(myPreset, "my-tone.json");
```

### Building for Different Platforms

#### Desktop (Windows/macOS/Linux)
```bash
cmake .. -DDOOMLOADER_BUILD_PLUGIN=ON \
         -DDOOMLOADER_BUILD_STANDALONE=ON
cmake --build . --config Release
```

#### Mobile (iOS)
```bash
cmake .. -DCMAKE_TOOLCHAIN_FILE=cmake/ios.toolchain.cmake \
         -DPLATFORM=OS64 \
         -DDOOMLOADER_BUILD_STANDALONE=ON
cmake --build . --config Release
```

#### Mobile (Android)
```bash
cmake .. -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
         -DANDROID_ABI=arm64-v8a \
         -DANDROID_PLATFORM=android-24
cmake --build . --config Release
```

### Adding New Features

#### Adding a New Amp Model Type
1. Extend `AmpModeler::ModelType` enum
2. Implement loading logic in `AmpModeler::loadModel()`
3. Add processing in `AmpModeler::processAudio()`
4. Update documentation

#### Adding New Effects
1. Add effect to DSP chain in `DoomloaderEngine`
2. Expose parameters in public API
3. Add preset support in `PresetManager`
4. Update UI if needed

#### Adding Mobile Platform Support
1. Create platform-specific code in `platforms/`
2. Update CMake configuration
3. Add platform detection
4. Test on target devices

### Testing

```bash
# Build with testing enabled
cmake .. -DDOOMLOADER_ENABLE_TESTING=ON

# Run all tests
ctest

# Run specific test
ctest -R "test_amp_modeling"

# Run with verbose output
ctest --verbose
```

### Documentation

- Add docstrings to all public APIs
- Update relevant .md files in `docs/`
- Include code examples where helpful
- Test examples to ensure they work

## Next Steps

- **Users**: Check out the [Preset Management Guide](preset-management.md)
- **Developers**: See [API Reference](api-reference.md) for detailed documentation
- **Mobile Developers**: Read [Mobile Development Guide](mobile-development.md)

## Getting Help

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/BOOPTIZZLE/DOOMLOADER/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/BOOPTIZZLE/DOOMLOADER/discussions)
- 📧 **Email**: support@doomloader.com