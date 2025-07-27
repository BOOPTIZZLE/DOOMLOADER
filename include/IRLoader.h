#pragma once

#include <string>
#include <vector>
#include <memory>

#include <juce_core/juce_core.h>

namespace doomloader {

/**
 * @brief Impulse Response (IR) loader and manager
 * 
 * Handles loading, caching, and managing impulse response files
 * for cabinet simulation in DOOMLOADER.
 */
class IRLoader {
public:
    IRLoader();
    ~IRLoader();

    /**
     * @brief Load an impulse response from file
     * @param filePath Path to the IR file (WAV, AIFF supported)
     * @return true if loaded successfully
     */
    bool loadIR(const std::string& filePath);

    /**
     * @brief Load IR from memory buffer
     * @param buffer Audio buffer containing IR data
     * @param sampleRate Sample rate of the IR
     * @return true if loaded successfully
     */
    bool loadIR(const std::vector<float>& buffer, double sampleRate);

    /**
     * @brief Get the loaded IR samples
     * @return Vector of IR samples
     */
    const std::vector<float>& getIRSamples() const;

    /**
     * @brief Get IR length in samples
     * @return Length of the loaded IR
     */
    size_t getIRLength() const;

    /**
     * @brief Get IR sample rate
     * @return Sample rate of the loaded IR
     */
    double getIRSampleRate() const;

    /**
     * @brief Check if an IR is currently loaded
     * @return true if IR is loaded
     */
    bool isLoaded() const;

    /**
     * @brief Clear the loaded IR
     */
    void clear();

    /**
     * @brief Get list of supported IR file formats
     * @return Vector of supported file extensions
     */
    static std::vector<std::string> getSupportedFormats();

    /**
     * @brief Validate if file is a supported IR format
     * @param filePath Path to check
     * @return true if format is supported
     */
    static bool isSupportedFormat(const std::string& filePath);

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

/**
 * @brief Convolution engine for IR processing
 * 
 * Performs real-time convolution of audio with loaded impulse responses.
 */
class ConvolutionEngine {
public:
    ConvolutionEngine();
    ~ConvolutionEngine();

    /**
     * @brief Initialize the convolution engine
     * @param sampleRate Audio sample rate
     * @param blockSize Processing block size
     * @return true if initialization successful
     */
    bool initialize(double sampleRate, int blockSize);

    /**
     * @brief Load impulse response for convolution
     * @param irSamples IR sample data
     * @param irSampleRate Sample rate of the IR
     * @return true if IR loaded successfully
     */
    bool loadIR(const std::vector<float>& irSamples, double irSampleRate);

    /**
     * @brief Process audio buffer with convolution
     * @param buffer Audio buffer to process (in-place)
     */
    void processAudio(juce::AudioBuffer<float>& buffer);

    /**
     * @brief Set wet/dry mix level
     * @param wetLevel Wet level (0.0 = dry, 1.0 = fully wet)
     */
    void setWetLevel(float wetLevel);

    /**
     * @brief Reset the convolution engine state
     */
    void reset();

    /**
     * @brief Check if engine is ready for processing
     * @return true if initialized and IR loaded
     */
    bool isReady() const;

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace doomloader