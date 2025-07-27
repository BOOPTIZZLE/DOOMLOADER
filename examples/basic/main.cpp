#include <iostream>
#include <memory>

#include "DoomloaderEngine.h"
#include <juce_core/juce_core.h>
#include <juce_audio_basics/juce_audio_basics.h>

/**
 * Basic DOOMLOADER example showing core functionality
 * 
 * This example demonstrates:
 * - Engine initialization
 * - Loading amp models and IRs
 * - Basic audio processing
 * - Preset management
 */

int main() {
    std::cout << "DOOMLOADER Basic Example" << std::endl;
    std::cout << "========================" << std::endl;
    
    // Initialize JUCE
    juce::MessageManager::getInstance();
    
    // Create DOOMLOADER engine
    auto engine = std::make_unique<doomloader::DoomloaderEngine>();
    
    // Initialize with common settings
    double sampleRate = 44100.0;
    int blockSize = 512;
    
    std::cout << "Initializing engine..." << std::endl;
    if (!engine->initialize(sampleRate, blockSize)) {
        std::cerr << "Failed to initialize DOOMLOADER engine!" << std::endl;
        return 1;
    }
    
    std::cout << "Engine initialized successfully" << std::endl;
    std::cout << "Sample Rate: " << engine->getSampleRate() << " Hz" << std::endl;
    std::cout << "Block Size: " << engine->getBlockSize() << " samples" << std::endl;
    
    // Configure amp settings
    std::cout << "\nConfiguring amp..." << std::endl;
    engine->setAmpGain(0.7f);        // 70% gain
    engine->setAmpTone(0.6f, 0.5f, 0.4f); // Bass, Mid, Treble
    
    // Set up effects
    std::cout << "Setting up effects..." << std::endl;
    engine->setReverbLevel(0.2f);    // 20% reverb
    engine->setDelayLevel(0.1f);     // 10% delay
    engine->setChorusLevel(0.0f);    // No chorus
    
    // Create a test audio buffer
    juce::AudioBuffer<float> testBuffer(2, blockSize); // Stereo buffer
    testBuffer.clear();
    
    // Generate a test signal (simple sine wave)
    float frequency = 440.0f; // A4
    float amplitude = 0.1f;
    
    for (int channel = 0; channel < testBuffer.getNumChannels(); ++channel) {
        auto* channelData = testBuffer.getWritePointer(channel);
        
        for (int sample = 0; sample < blockSize; ++sample) {
            float angle = (frequency / sampleRate) * 2.0f * juce::MathConstants<float>::pi * sample;
            channelData[sample] = amplitude * std::sin(angle);
        }
    }
    
    std::cout << "\nProcessing test audio..." << std::endl;
    
    // Process the buffer through DOOMLOADER
    engine->processAudio(testBuffer);
    
    // Analyze the output
    float maxLevel = 0.0f;
    for (int channel = 0; channel < testBuffer.getNumChannels(); ++channel) {
        const auto* channelData = testBuffer.getReadPointer(channel);
        for (int sample = 0; sample < blockSize; ++sample) {
            maxLevel = std::max(maxLevel, std::abs(channelData[sample]));
        }
    }
    
    std::cout << "Processed successfully!" << std::endl;
    std::cout << "Output peak level: " << maxLevel << std::endl;
    
    // Demonstrate preset management
    std::cout << "\nDemo: Preset Management" << std::endl;
    
    // Get available presets
    auto presets = engine->getAvailablePresets();
    std::cout << "Found " << presets.size() << " available presets:" << std::endl;
    
    for (const auto& preset : presets) {
        std::cout << "  - " << preset << std::endl;
    }
    
    // Try to save current settings as a preset
    std::string presetPath = "example-preset.json";
    std::cout << "\nSaving current settings to: " << presetPath << std::endl;
    
    if (engine->savePreset(presetPath)) {
        std::cout << "Preset saved successfully!" << std::endl;
        
        // Try to load it back
        std::cout << "Loading preset back..." << std::endl;
        if (engine->loadPreset(presetPath)) {
            std::cout << "Preset loaded successfully!" << std::endl;
        } else {
            std::cout << "Failed to load preset" << std::endl;
        }
    } else {
        std::cout << "Failed to save preset" << std::endl;
    }
    
    // Demonstrate IR loading (if IR files are available)
    std::cout << "\nDemo: IR Loading" << std::endl;
    
    // Check for example IR files
    juce::File irDir = juce::File::getCurrentWorkingDirectory()
                          .getChildFile("impulse_responses")
                          .getChildFile("examples");
    
    if (irDir.exists()) {
        auto irFiles = irDir.findChildFiles(juce::File::findFiles, false, "*.wav");
        
        if (!irFiles.isEmpty()) {
            auto firstIR = irFiles[0];
            std::cout << "Loading IR: " << firstIR.getFullPathName() << std::endl;
            
            if (engine->loadImpulseResponse(firstIR.getFullPathName().toStdString())) {
                std::cout << "IR loaded successfully!" << std::endl;
                engine->setIRMix(0.8f); // 80% wet
                std::cout << "IR mix set to 80%" << std::endl;
            } else {
                std::cout << "Failed to load IR" << std::endl;
            }
        } else {
            std::cout << "No IR files found in examples directory" << std::endl;
        }
    } else {
        std::cout << "IR examples directory not found" << std::endl;
    }
    
    // Demonstrate NAM model loading (if available)
    std::cout << "\nDemo: NAM Model Loading" << std::endl;
    
    juce::File modelsDir = juce::File::getCurrentWorkingDirectory()
                              .getChildFile("models");
    
    if (modelsDir.exists()) {
        auto modelFiles = modelsDir.findChildFiles(juce::File::findFiles, false, "*.nam");
        
        if (!modelFiles.isEmpty()) {
            auto firstModel = modelFiles[0];
            std::cout << "Loading NAM model: " << firstModel.getFullPathName() << std::endl;
            
            if (engine->loadAmpModel(firstModel.getFullPathName().toStdString())) {
                std::cout << "NAM model loaded successfully!" << std::endl;
            } else {
                std::cout << "Failed to load NAM model" << std::endl;
            }
        } else {
            std::cout << "No NAM model files found" << std::endl;
        }
    } else {
        std::cout << "Models directory not found" << std::endl;
    }
    
    // Performance test
    std::cout << "\nDemo: Performance Test" << std::endl;
    
    const int numBlocks = 1000;
    auto startTime = juce::Time::getMillisecondCounterHiRes();
    
    for (int i = 0; i < numBlocks; ++i) {
        // Generate new test signal for each block
        for (int channel = 0; channel < testBuffer.getNumChannels(); ++channel) {
            auto* channelData = testBuffer.getWritePointer(channel);
            
            for (int sample = 0; sample < blockSize; ++sample) {
                float angle = (frequency / sampleRate) * 2.0f * juce::MathConstants<float>::pi * (i * blockSize + sample);
                channelData[sample] = amplitude * std::sin(angle);
            }
        }
        
        engine->processAudio(testBuffer);
    }
    
    auto endTime = juce::Time::getMillisecondCounterHiRes();
    double processingTime = endTime - startTime;
    
    double audioLength = (numBlocks * blockSize) / sampleRate * 1000.0; // ms
    double realTimeRatio = audioLength / processingTime;
    
    std::cout << "Processed " << numBlocks << " blocks (" << audioLength/1000.0 << "s of audio)" << std::endl;
    std::cout << "Processing time: " << processingTime << "ms" << std::endl;
    std::cout << "Real-time performance: " << realTimeRatio << "x real-time" << std::endl;
    
    if (realTimeRatio > 1.0) {
        std::cout << "✅ Real-time performance achieved!" << std::endl;
    } else {
        std::cout << "⚠️ Real-time performance not achieved" << std::endl;
    }
    
    // Cleanup
    std::cout << "\nShutting down..." << std::endl;
    engine->shutdown();
    
    std::cout << "Example completed successfully!" << std::endl;
    
    return 0;
}