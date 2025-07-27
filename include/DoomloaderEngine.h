#pragma once

#include <memory>
#include <string>
#include <vector>

#include <juce_core/juce_core.h>
#include <juce_audio_basics/juce_audio_basics.h>

namespace doomloader {

/**
 * @brief Core engine for DOOMLOADER amp simulation
 * 
 * The DoomloaderEngine is the main orchestrator for all amp simulation
 * functionality, including NAM model loading, IR convolution, and preset management.
 */
class DoomloaderEngine {
public:
    DoomloaderEngine();
    ~DoomloaderEngine();

    // Engine lifecycle
    bool initialize(double sampleRate, int blockSize);
    void shutdown();
    bool isInitialized() const { return initialized_; }

    // Audio processing
    void processAudio(juce::AudioBuffer<float>& buffer);
    void reset();

    // Preset management
    bool loadPreset(const std::string& presetPath);
    bool savePreset(const std::string& presetPath) const;
    std::vector<std::string> getAvailablePresets() const;

    // Amp modeling
    bool loadAmpModel(const std::string& modelPath);
    void setAmpGain(float gain);
    void setAmpTone(float bass, float mid, float treble);

    // Impulse Response (IR) management
    bool loadImpulseResponse(const std::string& irPath);
    void setIRMix(float wetLevel);

    // Effect chain
    void setReverbLevel(float level);
    void setDelayLevel(float level);
    void setChorusLevel(float level);

    // Getters
    double getSampleRate() const { return sampleRate_; }
    int getBlockSize() const { return blockSize_; }

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
    
    bool initialized_ = false;
    double sampleRate_ = 44100.0;
    int blockSize_ = 512;
};

} // namespace doomloader