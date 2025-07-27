# Basic DOOMLOADER Example

This example demonstrates the basic usage of DOOMLOADER's core functionality.

add_executable(BasicExample main.cpp)
target_link_libraries(BasicExample PRIVATE DoomloaderCore)
doomloader_add_juce_target(BasicExample)

# Set properties
set_target_properties(BasicExample PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)