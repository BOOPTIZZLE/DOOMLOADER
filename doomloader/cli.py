"""
Command-line interface for DOOMLOADER

Provides basic CLI functionality for audio processing.
"""

import argparse
import sys
from .loader import AudioLoader
from .processor import AudioProcessor


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DOOMLOADER - Audio file loader and processor"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="DOOMLOADER 0.1.0-alpha"
    )
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Check if DOOMLOADER is ready for use"
    )
    parser.add_argument(
        "--formats", 
        action="store_true",
        help="List supported audio formats"
    )
    parser.add_argument(
        "--effects", 
        action="store_true",
        help="List available audio effects"
    )
    
    args = parser.parse_args()
    
    if args.check:
        print("🚧 DOOMLOADER Status: Alpha Development")
        print("✅ Basic structure: Ready")
        print("✅ Core modules: Ready") 
        print("⏳ Audio processing: In development")
        print("❌ Production features: Not ready")
        print("\nOverall: Not ready for production use, but basic framework is in place.")
        return
    
    if args.formats:
        loader = AudioLoader()
        formats = loader.get_supported_formats()
        print("Supported audio formats:")
        for fmt in formats:
            print(f"  - {fmt}")
        return
    
    if args.effects:
        processor = AudioProcessor()
        effects = processor.get_available_effects()
        print("Available audio effects:")
        for effect in effects:
            print(f"  - {effect}")
        return
    
    # Default behavior - show help
    parser.print_help()


if __name__ == "__main__":
    main()