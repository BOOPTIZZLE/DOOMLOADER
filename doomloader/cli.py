"""
Command-line interface for DOOMLOADER.
"""

import argparse
import sys
from pathlib import Path
import json

from doomloader import NAMLoader, AmpSimulator, FileHandler


def cmd_scan(args):
    """Scan directory for NAM files."""
    file_handler = FileHandler()
    
    try:
        scan_results = file_handler.scan_directory(args.directory)
        
        print(f"Scanning directory: {args.directory}")
        print("=" * 50)
        
        total_files = sum(len(files) for files in scan_results.values())
        print(f"Total files found: {total_files}")
        
        for category, files in scan_results.items():
            if files:
                print(f"\n{category.replace('_', ' ').title()}: {len(files)}")
                for file_path in files:
                    file_info = file_handler.get_file_info(file_path)
                    print(f"  - {file_info['name']} ({file_info['size_human']})")
        
        if args.validate:
            print(f"\nValidation Results:")
            validation = file_handler.validate_file_structure(args.directory)
            print(f"Valid structure: {validation['is_valid']}")
            
            if validation['warnings']:
                print("Warnings:")
                for warning in validation['warnings']:
                    print(f"  - {warning}")
                    
            if validation['errors']:
                print("Errors:")
                for error in validation['errors']:
                    print(f"  - {error}")
                    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_info(args):
    """Show information about a NAM file."""
    nam_loader = NAMLoader()
    
    try:
        model_data = nam_loader.load_nam_file(args.file)
        model_info = nam_loader.get_model_info(model_data)
        
        print(f"NAM File Information: {args.file}")
        print("=" * 50)
        
        for key, value in model_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        if args.detailed and 'raw_data' not in model_data:
            print(f"\nDetailed Model Data:")
            for key, value in model_data.items():
                if key not in ['raw_data']:
                    print(f"  {key}: {value}")
                    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def cmd_simulate(args):
    """Run amp simulation with a NAM file."""
    import numpy as np
    
    amp_sim = AmpSimulator(sample_rate=args.sample_rate)
    
    try:
        # Load NAM model
        model_name = amp_sim.load_nam_model(args.model)
        print(f"Loaded NAM model: {model_name}")
        
        # Set parameters
        if hasattr(args, 'gain') and args.gain is not None:
            amp_sim.set_parameters(gain=args.gain)
        if hasattr(args, 'tone') and args.tone is not None:
            amp_sim.set_parameters(tone=args.tone)
        if hasattr(args, 'volume') and args.volume is not None:
            amp_sim.set_parameters(volume=args.volume)
            
        params = amp_sim.get_parameters()
        print(f"Amp parameters: {params}")
        
        # Generate test signal
        duration = 1.0
        frequency = 440.0
        t = np.linspace(0, duration, int(args.sample_rate * duration))
        test_audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Process audio
        processed_audio = amp_sim.process_audio(test_audio)
        
        print(f"Processed {len(test_audio)} samples")
        print(f"Input RMS: {np.sqrt(np.mean(test_audio**2)):.4f}")
        print(f"Output RMS: {np.sqrt(np.mean(processed_audio**2)):.4f}")
        
        sim_info = amp_sim.get_simulation_info()
        print(f"Simulation info: {sim_info}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="DOOMLOADER - NAM File Support Tool")
    parser.add_argument("--version", action="version", version="DOOMLOADER 1.0.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan directory for NAM files")
    scan_parser.add_argument("directory", help="Directory to scan")
    scan_parser.add_argument("--validate", action="store_true", help="Validate file structure")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show NAM file information")
    info_parser.add_argument("file", help="NAM file to analyze")
    info_parser.add_argument("--detailed", action="store_true", help="Show detailed information")
    
    # Simulate command
    sim_parser = subparsers.add_parser("simulate", help="Run amp simulation")
    sim_parser.add_argument("model", help="NAM model file")
    sim_parser.add_argument("--sample-rate", type=int, default=44100, help="Sample rate (default: 44100)")
    sim_parser.add_argument("--gain", type=float, help="Gain parameter (0.0-1.0)")
    sim_parser.add_argument("--tone", type=float, help="Tone parameter (0.0-1.0)")
    sim_parser.add_argument("--volume", type=float, help="Volume parameter (0.0-1.0)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "scan":
        return cmd_scan(args)
    elif args.command == "info":
        return cmd_info(args)
    elif args.command == "simulate":
        return cmd_simulate(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())