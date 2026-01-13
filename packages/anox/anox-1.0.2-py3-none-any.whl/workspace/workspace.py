"""Anox Workspace - Core workspace management."""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from .file_explorer import FileExplorer
from .editor import Editor
from .terminal import Terminal
from .search import Search
from .events import get_event_bus, EventType, WorkspaceEvent
from .fs_watcher import FileSystemWatcher
from .workspace_core import get_workspace_core, WorkspaceCore
from .backend_api import BackendAPIFacade
from .workspace_ai import get_workspace_ai, WorkspaceAwareAI


class WorkspaceInitializationError(Exception):
    """Raised when workspace initialization fails."""
    pass


class WorkspaceFlowError(Exception):
    """Raised when workspace usage violates the Golden Path."""
    pass


class Workspace:
    """Main workspace class that integrates all components.
    
    This class implements the Sync Layer - the heart of Workspace v1.
    It ensures that Terminal, File Explorer, Editor, and Workspace Root
    stay synchronized in real-time.
    
    Key Principle: Terminal = Source of Truth
    - When terminal does cd, workspace root changes
    - When files are created/deleted in terminal, file explorer updates
    - When editor saves, terminal can immediately use the file
    """
    
    def __init__(self, root_path: Optional[str] = None, enable_sync: bool = False, enforce_golden_path: bool = True):
        """Initialize workspace with given root path.
        
        Args:
            root_path: Root directory for the workspace. Defaults to current directory.
            enable_sync: Whether to enable real-time synchronization. Defaults to False for backward compatibility.
            enforce_golden_path: Whether to enforce the Golden Path workflow. Defaults to True.
        
        Raises:
            WorkspaceInitializationError: If workspace initialization fails.
        """
        self.root_path = Path(root_path or os.getcwd()).resolve()
        
        # Validate root path exists
        if not self.root_path.exists():
            raise WorkspaceInitializationError(f"Workspace root does not exist: {self.root_path}")
        
        if not self.root_path.is_dir():
            raise WorkspaceInitializationError(f"Workspace root is not a directory: {self.root_path}")
        
        self._enable_sync = enable_sync
        self._enforce_golden_path = enforce_golden_path
        self._initialized = False
        self._usage_state = 'initialized'  # Track usage flow: initialized -> browsing -> editing -> running
        
        # Initialize workspace core (manages workspace root and settings)
        self.workspace_core = get_workspace_core()
        self.workspace_core.set_workspace_root(self.root_path)
        
        # Initialize backend API (clean separation of concerns)
        self.backend = BackendAPIFacade(self.root_path)
        
        # Initialize context-aware AI assistant
        try:
            self.ai_assistant = WorkspaceAwareAI(self.root_path)
            print("✅ AI Assistant initialized and monitoring workspace")
        except Exception as e:
            print(f"⚠️  AI Assistant initialization failed: {e}")
            self.ai_assistant = None
        
        # Initialize components
        self.file_explorer = FileExplorer(self.root_path)
        self.editor = Editor(self.root_path, emit_events=enable_sync)
        self.terminal = Terminal(self.root_path, emit_events=enable_sync)
        self.search = Search(self.root_path)
        
        # Track workspace state
        self._open_files: Dict[str, Any] = {}
        self._current_file: Optional[str] = None
        
        # Set up sync layer
        if enable_sync:
            self.event_bus = get_event_bus()
            self._setup_sync_layer()
            
            # Start filesystem watcher
            self.fs_watcher = FileSystemWatcher(self.root_path)
            self.fs_watcher.start()
        else:
            self.fs_watcher = None
        
        self._initialized = True
        
        # Show Golden Path guidance if enforced
        if enforce_golden_path:
            self._show_golden_path_guidance()
    
    def _setup_sync_layer(self) -> None:
        """Set up the sync layer - heart of Workspace v1.
        
        This connects all components through the event bus:
        - Terminal cd → Workspace root changes → File explorer refreshes
        - Terminal creates file → File explorer updates
        - Editor saves → Filesystem updates → Terminal can use file
        - Terminal error → Editor auto-jumps to error location (NEW!)
        """
        # Subscribe to CWD changes from terminal
        self.event_bus.subscribe(EventType.CWD_CHANGED, self._on_cwd_changed)
        
        # Subscribe to file system events
        self.event_bus.subscribe(EventType.FILE_CREATED, self._on_file_created)
        self.event_bus.subscribe(EventType.FILE_DELETED, self._on_file_deleted)
        self.event_bus.subscribe(EventType.FILE_MODIFIED, self._on_file_modified)
        self.event_bus.subscribe(EventType.FILE_RENAMED, self._on_file_renamed)
        
        # Subscribe to editor events
        self.event_bus.subscribe(EventType.FILE_SAVED, self._on_file_saved)
        
        # Subscribe to error detection for auto-jump (Editor + Terminal unification!)
        self.event_bus.subscribe(EventType.ERROR_DETECTED, self._on_error_detected)
    
    def _on_cwd_changed(self, event: WorkspaceEvent) -> None:
        """Handle terminal cwd change event.
        
        When terminal does cd, the workspace root may need to change.
        
        Args:
            event: CWD changed event from terminal.
        """
        new_cwd = Path(event.data['new_cwd'])
        
        # Check if new cwd should become workspace root
        # For now, keep workspace root stable but file explorer can navigate
        # Future: Could update workspace root if cd goes to parent
        pass
    
    def _on_file_created(self, event: WorkspaceEvent) -> None:
        """Handle file creation event.
        
        Args:
            event: File created event.
        """
        # File explorer will automatically refresh when listing files
        # This is just for tracking
        pass
    
    def _on_file_deleted(self, event: WorkspaceEvent) -> None:
        """Handle file deletion event.
        
        Args:
            event: File deleted event.
        """
        # Remove from open files if it was open
        file_path = event.data.get('path')
        if file_path in self._open_files:
            del self._open_files[file_path]
            if self._current_file == file_path:
                self._current_file = None
    
    def _on_file_modified(self, event: WorkspaceEvent) -> None:
        """Handle file modification event.
        
        Args:
            event: File modified event.
        """
        # Track external modifications
        file_path = event.data.get('path')
        if file_path in self._open_files:
            # Mark as potentially out of sync
            self._open_files[file_path]['external_modification'] = True
    
    def _on_file_saved(self, event: WorkspaceEvent) -> None:
        """Handle file save event from editor.
        
        Args:
            event: File saved event.
        """
        # File is now saved to real filesystem
        # Terminal can immediately use it
        pass
    
    def _on_file_renamed(self, event: WorkspaceEvent) -> None:
        """Handle file rename/move event.
        
        Args:
            event: File renamed event.
        """
        # Safely extract paths with defaults
        old_path = event.data.get('old_path')
        new_path = event.data.get('new_path')
        
        if not old_path or not new_path:
            return  # Invalid event data
        
        # Update open files tracking if renamed file was open
        if old_path in self._open_files:
            self._open_files[new_path] = self._open_files.pop(old_path)
            if self._current_file == old_path:
                self._current_file = new_path
    
    def _on_error_detected(self, event: WorkspaceEvent) -> None:
        """Handle error detection from terminal - auto-jump to editor.
        
        This is the heart of Editor + Terminal unification!
        When terminal detects an error, automatically open the file in editor.
        
        Args:
            event: Error detected event from terminal.
        """
        errors = event.data.get('errors', [])
        if not errors:
            return
        
        # Get first error for auto-jump
        first_error = errors[0]
        file_path = first_error.get('file')
        line_num = first_error.get('line', 1)
        
        if not file_path:
            return
        
        # Store error info for UI to display
        self._last_error = {
            'file': file_path,
            'line': line_num,
            'column': first_error.get('column', 0),
            'message': first_error.get('message', ''),
            'all_errors': errors,
            'command': event.data.get('command', ''),
            'timestamp': event.timestamp
        }
        
        # Mark file as having errors
        self._mark_file_with_errors(file_path, errors)
        
        # Set as current file so UI can jump to it
        self._current_file = file_path
    
    def _mark_file_with_errors(self, file_path: str, errors: List[Dict[str, Any]]) -> None:
        """Mark a file as having errors.
        
        Args:
            file_path: Path to file with errors.
            errors: List of error dictionaries.
        """
        if file_path not in self._open_files:
            self._open_files[file_path] = {}
        self._open_files[file_path]['has_errors'] = True
        self._open_files[file_path]['errors'] = errors
    
    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """Get last detected error for UI to handle.
        
        Returns:
            Dictionary with error info including file, line, and message.
        """
        return getattr(self, '_last_error', None)
    
    def clear_last_error(self) -> None:
        """Clear last error info."""
        if hasattr(self, '_last_error'):
            del self._last_error
    
    def cleanup(self) -> None:
        """Clean up workspace resources."""
        if self.editor:
            self.editor.cleanup()
        if self.fs_watcher:
            self.fs_watcher.stop()
    
    def _show_golden_path_guidance(self) -> None:
        """Show Golden Path guidance to users - THE ONE TRUE WAY."""
        guidance = """
╔═══════════════════════════════════════════════════════════════╗
║                    ANOX WORKSPACE v1                          ║
║                   🎯 THE GOLDEN PATH 🎯                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  There is ONLY ONE WAY to use this workspace:                ║
║                                                               ║
║  1️⃣  OPEN FOLDER → Auto-sets as workspace root              ║
║  2️⃣  FILES APPEAR → In explorer automatically                ║
║  3️⃣  CLICK FILE → Opens in editor                            ║
║  4️⃣  EDIT & SAVE → Real filesystem updated instantly         ║
║  5️⃣  RUN COMMAND → Terminal works with saved files           ║
║  6️⃣  ERROR? → Editor JUMPS to error line automatically       ║
║                                                               ║
║  🔥 UNIFIED EXPERIENCE: Editor + Terminal = ONE TOOL 🔥       ║
║                                                               ║
║  ✨ No thinking required. Just use it. ✨                    ║
║                                                               ║
║  Terminal error → File opens at exact line → Fix → Save      ║
║  Everything synchronized. Everything automatic.               ║
║                                                               ║
║  💡 NEXT STEP: Call workspace.list_files() to see your       ║
║                files, or workspace.open_file('file.txt')     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        if self._enforce_golden_path:
            print(guidance)
    
    def _validate_golden_path(self, operation: str) -> None:
        """Validate that operation follows the Golden Path.
        
        Args:
            operation: Name of the operation being performed.
            
        Raises:
            WorkspaceFlowError: If operation violates Golden Path.
        """
        if not self._enforce_golden_path:
            return
        
        if not self._initialized:
            raise WorkspaceFlowError(
                f"Cannot perform '{operation}' - workspace not fully initialized"
            )
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive workspace health status.
        
        Returns:
            Dictionary with health metrics for all components.
        """
        health = {
            'workspace_root': str(self.root_path),
            'sync_enabled': self._enable_sync,
            'initialized': self._initialized,
            'open_files': len(self._open_files),
            'current_file': self._current_file,
        }
        
        if self.fs_watcher:
            health['fs_watcher'] = self.fs_watcher.get_sync_health()
        
        if self.editor:
            health['unsaved_changes'] = self.editor.has_unsaved_changes()
            health['unsaved_files'] = self.editor.get_unsaved_files()
        
        return health
    
    def navigate_to_folder(self, folder_path: str) -> Dict[str, Any]:
        """Navigate to a folder by making terminal cd to it.
        
        This implements the requirement: "Click folder → terminal cd"
        
        Args:
            folder_path: Relative path to folder from workspace root.
            
        Returns:
            Result of cd command.
        """
        # Resolve to absolute path
        full_path = self.root_path / folder_path
        
        if not full_path.exists() or not full_path.is_dir():
            return {
                'success': False,
                'error': f"Not a valid directory: {folder_path}"
            }
        
        # Execute cd command in terminal
        return self.terminal.execute(f'cd {folder_path}')
    
    def get_current_directory(self) -> str:
        """Get current terminal working directory.
        
        Returns:
            Current working directory path.
        """
        return self.terminal.get_cwd()
    
    def get_root(self) -> Path:
        """Get workspace root path."""
        return self.root_path
    
    def list_files(self, path: Optional[str] = None, recursive: bool = False) -> list:
        """List files in the workspace.
        
        Args:
            path: Relative path within workspace. Defaults to root.
            recursive: Whether to list recursively.
            
        Returns:
            List of file paths relative to workspace root.
        """
        self._usage_state = 'browsing'
        result = self.file_explorer.list_files(path, recursive)
        
        # Provide contextual guidance
        if self._enforce_golden_path and not self._open_files:
            print(f"💡 Found {len(result)} file(s). Next: workspace.open_file('filename') to edit")
        
        return result
    
    def open_file(self, file_path: str) -> str:
        """Open a file for editing.
        
        Args:
            file_path: Path to file relative to workspace root.
            
        Returns:
            File content as string.
        """
        self._validate_golden_path('open_file')
        self._usage_state = 'editing'
        
        content = self.editor.open_file(file_path)
        self._open_files[file_path] = {'content': content, 'modified': False}
        self._current_file = file_path
        
        # Provide contextual guidance
        if self._enforce_golden_path:
            print(f"✅ Opened {file_path}. Next: Edit and call workspace.save_file('{file_path}', content)")
        
        return content
    
    def save_file(self, file_path: str, content: str, create_backup: bool = True) -> bool:
        """Save file content.
        
        Args:
            file_path: Path to file relative to workspace root.
            content: Content to save.
            create_backup: Whether to create backup before saving.
            
        Returns:
            True if successful, False otherwise.
        """
        self._validate_golden_path('save_file')
        
        try:
            success = self.editor.save_file(file_path, content, create_backup=create_backup)
            if success:
                if file_path in self._open_files:
                    self._open_files[file_path]['content'] = content
                    self._open_files[file_path]['modified'] = False
                
                # Provide contextual guidance
                if self._enforce_golden_path:
                    print(f"✅ Saved {file_path}. Next: workspace.execute_command('python {file_path}') to run")
            
            return success
        except (PermissionError, ValueError) as e:
            print(f"❌ Error saving file {file_path}: {e}")
            print(f"💡 Tip: Check file permissions and encoding. Use create_backup=False to skip backup.")
            return False
    
    def search_files(self, query: str, file_pattern: Optional[str] = None) -> list:
        """Search for content in workspace files.
        
        Args:
            query: Search query string.
            file_pattern: Optional glob pattern for files to search.
            
        Returns:
            List of search results with file paths and line numbers.
        """
        return self.search.search(query, file_pattern)
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a terminal command in workspace context.
        
        Args:
            command: Command to execute.
            
        Returns:
            Dictionary with stdout, stderr, and return code.
        """
        self._usage_state = 'running'
        result = self.terminal.execute(command)
        
        # Provide contextual guidance on errors
        if self._enforce_golden_path and not result.get('success', False):
            parsed_errors = result.get('parsed_errors', [])
            if parsed_errors:  # Non-empty list is truthy
                first_error = parsed_errors[0]
                print(f"💡 Errors detected! Editor will auto-jump to {first_error.get('file', 'file')} line {first_error.get('line', 0)}")
            else:
                print(f"⚠️  Command failed. Check output and fix any issues.")
        
        return result
    
    def get_workspace_info(self) -> Dict[str, Any]:
        """Get information about the current workspace state.
        
        Returns:
            Dictionary with workspace statistics and state.
        """
        # Get info from workspace core
        core_info = self.workspace_core.get_workspace_info()
        
        # Add component-specific info
        return {
            **core_info,
            'open_files': list(self._open_files.keys()),
            'current_file': self._current_file,
            'total_files': len(self.file_explorer.list_files(recursive=True)),
            'usage_state': self._usage_state,
            'sync_enabled': self._enable_sync,
        }
    
    def change_workspace_root(self, new_root: str | Path) -> None:
        """Change the workspace root atomically.
        
        This updates the entire workspace context - all components
        will reference the new root.
        
        Args:
            new_root: New workspace root directory
            
        Raises:
            WorkspaceInitializationError: If new root is invalid
        """
        new_root = Path(new_root).resolve()
        
        # Validate new root
        if not new_root.exists():
            raise WorkspaceInitializationError(f"New root does not exist: {new_root}")
        
        if not new_root.is_dir():
            raise WorkspaceInitializationError(f"New root is not a directory: {new_root}")
        
        # Update workspace core
        self.workspace_core.set_workspace_root(new_root)
        
        # Update all components
        self.root_path = new_root
        self.file_explorer = FileExplorer(new_root)
        self.editor = Editor(new_root, emit_events=self._enable_sync)
        self.terminal = Terminal(new_root, emit_events=self._enable_sync)
        self.search = Search(new_root)
        
        # Update backend
        self.backend = BackendAPIFacade(new_root)
        
        # Clear open files
        self._open_files.clear()
        self._current_file = None
        
        # Restart filesystem watcher if enabled
        if self.fs_watcher:
            self.fs_watcher.stop()
            self.fs_watcher = FileSystemWatcher(new_root)
            self.fs_watcher.start()
        
        print(f"✅ Workspace root changed to: {new_root}")
    
    def get_workspace_setting(self, key: str, default: Any = None) -> Any:
        """Get a workspace setting.
        
        Args:
            key: Setting key
            default: Default value if not found
            
        Returns:
            Setting value or default
        """
        return self.workspace_core.get_workspace_setting(key, default)
    
    def update_workspace_settings(self, settings: Dict[str, Any]) -> None:
        """Update workspace settings.
        
        Args:
            settings: Settings to update
        """
        self.workspace_core.update_workspace_settings(settings)
    
    def get_workspace_history(self) -> List[str]:
        """Get recently opened workspace paths.
        
        Returns:
            List of workspace root paths
        """
        return self.workspace_core.get_workspace_history()
