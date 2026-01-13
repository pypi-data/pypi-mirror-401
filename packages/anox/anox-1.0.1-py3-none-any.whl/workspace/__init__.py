"""Anox Workspace Module - VS Code-style workspace with integrated Copilot.

This module provides the core workspace functionality:
- File Explorer: Real file system access
- Editor: File editing with syntax highlighting
- Terminal: Integrated terminal tied to workspace root
- Search: Project-wide search functionality
- Sync Layer: Real-time synchronization between components (Terminal = source of truth)
- Event System: Event bus for component communication
- API Key Management: Add/edit/delete API keys with auto-detection
"""

from .file_explorer import FileExplorer
from .editor import Editor
from .terminal import Terminal
from .search import Search
from .workspace import Workspace, WorkspaceInitializationError, WorkspaceFlowError
from .copilot import AnoxCopilot
from .api_keys import APIKeyManager, get_api_key_manager
from .events import EventBus, EventType, WorkspaceEvent, get_event_bus, reset_event_bus
from .fs_watcher import FileSystemWatcher
from .workspace_core import (
    WorkspaceCore, 
    WorkspaceConfig, 
    WorkspaceStateError,
    get_workspace_core,
    reset_workspace_core
)
from .backend_api import (
    BackendAPIFacade,
    FilesystemBackend,
    AIBackend,
    PolicyBackend,
    FileOperation,
    OperationResult,
    FileInfo,
)
from .ui_adapter import (
    UIAdapter,
    UIState,
    get_ui_adapter,
    reset_ui_adapter
)
from .websocket_protocol import (
    WorkspaceProtocol,
    MobileOptimizedProtocol,
    WebSocketMessage,
    MessageType,
    WorkspaceAction
)
from .workspace_ai import (
    WorkspaceAwareAI,
    AIWarning,
    AIAction,
    get_workspace_ai,
    reset_workspace_ai
)
from .ai_models import (
    ModelType,
    ModelProvider,
    ModelConfig,
    ModelResponse,
    BaseModelProvider,
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    LlamaCppProvider,
    OllamaProvider,
    TransformersProvider,
    ModelManager,
    create_provider,
    create_model_manager_with_defaults,
    get_available_models,
    load_model_config_from_file
)


def create_workspace(folder_path: str = None):
    """
    🎯 THE GOLDEN PATH: One function to create a workspace.
    
    This is the ONLY way you should create a workspace.
    No thinking required. Just call this function.
    
    Args:
        folder_path: Path to workspace folder. Defaults to current directory.
    
    Returns:
        Fully configured Workspace with sync enabled and Golden Path enforced.
    
    Example:
        >>> workspace = create_workspace('/path/to/project')
        >>> # Files appear in explorer
        >>> files = workspace.list_files()
        >>> # Open file in editor
        >>> content = workspace.open_file('README.md')
        >>> # Run terminal command
        >>> result = workspace.execute_command('ls -la')
        >>> # Error? Editor automatically jumps to error line!
    """
    return Workspace(
        root_path=folder_path,
        enable_sync=True,  # Always enabled - this is v1 core feature
        enforce_golden_path=True  # Always enforced - no options
    )


__all__ = [
    'FileExplorer', 
    'Editor', 
    'Terminal', 
    'Search', 
    'Workspace',
    'WorkspaceInitializationError',
    'WorkspaceFlowError',
    'AnoxCopilot',
    'APIKeyManager',
    'get_api_key_manager',
    'EventBus',
    'EventType',
    'WorkspaceEvent',
    'get_event_bus',
    'reset_event_bus',
    'FileSystemWatcher',
    'WorkspaceCore',
    'WorkspaceConfig',
    'WorkspaceStateError',
    'get_workspace_core',
    'reset_workspace_core',
    'BackendAPIFacade',
    'FilesystemBackend',
    'AIBackend',
    'PolicyBackend',
    'FileOperation',
    'OperationResult',
    'FileInfo',
    'UIAdapter',
    'UIState',
    'get_ui_adapter',
    'reset_ui_adapter',
    'WorkspaceProtocol',
    'MobileOptimizedProtocol',
    'WebSocketMessage',
    'MessageType',
    'WorkspaceAction',
    'WorkspaceAwareAI',
    'AIWarning',
    'AIAction',
    'get_workspace_ai',
    'reset_workspace_ai',
    # Multi-Provider AI Models
    'ModelType',
    'ModelProvider',
    'ModelConfig',
    'ModelResponse',
    'BaseModelProvider',
    'OpenAIProvider',
    'AnthropicProvider',
    'GoogleProvider',
    'LlamaCppProvider',
    'OllamaProvider',
    'TransformersProvider',
    'ModelManager',
    'create_provider',
    'create_model_manager_with_defaults',
    'get_available_models',
    'load_model_config_from_file',
    'create_workspace'  # THE GOLDEN PATH
]
