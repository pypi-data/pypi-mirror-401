"""Editor - File editing with syntax highlighting and diff support."""

import os
import shutil
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List, Set
from threading import Thread, Event as ThreadEvent
import difflib
from .events import get_event_bus, EventType


class Editor:
    """Editor component for opening, editing, and saving files.
    
    Emits events when files are opened, saved, or closed so other
    components can stay synchronized.
    """
    
    # Encodings that are problematic and should not be preserved on save
    PROBLEMATIC_ENCODINGS = frozenset(['binary-utf8-replace'])
    
    # File size threshold for save verification (10MB)
    VERIFICATION_SIZE_THRESHOLD = 10 * 1024 * 1024
    
    def __init__(self, root_path: Path, emit_events: bool = True, auto_save_interval: float = 30.0):
        """Initialize editor.
        
        Args:
            root_path: Workspace root directory.
            emit_events: Whether to emit events to the event bus.
            auto_save_interval: Auto-save interval in seconds (default 30s).
        """
        self.root_path = root_path
        self._open_files: Dict[str, Dict[str, Any]] = {}
        self._emit_events = emit_events
        self._auto_save_enabled = False
        self._auto_save_interval = auto_save_interval
        self._unsaved_changes: Set[str] = set()
        self._auto_save_thread: Optional[Thread] = None
        self._auto_save_stop_event = ThreadEvent()
        
        if emit_events:
            self.event_bus = get_event_bus()
    
    def open_file(self, file_path: str) -> str:
        """Open a file for editing with robust encoding detection.
        
        Args:
            file_path: Path relative to workspace root.
            
        Returns:
            File content as string.
            
        Raises:
            FileNotFoundError: If file doesn't exist.
            PermissionError: If file is not readable.
            ValueError: If file encoding cannot be determined.
        """
        full_path = self._resolve_path(file_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not full_path.is_file():
            raise ValueError(f"Not a file: {file_path}")
        
        # Try multiple encodings in order of likelihood
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'ascii']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(full_path, 'r', encoding=encoding) as f:
                    content = f.read()
                used_encoding = encoding
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        # If all encodings fail, try binary with replacement
        if content is None:
            try:
                with open(full_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='replace')
                used_encoding = 'binary-utf8-replace'
                print(f"⚠️  Warning: {file_path} has encoding issues. Loaded with character replacement.")
            except Exception as e:
                raise ValueError(f"Cannot read file {file_path}: {e}")
        
        # Store original content and encoding for diff and save
        self._open_files[file_path] = {
            'path': str(full_path),
            'original_content': content,
            'modified': False,
            'encoding': used_encoding
        }
        
        # Emit file opened event
        if self._emit_events:
            self.event_bus.emit(
                EventType.FILE_OPENED,
                {'path': file_path, 'absolute_path': str(full_path), 'encoding': used_encoding},
                'editor'
            )
        
        return content
    
    def save_file(self, file_path: str, content: str, create_backup: bool = True, validate_text: bool = True, verify_save: bool = True) -> bool:
        """Save file content with comprehensive error handling and verification.
        
        Args:
            file_path: Path relative to workspace root.
            content: Content to save.
            create_backup: Whether to create backup before saving.
            validate_text: Whether to validate as text file (reject null bytes). Set False for binary.
            verify_save: Whether to verify saved content matches by computing checksum.
            
        Returns:
            True if successful.
            
        Raises:
            PermissionError: If file is not writable.
            ValueError: If content validation fails.
        """
        full_path = self._resolve_path(file_path)
        
        # Validate content before saving (if requested)
        if validate_text and not self._validate_content(file_path, content):
            raise ValueError(f"Content validation failed for {file_path}")
        
        # Determine encoding to use (prefer same as when opened)
        encoding = 'utf-8'
        if file_path in self._open_files:
            file_encoding = self._open_files[file_path].get('encoding', 'utf-8')
            # Use original encoding if it's not a problematic one
            if file_encoding not in self.PROBLEMATIC_ENCODINGS:
                encoding = file_encoding
        
        # Create parent directories if needed
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise PermissionError(f"Cannot create parent directory for {file_path}: {e}")
        
        # Create backup if file exists and backup is requested
        backup_path = None
        if create_backup and full_path.exists():
            backup_path = self._create_backup(full_path)
        
        # Compute checksum of content we're writing (if verification requested)
        # Note: MD5 is used for content verification only, not cryptographic security
        # It's fast and sufficient for detecting corruption/incomplete writes
        # Skip verification for very large files to avoid performance impact
        expected_hash = None
        content_size = len(content.encode(encoding))
        if verify_save and content_size <= self.VERIFICATION_SIZE_THRESHOLD:
            expected_hash = hashlib.md5(content.encode(encoding)).hexdigest()
        elif verify_save and content_size > self.VERIFICATION_SIZE_THRESHOLD:
            # Large file - skip verification for performance
            verify_save = False
        
        # Attempt to save with atomic write (write to temp, then rename)
        temp_path = full_path.with_suffix(full_path.suffix + '.tmp')
        try:
            # Write to temporary file first
            with open(temp_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # Verify write if requested
            if verify_save:
                with open(temp_path, 'r', encoding=encoding) as f:
                    written_content = f.read()
                actual_hash = hashlib.md5(written_content.encode(encoding)).hexdigest()
                
                if actual_hash != expected_hash:
                    raise ValueError(f"Save verification failed: content mismatch (expected {expected_hash}, got {actual_hash})")
            
            # Atomic rename
            shutil.move(str(temp_path), str(full_path))
            
            # Update tracking
            if file_path in self._open_files:
                self._open_files[file_path]['modified'] = False
                self._open_files[file_path]['original_content'] = content
            
            # Remove from unsaved changes
            self._unsaved_changes.discard(file_path)
            
            # Emit file saved event
            if self._emit_events:
                self.event_bus.emit(
                    EventType.FILE_SAVED,
                    {
                        'path': file_path,
                        'absolute_path': str(full_path),
                        'size': len(content),
                        'encoding': encoding,
                        'verified': verify_save
                    },
                    'editor'
                )
            
            # Clean up backup if everything succeeded
            if backup_path and backup_path.exists():
                try:
                    backup_path.unlink()
                except OSError:
                    pass  # Keep backup if we can't delete it
            
            return True
            
        except (OSError, PermissionError, ValueError) as e:
            # Restore from backup if save failed
            if backup_path and backup_path.exists():
                try:
                    shutil.copy2(str(backup_path), str(full_path))
                    print(f"✅ Restored {file_path} from backup after save failure")
                except OSError:
                    pass
            
            # Clean up temp file
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            
            raise PermissionError(f"Cannot save file {file_path}: {e}")
    
    def _validate_content(self, file_path: str, content: str) -> bool:
        """Validate content before saving.
        
        Args:
            file_path: Path to file.
            content: Content to validate.
            
        Returns:
            True if content is valid.
        """
        # Basic validation - can be extended
        # Check if content is a string
        if not isinstance(content, str):
            return False
        
        # Check for null bytes (not allowed in text files)
        if '\x00' in content:
            return False
        
        return True
    
    def _create_backup(self, file_path: Path) -> Optional[Path]:
        """Create backup of file before saving.
        
        Args:
            file_path: Path to file to backup.
            
        Returns:
            Path to backup file, or None if backup failed.
        """
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        try:
            shutil.copy2(str(file_path), str(backup_path))
            return backup_path
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not create backup for {file_path}: {e}")
            return None
    
    def get_diff(self, file_path: str, new_content: str) -> List[str]:
        """Get diff between original and new content.
        
        Args:
            file_path: Path relative to workspace root.
            new_content: New content to compare.
            
        Returns:
            List of diff lines.
        """
        if file_path not in self._open_files:
            # File not opened, read it first
            try:
                original = self.open_file(file_path)
            except (FileNotFoundError, PermissionError):
                return []
        else:
            original = self._open_files[file_path]['original_content']
        
        original_lines = original.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm=''
        ))
        
        return diff
    
    def highlight_errors(self, file_path: str, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Highlight errors in file content.
        
        Args:
            file_path: Path relative to workspace root.
            errors: List of error dictionaries with line, column, message.
            
        Returns:
            Dictionary with error annotations.
        """
        if file_path not in self._open_files:
            try:
                self.open_file(file_path)
            except (FileNotFoundError, PermissionError):
                return {'errors': []}
        
        annotations = []
        for error in errors:
            annotations.append({
                'line': error.get('line', 0),
                'column': error.get('column', 0),
                'message': error.get('message', ''),
                'severity': error.get('severity', 'error'),
                'source': error.get('source', 'unknown')
            })
        
        return {
            'file': file_path,
            'errors': annotations
        }
    
    def get_file_language(self, file_path: str) -> str:
        """Detect file language/type for syntax highlighting.
        
        Args:
            file_path: Path to file.
            
        Returns:
            Language identifier (e.g., 'python', 'javascript', 'markdown').
        """
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.sql': 'sql',
        }
        
        path = Path(file_path)
        return ext_map.get(path.suffix.lower(), 'text')
    
    def close_file(self, file_path: str) -> bool:
        """Close an open file.
        
        Args:
            file_path: Path relative to workspace root.
            
        Returns:
            True if file was open and closed.
        """
        if file_path in self._open_files:
            # Emit file closed event
            if self._emit_events:
                self.event_bus.emit(
                    EventType.FILE_CLOSED,
                    {'path': file_path},
                    'editor'
                )
            
            del self._open_files[file_path]
            return True
        return False
    
    def get_open_files(self) -> List[str]:
        """Get list of currently open files.
        
        Returns:
            List of file paths.
        """
        return list(self._open_files.keys())
    
    def has_unsaved_changes(self, file_path: Optional[str] = None) -> bool:
        """Check if there are unsaved changes.
        
        Args:
            file_path: Check specific file, or all files if None.
            
        Returns:
            True if there are unsaved changes.
        """
        if file_path:
            return file_path in self._unsaved_changes
        return len(self._unsaved_changes) > 0
    
    def get_unsaved_files(self) -> List[str]:
        """Get list of files with unsaved changes.
        
        Returns:
            List of file paths with unsaved changes.
        """
        return list(self._unsaved_changes)
    
    def mark_modified(self, file_path: str) -> None:
        """Mark a file as modified (has unsaved changes).
        
        Args:
            file_path: Path to file.
        """
        if file_path in self._open_files:
            self._open_files[file_path]['modified'] = True
            self._unsaved_changes.add(file_path)
    
    def enable_auto_save(self, enabled: bool = True) -> None:
        """Enable or disable auto-save.
        
        Args:
            enabled: Whether to enable auto-save.
        """
        if enabled and not self._auto_save_enabled:
            self._auto_save_enabled = True
            self._start_auto_save()
        elif not enabled and self._auto_save_enabled:
            self._auto_save_enabled = False
            self._stop_auto_save()
    
    def is_auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled.
        
        Returns:
            True if auto-save is enabled.
        """
        return self._auto_save_enabled
    
    def _start_auto_save(self) -> None:
        """Start auto-save background thread."""
        if self._auto_save_thread and self._auto_save_thread.is_alive():
            return
        
        self._auto_save_stop_event.clear()
        self._auto_save_thread = Thread(target=self._auto_save_loop, daemon=True)
        self._auto_save_thread.start()
    
    def _stop_auto_save(self) -> None:
        """Stop auto-save background thread."""
        if not self._auto_save_thread:
            return
        
        self._auto_save_stop_event.set()
        if self._auto_save_thread.is_alive():
            self._auto_save_thread.join(timeout=2.0)
        self._auto_save_thread = None
    
    def _auto_save_loop(self) -> None:
        """Auto-save loop running in background.
        
        Note: In a real implementation, this would need access to current
        editor content. For now, it just emits events to indicate auto-save occurred.
        """
        while not self._auto_save_stop_event.is_set():
            # Wait for interval
            self._auto_save_stop_event.wait(self._auto_save_interval)
            
            if self._auto_save_stop_event.is_set():
                break
            
            # In a real implementation, would save unsaved changes here
            # For now, just emit an event that auto-save ran
            if self._unsaved_changes and self._emit_events:
                self.event_bus.emit(
                    EventType.FILE_SAVED,
                    {'auto_save_check': True, 'unsaved_count': len(self._unsaved_changes)},
                    'editor'
                )
    
    def cleanup(self) -> None:
        """Clean up editor resources."""
        self._stop_auto_save()
    
    def _resolve_path(self, file_path: str) -> Path:
        """Resolve relative path to absolute path within workspace.
        
        Args:
            file_path: Relative path.
            
        Returns:
            Absolute Path object.
            
        Raises:
            ValueError: If path escapes workspace root.
        """
        full_path = (self.root_path / file_path).resolve()
        
        # Security check: ensure path is within workspace
        try:
            full_path.relative_to(self.root_path)
        except ValueError:
            raise ValueError(f"Path escapes workspace root: {file_path}")
        
        return full_path
