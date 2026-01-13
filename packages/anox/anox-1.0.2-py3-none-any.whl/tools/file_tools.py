"""File operations tool implementation."""

from __future__ import annotations

import os
import glob
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.base_tool import Tool


class FileTools(Tool):
    """
    Tool for file system operations.
    
    Provides safe file read, write, list, and search operations.
    All paths are validated to prevent directory traversal attacks.
    """
    
    tool_id = "file_tools"
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize FileTools.
        
        Args:
            workspace_root: Root directory for file operations (defaults to cwd)
        """
        self.workspace_root = Path(workspace_root or os.getcwd()).resolve()
    
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute file operation based on payload.
        
        Args:
            payload: Dictionary with:
                - operation: str (read, write, list, search, exists)
                - path: str (file or directory path)
                - content: str (for write operations)
                - pattern: str (for search operations)
                
        Returns:
            Dictionary with operation result
        """
        operation = payload.get("operation")
        
        if operation == "read":
            return self.read_file(payload["path"])
        elif operation == "write":
            return self.write_file(payload["path"], payload["content"])
        elif operation == "list":
            return self.list_directory(payload.get("path", "."))
        elif operation == "search":
            return self.search_files(payload["pattern"], payload.get("path", "."))
        elif operation == "exists":
            return self.check_exists(payload["path"])
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
            }
    
    def _validate_path(self, path: str) -> Path:
        """
        Validate and resolve path within workspace.
        
        Args:
            path: Relative or absolute path
            
        Returns:
            Resolved Path object
            
        Raises:
            ValueError: If path escapes workspace
        """
        # Convert to absolute path
        if os.path.isabs(path):
            resolved = Path(path).resolve()
        else:
            resolved = (self.workspace_root / path).resolve()
        
        # Ensure path is within workspace
        try:
            resolved.relative_to(self.workspace_root)
        except ValueError:
            raise ValueError(f"Path escapes workspace: {path}")
        
        return resolved
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read file contents.
        
        Args:
            path: File path
            
        Returns:
            Dictionary with success status and content or error
        """
        try:
            file_path = self._validate_path(path)
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {path}",
                }
            
            if not file_path.is_file():
                return {
                    "success": False,
                    "error": f"Not a file: {path}",
                }
            
            # Read with UTF-8, fallback to binary
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = file_path.read_bytes().decode("utf-8", errors="replace")
            
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "content": content,
                "size": file_path.stat().st_size,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to file.
        
        Args:
            path: File path
            content: Content to write
            
        Returns:
            Dictionary with success status
        """
        try:
            file_path = self._validate_path(path)
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            file_path.write_text(content, encoding="utf-8")
            
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "size": file_path.stat().st_size,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def list_directory(self, path: str = ".") -> Dict[str, Any]:
        """
        List directory contents.
        
        Args:
            path: Directory path (defaults to workspace root)
            
        Returns:
            Dictionary with files and directories
        """
        try:
            dir_path = self._validate_path(path)
            
            if not dir_path.exists():
                return {
                    "success": False,
                    "error": f"Directory not found: {path}",
                }
            
            if not dir_path.is_dir():
                return {
                    "success": False,
                    "error": f"Not a directory: {path}",
                }
            
            # List contents
            files = []
            directories = []
            
            for item in dir_path.iterdir():
                relative_path = str(item.relative_to(self.workspace_root))
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": relative_path,
                        "size": item.stat().st_size,
                    })
                elif item.is_dir():
                    directories.append({
                        "name": item.name,
                        "path": relative_path,
                    })
            
            return {
                "success": True,
                "path": str(dir_path.relative_to(self.workspace_root)),
                "files": files,
                "directories": directories,
                "total_files": len(files),
                "total_directories": len(directories),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def search_files(self, pattern: str, path: str = ".") -> Dict[str, Any]:
        """
        Search for files matching pattern.
        
        Args:
            pattern: Glob pattern (e.g., "*.py", "**/*.js")
            path: Directory to search in
            
        Returns:
            Dictionary with matching files
        """
        try:
            search_path = self._validate_path(path)
            
            if not search_path.exists():
                return {
                    "success": False,
                    "error": f"Directory not found: {path}",
                }
            
            # Search using glob
            matches = []
            for match in search_path.glob(pattern):
                if match.is_file():
                    try:
                        relative_path = str(match.relative_to(self.workspace_root))
                        matches.append({
                            "name": match.name,
                            "path": relative_path,
                            "size": match.stat().st_size,
                        })
                    except ValueError:
                        # Skip files outside workspace
                        continue
            
            return {
                "success": True,
                "pattern": pattern,
                "search_path": str(search_path.relative_to(self.workspace_root)),
                "matches": matches,
                "count": len(matches),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def check_exists(self, path: str) -> Dict[str, Any]:
        """
        Check if file or directory exists.
        
        Args:
            path: File or directory path
            
        Returns:
            Dictionary with existence status
        """
        try:
            file_path = self._validate_path(path)
            
            exists = file_path.exists()
            is_file = file_path.is_file() if exists else False
            is_dir = file_path.is_dir() if exists else False
            
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "exists": exists,
                "is_file": is_file,
                "is_directory": is_dir,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
