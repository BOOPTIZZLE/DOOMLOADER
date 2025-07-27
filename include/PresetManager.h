#pragma once

#include <string>
#include <vector>
#include <map>
#include <memory>

#include <juce_core/juce_core.h>
#include "AmpModeler.h"

namespace doomloader {

/**
 * @brief Preset data structure
 */
struct Preset {
    std::string name;
    std::string description;
    std::string author;
    std::string category;      // e.g., "Clean", "Crunch", "Lead", "Metal"
    std::string tags;          // Comma-separated tags
    
    // Model information
    std::string ampModelPath;
    std::string irPath;
    
    // Amp parameters
    AmpParameters ampParams;
    
    // IR parameters
    float irWetLevel = 1.0f;
    
    // Effect parameters
    struct Effects {
        float reverbLevel = 0.0f;
        float delayLevel = 0.0f;
        float chorusLevel = 0.0f;
        float compressorThreshold = 1.0f;
        float compressorRatio = 1.0f;
        float noiseGateThreshold = 0.0f;
    } effects;
    
    // Metadata
    std::string version = "1.0";
    std::string created;       // ISO 8601 timestamp
    std::string modified;      // ISO 8601 timestamp
    std::string uuid;          // Unique identifier
};

/**
 * @brief Preset manager for DOOMLOADER
 * 
 * Handles loading, saving, organizing, and syncing presets.
 * Supports both local presets and cloud sync via Tone3000 API.
 */
class PresetManager {
public:
    PresetManager();
    ~PresetManager();

    /**
     * @brief Initialize the preset manager
     * @param presetDirectory Base directory for storing presets
     * @return true if initialization successful
     */
    bool initialize(const std::string& presetDirectory);

    /**
     * @brief Load a preset from file
     * @param presetPath Path to the preset file (.json)
     * @return Loaded preset, or nullptr if failed
     */
    std::unique_ptr<Preset> loadPreset(const std::string& presetPath);

    /**
     * @brief Save a preset to file
     * @param preset Preset to save
     * @param presetPath Output file path (.json)
     * @return true if saved successfully
     */
    bool savePreset(const Preset& preset, const std::string& presetPath);

    /**
     * @brief Get all available presets
     * @return Vector of preset file paths
     */
    std::vector<std::string> getAvailablePresets() const;

    /**
     * @brief Get presets by category
     * @param category Category name (e.g., "Clean", "Metal")
     * @return Vector of matching preset paths
     */
    std::vector<std::string> getPresetsByCategory(const std::string& category) const;

    /**
     * @brief Search presets by name or tags
     * @param query Search query
     * @return Vector of matching preset paths
     */
    std::vector<std::string> searchPresets(const std::string& query) const;

    /**
     * @brief Create a new preset with default values
     * @param name Preset name
     * @param category Preset category
     * @return New preset with defaults
     */
    Preset createDefaultPreset(const std::string& name, const std::string& category = "User");

    /**
     * @brief Validate preset file format
     * @param presetPath Path to preset file
     * @return true if file is a valid preset
     */
    bool validatePreset(const std::string& presetPath) const;

    /**
     * @brief Import preset from another format
     * @param filePath Path to preset file (supports various formats)
     * @param outputPath Where to save the converted preset
     * @return true if import successful
     */
    bool importPreset(const std::string& filePath, const std::string& outputPath);

    /**
     * @brief Export preset to another format
     * @param presetPath Path to DOOMLOADER preset
     * @param outputPath Output file path
     * @param format Target format ("json", "xml", etc.)
     * @return true if export successful
     */
    bool exportPreset(const std::string& presetPath, const std::string& outputPath, 
                     const std::string& format = "json");

    // Cloud sync functionality (requires Tone3000 API)
    #ifdef DOOMLOADER_TONE3000_ENABLED
    /**
     * @brief Sync presets with Tone3000 cloud
     * @param apiKey Tone3000 API key
     * @return true if sync successful
     */
    bool syncWithCloud(const std::string& apiKey);

    /**
     * @brief Upload preset to Tone3000 cloud
     * @param preset Preset to upload
     * @param apiKey Tone3000 API key
     * @return Cloud preset ID, or empty string if failed
     */
    std::string uploadPreset(const Preset& preset, const std::string& apiKey);

    /**
     * @brief Download preset from Tone3000 cloud
     * @param presetId Cloud preset ID
     * @param apiKey Tone3000 API key
     * @return Downloaded preset, or nullptr if failed
     */
    std::unique_ptr<Preset> downloadPreset(const std::string& presetId, const std::string& apiKey);
    #endif

    /**
     * @brief Get preset directory path
     * @return Base preset directory
     */
    const std::string& getPresetDirectory() const;

    /**
     * @brief Get supported preset file formats
     * @return Vector of supported file extensions
     */
    static std::vector<std::string> getSupportedFormats();

private:
    class Impl;
    std::unique_ptr<Impl> impl_;
};

/**
 * @brief Preset category manager
 * 
 * Manages preset categories and organization.
 */
class PresetCategories {
public:
    static std::vector<std::string> getDefaultCategories();
    static std::string getCategoryDescription(const std::string& category);
    static std::vector<std::string> getCategoryTags(const std::string& category);
    static bool isValidCategory(const std::string& category);
};

} // namespace doomloader