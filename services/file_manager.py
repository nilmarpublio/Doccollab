"""
File Manager
Manages file operations for LaTeX projects
"""

import os
import shutil
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class FileManager:
    """Manage files and directories for LaTeX projects"""
    
    def __init__(self, base_path: str):
        """
        Initialize FileManager
        
        Args:
            base_path: Base directory for file operations
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def list_files(self, directory: Optional[str] = None, pattern: str = "*") -> List[Dict[str, any]]:
        """
        List files in a directory
        
        Args:
            directory: Directory to list (relative to base_path)
            pattern: File pattern to match (e.g., "*.tex")
            
        Returns:
            List of file info dictionaries
        """
        if directory:
            target_dir = self.base_path / directory
        else:
            target_dir = self.base_path
        
        if not target_dir.exists():
            return []
        
        files = []
        for item in target_dir.glob(pattern):
            files.append({
                'name': item.name,
                'path': str(item.relative_to(self.base_path)),
                'is_dir': item.is_dir(),
                'size': item.stat().st_size if item.is_file() else 0,
                'modified': item.stat().st_mtime
            })
        
        return sorted(files, key=lambda x: (not x['is_dir'], x['name']))
    
    def create_directory(self, directory: str) -> bool:
        """
        Create a directory
        
        Args:
            directory: Directory path (relative to base_path)
            
        Returns:
            True if successful
        """
        try:
            target_dir = self.base_path / directory
            target_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def create_file(self, filepath: str, content: str = "") -> bool:
        """
        Create a file
        
        Args:
            filepath: File path (relative to base_path)
            content: Initial content
            
        Returns:
            True if successful
        """
        try:
            target_file = self.base_path / filepath
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def read_file(self, filepath: str) -> Optional[str]:
        """
        Read file content
        
        Args:
            filepath: File path (relative to base_path)
            
        Returns:
            File content or None
        """
        try:
            target_file = self.base_path / filepath
            if target_file.exists() and target_file.is_file():
                return target_file.read_text(encoding='utf-8')
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def write_file(self, filepath: str, content: str) -> bool:
        """
        Write content to file
        
        Args:
            filepath: File path (relative to base_path)
            content: Content to write
            
        Returns:
            True if successful
        """
        try:
            target_file = self.base_path / filepath
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """
        Delete a file
        
        Args:
            filepath: File path (relative to base_path)
            
        Returns:
            True if successful
        """
        try:
            target_file = self.base_path / filepath
            if target_file.exists() and target_file.is_file():
                target_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def delete_directory(self, directory: str, recursive: bool = False) -> bool:
        """
        Delete a directory
        
        Args:
            directory: Directory path (relative to base_path)
            recursive: If True, delete non-empty directories
            
        Returns:
            True if successful
        """
        try:
            target_dir = self.base_path / directory
            if target_dir.exists() and target_dir.is_dir():
                if recursive:
                    shutil.rmtree(target_dir)
                else:
                    target_dir.rmdir()  # Only works if empty
                return True
            return False
        except Exception as e:
            print(f"Error deleting directory: {e}")
            return False
    
    def rename(self, old_path: str, new_name: str) -> bool:
        """
        Rename a file or directory
        
        Args:
            old_path: Current path (relative to base_path)
            new_name: New name (not full path)
            
        Returns:
            True if successful
        """
        try:
            old_file = self.base_path / old_path
            new_file = old_file.parent / new_name
            
            if old_file.exists():
                old_file.rename(new_file)
                return True
            return False
        except Exception as e:
            print(f"Error renaming: {e}")
            return False
    
    def move(self, source: str, destination: str) -> bool:
        """
        Move a file or directory
        
        Args:
            source: Source path (relative to base_path)
            destination: Destination path (relative to base_path)
            
        Returns:
            True if successful
        """
        try:
            source_path = self.base_path / source
            dest_path = self.base_path / destination
            
            if source_path.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_path), str(dest_path))
                return True
            return False
        except Exception as e:
            print(f"Error moving: {e}")
            return False
    
    def copy(self, source: str, destination: str) -> bool:
        """
        Copy a file or directory
        
        Args:
            source: Source path (relative to base_path)
            destination: Destination path (relative to base_path)
            
        Returns:
            True if successful
        """
        try:
            source_path = self.base_path / source
            dest_path = self.base_path / destination
            
            if source_path.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                if source_path.is_dir():
                    shutil.copytree(str(source_path), str(dest_path))
                else:
                    shutil.copy2(str(source_path), str(dest_path))
                return True
            return False
        except Exception as e:
            print(f"Error copying: {e}")
            return False
    
    def get_file_info(self, filepath: str) -> Optional[Dict[str, any]]:
        """
        Get detailed file information
        
        Args:
            filepath: File path (relative to base_path)
            
        Returns:
            Dictionary with file info or None
        """
        try:
            target_file = self.base_path / filepath
            if target_file.exists():
                stat = target_file.stat()
                return {
                    'name': target_file.name,
                    'path': str(target_file.relative_to(self.base_path)),
                    'is_dir': target_file.is_dir(),
                    'size': stat.st_size,
                    'created': stat.st_ctime,
                    'modified': stat.st_mtime,
                    'accessed': stat.st_atime
                }
            return None
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def search_files(self, pattern: str, directory: Optional[str] = None) -> List[str]:
        """
        Search for files matching a pattern
        
        Args:
            pattern: Search pattern (e.g., "*.tex")
            directory: Directory to search in (relative to base_path)
            
        Returns:
            List of matching file paths
        """
        if directory:
            search_dir = self.base_path / directory
        else:
            search_dir = self.base_path
        
        if not search_dir.exists():
            return []
        
        matches = []
        for item in search_dir.rglob(pattern):
            if item.is_file():
                matches.append(str(item.relative_to(self.base_path)))
        
        return sorted(matches)
