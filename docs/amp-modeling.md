# Amp Modeling in DOOMLOADER

DOOMLOADER provides comprehensive amp modeling capabilities through multiple technologies, with a focus on Neural Amp Modeler (NAM) integration and support for various modeling approaches.

## Overview

Amp modeling in DOOMLOADER supports:
- **Neural Amp Modeler (NAM)**: Machine learning-based models
- **Algorithmic Models**: Built-in amp simulations 
- **Tone3000 Integration**: Cloud-based models and sharing
- **Hybrid Processing**: Combining multiple modeling techniques

## Neural Amp Modeler (NAM) Integration

### What is NAM?

Neural Amp Modeler uses machine learning to capture the sonic characteristics of guitar amplifiers. It analyzes the input/output relationship of real amplifiers to create highly accurate digital models.

### Loading NAM Models

```cpp
#include "AmpModeler.h"

doomloader::AmpModeler modeler;
modeler.initialize(44100.0, 512);

// Load a NAM model file
bool success = modeler.loadModel("marshall-jcm800.nam", 
                                doomloader::AmpModeler::ModelType::NAM);

if (success) {
    std::cout << "NAM model loaded successfully!" << std::endl;
} else {
    std::cout << "Failed to load NAM model" << std::endl;
}
```

### NAM Model Parameters

```cpp
// Set amp parameters
doomloader::AmpParameters params;
params.gain = 0.7f;        // Input drive
params.bass = 0.6f;        // Low frequency response
params.mid = 0.5f;         // Mid frequency response  
params.treble = 0.4f;      // High frequency response
params.presence = 0.5f;    // High-mid presence
params.volume = 0.8f;      // Output level

modeler.setParameters(params);
```

### Processing Audio with NAM

```cpp
// Process audio buffer
juce::AudioBuffer<float> guitarBuffer; // Your guitar signal
modeler.processAudio(guitarBuffer);    // Processed in-place
```

## Built-in Algorithmic Models

DOOMLOADER includes several built-in amp models based on classic amplifier circuits:

### Available Models

```cpp
auto builtInModels = doomloader::AmpModeler::getBuiltInModels();
for (const auto& model : builtInModels) {
    std::cout << "Available model: " << model << std::endl;
}
```

### Model Types
- **Clean Twin**: Based on Fender Twin Reverb
- **Vintage Plexi**: Based on Marshall Plexi  
- **Modern High-Gain**: Based on modern metal amps
- **Vintage Crunch**: Classic rock overdrive
- **Bass Amp**: Optimized for bass guitar

### Loading Built-in Models

```cpp
// Load by name
bool success = modeler.loadModel("Clean Twin", 
                                doomloader::AmpModeler::ModelType::Algorithmic);
```

## Advanced Amp Modeling Techniques

### Tube Saturation Simulation

```cpp
doomloader::AmpParameters params;
params.saturation = 0.3f;   // Add tube-style saturation
params.asymmetry = 0.2f;    // Asymmetric clipping character  
params.sag = 0.1f;          // Power supply sag simulation

modeler.setParameters(params);
```

### Multi-Stage Processing

```cpp
class MultiStageAmp {
    doomloader::AmpModeler preamp_;
    doomloader::AmpModeler poweramp_;
    
public:
    void processAudio(juce::AudioBuffer<float>& buffer) {
        // Process through preamp first
        preamp_.processAudio(buffer);
        
        // Then through power amp
        poweramp_.processAudio(buffer);
    }
};
```

### Frequency-Dependent Processing

```cpp
// Split signal into frequency bands for different processing
juce::dsp::LinkwitzRileyFilter<float> crossover;
crossover.setCutoffFrequency(800.0f); // 800Hz crossover

// Process low and high frequencies with different models
```

## NAM Model Creation

### Prerequisites
- Python with NAM training tools
- Audio interface for recording
- Test signals (sine sweeps, noise)
- Target amplifier to model

### Recording Process

1. **Set up recording chain**:
   ```
   Guitar -> NAM Trainer Input -> Amp -> NAM Trainer Output -> Audio Interface
   ```

2. **Generate training data**:
   ```bash
   # Use NAM trainer to generate test signals
   python -m nam.train.trainer prepare_data --input_dir ./recordings
   ```

3. **Train the model**:
   ```bash
   # Train NAM model
   python -m nam.train.trainer train --data_dir ./training_data --output_dir ./models
   ```

4. **Export model**:
   ```bash
   # Export to .nam format
   python -m nam.train.trainer export --model_path ./models/model.pth --output_path ./my_amp.nam
   ```

### Model Validation

```cpp
// Validate NAM model before loading
if (doomloader::NAMWrapper::isValidNAMFile("my_amp.nam")) {
    // Model file is valid
    modeler.loadModel("my_amp.nam");
} else {
    std::cout << "Invalid NAM model file" << std::endl;
}
```

## Tone3000 Cloud Integration

### Accessing Cloud Models

```cpp
#ifdef DOOMLOADER_TONE3000_ENABLED
#include "Tone3000/APIClient.h"

doomloader::Tone3000::APIClient client;
client.authenticate("your-api-key");

// Browse available models
auto cloudModels = client.searchModels("marshall", "rock");

// Download and load model
auto modelData = client.downloadModel(cloudModels[0].id);
if (modelData) {
    modeler.loadModel(modelData->filePath, 
                     doomloader::AmpModeler::ModelType::Tone3000);
}
#endif
```

### Uploading Your Models

```cpp
// Upload NAM model to Tone3000
auto uploadResult = client.uploadModel("my-amp.nam", {
    .name = "My Custom Amp",
    .description = "Custom Marshall JCM800 model",
    .tags = {"marshall", "rock", "vintage"},
    .category = "Crunch"
});
```

## Performance Optimization

### Real-Time Processing

```cpp
// Configure for low latency
modeler.initialize(48000.0, 128); // Smaller buffer size

// Use efficient processing modes
modeler.setProcessingMode(doomloader::AmpModeler::ProcessingMode::LowLatency);
```

### CPU Usage Optimization

```cpp
// Monitor CPU usage
auto stats = modeler.getPerformanceStats();
std::cout << "CPU usage: " << stats.cpuUsage << "%" << std::endl;
std::cout << "Processing time: " << stats.processingTimeMs << "ms" << std::endl;

// Adjust quality vs performance
if (stats.cpuUsage > 80.0f) {
    modeler.setQualityMode(doomloader::AmpModeler::QualityMode::Performance);
}
```

### Memory Management

```cpp
// Preload commonly used models
modeler.preloadModel("clean-twin.nam");
modeler.preloadModel("vintage-crunch.nam");

// Manage model cache
modeler.setMaxCacheSize(256 * 1024 * 1024); // 256MB cache
modeler.clearUnusedModels();
```

## Troubleshooting

### Common Issues

#### NAM Model Won't Load
```cpp
// Check model file validity
if (!doomloader::NAMWrapper::isValidNAMFile("model.nam")) {
    std::cout << "Invalid NAM file format" << std::endl;
    return;
}

// Check sample rate compatibility
auto modelInfo = modeler.getModelInfo();
if (modelInfo.sampleRate != currentSampleRate) {
    std::cout << "Sample rate mismatch: " << modelInfo.sampleRate 
              << " vs " << currentSampleRate << std::endl;
}
```

#### Poor Performance
```cpp
// Reduce processing quality
modeler.setOversamplingFactor(1); // Disable oversampling
modeler.setQualityMode(doomloader::AmpModeler::QualityMode::Performance);

// Use smaller buffer sizes if possible
modeler.initialize(sampleRate, 64); // Very low latency
```

#### Unexpected Distortion
```cpp
// Check input levels
auto inputLevel = modeler.getInputLevel();
if (inputLevel > 0.95f) {
    std::cout << "Input level too high: " << inputLevel << std::endl;
    modeler.setInputGain(0.5f); // Reduce input gain
}

// Check for clipping
if (modeler.isClipping()) {
    std::cout << "Model is clipping, reduce gain" << std::endl;
}
```

## Best Practices

### Model Selection
1. **Match your input**: Use NAM models trained with similar pickup types
2. **Consider the mix**: Scooped models for rhythm, present mids for leads  
3. **Test thoroughly**: A/B test with reference recordings
4. **Document settings**: Save successful combinations as presets

### Gain Staging
```cpp
// Proper gain staging
modeler.setInputGain(0.7f);    // Leave headroom for peaks
modeler.setOutputLevel(0.8f);  // Consistent output level

// Monitor levels throughout chain
auto levels = modeler.getLevelMeters();
std::cout << "Input: " << levels.input << "dB" << std::endl;
std::cout << "Output: " << levels.output << "dB" << std::endl;
```

### Preset Organization
```cpp
// Organize models by style
struct ModelPreset {
    std::string modelPath;
    doomloader::AmpParameters params;
    std::string style;      // "clean", "crunch", "lead", "metal"
    std::string description;
};

std::vector<ModelPreset> rockPresets;
rockPresets.push_back({
    .modelPath = "plexi.nam",
    .params = {.gain = 0.6f, .bass = 0.5f, .mid = 0.7f, .treble = 0.6f},
    .style = "crunch",
    .description = "Classic rock crunch tone"
});
```

## Integration with IR Loading

Amp modeling works best when combined with impulse response (IR) loading:

```cpp
// Complete signal chain
modeler.processAudio(buffer);           // Amp modeling
convolutionEngine.processAudio(buffer); // Cabinet simulation
effectChain.processAudio(buffer);       // Reverb, delay, etc.
```

See [IR Loading Documentation](ir-loading.md) for details on cabinet simulation.

## See Also
- [IR Loading Guide](ir-loading.md)
- [Preset Management](preset-management.md)
- [Getting Started](getting-started.md)
- [API Reference](api-reference.md)