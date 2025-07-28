"""
DOOMLOADER Basic Usage Example

This example demonstrates basic usage of the DOOMLOADER library.
"""

from doomloader import AudioLoader, AudioProcessor


def main():
    """Demonstrate basic DOOMLOADER functionality."""
    print("🎵 DOOMLOADER Example")
    print("=" * 40)
    
    # Initialize components
    loader = AudioLoader()
    processor = AudioProcessor()
    
    # Show supported formats
    print("\nSupported audio formats:")
    for fmt in loader.get_supported_formats():
        print(f"  - {fmt}")
    
    # Show available effects  
    print("\nAvailable effects:")
    for effect in processor.get_available_effects():
        print(f"  - {effect}")
    
    # Example processing chain setup
    print("\nSetting up effect chain...")
    processor.add_effect('reverb', {'room_size': 0.8})
    processor.add_effect('delay', {'time': 0.3, 'feedback': 0.4})
    
    print("Effect chain:")
    for effect in processor.get_effect_chain():
        print(f"  - {effect['name']}: {effect['parameters']}")
    
    # Note about actual file processing
    print(f"\nNote: To process actual audio files, use:")
    print(f"  audio_data = loader.load('path/to/your/audio.wav')")
    print(f"  processed_audio = processor.process(audio_data)")
    print(f"\n⚠️  Currently in alpha - actual audio processing not yet implemented!")


if __name__ == "__main__":
    main()