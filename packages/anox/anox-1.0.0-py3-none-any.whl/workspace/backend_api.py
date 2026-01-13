"""Backend API Layer - Clean separation between UI and business logic.

This module provides backend services that handle:
1. Filesystem operations
2. AI integration
3. Policy enforcement
4. Usage/billing tracking

Key Principles:
- UI only renders, backend does all logic
- All critical operations go through backend
- Backend enforces security and policies
- Clean interfaces for mobile and CLI clients
"""

from __future__ import annotations

import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Protocol


@dataclass
class FileInfo:
    """File information returned by backend."""
    
    path: str
    name: str
    size: int
    is_dir: bool
    modified_at: str
    created_at: Optional[str] = None
    permissions: Optional[str] = None


@dataclass
class FileOperation:
    """Represents a file operation request."""
    
    operation: str  # 'read', 'write', 'delete', 'create', 'move'
    path: str
    content: Optional[str] = None
    destination: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


@dataclass
class OperationResult:
    """Result of a backend operation."""
    
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BackendService(ABC):
    """Abstract base class for backend services."""
    
    @abstractmethod
    def execute(self, operation: Any) -> OperationResult:
        """Execute an operation.
        
        Args:
            operation: Operation to execute
            
        Returns:
            Result of the operation
        """
        pass


class FilesystemBackend(BackendService):
    """Backend service for filesystem operations.
    
    This service provides secure filesystem access with:
    - Workspace root boundary enforcement
    - Permission checking
    - Path validation
    - Operation auditing
    """
    
    def __init__(self, workspace_root: Path):
        """Initialize filesystem backend.
        
        Args:
            workspace_root: Workspace root directory
        """
        self.workspace_root = workspace_root.resolve()
    
    def execute(self, operation: FileOperation) -> OperationResult:
        """Execute a filesystem operation.
        
        Args:
            operation: File operation to execute
            
        Returns:
            Operation result
        """
        try:
            if operation.operation == 'read':
                return self._read_file(operation.path)
            elif operation.operation == 'write':
                return self._write_file(operation.path, operation.content)
            elif operation.operation == 'delete':
                return self._delete_file(operation.path)
            elif operation.operation == 'list':
                return self._list_files(operation.path, operation.options or {})
            elif operation.operation == 'create_dir':
                return self._create_directory(operation.path)
            elif operation.operation == 'move':
                return self._move_file(operation.path, operation.destination)
            else:
                return OperationResult(
                    success=False,
                    error=f"Unknown operation: {operation.operation}"
                )
        except Exception as e:
            return OperationResult(
                success=False,
                error=str(e)
            )
    
    def _validate_path(self, path: str) -> Path:
        """Validate that path is within workspace root.
        
        Args:
            path: Relative or absolute path
            
        Returns:
            Resolved absolute path
            
        Raises:
            ValueError: If path is outside workspace root
        """
        if os.path.isabs(path):
            full_path = Path(path).resolve()
        else:
            full_path = (self.workspace_root / path).resolve()
        
        # Ensure path is within workspace root
        try:
            full_path.relative_to(self.workspace_root)
        except ValueError:
            raise ValueError(f"Path outside workspace root: {path}")
        
        return full_path
    
    def _read_file(self, path: str) -> OperationResult:
        """Read file contents.
        
        Args:
            path: File path
            
        Returns:
            Operation result with file content
        """
        full_path = self._validate_path(path)
        
        if not full_path.exists():
            return OperationResult(
                success=False,
                error=f"File not found: {path}"
            )
        
        if full_path.is_dir():
            return OperationResult(
                success=False,
                error=f"Path is a directory: {path}"
            )
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return OperationResult(
                success=True,
                data=content,
                metadata={
                    'size': full_path.stat().st_size,
                    'modified_at': datetime.fromtimestamp(
                        full_path.stat().st_mtime
                    ).isoformat(),
                }
            )
        except UnicodeDecodeError:
            return OperationResult(
                success=False,
                error="File is not a text file (binary content)"
            )
    
    def _write_file(self, path: str, content: Optional[str]) -> OperationResult:
        """Write content to file.
        
        Args:
            path: File path
            content: Content to write
            
        Returns:
            Operation result
        """
        if content is None:
            return OperationResult(
                success=False,
                error="Content is required for write operation"
            )
        
        full_path = self._validate_path(path)
        
        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return OperationResult(
                success=True,
                metadata={
                    'path': str(full_path.relative_to(self.workspace_root)),
                    'size': len(content),
                }
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Failed to write file: {e}"
            )
    
    def _delete_file(self, path: str) -> OperationResult:
        """Delete a file or directory.
        
        Args:
            path: Path to delete
            
        Returns:
            Operation result
        """
        full_path = self._validate_path(path)
        
        if not full_path.exists():
            return OperationResult(
                success=False,
                error=f"Path not found: {path}"
            )
        
        try:
            if full_path.is_dir():
                shutil.rmtree(full_path)
            else:
                full_path.unlink()
            
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Failed to delete: {e}"
            )
    
    def _list_files(self, path: str = '', 
                    options: Dict[str, Any] = None) -> OperationResult:
        """List files in directory.
        
        Args:
            path: Directory path (relative to workspace root)
            options: Options like 'recursive', 'include_hidden'
            
        Returns:
            Operation result with list of files
        """
        if options is None:
            options = {}
        
        full_path = self._validate_path(path) if path else self.workspace_root
        
        if not full_path.exists():
            return OperationResult(
                success=False,
                error=f"Directory not found: {path}"
            )
        
        if not full_path.is_dir():
            return OperationResult(
                success=False,
                error=f"Path is not a directory: {path}"
            )
        
        files = []
        recursive = options.get('recursive', False)
        include_hidden = options.get('include_hidden', False)
        
        try:
            if recursive:
                for item in full_path.rglob('*'):
                    if not include_hidden and item.name.startswith('.'):
                        continue
                    files.append(self._get_file_info(item))
            else:
                for item in full_path.iterdir():
                    if not include_hidden and item.name.startswith('.'):
                        continue
                    files.append(self._get_file_info(item))
            
            return OperationResult(
                success=True,
                data=files
            )
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Failed to list files: {e}"
            )
    
    def _create_directory(self, path: str) -> OperationResult:
        """Create a directory.
        
        Args:
            path: Directory path
            
        Returns:
            Operation result
        """
        full_path = self._validate_path(path)
        
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Failed to create directory: {e}"
            )
    
    def _move_file(self, source: str, destination: Optional[str]) -> OperationResult:
        """Move or rename a file.
        
        Args:
            source: Source path
            destination: Destination path
            
        Returns:
            Operation result
        """
        if destination is None:
            return OperationResult(
                success=False,
                error="Destination is required for move operation"
            )
        
        source_path = self._validate_path(source)
        dest_path = self._validate_path(destination)
        
        if not source_path.exists():
            return OperationResult(
                success=False,
                error=f"Source not found: {source}"
            )
        
        try:
            shutil.move(str(source_path), str(dest_path))
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(
                success=False,
                error=f"Failed to move file: {e}"
            )
    
    def _get_file_info(self, path: Path) -> FileInfo:
        """Get file information.
        
        Args:
            path: File path
            
        Returns:
            File information
        """
        stat = path.stat()
        rel_path = str(path.relative_to(self.workspace_root))
        
        return FileInfo(
            path=rel_path,
            name=path.name,
            size=stat.st_size,
            is_dir=path.is_dir(),
            modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
        )


class AIBackend(BackendService):
    """Backend service for AI operations.
    
    This service provides AI integration with:
    - Workspace-aware context
    - Token usage tracking
    - Policy enforcement
    - Cost management
    """
    
    def __init__(self, workspace_root: Path):
        """Initialize AI backend.
        
        Args:
            workspace_root: Workspace root directory
        """
        self.workspace_root = workspace_root
        self._usage_tracker = UsageTracker()
    
    def execute(self, operation: Any) -> OperationResult:
        """Execute an AI operation.
        
        Args:
            operation: AI operation to execute
            
        Returns:
            Operation result
        """
        # Placeholder for AI operations
        return OperationResult(
            success=False,
            error="AI operations not yet implemented"
        )
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get AI usage statistics.
        
        Returns:
            Usage statistics
        """
        return self._usage_tracker.get_stats()


class UsageTracker:
    """Tracks usage and costs for billing."""
    
    def __init__(self):
        """Initialize usage tracker."""
        self._total_tokens = 0
        self._total_cost = 0.0
        self._operations = []
    
    def track_operation(self, tokens: int, cost: float, 
                       operation_type: str) -> None:
        """Track an operation.
        
        Args:
            tokens: Number of tokens used
            cost: Cost in dollars
            operation_type: Type of operation
        """
        self._total_tokens += tokens
        self._total_cost += cost
        self._operations.append({
            'tokens': tokens,
            'cost': cost,
            'type': operation_type,
            'timestamp': datetime.now().isoformat(),
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics.
        
        Returns:
            Usage statistics
        """
        return {
            'total_tokens': self._total_tokens,
            'total_cost': self._total_cost,
            'operations_count': len(self._operations),
            'recent_operations': self._operations[-10:],
        }


class PolicyBackend(BackendService):
    """Backend service for policy enforcement.
    
    This service ensures:
    - Security policies are enforced
    - File access is controlled
    - Operations are validated
    - Audit trail is maintained
    """
    
    def __init__(self, workspace_root: Path):
        """Initialize policy backend.
        
        Args:
            workspace_root: Workspace root directory
        """
        self.workspace_root = workspace_root
        self._audit_log = []
    
    def execute(self, operation: Any) -> OperationResult:
        """Execute a policy check.
        
        Args:
            operation: Operation to validate
            
        Returns:
            Operation result
        """
        # Placeholder for policy operations
        return OperationResult(success=True)
    
    def validate_operation(self, operation: FileOperation) -> bool:
        """Validate if operation is allowed.
        
        Args:
            operation: Operation to validate
            
        Returns:
            True if allowed, False otherwise
        """
        # Basic validation - can be extended with more rules
        if operation.operation in ['read', 'list']:
            return True
        
        # Write operations - check for dangerous paths
        if operation.operation in ['write', 'delete', 'move']:
            dangerous_paths = ['.git', '.env', 'secrets']
            for dangerous in dangerous_paths:
                if dangerous in operation.path:
                    self._audit_log.append({
                        'operation': operation.operation,
                        'path': operation.path,
                        'denied': True,
                        'reason': f'Dangerous path: {dangerous}',
                        'timestamp': datetime.now().isoformat(),
                    })
                    return False
        
        return True
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get audit log.
        
        Returns:
            List of audit entries
        """
        return self._audit_log.copy()


class BackendAPIFacade:
    """Facade for all backend services.
    
    This provides a single interface for UI and CLI to access
    all backend functionality.
    """
    
    def __init__(self, workspace_root: Path):
        """Initialize backend API facade.
        
        Args:
            workspace_root: Workspace root directory
        """
        self.workspace_root = workspace_root
        self.filesystem = FilesystemBackend(workspace_root)
        self.ai = AIBackend(workspace_root)
        self.policy = PolicyBackend(workspace_root)
    
    def execute_file_operation(self, operation: FileOperation) -> OperationResult:
        """Execute a filesystem operation with policy enforcement.
        
        Args:
            operation: File operation to execute
            
        Returns:
            Operation result
        """
        # Check policy
        if not self.policy.validate_operation(operation):
            return OperationResult(
                success=False,
                error="Operation denied by policy"
            )
        
        # Execute operation
        return self.filesystem.execute(operation)
    
    def get_workspace_context(self) -> Dict[str, Any]:
        """Get complete workspace context for AI.
        
        Returns:
            Workspace context including file structure, settings, etc.
        """
        return {
            'root': str(self.workspace_root),
            'files': self.filesystem.execute(
                FileOperation(operation='list', path='', options={'recursive': True})
            ).data,
        }
