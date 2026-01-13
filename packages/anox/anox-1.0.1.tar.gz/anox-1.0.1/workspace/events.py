"""Event system for workspace synchronization.

This module provides the event bus that enables real-time synchronization
between Terminal, File Explorer, Editor, and Workspace Root.

Terminal = Source of Truth
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import deque


class EventType(Enum):
    """Types of workspace events."""
    
    # Terminal events
    CWD_CHANGED = "cwd_changed"
    COMMAND_EXECUTED = "command_executed"
    ERROR_DETECTED = "error_detected"  # Terminal error detected → Editor should jump
    
    # File system events
    FILE_CREATED = "file_created"
    FILE_DELETED = "file_deleted"
    FILE_MODIFIED = "file_modified"
    FILE_RENAMED = "file_renamed"
    
    # Directory events
    DIR_CREATED = "dir_created"
    DIR_DELETED = "dir_deleted"
    
    # Editor events
    FILE_OPENED = "file_opened"
    FILE_SAVED = "file_saved"
    FILE_CLOSED = "file_closed"
    
    # Workspace events
    WORKSPACE_ROOT_CHANGED = "workspace_root_changed"
    REFRESH_REQUESTED = "refresh_requested"
    
    # UI Layout events (NEW - Phase 3)
    LAYOUT_CHANGED = "layout_changed"
    PANEL_OPENED = "panel_opened"
    PANEL_CLOSED = "panel_closed"
    PANEL_RESIZED = "panel_resized"
    
    # Focus events (NEW - Phase 3)
    FOCUS_CHANGED = "focus_changed"
    EDITOR_FOCUSED = "editor_focused"
    TERMINAL_FOCUSED = "terminal_focused"
    EXPLORER_FOCUSED = "explorer_focused"
    
    # Workspace state events (NEW - Phase 3)
    WORKSPACE_STATE_CHANGED = "workspace_state_changed"
    SETTINGS_CHANGED = "settings_changed"


@dataclass
class WorkspaceEvent:
    """Represents a workspace event."""
    
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    source: str  # Component that emitted the event
    
    def __post_init__(self):
        """Ensure timestamp is set."""
        if not self.timestamp:
            self.timestamp = datetime.now()


class EventBus:
    """Central event bus for workspace synchronization.
    
    This is the heart of the Sync Layer. All components emit events here
    and subscribe to events they care about.
    
    Event Flow:
        Terminal cd → CWD_CHANGED → Workspace updates root → File Explorer refreshes
        Terminal touch → FILE_CREATED → File Explorer refreshes
        Editor save → FILE_MODIFIED → Terminal can see changes
        Click folder → CWD_CHANGED → Terminal cd
    """
    
    def __init__(self):
        """Initialize event bus."""
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._event_history: deque = deque(maxlen=1000)  # Automatically trims old events
    
    def subscribe(self, event_type: EventType, callback: Callable[[WorkspaceEvent], None]) -> None:
        """Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to.
            callback: Function to call when event is emitted.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[WorkspaceEvent], None]) -> None:
        """Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from.
            callback: Callback to remove.
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
    
    def emit(self, event_type: EventType, data: Dict[str, Any], source: str) -> None:
        """Emit an event to all subscribers.
        
        Args:
            event_type: Type of event.
            data: Event data.
            source: Component emitting the event.
        """
        event = WorkspaceEvent(
            event_type=event_type,
            data=data,
            timestamp=datetime.now(),
            source=source
        )
        
        # Add to history
        self._event_history.append(event)
        
        # Notify subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    # Log but don't crash on callback errors
                    print(f"Error in event callback: {e}")
    
    def get_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[WorkspaceEvent]:
        """Get event history.
        
        Args:
            event_type: Filter by event type (optional).
            limit: Maximum number of events to return.
            
        Returns:
            List of events, most recent first.
        """
        events = list(self._event_history)
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:][::-1]
    
    def clear_history(self) -> None:
        """Clear event history."""
        self._event_history.clear()


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance.
    
    Returns:
        Global EventBus instance.
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def reset_event_bus() -> None:
    """Reset the global event bus (mainly for testing)."""
    global _global_event_bus
    _global_event_bus = None
