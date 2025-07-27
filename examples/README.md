# DOOMLOADER Examples

## Build Examples
```bash
cmake -B build -DDOOMLOADER_BUILD_EXAMPLES=ON
cmake --build build --config Release
```

## Run Examples
```bash
# Basic example
./build/examples/basic/BasicExample

# Plugin example (if built)
./build/examples/plugin/PluginExample
```

## Examples Overview

- **basic/**: Core functionality demonstration
- **plugin/**: Audio plugin development example
- **mobile/**: Mobile-specific implementations
- **advanced/**: Complex processing scenarios