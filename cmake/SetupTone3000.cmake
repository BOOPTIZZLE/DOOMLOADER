# Setup Tone3000 API for DOOMLOADER

# Tone3000 provides cloud-based amp modeling and preset sharing
# This module handles the API integration

# Tone3000 API configuration
set(TONE3000_API_VERSION "v1" CACHE STRING "Tone3000 API version")
set(TONE3000_BASE_URL "https://api.tone3000.com" CACHE STRING "Tone3000 API base URL")

# Create interface library for Tone3000 integration
add_library(DOOMLOADER_TONE3000 INTERFACE)

# Check for cURL (required for API calls)
find_package(CURL QUIET)

if(CURL_FOUND)
    target_link_libraries(DOOMLOADER_TONE3000 INTERFACE CURL::libcurl)
    target_compile_definitions(DOOMLOADER_TONE3000 
        INTERFACE 
        DOOMLOADER_TONE3000_ENABLED=1
        TONE3000_API_VERSION="${TONE3000_API_VERSION}"
        TONE3000_BASE_URL="${TONE3000_BASE_URL}"
    )
    message(STATUS "Tone3000 API integration enabled with cURL")
else()
    # Fallback: disable Tone3000 integration
    target_compile_definitions(DOOMLOADER_TONE3000 
        INTERFACE 
        DOOMLOADER_NO_TONE3000=1
    )
    message(WARNING "cURL not found. Tone3000 API integration will be disabled.")
endif()

# Check for JSON library (nlohmann/json)
include(FetchContent)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.3
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(nlohmann_json)

if(TARGET nlohmann_json::nlohmann_json)
    target_link_libraries(DOOMLOADER_TONE3000 INTERFACE nlohmann_json::nlohmann_json)
    target_compile_definitions(DOOMLOADER_TONE3000 INTERFACE DOOMLOADER_HAS_JSON=1)
endif()

# Tone3000 API features
target_compile_definitions(DOOMLOADER_TONE3000 
    INTERFACE
    TONE3000_PRESET_SYNC=1
    TONE3000_CLOUD_MODELS=1
    TONE3000_USER_PROFILES=1
)

# Function to add Tone3000 support to targets
function(doomloader_add_tone3000_support target_name)
    target_link_libraries(${target_name} PRIVATE DOOMLOADER_TONE3000)
    
    # Add API key configuration (to be set at runtime)
    target_compile_definitions(${target_name}
        PRIVATE
        DOOMLOADER_ENABLE_TONE3000_SYNC=1
    )
endfunction()

message(STATUS "Tone3000 API configured for DOOMLOADER")