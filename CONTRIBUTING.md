# Contributing to DOOMLOADER

We welcome contributions to DOOMLOADER! This guide outlines how to contribute effectively to the project.

## Getting Started

### Prerequisites

- Git knowledge
- C++17 experience
- CMake familiarity
- Basic audio programming understanding

### Development Environment

1. **GitHub Codespaces (Recommended)**:
   - Click "Code" → "Open with Codespaces"
   - Environment automatically configured
   - All dependencies included

2. **Local Development**:
   ```bash
   git clone https://github.com/BOOPTIZZLE/DOOMLOADER.git
   cd DOOMLOADER
   cmake -B build -DDOOMLOADER_BUILD_EXAMPLES=ON -DDOOMLOADER_ENABLE_TESTING=ON
   cmake --build build
   ```

## Types of Contributions

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Platform support
- Documentation improvements

### Non-Code Contributions
- Bug reports
- Feature requests
- Documentation
- Testing
- Preset creation
- IR libraries

## Development Workflow

### 1. Issue Creation

Before starting work:
1. Check existing issues
2. Create new issue if needed
3. Discuss approach with maintainers
4. Get approval for large changes

### 2. Fork and Branch

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/DOOMLOADER.git
cd DOOMLOADER

# Create feature branch
git checkout -b feature/amp-modeling-improvements
```

### 3. Development

#### Code Style

Follow the existing code style:

```cpp
// Use PascalCase for classes
class AmpModeler {
public:
    // Use camelCase for methods
    bool loadModel(const std::string& modelPath);
    
private:
    // Use camelCase with trailing underscore for members
    bool isInitialized_;
    std::unique_ptr<Impl> impl_;
};

// Use snake_case for free functions
bool validate_preset_file(const std::string& path);

// Use UPPER_CASE for constants
const int MAX_BUFFER_SIZE = 4096;
```

#### Documentation

Document all public APIs:

```cpp
/**
 * @brief Load an amp model from file
 * 
 * Loads a neural amp model (.nam) or algorithmic model and prepares
 * it for audio processing.
 * 
 * @param modelPath Path to the model file
 * @param type Model type (auto-detected if None)
 * @return true if model loaded successfully
 * 
 * @note Model files must be compatible with current sample rate
 * @see AmpModeler::ModelType for supported types
 * 
 * Example:
 * @code
 * doomloader::AmpModeler modeler;
 * if (modeler.loadModel("marshall.nam")) {
 *     // Model ready for processing
 * }
 * @endcode
 */
bool loadModel(const std::string& modelPath, ModelType type = ModelType::None);
```

#### Testing

Add tests for new functionality:

```cpp
#include <gtest/gtest.h>
#include "AmpModeler.h"

class AmpModelerTest : public ::testing::Test {
protected:
    void SetUp() override {
        modeler = std::make_unique<doomloader::AmpModeler>();
        modeler->initialize(44100.0, 512);
    }
    
    std::unique_ptr<doomloader::AmpModeler> modeler;
};

TEST_F(AmpModelerTest, LoadValidNAMModel) {
    ASSERT_TRUE(modeler->loadModel("test-data/valid-model.nam"));
    EXPECT_TRUE(modeler->isReady());
}

TEST_F(AmpModelerTest, RejectInvalidModel) {
    EXPECT_FALSE(modeler->loadModel("test-data/invalid-file.txt"));
    EXPECT_FALSE(modeler->isReady());
}
```

### 4. Commit Guidelines

Use conventional commit format:

```bash
# Format: type(scope): description
git commit -m "feat(amp): add NAM model validation"
git commit -m "fix(ir): resolve convolution memory leak"
git commit -m "docs(api): update amp modeling examples"
git commit -m "test(preset): add preset loading tests"
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 5. Pull Request Process

1. **Create Pull Request**:
   ```bash
   git push origin feature/amp-modeling-improvements
   # Create PR on GitHub
   ```

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests added/updated
   - [ ] All tests pass
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No merge conflicts
   ```

3. **Review Process**:
   - Automated builds must pass
   - Code review by maintainers
   - Address feedback promptly
   - Rebase if requested

## Code Architecture Guidelines

### Core Components

```cpp
// DoomloaderEngine: Main orchestrator
// - Manages all other components
// - Provides high-level API
// - Handles audio routing

// AmpModeler: Amp simulation
// - NAM integration
// - Built-in models
// - Parameter management

// IRLoader/ConvolutionEngine: Cabinet simulation
// - IR file loading
// - Convolution processing
// - Wet/dry mixing

// PresetManager: Settings management
// - Save/load presets
// - Organization/search
// - Cloud sync
```

### Design Principles

1. **RAII**: Use smart pointers, automatic cleanup
2. **Immutability**: Prefer const-correctness
3. **Exception Safety**: Handle errors gracefully
4. **Performance**: Real-time audio constraints
5. **Portability**: Cross-platform compatibility

### Threading Considerations

```cpp
// Audio thread (real-time, no allocations)
class AudioProcessor {
public:
    void processAudio(juce::AudioBuffer<float>& buffer) {
        // NO heap allocations
        // NO system calls
        // NO locks (if possible)
        // Use lock-free data structures
    }
};

// UI thread (can allocate, slower operations)
class UIController {
public:
    void loadPreset(const std::string& path) {
        // File I/O allowed
        // Memory allocation allowed
        // Communicate with audio thread via lock-free queue
    }
};
```

## Platform-Specific Development

### Windows
```cpp
#ifdef DOOMLOADER_WINDOWS
    // Use WASAPI for low-latency audio
    // Handle DPI awareness
    // Support multiple audio devices
#endif
```

### macOS
```cpp
#ifdef DOOMLOADER_MACOS
    // Use Core Audio
    // Support Audio Units
    // Handle sample rate changes
#endif
```

### Linux
```cpp
#ifdef DOOMLOADER_LINUX
    // Use ALSA/JACK
    // Handle various audio systems
    // Support different distributions
#endif
```

### Mobile
```cpp
#ifdef DOOMLOADER_IOS
    // Use Core Audio/AVAudioEngine
    // Handle audio session interruptions
    // Support background audio
#endif

#ifdef DOOMLOADER_ANDROID
    // Use Oboe/AAudio
    // Handle audio focus changes
    // Support various Android versions
#endif
```

## Testing Guidelines

### Unit Tests
```bash
# Run all tests
ctest

# Run specific test suite
ctest -R AmpModeler

# Run with verbose output
ctest --verbose
```

### Integration Tests
```cpp
// Test component interactions
TEST(IntegrationTest, FullAudioChain) {
    doomloader::DoomloaderEngine engine;
    engine.initialize(44100.0, 512);
    
    // Load complete preset
    ASSERT_TRUE(engine.loadPreset("test-data/integration-preset.json"));
    
    // Process test audio
    juce::AudioBuffer<float> buffer(2, 512);
    generateTestSignal(buffer);
    
    engine.processAudio(buffer);
    
    // Verify output characteristics
    EXPECT_GT(getRMSLevel(buffer), 0.0f);
    EXPECT_LT(getRMSLevel(buffer), 1.0f);
}
```

### Performance Tests
```cpp
TEST(PerformanceTest, RealTimeProcessing) {
    doomloader::DoomloaderEngine engine;
    engine.initialize(48000.0, 128);
    
    juce::AudioBuffer<float> buffer(2, 128);
    const int numIterations = 1000;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < numIterations; ++i) {
        engine.processAudio(buffer);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // Should process faster than real-time
    double realTimeUs = (numIterations * 128.0 / 48000.0) * 1000000.0;
    EXPECT_LT(duration.count(), realTimeUs);
}
```

## Documentation Standards

### API Documentation
Use Doxygen-style comments:

```cpp
/**
 * @brief Brief description
 * 
 * Detailed description explaining the purpose,
 * behavior, and usage of the function.
 * 
 * @param parameter Description of parameter
 * @return Description of return value
 * 
 * @note Important notes or limitations
 * @warning Potential issues or warnings
 * @see Related functions or classes
 * 
 * @code
 * // Example usage
 * MyClass obj;
 * obj.myFunction(42);
 * @endcode
 */
```

### User Documentation
- Clear, step-by-step instructions
- Code examples that work
- Screenshots for UI features
- Common use cases covered
- Troubleshooting sections

## Release Process

### Version Numbering
Follow Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] Tagged release created
- [ ] Binaries built and uploaded
- [ ] Release notes written

## Community Guidelines

### Code of Conduct
- Be respectful and professional
- Welcome newcomers
- Provide constructive feedback
- Help others learn and grow

### Communication Channels
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Pull Requests**: Code review and collaboration

### Getting Help
- Check documentation first
- Search existing issues
- Ask specific, detailed questions
- Provide context and examples

## Specialized Contributing Areas

### NAM Model Integration
```cpp
// Contributing to NAM support
class NAMContributor {
public:
    // Focus areas:
    // - Model format compatibility
    // - Performance optimization
    // - Memory usage reduction
    // - Error handling improvement
};
```

### IR Processing
```cpp
// Contributing to IR support
class IRContributor {
public:
    // Focus areas:
    // - File format support
    // - Convolution algorithms
    // - Real-time processing
    // - Quality vs performance
};
```

### Mobile Development
```cpp
// Contributing to mobile support
class MobileContributor {
public:
    // Focus areas:
    // - Platform-specific audio
    // - UI/UX for touch interfaces
    // - Performance optimization
    // - Battery usage reduction
};
```

### Cloud Integration
```cpp
// Contributing to cloud features
class CloudContributor {
public:
    // Focus areas:
    // - API integration
    // - Sync reliability
    // - Offline functionality
    // - Security considerations
};
```

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Special thanks in major releases

## Questions?

- 📧 Email: contributors@doomloader.com
- 💬 GitHub Discussions
- 🐛 GitHub Issues

Thank you for contributing to DOOMLOADER! 🎸🔥