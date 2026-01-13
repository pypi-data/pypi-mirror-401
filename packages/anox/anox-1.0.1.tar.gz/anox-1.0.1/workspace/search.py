"""Search - Project-wide search functionality."""

import re
from pathlib import Path
from typing import List, Optional, Dict, Any


class Search:
    """Search component for finding content across project files."""
    
    def __init__(self, root_path: Path):
        """Initialize search.
        
        Args:
            root_path: Workspace root directory.
        """
        self.root_path = root_path
        self._ignored_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build'
        }
    
    def search(self, query: str, file_pattern: Optional[str] = None,
               case_sensitive: bool = False, use_regex: bool = False,
               max_results: int = 1000) -> List[Dict[str, Any]]:
        """Search for query in project files.
        
        Args:
            query: Search query string.
            file_pattern: Optional glob pattern (e.g., '*.py', '**/*.js').
            case_sensitive: Whether search is case-sensitive.
            use_regex: Whether query is a regular expression.
            max_results: Maximum number of results to return.
            
        Returns:
            List of search results with file, line number, and context.
        """
        results = []
        
        # Compile search pattern
        if use_regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            try:
                pattern = re.compile(query, flags)
            except re.error:
                return [{'error': f'Invalid regex pattern: {query}'}]
        else:
            flags = 0 if case_sensitive else re.IGNORECASE
            escaped_query = re.escape(query)
            pattern = re.compile(escaped_query, flags)
        
        # Determine files to search
        if file_pattern:
            files = list(self.root_path.glob(file_pattern))
        else:
            files = list(self.root_path.rglob('*'))
        
        # Search each file
        for file_path in files:
            if len(results) >= max_results:
                break
            
            # Skip directories and ignored paths
            if not file_path.is_file() or self._should_ignore(file_path):
                continue
            
            # Try to read file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except (UnicodeDecodeError, PermissionError, OSError):
                continue
            
            # Search in file
            for line_num, line in enumerate(lines, start=1):
                if len(results) >= max_results:
                    break
                
                match = pattern.search(line)
                if match:
                    results.append({
                        'file': str(file_path.relative_to(self.root_path)),
                        'line': line_num,
                        'column': match.start() + 1,
                        'content': line.rstrip(),
                        'match': match.group(0),
                        'context_before': self._get_context(lines, line_num - 2, line_num - 1),
                        'context_after': self._get_context(lines, line_num, line_num + 1),
                    })
        
        return results
    
    def search_files_by_name(self, name_pattern: str, 
                             case_sensitive: bool = False) -> List[str]:
        """Search for files by name pattern.
        
        Args:
            name_pattern: File name pattern (glob or regex).
            case_sensitive: Whether search is case-sensitive.
            
        Returns:
            List of matching file paths.
        """
        results = []
        
        # Try glob pattern first
        try:
            files = list(self.root_path.rglob(name_pattern))
            for file_path in files:
                if file_path.is_file() and not self._should_ignore(file_path):
                    results.append(str(file_path.relative_to(self.root_path)))
            return results
        except ValueError:
            # If glob fails, use regex
            pass
        
        # Use regex matching
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            pattern = re.compile(name_pattern, flags)
        except re.error:
            return []
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                if pattern.search(file_path.name):
                    results.append(str(file_path.relative_to(self.root_path)))
        
        return results
    
    def search_replace(self, query: str, replacement: str,
                      file_pattern: Optional[str] = None,
                      case_sensitive: bool = False,
                      use_regex: bool = False,
                      dry_run: bool = True) -> Dict[str, Any]:
        """Search and replace across files.
        
        Args:
            query: Search query string.
            replacement: Replacement string.
            file_pattern: Optional glob pattern.
            case_sensitive: Whether search is case-sensitive.
            use_regex: Whether query is a regex pattern.
            dry_run: If True, don't actually modify files.
            
        Returns:
            Dictionary with results and modified files.
        """
        # Find all matches first
        matches = self.search(query, file_pattern, case_sensitive, use_regex)
        
        if dry_run:
            return {
                'matches': len(matches),
                'files_affected': len(set(m['file'] for m in matches)),
                'dry_run': True,
                'preview': matches[:10]  # Preview first 10 matches
            }
        
        # Perform actual replacement
        files_modified = {}
        
        for file_rel_path in set(m['file'] for m in matches):
            file_path = self.root_path / file_rel_path
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = query if use_regex else re.escape(query)
                new_content = re.sub(
                    pattern,
                    replacement,
                    content,
                    flags=flags
                )
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified[file_rel_path] = True
            except (OSError, PermissionError):
                files_modified[file_rel_path] = False
        
        return {
            'matches': len(matches),
            'files_affected': len(files_modified),
            'files_modified': files_modified,
            'dry_run': False
        }
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored in search.
        
        Args:
            path: Path to check.
            
        Returns:
            True if path should be ignored.
        """
        # Check if any parent directory is in ignored list
        for parent in path.parents:
            if parent.name in self._ignored_dirs:
                return True
        
        return path.name.startswith('.')
    
    def _get_context(self, lines: List[str], start: int, end: int) -> List[str]:
        """Get context lines from file.
        
        Args:
            lines: All file lines.
            start: Start line number (0-indexed).
            end: End line number (0-indexed, exclusive).
            
        Returns:
            List of context lines.
        """
        start = max(0, start)
        end = min(len(lines), end)
        return [line.rstrip() for line in lines[start:end]]
