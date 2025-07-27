# DOOMLOADER Core Library

add_library(DoomloaderCore STATIC)

# Core source files
target_sources(DoomloaderCore
    PRIVATE
        Core/DoomloaderEngine.cpp
        Core/AudioProcessor.cpp
        Core/PresetManager.cpp
        Core/IRLoader.cpp
        Core/AmpModeler.cpp
        
        # NAM Integration
        NAM/NAMWrapper.cpp
        NAM/ModelLoader.cpp
        
        # Tone3000 Integration  
        Tone3000/APIClient.cpp
        Tone3000/PresetSync.cpp
        
        # Audio Processing
        Audio/BufferProcessor.cpp
        Audio/EffectChain.cpp
        Audio/ConvolutionEngine.cpp
        
        # Utils
        Utils/FileUtils.cpp
        Utils/AudioUtils.cpp
        Utils/ConfigManager.cpp
)

# Include directories
target_include_directories(DoomloaderCore
    PUBLIC 
        ${CMAKE_SOURCE_DIR}/include
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# Link dependencies
doomloader_add_juce_target(DoomloaderCore)
doomloader_add_nam_support(DoomloaderCore)  
doomloader_add_tone3000_support(DoomloaderCore)

# Compiler features
target_compile_features(DoomloaderCore PUBLIC cxx_std_17)

# Preprocessor definitions
target_compile_definitions(DoomloaderCore
    PUBLIC
        DOOMLOADER_VERSION_MAJOR=${PROJECT_VERSION_MAJOR}
        DOOMLOADER_VERSION_MINOR=${PROJECT_VERSION_MINOR}
        DOOMLOADER_VERSION_PATCH=${PROJECT_VERSION_PATCH}
    PRIVATE
        DOOMLOADER_BUILDING_CORE=1
)

# Platform-specific configuration
if(DOOMLOADER_MOBILE)
    target_compile_definitions(DoomloaderCore PUBLIC DOOMLOADER_MOBILE=1)
endif()

# Plugin target
if(DOOMLOADER_BUILD_PLUGIN)
    juce_add_plugin(DoomloaderPlugin
        COMPANY_NAME "DOOMLOADER"
        PLUGIN_MANUFACTURER_CODE "DOOM"
        PLUGIN_CODE "DLDR"
        FORMATS VST3 AU Standalone
        PRODUCT_NAME "DOOMLOADER"
        IS_SYNTH FALSE
        NEEDS_MIDI_INPUT FALSE
        NEEDS_MIDI_OUTPUT FALSE
        IS_MIDI_EFFECT FALSE
        EDITOR_WANTS_KEYBOARD_FOCUS FALSE
        COPY_PLUGIN_AFTER_BUILD TRUE
        VST3_CATEGORIES "Fx;Distortion;Dynamics"
    )
    
    target_sources(DoomloaderPlugin PRIVATE Plugin/PluginProcessor.cpp Plugin/PluginEditor.cpp)
    target_link_libraries(DoomloaderPlugin PRIVATE DoomloaderCore)
    doomloader_add_juce_target(DoomloaderPlugin)
endif()

# Standalone application
if(DOOMLOADER_BUILD_STANDALONE)
    juce_add_gui_app(DoomloaderApp
        PRODUCT_NAME "DOOMLOADER"
        COMPANY_NAME "DOOMLOADER Project"
    )
    
    target_sources(DoomloaderApp PRIVATE Standalone/Main.cpp Standalone/MainWindow.cpp)
    target_link_libraries(DoomloaderApp PRIVATE DoomloaderCore)
    doomloader_add_juce_target(DoomloaderApp)
endif()