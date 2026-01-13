"""File Explorer - VS Code-style file browsing."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any


class FileExplorer:
    """File explorer that shows all real files under workspace root."""
    
    def __init__(self, root_path: Path):
        """Initialize file explorer.
        
        Args:
            root_path: Workspace root directory.
        """
        self.root_path = root_path
        self._ignored_patterns = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build',
            '*.pyc', '*.pyo', '*.egg-info', '.DS_Store'
        }
    
    def list_files(self, path: Optional[str] = None, recursive: bool = False) -> List[Dict[str, Any]]:
        """List files in the given path.
        
        Args:
            path: Relative path within workspace. Defaults to root.
            recursive: Whether to list recursively.
            
        Returns:
            List of file/directory entries with metadata.
        """
        target_path = self.root_path / (path or "")
        
        if not target_path.exists():
            return []
        
        if not target_path.is_dir():
            # Return single file info
            return [self._get_file_info(target_path)]
        
        results = []
        
        if recursive:
            for item in target_path.rglob('*'):
                if not self._should_ignore(item):
                    results.append(self._get_file_info(item))
        else:
            for item in target_path.iterdir():
                if not self._should_ignore(item):
                    results.append(self._get_file_info(item))
        
        # Sort: directories first, then files
        results.sort(key=lambda x: (not x['is_directory'], x['name'].lower()))
        return results
    
    def get_file_tree(self, max_depth: int = 3) -> Dict[str, Any]:
        """Get hierarchical file tree structure.
        
        Args:
            max_depth: Maximum depth to traverse.
            
        Returns:
            Nested dictionary representing file tree.
        """
        def build_tree(path: Path, depth: int) -> Dict[str, Any]:
            if depth > max_depth or self._should_ignore(path):
                return None
            
            node = self._get_file_info(path)
            
            if path.is_dir():
                children = []
                try:
                    for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                        child = build_tree(item, depth + 1)
                        if child:
                            children.append(child)
                    node['children'] = children
                except PermissionError:
                    node['children'] = []
            
            return node
        
        return build_tree(self.root_path, 0)
    
    def _get_file_info(self, path: Path) -> Dict[str, Any]:
        """Get file/directory metadata.
        
        Args:
            path: Path to file or directory.
            
        Returns:
            Dictionary with file metadata.
        """
        try:
            stat = path.stat()
            relative_path = path.relative_to(self.root_path)
            
            return {
                'name': path.name,
                'path': str(relative_path),
                'absolute_path': str(path),
                'is_directory': path.is_dir(),
                'is_file': path.is_file(),
                'size': stat.st_size if path.is_file() else 0,
                'modified': stat.st_mtime,
                'extension': path.suffix if path.is_file() else None,
            }
        except (OSError, PermissionError):
            return {
                'name': path.name,
                'path': str(path.relative_to(self.root_path)),
                'absolute_path': str(path),
                'is_directory': path.is_dir(),
                'is_file': False,
                'size': 0,
                'modified': 0,
                'extension': None,
                'error': 'Permission denied or file not accessible'
            }
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored.
        
        Args:
            path: Path to check.
            
        Returns:
            True if path should be ignored.
        """
        name = path.name
        
        # Check exact matches
        if name in self._ignored_patterns:
            return True
        
        # Check pattern matches
        for pattern in self._ignored_patterns:
            if pattern.startswith('*') and name.endswith(pattern[1:]):
                return True
            if pattern.endswith('*') and name.startswith(pattern[:-1]):
                return True
        
        return False
    
    def sync_with_terminal(self, terminal_cwd: str) -> bool:
        """Sync file explorer view with terminal working directory.
        
        Args:
            terminal_cwd: Current working directory from terminal.
            
        Returns:
            True if sync successful.
        """
        try:
            cwd_path = Path(terminal_cwd).resolve()
            # Check if terminal cwd is within workspace
            cwd_path.relative_to(self.root_path)
            return True
        except (ValueError, OSError):
            return False
