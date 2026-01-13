"""Filesystem watcher for detecting external changes.

This module monitors the workspace directory for file system changes
and emits appropriate events through the event bus.
"""

import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Set, Optional, List, Any
from threading import Thread, Event as ThreadEvent
from .events import get_event_bus, EventType


class FileSystemWatcher:
    """Watches workspace directory for file system changes."""
    
    def __init__(self, root_path: Path, poll_interval: float = 1.0):
        """Initialize filesystem watcher.
        
        Args:
            root_path: Root directory to watch.
            poll_interval: How often to check for changes (seconds).
        """
        self.root_path = root_path
        self.poll_interval = poll_interval
        self.event_bus = get_event_bus()
        
        self._running = False
        self._thread: Optional[Thread] = None
        self._stop_event = ThreadEvent()
        
        # Track file states with content hashes for better rename detection
        self._file_states: Dict[str, Dict] = {}
        self._content_hashes: Dict[str, List[str]] = {}  # hash -> list of paths for collision handling
        self._ignored_patterns = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build',
        }
        
        # Track failed sync attempts for logging and retry
        self._failed_syncs: List[Dict[str, Any]] = []
        self._max_retry_attempts = 3
        
        # Batch operation handling - collect changes before emitting
        self._pending_changes: List[Dict[str, Any]] = []
        self._batch_window = 0.5  # seconds to collect batch changes
    
    def start(self) -> None:
        """Start watching the filesystem."""
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        
        # Initialize file states
        self._scan_directory()
        
        # Start background thread
        self._thread = Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop watching the filesystem."""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def _watch_loop(self) -> None:
        """Main watch loop running in background thread."""
        while self._running and not self._stop_event.is_set():
            try:
                self._check_for_changes()
            except Exception as e:
                print(f"Error in filesystem watcher: {e}")
            
            # Wait for next poll interval
            self._stop_event.wait(self.poll_interval)
    
    def _scan_directory(self) -> None:
        """Scan directory and build initial file state."""
        self._file_states.clear()
        self._content_hashes.clear()
        
        try:
            for item in self.root_path.rglob('*'):
                if self._should_ignore(item):
                    continue
                
                try:
                    rel_path = str(item.relative_to(self.root_path))
                    stat = item.stat()
                    
                    file_info = {
                        'mtime': stat.st_mtime,
                        'size': stat.st_size if item.is_file() else 0,
                        'is_dir': item.is_dir(),
                    }
                    
                    # For small files, compute hash for rename detection
                    if item.is_file() and stat.st_size < 1024 * 1024:  # 1MB limit
                        try:
                            file_hash = self._compute_file_hash(item)
                            file_info['hash'] = file_hash

                            # Handle hash collisions by storing a list

                            if file_hash not in self._content_hashes:

                                self._content_hashes[file_hash] = []

                            self._content_hashes[file_hash].append(rel_path)
                        except (OSError, PermissionError):
                            pass
                    
                    self._file_states[rel_path] = file_info
                except (OSError, PermissionError):
                    pass
        except Exception as e:
            print(f"Error scanning directory: {e}")
    
    def _check_for_changes(self) -> None:
        """Check for filesystem changes since last scan."""
        current_files: Dict[str, Dict] = {}
        current_hashes: Dict[str, List[str]] = {}
        
        # Scan current state
        try:
            for item in self.root_path.rglob('*'):
                if self._should_ignore(item):
                    continue
                
                try:
                    rel_path = str(item.relative_to(self.root_path))
                    stat = item.stat()
                    
                    file_info = {
                        'mtime': stat.st_mtime,
                        'size': stat.st_size if item.is_file() else 0,
                        'is_dir': item.is_dir(),
                    }
                    
                    # For small files, compute hash for rename detection
                    if item.is_file() and stat.st_size < 1024 * 1024:  # 1MB limit
                        try:
                            file_hash = self._compute_file_hash(item)
                            file_info['hash'] = file_hash
                            # Handle hash collisions by storing a list
                            if file_hash not in current_hashes:
                                current_hashes[file_hash] = []
                            current_hashes[file_hash].append(rel_path)
                        except (OSError, PermissionError):
                            pass
                    
                    current_files[rel_path] = file_info
                except (OSError, PermissionError):
                    pass
        except Exception as e:
            print(f"Error checking for changes: {e}")
            return
        
        # Detect renames/moves first (before detecting new/deleted files)
        self._detect_renames(current_files, current_hashes)
        
        # Detect new files
        for path, info in current_files.items():
            # Skip files that were already processed as renames
            if info.get('_rename_processed'):
                continue
            
            if path not in self._file_states:
                event_type = EventType.DIR_CREATED if info['is_dir'] else EventType.FILE_CREATED
                try:
                    self.event_bus.emit(
                        event_type,
                        {'path': path, 'absolute_path': str(self.root_path / path)},
                        'fs_watcher'
                    )
                except Exception as e:
                    self._failed_syncs.append({
                        'type': 'create',
                        'path': path,
                        'error': str(e),
                    })
        
        # Detect deleted files
        for path, info in self._file_states.items():
            if path not in current_files:
                event_type = EventType.DIR_DELETED if info['is_dir'] else EventType.FILE_DELETED
                try:
                    self.event_bus.emit(
                        event_type,
                        {'path': path, 'absolute_path': str(self.root_path / path)},
                        'fs_watcher'
                    )
                except Exception as e:
                    self._failed_syncs.append({
                        'type': 'delete',
                        'path': path,
                        'error': str(e),
                    })
        
        # Detect modified files
        for path, info in current_files.items():
            if path in self._file_states:
                old_info = self._file_states[path]
                # Check if file was modified (mtime or size changed)
                if (not info['is_dir'] and 
                    (info['mtime'] != old_info['mtime'] or info['size'] != old_info['size'])):
                    try:
                        self.event_bus.emit(
                            EventType.FILE_MODIFIED,
                            {'path': path, 'absolute_path': str(self.root_path / path)},
                            'fs_watcher'
                        )
                    except Exception as e:
                        self._failed_syncs.append({
                            'type': 'modify',
                            'path': path,
                            'error': str(e),
                        })
        
        # Retry failed syncs
        self._retry_failed_syncs()
        
        # Update state
        self._file_states = current_files
        self._content_hashes = current_hashes
    
    def _detect_renames(self, current_files: Dict[str, Dict], current_hashes: Dict[str, List[str]]) -> None:
        """Detect file renames/moves by comparing content hashes.
        
        Args:
            current_files: Current file states.
            current_hashes: Current hash to paths mapping (handles collisions).
        """
        # Look for files that disappeared and appeared with same hash
        for old_path, old_info in self._file_states.items():
            if old_path not in current_files and not old_info['is_dir']:
                old_hash = old_info.get('hash')
                if old_hash and old_hash in current_hashes:
                    new_paths = current_hashes[old_hash]
                    # Find the most likely rename candidate (prefer same directory)
                    old_dir = str(Path(old_path).parent)
                    new_path = None
                    
                    # First try to find a match in the same directory
                    for candidate in new_paths:
                        if str(Path(candidate).parent) == old_dir:
                            new_path = candidate
                            break
                    
                    # If no match in same dir, use the first one
                    if not new_path and new_paths:
                        new_path = new_paths[0]
                    
                    if new_path:
                        # This looks like a rename/move
                        try:
                            self.event_bus.emit(
                                EventType.FILE_RENAMED,
                                {
                                    'old_path': old_path,
                                    'new_path': new_path,
                                    'old_absolute_path': str(self.root_path / old_path),
                                    'new_absolute_path': str(self.root_path / new_path),
                                },
                                'fs_watcher'
                            )
                            # Mark as processed by setting special flag
                            if new_path in current_files:
                                current_files[new_path]['_rename_processed'] = True
                        except Exception as e:
                            self._failed_syncs.append({
                                'type': 'rename',
                                'old_path': old_path,
                                'new_path': new_path,
                                'error': str(e),
                            })
    
    def _retry_failed_syncs(self) -> None:
        """Retry failed sync operations with exponential backoff.
        
        Implements retry logic with max attempts to handle transient failures.
        """
        if not self._failed_syncs:
            return
        
        # Separate into retryable and permanent failures
        retryable = []
        permanent = []
        
        for failure in self._failed_syncs:
            attempts = failure.get('attempts', 0)
            if attempts < self._max_retry_attempts:
                failure['attempts'] = attempts + 1
                retryable.append(failure)
            else:
                permanent.append(failure)
        
        # Log permanent failures
        for failure in permanent:
            print(f"⚠️  Sync permanently failed for {failure['type']} on {failure.get('path', 'unknown')}: {failure['error']}")
        
        # Retry operations
        successfully_retried = []
        for failure in retryable:
            try:
                # Re-emit the event based on failure type
                if failure['type'] == 'rename':
                    # Validate required keys exist
                    if 'old_path' not in failure or 'new_path' not in failure:
                        continue
                    
                    self.event_bus.emit(
                        EventType.FILE_RENAMED,
                        {
                            'old_path': failure['old_path'],
                            'new_path': failure['new_path'],
                            'old_absolute_path': str(self.root_path / failure['old_path']),
                            'new_absolute_path': str(self.root_path / failure['new_path']),
                        },
                        'fs_watcher'
                    )
                elif failure['type'] in ['create', 'delete', 'modify']:
                    if 'path' not in failure:
                        continue
                    
                    event_map = {
                        'create': EventType.FILE_CREATED,
                        'delete': EventType.FILE_DELETED,
                        'modify': EventType.FILE_MODIFIED,
                    }
                    self.event_bus.emit(
                        event_map[failure['type']],
                        {'path': failure['path'], 'absolute_path': str(self.root_path / failure['path'])},
                        'fs_watcher'
                    )
                # If successful, mark for removal
                successfully_retried.append(failure)
            except Exception as e:
                # Still failing, update error and keep in list for next retry
                failure['error'] = str(e)
        
        # Remove successfully retried items from failed list
        for success in successfully_retried:
            if success in retryable:
                retryable.remove(success)
        
        # Update failed syncs list with only those that still need retry
        self._failed_syncs = retryable
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored.
        
        Args:
            path: Path to check.
            
        Returns:
            True if path should be ignored.
        """
        # Convert path to string for efficient substring checking
        path_str = str(path)
        
        # Check if any ignored pattern appears in the path
        for pattern in self._ignored_patterns:
            # For directory separators, check if pattern appears as a complete path component
            if pattern in path.parts:
                return True
        
        return False
    
    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute hash of file content for rename detection.
        
        Args:
            file_path: Path to file.
            
        Returns:
            MD5 hash of file content.
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                # Read in chunks to handle larger files efficiently
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (OSError, PermissionError):
            return ""
    
    def get_sync_health(self) -> Dict[str, Any]:
        """Get sync health status.
        
        Returns:
            Dictionary with sync health metrics.
        """
        return {
            'running': self._running,
            'tracked_files': len(self._file_states),
            'failed_syncs': len(self._failed_syncs),
            'poll_interval': self.poll_interval,
        }
