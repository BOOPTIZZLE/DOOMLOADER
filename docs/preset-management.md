# Preset Management in DOOMLOADER

DOOMLOADER provides comprehensive preset management capabilities, allowing you to save, load, organize, and share your guitar tones. The preset system supports local storage and cloud synchronization via Tone3000 API.

## Understanding Presets

A DOOMLOADER preset contains:
- **Amp model settings** (gain, EQ, model path)
- **Impulse response configuration** (IR file, wet/dry mix)
- **Effect settings** (reverb, delay, chorus, etc.)
- **Metadata** (name, category, author, tags)

## Basic Preset Operations

### Loading Presets

```cpp
#include "PresetManager.h"
#include "DoomloaderEngine.h"

doomloader::DoomloaderEngine engine;
engine.initialize(44100.0, 512);

// Load a preset
bool success = engine.loadPreset("presets/clean-twin.json");
if (success) {
    std::cout << "Preset loaded successfully!" << std::endl;
}
```

### Saving Presets

```cpp
// Configure your tone
engine.setAmpGain(0.7f);
engine.setAmpTone(0.6f, 0.5f, 0.4f); // bass, mid, treble
engine.loadImpulseResponse("ir/vintage-4x12.wav");
engine.setReverbLevel(0.2f);

// Save current settings as preset
bool saved = engine.savePreset("presets/my-tone.json");
if (saved) {
    std::cout << "Preset saved!" << std::endl;
}
```

### Using PresetManager Directly

```cpp
doomloader::PresetManager presets;
presets.initialize("./presets");

// Create a custom preset
auto preset = presets.createDefaultPreset("My Metal Tone", "Metal");
preset.ampParams.gain = 0.9f;
preset.ampParams.bass = 0.4f;
preset.ampParams.mid = 0.6f;
preset.ampParams.treble = 0.8f;
preset.effects.reverbLevel = 0.05f;
preset.effects.noiseGateThreshold = 0.15f;

// Save the preset
presets.savePreset(preset, "presets/my-metal-tone.json");
```

## Preset Structure

### JSON Format

DOOMLOADER presets are stored as JSON files with the following structure:

```json
{
  "name": "Clean Twin",
  "description": "Classic clean Fender Twin Reverb tone",
  "author": "DOOMLOADER Team",
  "category": "Clean",
  "tags": "clean, vintage, fender, twin, reverb",
  
  "ampModelPath": "models/twin-reverb.nam",
  "irPath": "ir/twin-2x12.wav",
  
  "ampParams": {
    "gain": 0.3,
    "bass": 0.6,
    "mid": 0.5,
    "treble": 0.7,
    "presence": 0.4,
    "volume": 0.8,
    "saturation": 0.0,
    "asymmetry": 0.1,
    "sag": 0.2
  },
  
  "irWetLevel": 0.85,
  
  "effects": {
    "reverbLevel": 0.25,
    "delayLevel": 0.0,
    "chorusLevel": 0.0,
    "compressorThreshold": 0.9,
    "compressorRatio": 2.0,
    "noiseGateThreshold": 0.0
  },
  
  "version": "1.0",
  "created": "2024-01-01T00:00:00Z",
  "modified": "2024-01-01T00:00:00Z",
  "uuid": "clean-twin-001"
}
```

### Programmatic Access

```cpp
// Load and inspect preset
auto preset = presets.loadPreset("presets/clean-twin.json");
if (preset) {
    std::cout << "Preset: " << preset->name << std::endl;
    std::cout << "Category: " << preset->category << std::endl;
    std::cout << "Amp Gain: " << preset->ampParams.gain << std::endl;
    std::cout << "IR Path: " << preset->irPath << std::endl;
}
```

## Organizing Presets

### Categories

DOOMLOADER organizes presets into categories:

```cpp
// Get default categories
auto categories = doomloader::PresetCategories::getDefaultCategories();
for (const auto& category : categories) {
    std::cout << category << ": " 
              << doomloader::PresetCategories::getCategoryDescription(category) 
              << std::endl;
}
```

**Available Categories:**
- **Clean**: Clean amp tones
- **Crunch**: Light overdrive and crunch
- **Lead**: Lead guitar tones 
- **Metal**: High-gain metal tones
- **Bass**: Bass guitar presets
- **Experimental**: Unusual or creative tones
- **User**: Custom user presets

### Browsing by Category

```cpp
// Get presets in a specific category
auto cleanPresets = presets.getPresetsByCategory("Clean");
std::cout << "Clean presets:" << std::endl;
for (const auto& presetPath : cleanPresets) {
    auto preset = presets.loadPreset(presetPath);
    if (preset) {
        std::cout << "  - " << preset->name << std::endl;
    }
}
```

### Searching Presets

```cpp
// Search by name or tags
auto searchResults = presets.searchPresets("fender");
std::cout << "Found " << searchResults.size() << " Fender-related presets" << std::endl;

// Search for metal presets
auto metalResults = presets.searchPresets("metal high-gain");
```

## Advanced Preset Features

### Preset Validation

```cpp
// Validate preset file before loading
if (presets.validatePreset("presets/suspicious-preset.json")) {
    auto preset = presets.loadPreset("presets/suspicious-preset.json");
    // Safe to use
} else {
    std::cout << "Invalid preset file!" << std::endl;
}
```

### Importing from Other Formats

```cpp
// Import presets from other software
bool imported = presets.importPreset("amplitube-preset.xml", "converted-preset.json");
if (imported) {
    std::cout << "Preset converted successfully!" << std::endl;
}

// Supported import formats
auto formats = presets.getSupportedFormats();
for (const auto& format : formats) {
    std::cout << "Supported: " << format << std::endl;
}
```

### Exporting Presets

```cpp
// Export to different formats
presets.exportPreset("my-preset.json", "exported.xml", "xml");
presets.exportPreset("my-preset.json", "exported.txt", "text");
```

## Cloud Synchronization (Tone3000)

### Setting Up Cloud Sync

```cpp
#ifdef DOOMLOADER_TONE3000_ENABLED
// Sync with Tone3000 cloud
bool synced = presets.syncWithCloud("your-tone3000-api-key");
if (synced) {
    std::cout << "Presets synchronized with cloud!" << std::endl;
}
#endif
```

### Uploading Presets

```cpp
// Upload preset to cloud
std::string cloudId = presets.uploadPreset(*myPreset, "api-key");
if (!cloudId.empty()) {
    std::cout << "Preset uploaded with ID: " << cloudId << std::endl;
}
```

### Downloading Cloud Presets

```cpp
// Download preset from cloud
auto cloudPreset = presets.downloadPreset("cloud-preset-id", "api-key");
if (cloudPreset) {
    // Save locally
    presets.savePreset(*cloudPreset, "downloaded-preset.json");
}
```

## Preset Banks and Collections

### Creating Preset Banks

```cpp
class PresetBank {
    std::vector<std::string> presetPaths_;
    std::string name_;
    
public:
    PresetBank(const std::string& name) : name_(name) {}
    
    void addPreset(const std::string& presetPath) {
        presetPaths_.push_back(presetPath);
    }
    
    void loadPreset(int index, doomloader::DoomloaderEngine& engine) {
        if (index < presetPaths_.size()) {
            engine.loadPreset(presetPaths_[index]);
        }
    }
    
    size_t size() const { return presetPaths_.size(); }
};

// Usage
PresetBank liveBank("Live Performance");
liveBank.addPreset("presets/verse-clean.json");
liveBank.addPreset("presets/chorus-crunch.json");
liveBank.addPreset("presets/solo-lead.json");

// Switch between presets during performance
liveBank.loadPreset(0, engine); // Verse
liveBank.loadPreset(1, engine); // Chorus
liveBank.loadPreset(2, engine); // Solo
```

### Preset Collections

```cpp
struct PresetCollection {
    std::string name;
    std::string description;
    std::vector<std::string> presetPaths;
    std::string genre;
};

// Rock collection
PresetCollection rockCollection{
    .name = "Classic Rock Tones",
    .description = "Essential tones for classic rock",
    .presetPaths = {
        "presets/clean-twin.json",
        "presets/vintage-crunch.json", 
        "presets/lead-solo.json"
    },
    .genre = "Rock"
};
```

## MIDI and Automation

### MIDI Preset Switching

```cpp
class MIDIPresetController {
    doomloader::PresetManager& presets_;
    doomloader::DoomloaderEngine& engine_;
    std::vector<std::string> presetBank_;
    
public:
    MIDIPresetController(doomloader::PresetManager& pm, 
                        doomloader::DoomloaderEngine& eng)
        : presets_(pm), engine_(eng) {}
    
    void handleMIDI(int programChange) {
        if (programChange < presetBank_.size()) {
            engine_.loadPreset(presetBank_[programChange]);
        }
    }
    
    void loadBank(const std::vector<std::string>& presets) {
        presetBank_ = presets;
    }
};
```

### Automated Preset Creation

```cpp
// Generate presets with parameter sweeps
void generatePresetVariations(const doomloader::Preset& basePreset) {
    doomloader::PresetManager presets;
    presets.initialize("./generated-presets");
    
    // Create gain variations
    for (float gain = 0.1f; gain <= 1.0f; gain += 0.1f) {
        auto variant = basePreset;
        variant.ampParams.gain = gain;
        variant.name = basePreset.name + " Gain " + std::to_string(int(gain * 10));
        
        std::string filename = "generated/" + variant.name + ".json";
        presets.savePreset(variant, filename);
    }
}
```

## Performance Considerations

### Preset Loading Performance

```cpp
// Preload commonly used presets
class PresetCache {
    std::map<std::string, doomloader::Preset> cache_;
    size_t maxCacheSize_ = 50;
    
public:
    void preloadPreset(const std::string& path, doomloader::PresetManager& pm) {
        if (cache_.size() >= maxCacheSize_) {
            // Remove oldest entry
            cache_.erase(cache_.begin());
        }
        
        auto preset = pm.loadPreset(path);
        if (preset) {
            cache_[path] = *preset;
        }
    }
    
    const doomloader::Preset* getCachedPreset(const std::string& path) {
        auto it = cache_.find(path);
        return (it != cache_.end()) ? &it->second : nullptr;
    }
};
```

### Fast Preset Switching

```cpp
// Minimize audio dropouts during preset changes
void fastPresetSwitch(const std::string& newPresetPath) {
    // Load preset in background thread
    auto future = std::async(std::launch::async, [&]() {
        return presets.loadPreset(newPresetPath);
    });
    
    // Continue processing audio with current settings
    // Switch when new preset is ready
    auto newPreset = future.get();
    if (newPreset) {
        // Apply new settings during audio callback gap
        engine.applyPresetAtomic(*newPreset);
    }
}
```

## Troubleshooting

### Common Issues

#### Preset Won't Load
```cpp
// Check file existence and validity
if (!juce::File(presetPath).exists()) {
    std::cout << "Preset file not found: " << presetPath << std::endl;
    return false;
}

if (!presets.validatePreset(presetPath)) {
    std::cout << "Invalid preset format: " << presetPath << std::endl;
    return false;
}
```

#### Missing Model Files
```cpp
// Handle missing amp models or IRs gracefully
auto preset = presets.loadPreset(presetPath);
if (preset) {
    if (!preset->ampModelPath.empty() && 
        !juce::File(preset->ampModelPath).exists()) {
        std::cout << "Warning: Amp model not found: " 
                  << preset->ampModelPath << std::endl;
        // Continue with built-in model
    }
    
    if (!preset->irPath.empty() && 
        !juce::File(preset->irPath).exists()) {
        std::cout << "Warning: IR file not found: " 
                  << preset->irPath << std::endl;
        // Continue without IR
    }
}
```

#### Cloud Sync Issues
```cpp
// Handle network connectivity issues
try {
    bool synced = presets.syncWithCloud(apiKey);
    if (!synced) {
        std::cout << "Cloud sync failed - working offline" << std::endl;
    }
} catch (const std::exception& e) {
    std::cout << "Network error: " << e.what() << std::endl;
    // Fall back to local presets only
}
```

## Best Practices

### Preset Naming

```cpp
// Use descriptive, consistent naming
// Good examples:
"Clean - Fender Twin - Bright"
"Crunch - Marshall Plexi - Mid Gain"
"Lead - Mesa Boogie - High Gain"
"Metal - 5150 - Tight"

// Include key characteristics:
// [Style] - [Amp] - [Character/Setting]
```

### Organization Strategy

```cpp
// Organize by usage context
struct PresetOrganization {
    std::string context;
    std::vector<std::string> presets;
};

std::vector<PresetOrganization> organization = {
    {"Live - Verse", {"clean-bright.json", "clean-warm.json"}},
    {"Live - Chorus", {"crunch-mid.json", "crunch-high.json"}},
    {"Live - Solo", {"lead-smooth.json", "lead-aggressive.json"}},
    {"Studio - Clean", {"studio-clean-1.json", "studio-clean-2.json"}},
    {"Studio - Driven", {"studio-crunch.json", "studio-lead.json"}}
};
```

### Version Control

```cpp
// Track preset versions
struct PresetVersion {
    std::string version;
    std::string changes;
    std::string timestamp;
};

// Save version history
void savePresetWithHistory(const doomloader::Preset& preset, 
                          const std::string& changes) {
    // Update version info
    auto updatedPreset = preset;
    updatedPreset.version = incrementVersion(preset.version);
    updatedPreset.modified = getCurrentTimestamp();
    
    // Save history
    PresetVersion version{
        .version = updatedPreset.version,
        .changes = changes,
        .timestamp = updatedPreset.modified
    };
    
    saveVersionHistory(preset.uuid, version);
    presets.savePreset(updatedPreset, getPresetPath(preset.uuid));
}
```

## See Also
- [Amp Modeling Guide](amp-modeling.md)
- [IR Loading Guide](ir-loading.md)
- [Getting Started](getting-started.md)
- [API Reference](api-reference.md)