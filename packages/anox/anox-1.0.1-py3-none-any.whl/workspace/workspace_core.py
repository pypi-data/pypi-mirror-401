"""Workspace Core - Central workspace state management for Anox.

This module implements the workspace-first architecture where:
1. There is always a single active workspace root
2. All operations reference this root
3. Root changes are atomic and update entire context
4. Clear separation between state management and UI
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from .events import get_event_bus, EventType


@dataclass
class WorkspaceConfig:
    """Configuration for a workspace."""
    
    root_path: str
    name: Optional[str] = None
    created_at: Optional[str] = None
    last_opened: Optional[str] = None
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.settings is None:
            self.settings = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.last_opened is None:
            self.last_opened = datetime.now().isoformat()
        if self.name is None:
            self.name = Path(self.root_path).name
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WorkspaceConfig:
        """Create from dictionary."""
        return cls(**data)


class WorkspaceStateError(Exception):
    """Raised when workspace state operation fails."""
    pass


class WorkspaceCore:
    """Core workspace state manager.
    
    This class is the heart of the workspace-first architecture.
    It manages:
    - Single active workspace root (source of truth)
    - Workspace configuration and settings
    - Atomic workspace root changes
    - State persistence
    
    Key Principles:
    1. Single active workspace - only one root at a time
    2. Atomic changes - root changes update entire context
    3. State persistence - workspace settings saved to disk
    4. Event-driven - all changes emit events for UI/backend
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize workspace core.
        
        Args:
            config_dir: Directory to store workspace configs. 
                       Defaults to ~/.anox/workspaces/
        """
        if config_dir is None:
            config_dir = Path.home() / '.anox' / 'workspaces'
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self._current_workspace: Optional[WorkspaceConfig] = None
        self._workspace_history: List[str] = []
        
        # Load last workspace if exists
        self._load_state()
    
    def get_current_root(self) -> Optional[Path]:
        """Get current workspace root path.
        
        Returns:
            Current workspace root or None if no workspace is active.
        """
        if self._current_workspace is None:
            return None
        return Path(self._current_workspace.root_path)
    
    def get_current_workspace(self) -> Optional[WorkspaceConfig]:
        """Get current workspace configuration.
        
        Returns:
            Current workspace config or None.
        """
        return self._current_workspace
    
    def set_workspace_root(self, root_path: str | Path, 
                          name: Optional[str] = None) -> WorkspaceConfig:
        """Set the active workspace root atomically.
        
        This is the critical operation - changing workspace root updates
        the entire context for all components.
        
        Args:
            root_path: New workspace root directory
            name: Optional workspace name
            
        Returns:
            New workspace configuration
            
        Raises:
            WorkspaceStateError: If root path is invalid
        """
        root_path = Path(root_path).resolve()
        
        # Validate path
        if not root_path.exists():
            raise WorkspaceStateError(f"Workspace root does not exist: {root_path}")
        
        if not root_path.is_dir():
            raise WorkspaceStateError(f"Workspace root is not a directory: {root_path}")
        
        # Store old workspace for event
        old_root = self.get_current_root()
        
        # Create or load workspace config
        config = self._load_or_create_config(root_path, name)
        
        # Update last opened time
        config.last_opened = datetime.now().isoformat()
        
        # Atomic update
        self._current_workspace = config
        
        # Add to history
        if str(root_path) not in self._workspace_history:
            self._workspace_history.insert(0, str(root_path))
            # Keep only last 20 workspaces
            self._workspace_history = self._workspace_history[:20]
        
        # Persist state
        self._save_state()
        self._save_workspace_config(config)
        
        # Emit workspace root changed event (get fresh event bus)
        event_bus = get_event_bus()
        event_bus.emit(
            EventType.WORKSPACE_ROOT_CHANGED,
            {
                'old_root': str(old_root) if old_root else None,
                'new_root': str(root_path),
                'workspace_name': config.name,
            },
            source='workspace_core'
        )
        
        return config
    
    def update_workspace_settings(self, settings: Dict[str, Any]) -> None:
        """Update current workspace settings.
        
        Args:
            settings: Settings to update (merged with existing)
            
        Raises:
            WorkspaceStateError: If no workspace is active
        """
        if self._current_workspace is None:
            raise WorkspaceStateError("No active workspace")
        
        # Merge settings
        self._current_workspace.settings.update(settings)
        
        # Persist
        self._save_workspace_config(self._current_workspace)
    
    def get_workspace_setting(self, key: str, default: Any = None) -> Any:
        """Get a workspace setting value.
        
        Args:
            key: Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        if self._current_workspace is None:
            return default
        
        return self._current_workspace.settings.get(key, default)
    
    def get_workspace_history(self) -> List[str]:
        """Get list of recently opened workspace paths.
        
        Returns:
            List of workspace root paths (most recent first)
        """
        return self._workspace_history.copy()
    
    def clear_workspace(self) -> None:
        """Clear the current workspace (no active workspace)."""
        old_root = self.get_current_root()
        self._current_workspace = None
        
        # Emit event (get fresh event bus)
        if old_root:
            event_bus = get_event_bus()
            event_bus.emit(
                EventType.WORKSPACE_ROOT_CHANGED,
                {
                    'old_root': str(old_root),
                    'new_root': None,
                    'workspace_name': None,
                },
                source='workspace_core'
            )
        
        self._save_state()
    
    def get_workspace_info(self) -> Dict[str, Any]:
        """Get comprehensive workspace information.
        
        Returns:
            Dictionary with workspace state information
        """
        if self._current_workspace is None:
            return {
                'active': False,
                'root': None,
                'name': None,
            }
        
        return {
            'active': True,
            'root': str(self._current_workspace.root_path),
            'name': self._current_workspace.name,
            'created_at': self._current_workspace.created_at,
            'last_opened': self._current_workspace.last_opened,
            'settings': self._current_workspace.settings.copy(),
        }
    
    def _load_or_create_config(self, root_path: Path, 
                               name: Optional[str]) -> WorkspaceConfig:
        """Load existing config or create new one.
        
        Args:
            root_path: Workspace root path
            name: Optional workspace name
            
        Returns:
            Workspace configuration
        """
        config_file = self._get_workspace_config_path(root_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                return WorkspaceConfig.from_dict(data)
            except Exception:
                # If config is corrupted, create new one
                pass
        
        # Create new config
        return WorkspaceConfig(
            root_path=str(root_path),
            name=name or root_path.name,
        )
    
    def _get_workspace_config_path(self, root_path: Path) -> Path:
        """Get path to workspace config file.
        
        Args:
            root_path: Workspace root path
            
        Returns:
            Path to config file
        """
        # Use hash of root path as filename to avoid path separator issues
        import hashlib
        path_hash = hashlib.sha256(str(root_path).encode()).hexdigest()[:16]
        return self.config_dir / f"{path_hash}.json"
    
    def _save_workspace_config(self, config: WorkspaceConfig) -> None:
        """Save workspace configuration to disk.
        
        Args:
            config: Workspace configuration to save
        """
        config_file = self._get_workspace_config_path(Path(config.root_path))
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save workspace config: {e}")
    
    def _load_state(self) -> None:
        """Load workspace state from disk."""
        state_file = self.config_dir / 'state.json'
        
        if not state_file.exists():
            return
        
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            # Restore history
            self._workspace_history = state.get('history', [])
            
            # Restore last workspace if it still exists
            last_root = state.get('last_root')
            if last_root and Path(last_root).exists():
                try:
                    self.set_workspace_root(last_root)
                except WorkspaceStateError:
                    # If last workspace is invalid, just skip it
                    pass
                    
        except Exception as e:
            print(f"Warning: Could not load workspace state: {e}")
    
    def _save_state(self) -> None:
        """Save workspace state to disk."""
        state_file = self.config_dir / 'state.json'
        
        state = {
            'last_root': str(self.get_current_root()) if self.get_current_root() else None,
            'history': self._workspace_history,
            'updated_at': datetime.now().isoformat(),
        }
        
        try:
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save workspace state: {e}")


# Global workspace core instance
_global_workspace_core: Optional[WorkspaceCore] = None


def get_workspace_core() -> WorkspaceCore:
    """Get the global workspace core instance.
    
    Returns:
        Global WorkspaceCore instance
    """
    global _global_workspace_core
    if _global_workspace_core is None:
        _global_workspace_core = WorkspaceCore()
    return _global_workspace_core


def reset_workspace_core() -> None:
    """Reset the global workspace core (mainly for testing)."""
    global _global_workspace_core
    _global_workspace_core = None
