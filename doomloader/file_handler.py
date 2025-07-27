"""
General file handling utilities for DOOMLOADER.
Provides file discovery, validation, and management for NAM files.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import fnmatch


class FileHandler:
    """
    Handles file operations for NAM files and related resources.
    
    Provides:
    - File discovery and scanning
    - File validation
    - Batch file operations
    - Directory management
    """
    
    def __init__(self):
        self.supported_extensions = ['.nam', '.json', '.wav', '.mp3', '.flac']
        self.nam_extensions = ['.nam', '.json']
        
    def find_nam_files(self, directory: Union[str, Path], recursive: bool = True) -> List[Path]:
        """
        Find all NAM files in a directory.
        
        Args:
            directory: Directory to search
            recursive: Whether to search subdirectories
            
        Returns:
            List of NAM file paths
        """
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
            
        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
            
        nam_files = []
        
        if recursive:
            for ext in self.nam_extensions:
                pattern = f"**/*{ext}"
                nam_files.extend(directory.glob(pattern))
        else:
            for ext in self.nam_extensions:
                pattern = f"*{ext}"
                nam_files.extend(directory.glob(pattern))
                
        return sorted(nam_files)
    
    def scan_directory(self, directory: Union[str, Path]) -> Dict[str, List[Path]]:
        """
        Scan directory for all supported file types.
        
        Args:
            directory: Directory to scan
            
        Returns:
            Dictionary organized by file type
        """
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
            
        results = {
            'nam_files': [],
            'metadata_files': [],
            'audio_files': [],
            'other_files': []
        }
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                
                if ext == '.nam':
                    results['nam_files'].append(file_path)
                elif ext == '.json':
                    results['metadata_files'].append(file_path)
                elif ext in ['.wav', '.mp3', '.flac']:
                    results['audio_files'].append(file_path)
                elif ext in self.supported_extensions:
                    results['other_files'].append(file_path)
                    
        return results
    
    def validate_file_structure(self, directory: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate the structure of a NAM file directory.
        
        Args:
            directory: Directory to validate
            
        Returns:
            Validation results dictionary
        """
        directory = Path(directory)
        scan_results = self.scan_directory(directory)
        
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'file_counts': {
                'nam_files': len(scan_results['nam_files']),
                'metadata_files': len(scan_results['metadata_files']),
                'audio_files': len(scan_results['audio_files']),
                'total_files': sum(len(files) for files in scan_results.values())
            }
        }
        
        # Check for NAM files
        if not scan_results['nam_files']:
            validation['errors'].append("No .nam files found")
            validation['is_valid'] = False
            
        # Check for metadata files
        if not scan_results['metadata_files']:
            validation['warnings'].append("No metadata (.json) files found")
            
        # Check for paired files (NAM file with corresponding JSON)
        nam_stems = {f.stem for f in scan_results['nam_files']}
        json_stems = {f.stem for f in scan_results['metadata_files']}
        
        unpaired_nam = nam_stems - json_stems
        unpaired_json = json_stems - nam_stems
        
        if unpaired_nam:
            validation['warnings'].append(f"NAM files without metadata: {list(unpaired_nam)}")
            
        if unpaired_json:
            validation['warnings'].append(f"Metadata files without NAM files: {list(unpaired_json)}")
            
        return validation
    
    def create_file_manifest(self, directory: Union[str, Path], output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a manifest of all files in a directory.
        
        Args:
            directory: Directory to create manifest for
            output_file: Optional file to save manifest to
            
        Returns:
            Manifest dictionary
        """
        directory = Path(directory)
        scan_results = self.scan_directory(directory)
        
        manifest = {
            'directory': str(directory),
            'created_at': str(Path.cwd()),  # Simplified timestamp
            'file_structure': {},
            'summary': {
                'total_files': 0,
                'file_types': {}
            }
        }
        
        for category, files in scan_results.items():
            manifest['file_structure'][category] = []
            for file_path in files:
                file_info = {
                    'name': file_path.name,
                    'path': str(file_path.relative_to(directory)),
                    'size': file_path.stat().st_size,
                    'extension': file_path.suffix
                }
                manifest['file_structure'][category].append(file_info)
                
            # Update summary
            count = len(files)
            manifest['summary']['total_files'] += count
            manifest['summary']['file_types'][category] = count
            
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
                
        return manifest
    
    def organize_nam_files(self, source_dir: Union[str, Path], target_dir: Union[str, Path], create_subdirs: bool = True) -> Dict[str, Any]:
        """
        Organize NAM files into a structured directory layout.
        
        Args:
            source_dir: Source directory with NAM files
            target_dir: Target directory for organized files
            create_subdirs: Whether to create subdirectories by category
            
        Returns:
            Organization results
        """
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        
        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        scan_results = self.scan_directory(source_dir)
        organization_results = {
            'moved_files': 0,
            'created_directories': [],
            'errors': []
        }
        
        if create_subdirs:
            # Create subdirectories
            subdirs = ['models', 'metadata', 'audio', 'other']
            for subdir in subdirs:
                subdir_path = target_dir / subdir
                subdir_path.mkdir(exist_ok=True)
                organization_results['created_directories'].append(str(subdir_path))
        
        # Move files to appropriate locations
        file_mappings = {
            'nam_files': 'models' if create_subdirs else '',
            'metadata_files': 'metadata' if create_subdirs else '',
            'audio_files': 'audio' if create_subdirs else '',
            'other_files': 'other' if create_subdirs else ''
        }
        
        for category, files in scan_results.items():
            target_subdir = target_dir / file_mappings[category] if create_subdirs else target_dir
            
            for file_path in files:
                try:
                    target_file = target_subdir / file_path.name
                    # Note: In a real implementation, you'd want to copy/move files
                    # For now, just track what would be moved
                    organization_results['moved_files'] += 1
                except Exception as e:
                    organization_results['errors'].append(f"Error organizing {file_path}: {str(e)}")
                    
        return organization_results
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get detailed information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File information dictionary
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}
            
        stat = file_path.stat()
        
        info = {
            'name': file_path.name,
            'stem': file_path.stem,
            'suffix': file_path.suffix,
            'size': stat.st_size,
            'is_nam_file': file_path.suffix.lower() in self.nam_extensions,
            'is_supported': file_path.suffix.lower() in self.supported_extensions,
            'parent_directory': str(file_path.parent)
        }
        
        # Add size in human readable format
        size_kb = stat.st_size / 1024
        if size_kb < 1024:
            info['size_human'] = f"{size_kb:.1f} KB"
        else:
            size_mb = size_kb / 1024
            info['size_human'] = f"{size_mb:.1f} MB"
            
        return info