cmake_minimum_required(VERSION 3.20)

project(DOOMLOADER VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Platform detection
if(APPLE)
    set(DOOMLOADER_APPLE TRUE)
    if(IOS)
        set(DOOMLOADER_IOS TRUE)
    else()
        set(DOOMLOADER_MACOS TRUE)
    endif()
elseif(ANDROID)
    set(DOOMLOADER_ANDROID TRUE)
elseif(WIN32)
    set(DOOMLOADER_WINDOWS TRUE)
else()
    set(DOOMLOADER_LINUX TRUE)
endif()

# Build options
option(DOOMLOADER_BUILD_PLUGIN "Build audio plugin formats" ON)
option(DOOMLOADER_BUILD_STANDALONE "Build standalone application" ON)
option(DOOMLOADER_BUILD_EXAMPLES "Build example projects" ON)
option(DOOMLOADER_ENABLE_TESTING "Enable testing" OFF)

# Include custom CMake modules
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Find dependencies
find_package(PkgConfig)

# JUCE Framework
include(cmake/SetupJUCE.cmake)

# NeuralAmpModelerCore
include(cmake/SetupNAM.cmake)

# Tone3000 API
include(cmake/SetupTone3000.cmake)

# Source directories
add_subdirectory(src)

# Examples (optional)
if(DOOMLOADER_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Testing (optional)
if(DOOMLOADER_ENABLE_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# Installation
include(cmake/Install.cmake)

# Package configuration
include(cmake/Package.cmake)