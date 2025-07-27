#pragma once

#include <string>
#include <vector>
#include <map>
#include <memory>

#include <juce_core/juce_core.h>

namespace doomloader {

/**
 * @brief Amp model parameter structure
 */
struct AmpParameters {
    float gain = 0.5f;        // Input gain (0.0 - 1.0)
    float bass = 0.5f;        // Bass EQ (0.0 - 1.0)
    float mid = 0.5f;         // Mid EQ (0.0 - 1.0)
    float treble = 0.5f;      // Treble EQ (0.0 - 1.0)
    float presence = 0.5f;    // Presence control (0.0 - 1.0)
    float volume = 0.5f;      // Output volume (0.0 - 1.0)
    
    // Advanced parameters
    float saturation = 0.0f;  // Additional saturation (0.0 - 1.0)
    float asymmetry = 0.0f;   // Tube asymmetry simulation (0.0 - 1.0)
    float sag = 0.0f;         // Power supply sag simulation (0.0 - 1.0)
};

/**
 * @brief Amp model metadata
 */
struct AmpModelInfo {
    std::string name;
    std::string description;
    std::string author;
    std::string version;
    std::string ampType;      // e.g., "tube", "solid_state", "digital"
    std::string modelFormat;  // e.g., "nam", "neural", "algorithmic"
    double sampleRate = 48000.0;
    
    // File information
    std::string filePath;
    size_t fileSize = 0;
    std::string checksum;
};

/**
 * @brief Neural Amp Modeler (NAM) integration wrapper
 * 
 * Provides interface to load and process NAM models for amp simulation.
 */
class NAMWrapper {
public:
    NAMWrapper();
    ~NAMWrapper();

    /**
     * @brief Initialize NAM processing
     * @param sampleRate Audio sample rate
     * @param blockSize Processing block size
     * @return true if initialization successful
     */
    bool initialize(double sampleRate, int blockSize);

    /**
     * @brief Load a NAM model file
     * @param modelPath Path to the .nam model file
     * @return true if model loaded successfully
     */
    bool loadModel(const std::string& modelPath);

    /**
     * @brief Process audio buffer through NAM model
     * @param buffer Audio buffer to process (in-place)
     */
    void processAudio(juce::AudioBuffer<float>& buffer);

    /**
     * @brief Set input gain for the model
     * @param gain Input gain level (typically 0.0 - 2.0)
     */
    void setInputGain(float gain);

    /**
     * @brief Set output level for the model
     * @param level Output level (0.0 - 1.0)
     */
    void setOutputLevel(float level);

    /**
     * @brief Reset the model state
     */
    void reset();

    /**
     * @brief Check if model is loaded and ready
     * @return true if ready for processing
     */
    bool isReady() const;

    /**
     * @brief Get information about the loaded model
     * @return Model information structure
     */
    const AmpModelInfo& getModelInfo() const;

    /**
     * @brief Validate NAM model file
     * @param modelPath Path to check
     * @return true if file is a valid NAM model
     */
    static bool isValidNAMFile(const std::string& modelPath);

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

/**
 * @brief Generic amp modeler supporting multiple model formats
 * 
 * High-level interface that can handle NAM models, built-in algorithmic
 * models, and other amp simulation formats.
 */
class AmpModeler {
public:
    enum class ModelType {
        None,
        NAM,           // Neural Amp Modeler
        Algorithmic,   // Built-in algorithmic models
        Tone3000       // Cloud-based models from Tone3000
    };

    AmpModeler();
    ~AmpModeler();

    /**
     * @brief Initialize the amp modeler
     * @param sampleRate Audio sample rate
     * @param blockSize Processing block size
     * @return true if initialization successful
     */
    bool initialize(double sampleRate, int blockSize);

    /**
     * @brief Load an amp model
     * @param modelPath Path to model file or model identifier
     * @param type Model type (auto-detected if None)
     * @return true if model loaded successfully
     */
    bool loadModel(const std::string& modelPath, ModelType type = ModelType::None);

    /**
     * @brief Process audio with the loaded amp model
     * @param buffer Audio buffer to process (in-place)
     */
    void processAudio(juce::AudioBuffer<float>& buffer);

    /**
     * @brief Set amp parameters
     * @param params Amp parameter structure
     */
    void setParameters(const AmpParameters& params);

    /**
     * @brief Get current amp parameters
     * @return Current parameter values
     */
    const AmpParameters& getParameters() const;

    /**
     * @brief Reset the amp model state
     */
    void reset();

    /**
     * @brief Check if model is loaded
     * @return true if ready for processing
     */
    bool isReady() const;

    /**
     * @brief Get loaded model type
     * @return Current model type
     */
    ModelType getModelType() const;

    /**
     * @brief Get list of available built-in models
     * @return Vector of built-in model names
     */
    static std::vector<std::string> getBuiltInModels();

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace doomloader