# Installation configuration for DOOMLOADER

include(GNUInstallDirs)

# Install directories
set(DOOMLOADER_INSTALL_BINDIR ${CMAKE_INSTALL_BINDIR})
set(DOOMLOADER_INSTALL_LIBDIR ${CMAKE_INSTALL_LIBDIR})
set(DOOMLOADER_INSTALL_INCLUDEDIR ${CMAKE_INSTALL_INCLUDEDIR}/doomloader)
set(DOOMLOADER_INSTALL_DATADIR ${CMAKE_INSTALL_DATADIR}/doomloader)

# Platform-specific plugin directories
if(DOOMLOADER_APPLE)
    set(DOOMLOADER_VST3_INSTALL_DIR "~/Library/Audio/Plug-Ins/VST3")
    set(DOOMLOADER_AU_INSTALL_DIR "~/Library/Audio/Plug-Ins/Components")
elseif(DOOMLOADER_WINDOWS)
    set(DOOMLOADER_VST3_INSTALL_DIR "$ENV{COMMONPROGRAMFILES}/VST3")
else()
    set(DOOMLOADER_VST3_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/vst3")
endif()

# Install presets and impulse responses
install(DIRECTORY ${CMAKE_SOURCE_DIR}/presets/
    DESTINATION ${DOOMLOADER_INSTALL_DATADIR}/presets
    FILES_MATCHING PATTERN "*.json"
)

install(DIRECTORY ${CMAKE_SOURCE_DIR}/impulse_responses/examples/
    DESTINATION ${DOOMLOADER_INSTALL_DATADIR}/impulse_responses
    FILES_MATCHING PATTERN "*.wav"
)

# Install documentation
install(FILES 
    ${CMAKE_SOURCE_DIR}/README.md
    ${CMAKE_SOURCE_DIR}/LICENSE
    DESTINATION ${DOOMLOADER_INSTALL_DATADIR}/docs
)

install(DIRECTORY ${CMAKE_SOURCE_DIR}/docs/
    DESTINATION ${DOOMLOADER_INSTALL_DATADIR}/docs
    FILES_MATCHING PATTERN "*.md"
)

# Create uninstall target
if(NOT TARGET uninstall)
    configure_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
        IMMEDIATE @ONLY
    )

    add_custom_target(uninstall
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
    )
endif()