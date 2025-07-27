# Setup JUCE Framework for DOOMLOADER

# JUCE is a cross-platform C++ application framework
# We'll use it for audio processing, UI, and plugin hosting

include(FetchContent)

# Set JUCE options before fetching
set(JUCE_BUILD_EXTRAS OFF CACHE BOOL "Build JUCE Extras")
set(JUCE_BUILD_EXAMPLES OFF CACHE BOOL "Build JUCE Examples")

# Fetch JUCE from GitHub
FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 7.0.9
    GIT_SHALLOW TRUE
)

FetchContent_MakeAvailable(JUCE)

# JUCE modules we need for DOOMLOADER
set(DOOMLOADER_JUCE_MODULES
    juce_core
    juce_events
    juce_graphics
    juce_data_structures
    juce_gui_basics
    juce_gui_extra
    juce_cryptography
    juce_audio_basics
    juce_audio_devices
    juce_audio_formats
    juce_audio_processors
    juce_audio_utils
    juce_dsp
)

# For plugin builds
if(DOOMLOADER_BUILD_PLUGIN)
    list(APPEND DOOMLOADER_JUCE_MODULES juce_audio_plugin_client)
endif()

# Create JUCE target with our required modules
function(doomloader_add_juce_target target_name)
    target_link_libraries(${target_name} 
        PRIVATE 
        ${DOOMLOADER_JUCE_MODULES}
    )
    
    # JUCE preprocessor definitions
    target_compile_definitions(${target_name}
        PRIVATE
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_APPLICATION_NAME_STRING="$<TARGET_PROPERTY:${target_name},JUCE_PRODUCT_NAME>"
        JUCE_APPLICATION_VERSION_STRING="$<TARGET_PROPERTY:${target_name},JUCE_VERSION>"
    )
    
    # Platform-specific settings
    if(DOOMLOADER_IOS)
        target_compile_definitions(${target_name} 
            PRIVATE 
            JUCE_STANDALONE_APPLICATION=1
        )
    endif()
endfunction()

message(STATUS "JUCE Framework configured for DOOMLOADER")