#include "DoomloaderEngine.h"
#include "AmpModeler.h"
#include "IRLoader.h"
#include "PresetManager.h"

#include <juce_dsp/juce_dsp.h>

namespace doomloader {

class DoomloaderEngine::Impl {
public:
    Impl() = default;
    ~Impl() = default;

    // Core components
    std::unique_ptr<AmpModeler> ampModeler;
    std::unique_ptr<ConvolutionEngine> convolutionEngine;
    std::unique_ptr<PresetManager> presetManager;
    std::unique_ptr<IRLoader> irLoader;
    
    // Audio processing chain
    juce::dsp::ProcessorChain<
        juce::dsp::Gain<float>,           // Input gain
        juce::dsp::Compressor<float>,     // Compressor
        juce::dsp::Gain<float>,           // Amp model (placeholder)
        juce::dsp::Reverb,                // Reverb
        juce::dsp::DelayLine<float>,      // Delay
        juce::dsp::Chorus<float>,         // Chorus
        juce::dsp::Gain<float>            // Output gain
    > effectChain;
    
    juce::dsp::ProcessSpec processSpec;
    
    // Current settings
    AmpParameters currentAmpParams;
    float irWetLevel = 1.0f;
    float reverbLevel = 0.0f;
    float delayLevel = 0.0f;
    float chorusLevel = 0.0f;
    
    bool isReady = false;
};

DoomloaderEngine::DoomloaderEngine() 
    : impl_(std::make_unique<Impl>()) {
}

DoomloaderEngine::~DoomloaderEngine() {
    shutdown();
}

bool DoomloaderEngine::initialize(double sampleRate, int blockSize) {
    if (initialized_) {
        return true;
    }
    
    sampleRate_ = sampleRate;
    blockSize_ = blockSize;
    
    // Initialize core components
    impl_->ampModeler = std::make_unique<AmpModeler>();
    impl_->convolutionEngine = std::make_unique<ConvolutionEngine>();
    impl_->presetManager = std::make_unique<PresetManager>();
    impl_->irLoader = std::make_unique<IRLoader>();
    
    // Initialize amp modeler
    if (!impl_->ampModeler->initialize(sampleRate, blockSize)) {
        return false;
    }
    
    // Initialize convolution engine
    if (!impl_->convolutionEngine->initialize(sampleRate, blockSize)) {
        return false;
    }
    
    // Initialize preset manager
    auto userDir = juce::File::getSpecialLocation(juce::File::userDocumentsDirectory)
                      .getChildFile("DOOMLOADER").getChildFile("Presets");
    if (!impl_->presetManager->initialize(userDir.getFullPathName().toStdString())) {
        return false;
    }
    
    // Setup DSP chain
    impl_->processSpec.sampleRate = sampleRate;
    impl_->processSpec.maximumBlockSize = static_cast<juce::uint32>(blockSize);
    impl_->processSpec.numChannels = 2;
    
    impl_->effectChain.prepare(impl_->processSpec);
    
    // Configure default effect settings
    auto& compressor = impl_->effectChain.get<1>();
    compressor.setThreshold(-20.0f);
    compressor.setRatio(4.0f);
    compressor.setAttack(5.0f);
    compressor.setRelease(100.0f);
    
    auto& reverb = impl_->effectChain.get<3>();
    juce::Reverb::Parameters reverbParams;
    reverbParams.roomSize = 0.3f;
    reverbParams.damping = 0.5f;
    reverbParams.wetLevel = 0.0f;
    reverbParams.dryLevel = 1.0f;
    reverb.setParameters(reverbParams);
    
    impl_->isReady = true;
    initialized_ = true;
    
    return true;
}

void DoomloaderEngine::shutdown() {
    if (!initialized_) {
        return;
    }
    
    impl_->isReady = false;
    impl_->ampModeler.reset();
    impl_->convolutionEngine.reset();
    impl_->presetManager.reset();
    impl_->irLoader.reset();
    
    initialized_ = false;
}

void DoomloaderEngine::processAudio(juce::AudioBuffer<float>& buffer) {
    if (!impl_->isReady) {
        buffer.clear();
        return;
    }
    
    // Create JUCE DSP context
    juce::dsp::AudioBlock<float> block(buffer);
    juce::dsp::ProcessContextReplacing<float> context(block);
    
    // Process through amp model
    if (impl_->ampModeler && impl_->ampModeler->isReady()) {
        impl_->ampModeler->processAudio(buffer);
    }
    
    // Process through IR convolution
    if (impl_->convolutionEngine && impl_->convolutionEngine->isReady()) {
        impl_->convolutionEngine->processAudio(buffer);
    }
    
    // Process through effect chain
    impl_->effectChain.process(context);
}

void DoomloaderEngine::reset() {
    if (!impl_->isReady) {
        return;
    }
    
    if (impl_->ampModeler) {
        impl_->ampModeler->reset();
    }
    
    if (impl_->convolutionEngine) {
        impl_->convolutionEngine->reset();
    }
    
    impl_->effectChain.reset();
}

bool DoomloaderEngine::loadPreset(const std::string& presetPath) {
    if (!impl_->presetManager) {
        return false;
    }
    
    auto preset = impl_->presetManager->loadPreset(presetPath);
    if (!preset) {
        return false;
    }
    
    // Load amp model
    if (!preset->ampModelPath.empty()) {
        loadAmpModel(preset->ampModelPath);
    }
    
    // Load IR
    if (!preset->irPath.empty()) {
        loadImpulseResponse(preset->irPath);
        setIRMix(preset->irWetLevel);
    }
    
    // Apply amp parameters
    impl_->currentAmpParams = preset->ampParams;
    if (impl_->ampModeler) {
        impl_->ampModeler->setParameters(impl_->currentAmpParams);
    }
    
    // Apply effect settings
    setReverbLevel(preset->effects.reverbLevel);
    setDelayLevel(preset->effects.delayLevel);
    setChorusLevel(preset->effects.chorusLevel);
    
    return true;
}

bool DoomloaderEngine::savePreset(const std::string& presetPath) const {
    if (!impl_->presetManager) {
        return false;
    }
    
    // Create preset from current settings
    auto preset = impl_->presetManager->createDefaultPreset("Current Settings");
    preset.ampParams = impl_->currentAmpParams;
    preset.irWetLevel = impl_->irWetLevel;
    preset.effects.reverbLevel = impl_->reverbLevel;
    preset.effects.delayLevel = impl_->delayLevel;
    preset.effects.chorusLevel = impl_->chorusLevel;
    
    return impl_->presetManager->savePreset(preset, presetPath);
}

std::vector<std::string> DoomloaderEngine::getAvailablePresets() const {
    if (!impl_->presetManager) {
        return {};
    }
    
    return impl_->presetManager->getAvailablePresets();
}

bool DoomloaderEngine::loadAmpModel(const std::string& modelPath) {
    if (!impl_->ampModeler) {
        return false;
    }
    
    return impl_->ampModeler->loadModel(modelPath);
}

void DoomloaderEngine::setAmpGain(float gain) {
    impl_->currentAmpParams.gain = juce::jlimit(0.0f, 1.0f, gain);
    
    if (impl_->ampModeler) {
        impl_->ampModeler->setParameters(impl_->currentAmpParams);
    }
}

void DoomloaderEngine::setAmpTone(float bass, float mid, float treble) {
    impl_->currentAmpParams.bass = juce::jlimit(0.0f, 1.0f, bass);
    impl_->currentAmpParams.mid = juce::jlimit(0.0f, 1.0f, mid);
    impl_->currentAmpParams.treble = juce::jlimit(0.0f, 1.0f, treble);
    
    if (impl_->ampModeler) {
        impl_->ampModeler->setParameters(impl_->currentAmpParams);
    }
}

bool DoomloaderEngine::loadImpulseResponse(const std::string& irPath) {
    if (!impl_->irLoader || !impl_->convolutionEngine) {
        return false;
    }
    
    if (!impl_->irLoader->loadIR(irPath)) {
        return false;
    }
    
    const auto& irSamples = impl_->irLoader->getIRSamples();
    double irSampleRate = impl_->irLoader->getIRSampleRate();
    
    return impl_->convolutionEngine->loadIR(irSamples, irSampleRate);
}

void DoomloaderEngine::setIRMix(float wetLevel) {
    impl_->irWetLevel = juce::jlimit(0.0f, 1.0f, wetLevel);
    
    if (impl_->convolutionEngine) {
        impl_->convolutionEngine->setWetLevel(impl_->irWetLevel);
    }
}

void DoomloaderEngine::setReverbLevel(float level) {
    impl_->reverbLevel = juce::jlimit(0.0f, 1.0f, level);
    
    auto& reverb = impl_->effectChain.get<3>();
    auto params = reverb.getParameters();
    params.wetLevel = impl_->reverbLevel;
    params.dryLevel = 1.0f - impl_->reverbLevel;
    reverb.setParameters(params);
}

void DoomloaderEngine::setDelayLevel(float level) {
    impl_->delayLevel = juce::jlimit(0.0f, 1.0f, level);
    // Delay implementation would go here
}

void DoomloaderEngine::setChorusLevel(float level) {
    impl_->chorusLevel = juce::jlimit(0.0f, 1.0f, level);
    
    auto& chorus = impl_->effectChain.get<5>();
    chorus.setMix(impl_->chorusLevel);
}

} // namespace doomloader