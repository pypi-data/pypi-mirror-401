"""WebSocket Protocol - Clean message protocol for workspace operations.

This module defines the WebSocket message protocol for:
1. UI ↔ Backend communication
2. Mobile client support
3. CLI integration
4. Real-time state synchronization

Message Format:
{
    "type": "request|response|event|notification",
    "action": "open_file|save_file|list_files|...",
    "data": {...},
    "id": "optional_request_id",
    "timestamp": "ISO8601"
}
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from .ui_adapter import UIAdapter, get_ui_adapter
from .workspace_core import get_workspace_core


class MessageType(Enum):
    """Types of WebSocket messages."""
    
    REQUEST = "request"  # UI requesting action
    RESPONSE = "response"  # Backend responding to request
    EVENT = "event"  # Backend notifying UI of state change
    NOTIFICATION = "notification"  # Info/warning/error message


class WorkspaceAction(Enum):
    """Workspace actions that can be requested via WebSocket."""
    
    # File operations
    OPEN_FILE = "open_file"
    SAVE_FILE = "save_file"
    CLOSE_FILE = "close_file"
    LIST_FILES = "list_files"
    CREATE_FILE = "create_file"
    DELETE_FILE = "delete_file"
    RENAME_FILE = "rename_file"
    
    # Workspace operations
    GET_STATE = "get_state"
    CHANGE_ROOT = "change_root"
    GET_SETTINGS = "get_settings"
    UPDATE_SETTINGS = "update_settings"
    
    # Terminal operations
    EXECUTE_COMMAND = "execute_command"
    GET_TERMINAL_OUTPUT = "get_terminal_output"
    
    # Layout operations
    TOGGLE_PANEL = "toggle_panel"
    RESIZE_PANEL = "resize_panel"
    FOCUS_PANEL = "focus_panel"
    
    # Search operations
    SEARCH_FILES = "search_files"


@dataclass
class WebSocketMessage:
    """WebSocket message structure."""
    
    type: str
    action: str
    data: Dict[str, Any]
    id: Optional[str] = None
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str: str) -> WebSocketMessage:
        """Create from JSON string."""
        data = json.loads(json_str)
        return cls(**data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebSocketMessage:
        """Create from dictionary."""
        return cls(**data)


class WorkspaceProtocol:
    """WebSocket protocol handler for workspace operations.
    
    This class:
    1. Receives messages from UI (WebSocket, CLI, mobile)
    2. Routes actions to appropriate handlers
    3. Returns responses in standard format
    4. Emits events for state changes
    
    Mobile-First Design:
    - Low bandwidth - only send changed data
    - Offline support - queue operations
    - Battery efficient - batch updates
    """
    
    def __init__(self, ui_adapter: Optional[UIAdapter] = None):
        """Initialize protocol handler.
        
        Args:
            ui_adapter: UIAdapter instance (uses global if None)
        """
        self.ui_adapter = ui_adapter or get_ui_adapter()
        self.workspace_core = get_workspace_core()
        
        # Action handlers
        self._handlers = {
            WorkspaceAction.OPEN_FILE.value: self._handle_open_file,
            WorkspaceAction.SAVE_FILE.value: self._handle_save_file,
            WorkspaceAction.CLOSE_FILE.value: self._handle_close_file,
            WorkspaceAction.LIST_FILES.value: self._handle_list_files,
            WorkspaceAction.GET_STATE.value: self._handle_get_state,
            WorkspaceAction.CHANGE_ROOT.value: self._handle_change_root,
            WorkspaceAction.GET_SETTINGS.value: self._handle_get_settings,
            WorkspaceAction.UPDATE_SETTINGS.value: self._handle_update_settings,
            WorkspaceAction.TOGGLE_PANEL.value: self._handle_toggle_panel,
            WorkspaceAction.FOCUS_PANEL.value: self._handle_focus_panel,
        }
    
    def handle_message(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle incoming WebSocket message.
        
        Args:
            message: Incoming message
            
        Returns:
            Response message
        """
        if message.type != MessageType.REQUEST.value:
            return self._error_response(
                "Invalid message type, expected 'request'",
                message.id
            )
        
        handler = self._handlers.get(message.action)
        
        if handler is None:
            return self._error_response(
                f"Unknown action: {message.action}",
                message.id
            )
        
        try:
            return handler(message)
        except Exception as e:
            return self._error_response(str(e), message.id)
    
    def handle_message_json(self, json_str: str) -> str:
        """Handle message from JSON string (convenience method).
        
        Args:
            json_str: JSON string message
            
        Returns:
            JSON string response
        """
        try:
            message = WebSocketMessage.from_json(json_str)
            response = self.handle_message(message)
            return response.to_json()
        except json.JSONDecodeError as e:
            error_response = self._error_response(f"Invalid JSON: {e}")
            return error_response.to_json()
    
    # Action handlers
    
    def _handle_open_file(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle open_file action."""
        file_path = message.data.get('path')
        
        if not file_path:
            return self._error_response("Missing 'path' in data", message.id)
        
        result = self.ui_adapter.handle_open_file(file_path)
        
        if result.success:
            return self._success_response(
                {'content': result.data, 'path': file_path},
                message.id
            )
        else:
            return self._error_response(result.error, message.id)
    
    def _handle_save_file(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle save_file action."""
        file_path = message.data.get('path')
        content = message.data.get('content')
        
        if not file_path or content is None:
            return self._error_response(
                "Missing 'path' or 'content' in data",
                message.id
            )
        
        result = self.ui_adapter.handle_save_file(file_path, content)
        
        if result.success:
            return self._success_response({'path': file_path}, message.id)
        else:
            return self._error_response(result.error, message.id)
    
    def _handle_close_file(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle close_file action."""
        file_path = message.data.get('path')
        
        if not file_path:
            return self._error_response("Missing 'path' in data", message.id)
        
        self.ui_adapter.handle_close_file(file_path)
        return self._success_response({'path': file_path}, message.id)
    
    def _handle_list_files(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle list_files action."""
        directory = message.data.get('directory', '')
        
        result = self.ui_adapter.handle_list_files(directory)
        
        if result.success:
            return self._success_response({'files': result.data}, message.id)
        else:
            return self._error_response(result.error, message.id)
    
    def _handle_get_state(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle get_state action."""
        state = self.ui_adapter.get_state_dict()
        return self._success_response({'state': state}, message.id)
    
    def _handle_change_root(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle change_root action."""
        new_root = message.data.get('root')
        
        if not new_root:
            return self._error_response("Missing 'root' in data", message.id)
        
        try:
            self.workspace_core.set_workspace_root(new_root)
            return self._success_response({'root': new_root}, message.id)
        except Exception as e:
            return self._error_response(str(e), message.id)
    
    def _handle_get_settings(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle get_settings action."""
        workspace = self.workspace_core.get_current_workspace()
        
        if not workspace:
            return self._error_response("No active workspace", message.id)
        
        return self._success_response({'settings': workspace.settings}, message.id)
    
    def _handle_update_settings(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle update_settings action."""
        settings = message.data.get('settings')
        
        if not settings:
            return self._error_response("Missing 'settings' in data", message.id)
        
        try:
            self.workspace_core.update_workspace_settings(settings)
            return self._success_response({'settings': settings}, message.id)
        except Exception as e:
            return self._error_response(str(e), message.id)
    
    def _handle_toggle_panel(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle toggle_panel action."""
        panel_name = message.data.get('panel')
        
        if not panel_name:
            return self._error_response("Missing 'panel' in data", message.id)
        
        self.ui_adapter.handle_toggle_panel(panel_name)
        return self._success_response({'panel': panel_name}, message.id)
    
    def _handle_focus_panel(self, message: WebSocketMessage) -> WebSocketMessage:
        """Handle focus_panel action."""
        panel_name = message.data.get('panel')
        
        if not panel_name:
            return self._error_response("Missing 'panel' in data", message.id)
        
        self.ui_adapter.handle_focus_panel(panel_name)
        return self._success_response({'panel': panel_name}, message.id)
    
    # Response helpers
    
    def _success_response(self, data: Dict[str, Any], 
                         request_id: Optional[str] = None) -> WebSocketMessage:
        """Create success response."""
        return WebSocketMessage(
            type=MessageType.RESPONSE.value,
            action="success",
            data={'success': True, **data},
            id=request_id
        )
    
    def _error_response(self, error: str, 
                       request_id: Optional[str] = None) -> WebSocketMessage:
        """Create error response."""
        return WebSocketMessage(
            type=MessageType.RESPONSE.value,
            action="error",
            data={'success': False, 'error': error},
            id=request_id
        )
    
    def create_event(self, event_type: str, data: Dict[str, Any]) -> WebSocketMessage:
        """Create event message for UI.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            Event message
        """
        return WebSocketMessage(
            type=MessageType.EVENT.value,
            action=event_type,
            data=data
        )
    
    def create_notification(self, level: str, message: str, 
                          details: Optional[Dict[str, Any]] = None) -> WebSocketMessage:
        """Create notification message.
        
        Args:
            level: Notification level (info, warning, error)
            message: Notification message
            details: Optional additional details
            
        Returns:
            Notification message
        """
        return WebSocketMessage(
            type=MessageType.NOTIFICATION.value,
            action=level,
            data={
                'message': message,
                'level': level,
                **(details or {})
            }
        )


# Example usage for mobile client optimization
class MobileOptimizedProtocol(WorkspaceProtocol):
    """Mobile-optimized protocol with batching and compression."""
    
    def __init__(self, ui_adapter: Optional[UIAdapter] = None):
        """Initialize mobile protocol."""
        super().__init__(ui_adapter)
        self._pending_events: List[WebSocketMessage] = []
    
    def batch_events(self, events: List[WebSocketMessage]) -> WebSocketMessage:
        """Batch multiple events into single message (reduces bandwidth).
        
        Args:
            events: List of events to batch
            
        Returns:
            Batched event message
        """
        return WebSocketMessage(
            type=MessageType.EVENT.value,
            action="batch",
            data={
                'events': [asdict(e) for e in events],
                'count': len(events)
            }
        )
    
    def get_state_delta(self, old_state: Dict[str, Any], 
                       new_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get only changed fields (reduces bandwidth).
        
        Args:
            old_state: Previous state
            new_state: Current state
            
        Returns:
            Dictionary with only changed fields
        """
        delta = {}
        
        for key, value in new_state.items():
            if key not in old_state or old_state[key] != value:
                delta[key] = value
        
        return delta
