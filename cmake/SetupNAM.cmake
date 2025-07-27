# Setup NeuralAmpModelerCore (NAM) for DOOMLOADER

# NAM provides neural network-based amp modeling
# This module handles fetching and configuring NAM

include(FetchContent)

# Fetch NeuralAmpModelerCore
FetchContent_Declare(
    NeuralAmpModelerCore
    GIT_REPOSITORY https://github.com/sdatkinson/NeuralAmpModelerCore.git
    GIT_TAG main
    GIT_SHALLOW TRUE
)

# NAM build options
set(NAM_BUILD_STATIC ON CACHE BOOL "Build NAM as static library")
set(NAM_SAMPLE_RATE 48000 CACHE STRING "Default sample rate for NAM")

FetchContent_MakeAvailable(NeuralAmpModelerCore)

# Create interface library for NAM integration
add_library(DOOMLOADER_NAM INTERFACE)

# NAM headers and library
if(TARGET NeuralAmpModelerCore)
    target_link_libraries(DOOMLOADER_NAM INTERFACE NeuralAmpModelerCore)
else()
    # Fallback: manual NAM setup
    find_path(NAM_INCLUDE_DIR 
        NAMES NAM.h
        PATHS ${CMAKE_CURRENT_SOURCE_DIR}/libs/NeuralAmpModelerCore/NAM
    )
    
    if(NAM_INCLUDE_DIR)
        target_include_directories(DOOMLOADER_NAM INTERFACE ${NAM_INCLUDE_DIR})
        message(STATUS "Found NAM headers at: ${NAM_INCLUDE_DIR}")
    else()
        message(WARNING "NAM not found. Neural amp modeling will be disabled.")
        target_compile_definitions(DOOMLOADER_NAM INTERFACE DOOMLOADER_NO_NAM=1)
    endif()
endif()

# NAM configuration for DOOMLOADER
target_compile_definitions(DOOMLOADER_NAM 
    INTERFACE 
    NAM_SAMPLE_RATE=${NAM_SAMPLE_RATE}
    DOOMLOADER_NAM_ENABLED=1
)

# Function to link NAM to DOOMLOADER targets
function(doomloader_add_nam_support target_name)
    target_link_libraries(${target_name} PRIVATE DOOMLOADER_NAM)
    
    # Add NAM model loading capabilities
    target_compile_definitions(${target_name}
        PRIVATE
        DOOMLOADER_ENABLE_NAM_MODELS=1
    )
endfunction()

message(STATUS "NeuralAmpModelerCore configured for DOOMLOADER")