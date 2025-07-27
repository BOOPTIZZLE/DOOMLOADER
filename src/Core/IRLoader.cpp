#include "IRLoader.h"
#include <juce_audio_formats/juce_audio_formats.h>

namespace doomloader {

class IRLoader::Impl {
public:
    std::vector<float> irSamples;
    double irSampleRate = 44100.0;
    
    juce::AudioFormatManager formatManager;
    
    Impl() {
        formatManager.registerBasicFormats();
    }
};

IRLoader::IRLoader() : impl_(std::make_unique<Impl>()) {}
IRLoader::~IRLoader() = default;

bool IRLoader::loadIR(const std::string& filePath) {
    juce::File file(filePath);
    if (!file.exists()) {
        return false;
    }
    
    auto* reader = impl_->formatManager.createReaderFor(file);
    if (!reader) {
        return false;
    }
    
    juce::AudioBuffer<float> buffer(static_cast<int>(reader->numChannels), 
                                   static_cast<int>(reader->lengthInSamples));
    reader->read(&buffer, 0, static_cast<int>(reader->lengthInSamples), 0, true, true);
    
    // Convert to mono if stereo (mix down)
    impl_->irSamples.clear();
    impl_->irSamples.resize(static_cast<size_t>(buffer.getNumSamples()));
    
    if (buffer.getNumChannels() == 1) {
        // Mono - copy directly
        std::copy(buffer.getReadPointer(0), 
                 buffer.getReadPointer(0) + buffer.getNumSamples(),
                 impl_->irSamples.begin());
    } else {
        // Multi-channel - mix to mono
        for (int i = 0; i < buffer.getNumSamples(); ++i) {
            float sum = 0.0f;
            for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
                sum += buffer.getSample(ch, i);
            }
            impl_->irSamples[i] = sum / buffer.getNumChannels();
        }
    }
    
    impl_->irSampleRate = reader->sampleRate;
    delete reader;
    
    return true;
}

bool IRLoader::loadIR(const std::vector<float>& buffer, double sampleRate) {
    impl_->irSamples = buffer;
    impl_->irSampleRate = sampleRate;
    return true;
}

const std::vector<float>& IRLoader::getIRSamples() const {
    return impl_->irSamples;
}

size_t IRLoader::getIRLength() const {
    return impl_->irSamples.size();
}

double IRLoader::getIRSampleRate() const {
    return impl_->irSampleRate;
}

bool IRLoader::isLoaded() const {
    return !impl_->irSamples.empty();
}

void IRLoader::clear() {
    impl_->irSamples.clear();
    impl_->irSampleRate = 44100.0;
}

std::vector<std::string> IRLoader::getSupportedFormats() {
    return {".wav", ".aiff", ".aif", ".flac"};
}

bool IRLoader::isSupportedFormat(const std::string& filePath) {
    auto extension = juce::File(filePath).getFileExtension().toLowerCase().toStdString();
    auto formats = getSupportedFormats();
    return std::find(formats.begin(), formats.end(), extension) != formats.end();
}

// ConvolutionEngine implementation
class ConvolutionEngine::Impl {
public:
    juce::dsp::Convolution convolution;
    float wetLevel = 1.0f;
    bool isInitialized = false;
    bool hasIR = false;
};

ConvolutionEngine::ConvolutionEngine() : impl_(std::make_unique<Impl>()) {}
ConvolutionEngine::~ConvolutionEngine() = default;

bool ConvolutionEngine::initialize(double sampleRate, int blockSize) {
    juce::dsp::ProcessSpec spec;
    spec.sampleRate = sampleRate;
    spec.maximumBlockSize = static_cast<juce::uint32>(blockSize);
    spec.numChannels = 2;
    
    impl_->convolution.prepare(spec);
    impl_->isInitialized = true;
    
    return true;
}

bool ConvolutionEngine::loadIR(const std::vector<float>& irSamples, double irSampleRate) {
    if (!impl_->isInitialized || irSamples.empty()) {
        return false;
    }
    
    // Create JUCE AudioBuffer from IR samples
    juce::AudioBuffer<float> irBuffer(1, static_cast<int>(irSamples.size()));
    std::copy(irSamples.begin(), irSamples.end(), irBuffer.getWritePointer(0));
    
    impl_->convolution.loadImpulseResponse(std::move(irBuffer), irSampleRate, 
                                          juce::dsp::Convolution::Stereo::yes,
                                          juce::dsp::Convolution::Trim::yes,
                                          juce::dsp::Convolution::Normalise::yes);
    
    impl_->hasIR = true;
    return true;
}

void ConvolutionEngine::processAudio(juce::AudioBuffer<float>& buffer) {
    if (!isReady()) {
        return;
    }
    
    juce::dsp::AudioBlock<float> block(buffer);
    juce::dsp::ProcessContextReplacing<float> context(block);
    
    impl_->convolution.process(context);
    
    // Apply wet/dry mix
    if (impl_->wetLevel < 1.0f) {
        // This is a simplified implementation - in practice you'd need
        // to maintain a dry buffer for proper wet/dry mixing
        buffer.applyGain(impl_->wetLevel);
    }
}

void ConvolutionEngine::setWetLevel(float wetLevel) {
    impl_->wetLevel = juce::jlimit(0.0f, 1.0f, wetLevel);
}

void ConvolutionEngine::reset() {
    if (impl_->isInitialized) {
        impl_->convolution.reset();
    }
}

bool ConvolutionEngine::isReady() const {
    return impl_->isInitialized && impl_->hasIR;
}

} // namespace doomloader