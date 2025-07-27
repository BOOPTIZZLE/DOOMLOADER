# Impulse Response (IR) Loading in DOOMLOADER

Impulse responses are crucial for realistic cabinet simulation in guitar amp modeling. DOOMLOADER provides comprehensive IR loading and management capabilities.

## Understanding Impulse Responses

An impulse response captures the acoustic characteristics of a speaker cabinet, microphone placement, and room acoustics. When convolved with your guitar signal, it simulates the sound of playing through that specific setup.

### What IRs Capture
- **Speaker cabinet characteristics** (frequency response, resonance)
- **Microphone type and placement** (dynamics, condensers, ribbons)
- **Room acoustics** (size, reflections, ambient characteristics)
- **Recording chain** (preamps, converters, processing)

## Supported Formats

DOOMLOADER supports the following IR file formats:

| Format | Extension | Bit Depth | Sample Rate | Notes |
|--------|-----------|-----------|-------------|-------|
| WAV | `.wav` | 16/24/32-bit | Any | Most common format |
| AIFF | `.aiff`, `.aif` | 16/24/32-bit | Any | Apple format |
| FLAC | `.flac` | 16/24-bit | Any | Compressed lossless |

### Recommended Specifications
- **Sample Rate**: 44.1kHz or 48kHz (matching your project)
- **Bit Depth**: 24-bit minimum for quality
- **Length**: 0.1 to 2.0 seconds (most are 0.2-0.5s)
- **Channels**: Mono or stereo

## Loading IRs

### Via User Interface
1. Click the **"IR"** section in DOOMLOADER
2. Click **"Load IR"** button
3. Browse to your IR file
4. Select and confirm

### Programmatically
```cpp
#include "IRLoader.h"
#include "DoomloaderEngine.h"

doomloader::DoomloaderEngine engine;
engine.initialize(44100.0, 512);

// Load IR file
bool success = engine.loadImpulseResponse("path/to/cabinet.wav");
if (success) {
    std::cout << "IR loaded successfully" << std::endl;
}

// Adjust IR wet/dry mix
engine.setIRMix(0.8f); // 80% wet, 20% dry
```

### Using IRLoader Directly
```cpp
#include "IRLoader.h"

doomloader::IRLoader loader;

// Load IR from file
if (loader.loadIR("vintage-4x12.wav")) {
    auto samples = loader.getIRSamples();
    auto sampleRate = loader.getIRSampleRate();
    auto length = loader.getIRLength();
    
    std::cout << "Loaded IR: " << length << " samples at " 
              << sampleRate << "Hz" << std::endl;
}

// Check if format is supported
if (doomloader::IRLoader::isSupportedFormat("my-ir.wav")) {
    // Proceed with loading
}
```

## IR Management

### Organizing Your IR Collection
Create a logical folder structure:
```
IRs/
├── 4x12/
│   ├── Marshall-1960A/
│   ├── Mesa-Rectifier/
│   └── Orange-PPC412/
├── 2x12/
│   ├── Vox-AC30/
│   └── Fender-Twin/
├── 1x12/
│   └── Celestion-Blue/
└── DI/
    ├── Bass-DI/
    └── Guitar-DI/
```

### Batch Loading
```cpp
#include "PresetManager.h"

doomloader::PresetManager presets;
auto irFiles = presets.findIRFiles("./IRs/4x12/");

for (const auto& irFile : irFiles) {
    // Create preset for each IR
    auto preset = presets.createDefaultPreset(
        juce::File(irFile).getFileNameWithoutExtension().toStdString()
    );
    preset.irPath = irFile;
    
    // Save preset
    auto presetPath = "presets/" + preset.name + ".json";
    presets.savePreset(preset, presetPath);
}
```

## IR Processing Parameters

### Wet/Dry Mix
Controls the balance between processed (wet) and unprocessed (dry) signal:
```cpp
// 100% wet (fully processed)
engine.setIRMix(1.0f);

// 50/50 mix
engine.setIRMix(0.5f);

// 100% dry (bypassed)
engine.setIRMix(0.0f);
```

### Length and Trimming
IRs can be automatically trimmed to optimize processing:
```cpp
doomloader::ConvolutionEngine conv;
conv.initialize(48000.0, 512);

// Load with automatic trimming
std::vector<float> irSamples = loadIRFromFile("long-ir.wav");
conv.loadIR(irSamples, 48000.0, true); // true = auto-trim
```

## Best Practices

### IR Selection
1. **Match the amp style**: Modern high-gain amps pair well with tight, focused IRs
2. **Consider the mix context**: Scooped IRs for rhythm, present mids for leads
3. **Microphone character**: Dynamic mics for aggression, condensers for detail
4. **Distance matters**: Close mics for punch, room mics for ambience

### Technical Considerations
1. **Sample rate matching**: Use IRs at your project's sample rate when possible
2. **Phase alignment**: Ensure stereo IRs are properly phase-aligned
3. **Level matching**: Normalize IRs to prevent unexpected volume jumps
4. **Latency**: Longer IRs add latency; consider this for live performance

### Performance Optimization
```cpp
// For real-time performance
doomloader::ConvolutionEngine conv;
conv.initialize(48000.0, 128); // Smaller buffer size

// Load IR with length limit for low latency
conv.setMaxIRLength(8192); // ~170ms at 48kHz
conv.loadIR(irSamples, irSampleRate);
```

## Creating Custom IRs

### Equipment Needed
- Audio interface with quality preamps
- Microphones (SM57, Royer R-121, etc.)
- Studio monitors or headphones
- DAW software
- Impulse generation software

### Recording Process
1. **Set up cabinet and microphone**
2. **Generate test signal** (sine sweep or white noise burst)
3. **Record the response**
4. **Process to create IR** (deconvolution)
5. **Trim and normalize**

### Using Third-Party Tools
- **Voxengo Deconvolver**: Professional IR creation
- **Reaper**: Built-in impulse generation
- **SIR Audio Tools**: Free IR utilities

## Common Issues and Solutions

### Problem: IR sounds muffled
**Solutions:**
- Check sample rate matching
- Verify IR wasn't recorded too close to speaker
- Try different microphone position IRs

### Problem: Harsh high frequencies  
**Solutions:**
- Use ribbon microphone IRs instead of condensers
- Apply gentle high-frequency roll-off
- Try off-axis microphone position IRs

### Problem: Lack of low end
**Solutions:**
- Ensure IR includes room information
- Use IRs recorded with dynamic microphones
- Blend with DI signal

### Problem: Phase issues in stereo
**Solutions:**
- Check stereo IR phase alignment
- Use mono IRs for mono sources
- Manually align phases in DAW

## Advanced Techniques

### IR Blending
```cpp
// Load multiple IRs and blend
doomloader::ConvolutionEngine conv1, conv2;
conv1.loadIR(closeIR, sampleRate);
conv2.loadIR(roomIR, sampleRate);

// Process with different levels
conv1.setWetLevel(0.7f);
conv2.setWetLevel(0.3f);

// Mix the results
```

### Dynamic IR Switching
```cpp
class IRSwitcher {
    std::vector<doomloader::ConvolutionEngine> engines_;
    int currentIR_ = 0;
    
public:
    void switchIR(int index) {
        if (index < engines_.size()) {
            // Crossfade to new IR
            currentIR_ = index;
        }
    }
};
```

### Frequency-Dependent IR Processing
```cpp
// Split signal into frequency bands
// Apply different IRs to each band
// Recombine for complex cabinet simulation
```

## Resources

### Free IR Collections
- **God's Cab**: High-quality free IRs
- **Lancaster Audio**: Free starter pack
- **Seacow Cabs**: Vintage cabinet IRs

### Commercial IR Libraries
- **Ownhammer**: Extensive professional collection
- **Celestion**: Official speaker IRs
- **Two Notes**: Cabinet simulation specialists

### IR Creation Software
- **Voxengo Deconvolver**: Professional grade
- **Reaper ReaVerb**: Built into Reaper DAW
- **Audio Ease Altiverb**: Convolution reverb with IR tools

## See Also
- [Amp Modeling Guide](amp-modeling.md)
- [Preset Management](preset-management.md)  
- [API Reference](api-reference.md)