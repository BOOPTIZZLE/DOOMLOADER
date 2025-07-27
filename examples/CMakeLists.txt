# Examples CMakeLists.txt

# Basic example
add_subdirectory(basic)

# Plugin example (if plugins are enabled)
if(DOOMLOADER_BUILD_PLUGIN)
    # add_subdirectory(plugin)
endif()

# Mobile examples (if mobile platforms detected)
if(DOOMLOADER_IOS OR DOOMLOADER_ANDROID)
    # add_subdirectory(mobile)
endif()