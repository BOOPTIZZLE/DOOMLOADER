# Mobile Development with DOOMLOADER

DOOMLOADER is designed from the ground up to support mobile platforms, including iOS and Android. This guide covers platform-specific considerations, setup, and development practices for mobile deployments.

## Platform Support Status

| Platform | Status | Audio Engine | UI Framework | Notes |
|----------|--------|--------------|--------------|-------|
| iOS | ✅ Ready | Core Audio | JUCE | Full feature support |
| Android | 🚧 Beta | Oboe/AAudio | JUCE | Limited testing |

## iOS Development

### Prerequisites

- Xcode 14.0 or later
- iOS 13.0+ target
- Valid Apple Developer account
- macOS development machine

### Project Setup

```bash
# Configure for iOS
cmake -B build-ios \
  -DCMAKE_TOOLCHAIN_FILE=cmake/ios.toolchain.cmake \
  -DPLATFORM=OS64 \
  -DDOOMLOADER_BUILD_STANDALONE=ON \
  -DDOOMLOADER_IOS=ON

# Build
cmake --build build-ios --config Release
```

### iOS-Specific Features

#### Audio Session Configuration

```cpp
#if DOOMLOADER_IOS
#include <AVFoundation/AVFoundation.h>

class iOSAudioSetup {
public:
    static bool configureAudioSession() {
        NSError* error = nil;
        AVAudioSession* session = [AVAudioSession sharedInstance];
        
        // Set category for audio processing
        [session setCategory:AVAudioSessionCategoryPlayAndRecord
                 withOptions:AVAudioSessionCategoryOptionMixWithOthers |
                            AVAudioSessionCategoryOptionAllowBluetooth |
                            AVAudioSessionCategoryOptionDefaultToSpeaker
                       error:&error];
        
        if (error) {
            return false;
        }
        
        // Set preferred buffer size (low latency)
        [session setPreferredIOBufferDuration:0.005 error:&error]; // 5ms
        
        // Activate session
        [session setActive:YES error:&error];
        
        return error == nil;
    }
};
#endif
```

#### Background Audio Support

```cpp
// Enable background audio processing
#if DOOMLOADER_IOS
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Configure background audio
    [[AVAudioSession sharedInstance] setCategory:AVAudioSessionCategoryPlayAndRecord error:nil];
    [[AVAudioSession sharedInstance] setActive:YES error:nil];
    
    return YES;
}
#endif
```

#### Inter-App Audio

```cpp
#if DOOMLOADER_IOS
class InterAppAudioSupport {
public:
    static void enableInterAppAudio() {
        // Enable Inter-App Audio hosting
        AudioComponentDescription desc;
        desc.componentType = kAudioUnitType_RemoteEffect;
        desc.componentSubType = 'DOOM';
        desc.componentManufacturer = 'DLDR';
        desc.componentFlags = 0;
        desc.componentFlagsMask = 0;
        
        // Register as Inter-App Audio effect
        AudioComponentRegister(&desc, CFSTR("DOOMLOADER"), 0, nullptr);
    }
};
#endif
```

### iOS UI Considerations

```cpp
#if DOOMLOADER_IOS
class iOSUIOptimizations {
public:
    static void setupTouchInterface() {
        // Larger touch targets for mobile
        const int minTouchSize = 44; // Apple HIG recommendation
        
        // Enable gesture recognition
        // Implement swipe gestures for preset switching
        // Use long press for parameter automation
    }
    
    static void handleOrientationChange() {
        // Adapt UI layout for landscape/portrait
        // Optimize control placement for thumbs
    }
    
    static void enableAccessibility() {
        // VoiceOver support for visually impaired users
        // Dynamic type support
        // High contrast mode support
    }
};
#endif
```

## Android Development

### Prerequisites

- Android Studio 2022.3.1 or later
- Android NDK 25.0+
- API Level 24+ (Android 7.0)
- CMake 3.20+

### Project Setup

```bash
# Configure for Android
cmake -B build-android \
  -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-24 \
  -DDOOMLOADER_ANDROID=ON \
  -DDOOMLOADER_BUILD_STANDALONE=ON

# Build
cmake --build build-android --config Release
```

### Android Audio Configuration

```cpp
#if DOOMLOADER_ANDROID
#include <oboe/Oboe.h>

class AndroidAudioSetup {
public:
    static std::unique_ptr<oboe::AudioStream> createStream() {
        oboe::AudioStreamBuilder builder;
        
        builder.setDirection(oboe::Direction::InputOutput)
               ->setPerformanceMode(oboe::PerformanceMode::LowLatency)
               ->setSharingMode(oboe::SharingMode::Exclusive)
               ->setFormat(oboe::AudioFormat::Float)
               ->setChannelCount(2)
               ->setSampleRate(48000)
               ->setBufferCapacityInFrames(192) // 4ms at 48kHz
               ->setCallback(audioCallback);
        
        std::unique_ptr<oboe::AudioStream> stream;
        oboe::Result result = builder.openStream(stream);
        
        if (result == oboe::Result::OK) {
            stream->start();
            return stream;
        }
        
        return nullptr;
    }
};
#endif
```

### Android Permissions

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />

<!-- For low-latency audio -->
<uses-feature android:name="android.hardware.audio.low_latency" android:required="false" />
<uses-feature android:name="android.hardware.audio.pro" android:required="false" />
```

## Cross-Platform Mobile Architecture

### Shared Audio Engine

```cpp
class MobileAudioEngine {
    doomloader::DoomloaderEngine engine_;
    
#if DOOMLOADER_IOS
    std::unique_ptr<iOSAudioInterface> audioInterface_;
#elif DOOMLOADER_ANDROID
    std::unique_ptr<AndroidAudioInterface> audioInterface_;
#endif

public:
    bool initialize() {
        // Platform-agnostic initialization
        if (!engine_.initialize(48000.0, 128)) {
            return false;
        }
        
#if DOOMLOADER_IOS
        audioInterface_ = std::make_unique<iOSAudioInterface>();
        iOSAudioSetup::configureAudioSession();
#elif DOOMLOADER_ANDROID
        audioInterface_ = std::make_unique<AndroidAudioInterface>();
#endif
        
        return audioInterface_->start();
    }
    
    void processAudio(float* inputBuffer, float* outputBuffer, int numFrames) {
        juce::AudioBuffer<float> buffer(outputBuffer, 2, numFrames);
        
        // Copy input to buffer
        for (int ch = 0; ch < 2; ++ch) {
            std::copy(inputBuffer + ch * numFrames,
                     inputBuffer + (ch + 1) * numFrames,
                     buffer.getWritePointer(ch));
        }
        
        // Process through DOOMLOADER
        engine_.processAudio(buffer);
    }
};
```

### Mobile UI Framework

```cpp
class MobileUI {
protected:
    float scaleFactor_ = 1.0f;
    bool isTablet_ = false;
    
public:
    virtual void setupForMobile() {
        // Detect device type
        isTablet_ = detectTablet();
        scaleFactor_ = calculateScaleFactor();
        
        // Configure UI elements
        setupTouchControls();
        setupGestures();
        enableHapticFeedback();
    }
    
private:
    bool detectTablet() {
#if DOOMLOADER_IOS
        return UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPad;
#elif DOOMLOADER_ANDROID
        // Check screen size and density
        return getScreenSizeInches() >= 7.0f;
#endif
    }
    
    void setupTouchControls() {
        // Minimum touch target size
        const float minTouchSize = isTablet_ ? 44.0f : 48.0f;
        
        // Adjust control sizes
        resizeControlsForTouch(minTouchSize * scaleFactor_);
    }
    
    void setupGestures() {
        // Swipe gestures for preset navigation
        enableSwipeGestures();
        
        // Pinch to zoom for detailed editing
        enablePinchZoom();
        
        // Two-finger gestures for advanced controls
        enableMultiTouchGestures();
    }
};
```

## Performance Optimization for Mobile

### CPU Optimization

```cpp
class MobilePerformanceManager {
    bool isLowPowerMode_ = false;
    
public:
    void adaptToPowerState() {
#if DOOMLOADER_IOS
        isLowPowerMode_ = [[NSProcessInfo processInfo] isLowPowerModeEnabled];
#elif DOOMLOADER_ANDROID
        // Check battery level and thermal state
        isLowPowerMode_ = getBatteryLevel() < 20 || getThermalState() > 2;
#endif
        
        if (isLowPowerMode_) {
            enablePowerSavingMode();
        }
    }
    
private:
    void enablePowerSavingMode() {
        // Reduce processing quality
        engine_.setQualityMode(doomloader::QualityMode::Performance);
        
        // Increase buffer size to reduce CPU load
        engine_.setBufferSize(256);
        
        // Disable expensive effects
        engine_.setOversamplingEnabled(false);
    }
};
```

### Memory Management

```cpp
class MobileMemoryManager {
public:
    static void optimizeForMobile() {
        // Limit cache sizes
        doomloader::AmpModeler::setMaxCacheSize(64 * 1024 * 1024); // 64MB
        
        // Preload only essential presets
        preloadCriticalPresets();
        
        // Use compressed IR storage
        enableIRCompression();
        
        // Monitor memory usage
        setupMemoryWarnings();
    }
    
private:
    static void setupMemoryWarnings() {
#if DOOMLOADER_IOS
        [[NSNotificationCenter defaultCenter] 
            addObserverForName:UIApplicationDidReceiveMemoryWarningNotification
                        object:nil
                         queue:nil
                    usingBlock:^(NSNotification *note) {
                        handleMemoryWarning();
                    }];
#elif DOOMLOADER_ANDROID
        // Register for trim memory callbacks
        registerTrimMemoryCallback();
#endif
    }
    
    static void handleMemoryWarning() {
        // Clear non-essential caches
        doomloader::AmpModeler::clearCache();
        doomloader::PresetManager::clearUnusedPresets();
        
        // Force garbage collection if applicable
        System.gc(); // Android
    }
};
```

## Mobile-Specific Features

### Haptic Feedback

```cpp
class HapticFeedback {
public:
    static void playSelectionFeedback() {
#if DOOMLOADER_IOS
        UISelectionFeedbackGenerator* generator = [[UISelectionFeedbackGenerator alloc] init];
        [generator selectionChanged];
#elif DOOMLOADER_ANDROID
        // Use system haptic feedback
        vibratePattern({50}); // 50ms vibration
#endif
    }
    
    static void playImpactFeedback(ImpactStrength strength) {
#if DOOMLOADER_IOS
        UIImpactFeedbackGenerator* generator;
        switch (strength) {
            case Light: generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleLight]; break;
            case Medium: generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleMedium]; break;
            case Heavy: generator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleHeavy]; break;
        }
        [generator impactOccurred];
#endif
    }
};
```

### Cloud Integration

```cpp
class MobileCloudSync {
public:
    void enableBackgroundSync() {
#if DOOMLOADER_IOS
        // Use background app refresh
        UIApplication* app = [UIApplication sharedApplication];
        if ([app backgroundRefreshStatus] == UIBackgroundRefreshStatusAvailable) {
            scheduleBackgroundSync();
        }
#elif DOOMLOADER_ANDROID
        // Use WorkManager for background tasks
        schedulePeriodicWorkRequest();
#endif
    }
    
private:
    void syncPresetsInBackground() {
        // Sync only when on WiFi to save data
        if (isConnectedToWiFi()) {
            tone3000Client_.syncPresets();
        }
    }
};
```

## Testing on Mobile Devices

### iOS Testing

```bash
# Build for iOS Simulator
cmake -B build-ios-sim \
  -DCMAKE_TOOLCHAIN_FILE=cmake/ios.toolchain.cmake \
  -DPLATFORM=SIMULATOR64 \
  -DDOOMLOADER_IOS=ON

# Run on simulator
xcrun simctl install booted build-ios-sim/src/DOOMLOADER.app
xcrun simctl launch booted com.doomloader.app
```

### Android Testing

```bash
# Build APK
cd build-android
./gradlew assembleDebug

# Install on device
adb install -r app/build/outputs/apk/debug/app-debug.apk

# Launch app
adb shell am start -n com.doomloader.app/.MainActivity

# Monitor logs
adb logcat | grep DOOMLOADER
```

### Performance Profiling

```cpp
class MobileProfiler {
public:
    static void profileAudioPerformance() {
#if DOOMLOADER_IOS
        // Use Instruments for iOS profiling
        // Check CPU usage, memory allocations, audio dropouts
#elif DOOMLOADER_ANDROID
        // Use systrace for Android profiling
        // Monitor audio callback timing
#endif
    }
    
    static void logPerformanceMetrics() {
        auto stats = engine_.getPerformanceStats();
        
        DOOMLOADER_LOG("CPU Usage: %.1f%%", stats.cpuUsage);
        DOOMLOADER_LOG("Memory Usage: %.1f MB", stats.memoryUsageMB);
        DOOMLOADER_LOG("Audio Dropouts: %d", stats.audioDropouts);
        DOOMLOADER_LOG("Latency: %.1f ms", stats.latencyMs);
    }
};
```

## Distribution

### iOS App Store

1. **Prepare for submission**:
   ```bash
   # Archive for distribution
   xcodebuild archive -project DOOMLOADER.xcodeproj \
                     -scheme DOOMLOADER \
                     -configuration Release \
                     -archivePath build/DOOMLOADER.xcarchive
   
   # Export IPA
   xcodebuild -exportArchive -archivePath build/DOOMLOADER.xcarchive \
                            -exportPath build/AppStore \
                            -exportOptionsPlist ExportOptions.plist
   ```

2. **App Store metadata**:
   - Categories: Music, Entertainment
   - Age rating: 4+ (no objectionable content)
   - Privacy policy for audio recording

### Google Play Store

1. **Prepare Android App Bundle**:
   ```bash
   # Generate signed AAB
   ./gradlew bundleRelease
   
   # Sign with upload key
   jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
            -keystore upload-keystore.jks \
            app-release.aab upload
   ```

2. **Play Console setup**:
   - Target API level: Latest (API 34+)
   - 64-bit requirement compliance
   - Audio recording permission justification

## Troubleshooting

### Common iOS Issues

```cpp
// Audio session interruption handling
#if DOOMLOADER_IOS
- (void)handleAudioSessionInterruption:(NSNotification*)notification {
    NSNumber* interruptionType = notification.userInfo[AVAudioSessionInterruptionTypeKey];
    
    if (interruptionType.unsignedIntegerValue == AVAudioSessionInterruptionTypeBegan) {
        // Pause audio processing
        engine_.pause();
    } else if (interruptionType.unsignedIntegerValue == AVAudioSessionInterruptionTypeEnded) {
        // Resume audio processing
        engine_.resume();
    }
}
#endif
```

### Common Android Issues

```cpp
// Handle audio focus changes
#if DOOMLOADER_ANDROID
class AudioFocusHandler : public oboe::AudioStreamCallback {
public:
    oboe::DataCallbackResult onAudioReady(oboe::AudioStream* stream,
                                         void* audioData,
                                         int32_t numFrames) override {
        if (hasAudioFocus_) {
            // Process audio normally
            return oboe::DataCallbackResult::Continue;
        } else {
            // Mute output when focus lost
            memset(audioData, 0, numFrames * sizeof(float) * 2);
            return oboe::DataCallbackResult::Continue;
        }
    }
    
    void onAudioFocusLost() { hasAudioFocus_ = false; }
    void onAudioFocusGained() { hasAudioFocus_ = true; }
    
private:
    bool hasAudioFocus_ = true;
};
#endif
```

## See Also
- [Getting Started Guide](getting-started.md)
- [API Reference](api-reference.md)
- [Plugin Development](plugin-development.md)