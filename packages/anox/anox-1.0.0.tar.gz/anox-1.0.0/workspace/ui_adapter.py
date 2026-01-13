"""UI Adapter - Clean separation between workspace state and UI rendering.

This module implements the UI layer separation principle:
- UI only renders, never manages state
- All state changes go through backend
- UI subscribes to state change events
- UI sends user actions to backend

This is critical for:
1. Mobile support - UI can be on different device
2. WebSocket integration - Clean message protocol
3. Testing - Mock UI without affecting logic
4. Multiple UIs - CLI, Web, Mobile can coexist
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from .events import get_event_bus, EventType, WorkspaceEvent
from .workspace_core import get_workspace_core, WorkspaceCore
from .backend_api import BackendAPIFacade, FileOperation, OperationResult


@dataclass
class UIState:
    """Complete UI state - everything the UI needs to render.
    
    The UI is stateless - it only renders based on this state.
    State changes come from workspace backend.
    """
    
    # Workspace state
    workspace_active: bool
    workspace_root: Optional[str]
    workspace_name: Optional[str]
    
    # File explorer state
    current_directory: str
    files: List[Dict[str, Any]]
    
    # Editor state
    open_files: List[str]
    current_file: Optional[str]
    current_file_content: Optional[str]
    unsaved_changes: bool
    
    # Terminal state
    terminal_cwd: str
    terminal_output: List[str]
    
    # Layout state
    panels: Dict[str, Dict[str, Any]]  # panel_name -> {visible, size, position}
    current_focus: Optional[str]  # Which panel has focus
    
    # Errors and notifications
    last_error: Optional[Dict[str, Any]]
    notifications: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class UIAdapter:
    """Adapter between Workspace backend and UI rendering.
    
    The UI adapter:
    1. Subscribes to all workspace events
    2. Maintains current UI state
    3. Provides methods for UI to query state
    4. Routes UI actions to backend
    5. Emits UI-specific events for rendering
    
    Key Principle: UI never modifies state directly
    """
    
    def __init__(self, workspace_core: Optional[WorkspaceCore] = None):
        """Initialize UI adapter.
        
        Args:
            workspace_core: WorkspaceCore instance (optional, uses global if None)
        """
        self.workspace_core = workspace_core or get_workspace_core()
        self.event_bus = get_event_bus()
        
        # Initialize UI state
        self._ui_state = self._build_initial_state()
        
        # Subscribe to workspace events
        self._subscribe_to_events()
        
        # UI event subscribers (UI components subscribe to these)
        self._ui_subscribers: Dict[str, List[Callable]] = {}
    
    def _build_initial_state(self) -> UIState:
        """Build initial UI state from workspace."""
        workspace_info = self.workspace_core.get_workspace_info()
        
        return UIState(
            workspace_active=workspace_info['active'],
            workspace_root=workspace_info.get('root'),
            workspace_name=workspace_info.get('name'),
            current_directory=workspace_info.get('root', '/'),
            files=[],
            open_files=[],
            current_file=None,
            current_file_content=None,
            unsaved_changes=False,
            terminal_cwd=workspace_info.get('root', '/'),
            terminal_output=[],
            panels={
                'explorer': {'visible': True, 'size': 250, 'position': 'left'},
                'editor': {'visible': True, 'size': '60%', 'position': 'center'},
                'terminal': {'visible': True, 'size': 200, 'position': 'bottom'},
            },
            current_focus='editor',
            last_error=None,
            notifications=[],
        )
    
    def _subscribe_to_events(self) -> None:
        """Subscribe to workspace events to update UI state."""
        # Workspace events
        self.event_bus.subscribe(
            EventType.WORKSPACE_ROOT_CHANGED, 
            self._on_workspace_root_changed
        )
        
        # File events
        self.event_bus.subscribe(EventType.FILE_OPENED, self._on_file_opened)
        self.event_bus.subscribe(EventType.FILE_SAVED, self._on_file_saved)
        self.event_bus.subscribe(EventType.FILE_CLOSED, self._on_file_closed)
        
        # Terminal events
        self.event_bus.subscribe(EventType.CWD_CHANGED, self._on_cwd_changed)
        self.event_bus.subscribe(EventType.ERROR_DETECTED, self._on_error_detected)
        
        # Layout events
        self.event_bus.subscribe(EventType.LAYOUT_CHANGED, self._on_layout_changed)
        self.event_bus.subscribe(EventType.FOCUS_CHANGED, self._on_focus_changed)
    
    def get_state(self) -> UIState:
        """Get current UI state for rendering.
        
        Returns:
            Current UI state
        """
        return self._ui_state
    
    def get_state_dict(self) -> Dict[str, Any]:
        """Get UI state as dictionary (for JSON serialization).
        
        Returns:
            UI state as dictionary
        """
        return self._ui_state.to_dict()
    
    # Event handlers - update UI state based on workspace events
    
    def _on_workspace_root_changed(self, event: WorkspaceEvent) -> None:
        """Handle workspace root change."""
        new_root = event.data.get('new_root')
        workspace_name = event.data.get('workspace_name')
        
        self._ui_state.workspace_active = new_root is not None
        self._ui_state.workspace_root = new_root
        self._ui_state.workspace_name = workspace_name
        self._ui_state.current_directory = new_root or '/'
        self._ui_state.terminal_cwd = new_root or '/'
        
        # Clear open files on workspace change
        self._ui_state.open_files = []
        self._ui_state.current_file = None
        self._ui_state.current_file_content = None
        
        # Emit UI update
        self._emit_ui_event('state_changed', {'state': self._ui_state})
    
    def _on_file_opened(self, event: WorkspaceEvent) -> None:
        """Handle file opened event."""
        file_path = event.data.get('path')
        content = event.data.get('content')
        
        if file_path and file_path not in self._ui_state.open_files:
            self._ui_state.open_files.append(file_path)
        
        self._ui_state.current_file = file_path
        self._ui_state.current_file_content = content
        self._ui_state.unsaved_changes = False
        
        self._emit_ui_event('file_opened', {'path': file_path})
    
    def _on_file_saved(self, event: WorkspaceEvent) -> None:
        """Handle file saved event."""
        self._ui_state.unsaved_changes = False
        self._emit_ui_event('file_saved', event.data)
    
    def _on_file_closed(self, event: WorkspaceEvent) -> None:
        """Handle file closed event."""
        file_path = event.data.get('path')
        if file_path in self._ui_state.open_files:
            self._ui_state.open_files.remove(file_path)
        
        if self._ui_state.current_file == file_path:
            self._ui_state.current_file = None
            self._ui_state.current_file_content = None
        
        self._emit_ui_event('file_closed', event.data)
    
    def _on_cwd_changed(self, event: WorkspaceEvent) -> None:
        """Handle terminal cwd change."""
        new_cwd = event.data.get('new_cwd')
        self._ui_state.terminal_cwd = new_cwd
        self._emit_ui_event('terminal_cwd_changed', {'cwd': new_cwd})
    
    def _on_error_detected(self, event: WorkspaceEvent) -> None:
        """Handle error detection."""
        errors = event.data.get('errors', [])
        if errors:
            self._ui_state.last_error = errors[0]
            self._emit_ui_event('error_detected', {'error': errors[0]})
    
    def _on_layout_changed(self, event: WorkspaceEvent) -> None:
        """Handle layout change."""
        panel_name = event.data.get('panel')
        changes = event.data.get('changes', {})
        
        if panel_name in self._ui_state.panels:
            self._ui_state.panels[panel_name].update(changes)
        
        self._emit_ui_event('layout_changed', event.data)
    
    def _on_focus_changed(self, event: WorkspaceEvent) -> None:
        """Handle focus change."""
        new_focus = event.data.get('panel')
        self._ui_state.current_focus = new_focus
        self._emit_ui_event('focus_changed', {'focus': new_focus})
    
    # UI actions - route user actions to backend
    
    def handle_open_file(self, file_path: str) -> OperationResult:
        """Handle UI action: open file.
        
        Args:
            file_path: File to open
            
        Returns:
            Operation result
        """
        if not self._ui_state.workspace_root:
            return OperationResult(
                success=False,
                error="No workspace active"
            )
        
        backend = BackendAPIFacade(Path(self._ui_state.workspace_root))
        operation = FileOperation(operation='read', path=file_path)
        return backend.execute_file_operation(operation)
    
    def handle_save_file(self, file_path: str, content: str) -> OperationResult:
        """Handle UI action: save file.
        
        Args:
            file_path: File to save
            content: File content
            
        Returns:
            Operation result
        """
        if not self._ui_state.workspace_root:
            return OperationResult(
                success=False,
                error="No workspace active"
            )
        
        backend = BackendAPIFacade(Path(self._ui_state.workspace_root))
        operation = FileOperation(operation='write', path=file_path, content=content)
        result = backend.execute_file_operation(operation)
        
        if result.success:
            self._ui_state.unsaved_changes = False
        
        return result
    
    def handle_close_file(self, file_path: str) -> None:
        """Handle UI action: close file.
        
        Args:
            file_path: File to close
        """
        if file_path in self._ui_state.open_files:
            self._ui_state.open_files.remove(file_path)
        
        if self._ui_state.current_file == file_path:
            self._ui_state.current_file = None
            self._ui_state.current_file_content = None
    
    def handle_list_files(self, directory: str = '') -> OperationResult:
        """Handle UI action: list files.
        
        Args:
            directory: Directory to list (relative to workspace root)
            
        Returns:
            Operation result with file list
        """
        if not self._ui_state.workspace_root:
            return OperationResult(
                success=False,
                error="No workspace active"
            )
        
        backend = BackendAPIFacade(Path(self._ui_state.workspace_root))
        operation = FileOperation(
            operation='list',
            path=directory,
            options={'recursive': False}
        )
        result = backend.execute_file_operation(operation)
        
        if result.success:
            self._ui_state.files = [asdict(f) for f in result.data]
        
        return result
    
    def handle_toggle_panel(self, panel_name: str) -> None:
        """Handle UI action: toggle panel visibility.
        
        Args:
            panel_name: Name of panel to toggle
        """
        if panel_name in self._ui_state.panels:
            current_visibility = self._ui_state.panels[panel_name]['visible']
            self._ui_state.panels[panel_name]['visible'] = not current_visibility
            
            # Emit layout changed event
            self.event_bus.emit(
                EventType.LAYOUT_CHANGED,
                {
                    'panel': panel_name,
                    'changes': {'visible': not current_visibility}
                },
                source='ui_adapter'
            )
    
    def handle_focus_panel(self, panel_name: str) -> None:
        """Handle UI action: focus panel.
        
        Args:
            panel_name: Name of panel to focus
        """
        old_focus = self._ui_state.current_focus
        self._ui_state.current_focus = panel_name
        
        # Emit focus changed event
        self.event_bus.emit(
            EventType.FOCUS_CHANGED,
            {
                'old_focus': old_focus,
                'panel': panel_name
            },
            source='ui_adapter'
        )
    
    # UI event system - for UI components to subscribe
    
    def subscribe_ui_event(self, event_name: str, 
                          callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to UI events.
        
        Args:
            event_name: Name of UI event
            callback: Callback function
        """
        if event_name not in self._ui_subscribers:
            self._ui_subscribers[event_name] = []
        
        self._ui_subscribers[event_name].append(callback)
    
    def _emit_ui_event(self, event_name: str, data: Dict[str, Any]) -> None:
        """Emit UI event to subscribers.
        
        Args:
            event_name: Name of event
            data: Event data
        """
        if event_name in self._ui_subscribers:
            for callback in self._ui_subscribers[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in UI event callback: {e}")


# Global UI adapter instance
_global_ui_adapter: Optional[UIAdapter] = None


def get_ui_adapter() -> UIAdapter:
    """Get the global UI adapter instance.
    
    Returns:
        Global UIAdapter instance
    """
    global _global_ui_adapter
    if _global_ui_adapter is None:
        _global_ui_adapter = UIAdapter()
    return _global_ui_adapter


def reset_ui_adapter() -> None:
    """Reset the global UI adapter (mainly for testing)."""
    global _global_ui_adapter
    _global_ui_adapter = None
