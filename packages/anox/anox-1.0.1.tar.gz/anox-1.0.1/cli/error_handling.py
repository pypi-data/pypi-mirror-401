"""Error handling utilities for ANOX commands."""

from __future__ import annotations

import sys
import traceback
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

from core.sentry_config import capture_exception


class AnoxError(Exception):
    """Base exception for ANOX errors."""
    
    def __init__(self, message: str, recoverable: bool = True, recovery_hint: Optional[str] = None):
        super().__init__(message)
        self.recoverable = recoverable
        self.recovery_hint = recovery_hint


class ProjectNotInitializedError(AnoxError):
    """Raised when project is not initialized."""
    
    def __init__(self):
        super().__init__(
            "Project not initialized",
            recoverable=True,
            recovery_hint="Run 'anox init' to initialize this project"
        )


class ConfigurationError(AnoxError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Configuration error: {message}",
            recoverable=True,
            recovery_hint="Check .anox/config.json or run 'anox init --force'"
        )


class AnalysisError(AnoxError):
    """Raised when analysis fails."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Analysis failed: {message}",
            recoverable=True,
            recovery_hint="Check file permissions and try again"
        )


class ReviewError(AnoxError):
    """Raised when review fails."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Review failed: {message}",
            recoverable=True,
            recovery_hint="Verify file paths and try again"
        )


class FixError(AnoxError):
    """Raised when fix operation fails."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Fix failed: {message}",
            recoverable=True,
            recovery_hint="Use 'anox fix' (dry-run) first to preview changes"
        )


class ModelError(AnoxError):
    """Raised when model operation fails."""
    
    def __init__(self, message: str):
        super().__init__(
            f"Model error: {message}",
            recoverable=True,
            recovery_hint="Check your API key or try offline mode: 'anox setup'"
        )


def handle_command_errors(command_name: str) -> Callable:
    """
    Decorator to handle errors in command functions.
    
    Args:
        command_name: Name of the command for error reporting
        
    Returns:
        Decorated function with error handling
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except AnoxError as e:
                # Handle known ANOX errors
                print(f"\n❌ Error: {e}")
                if e.recovery_hint:
                    print(f"\n💡 Tip: {e.recovery_hint}")
                
                # Log to Sentry
                capture_exception(e, context={
                    'command': command_name,
                    'recoverable': e.recoverable
                })
                
                if not e.recoverable:
                    sys.exit(1)
                return None
                
            except FileNotFoundError as e:
                print(f"\n❌ File not found: {e}")
                print(f"\n💡 Tip: Check that the file path is correct")
                capture_exception(e, context={'command': command_name})
                return None
                
            except PermissionError as e:
                print(f"\n❌ Permission denied: {e}")
                print(f"\n💡 Tip: Check file permissions or run with appropriate access")
                capture_exception(e, context={'command': command_name})
                return None
                
            except KeyboardInterrupt:
                print(f"\n\n⚠️  {command_name} interrupted by user")
                sys.exit(130)  # Standard exit code for Ctrl+C
                
            except Exception as e:
                # Handle unexpected errors
                print(f"\n❌ Unexpected error in {command_name}: {e}")
                print(f"\n📋 Stack trace:")
                traceback.print_exc()
                print(f"\n💡 This is an unexpected error. Please report it to the maintainers.")
                
                # Log to Sentry with full context
                capture_exception(e, context={
                    'command': command_name,
                    'args': str(args),
                    'kwargs': str(kwargs)
                })
                
                sys.exit(1)
        
        return wrapper
    return decorator


def validate_project_initialized(project_path: Path) -> None:
    """
    Validate that a project is initialized.
    
    Args:
        project_path: Path to project directory
        
    Raises:
        ProjectNotInitializedError: If project is not initialized
    """
    config_file = project_path / ".anox" / "config.json"
    if not config_file.exists():
        raise ProjectNotInitializedError()


def validate_file_exists(file_path: Path, file_type: str = "File") -> None:
    """
    Validate that a file exists.
    
    Args:
        file_path: Path to file
        file_type: Type of file for error message
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"{file_type} not found: {file_path}")


def validate_file_readable(file_path: Path) -> None:
    """
    Validate that a file is readable.
    
    Args:
        file_path: Path to file
        
    Raises:
        PermissionError: If file is not readable
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Not a file: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            f.read(1)  # Try to read one character
    except PermissionError:
        raise PermissionError(f"Cannot read file: {file_path}")


def safe_file_read(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read a file with error handling.
    
    Args:
        file_path: Path to file
        encoding: File encoding
        
    Returns:
        File content or None if error
    """
    try:
        validate_file_exists(file_path)
        validate_file_readable(file_path)
        return file_path.read_text(encoding=encoding)
    except UnicodeDecodeError:
        print(f"⚠️  Warning: Could not decode {file_path} as {encoding}")
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not read {file_path}: {e}")
        return None


def safe_json_load(file_path: Path) -> Optional[dict]:
    """
    Safely load JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON or None if error
    """
    import json
    
    content = safe_file_read(file_path)
    if content is None:
        return None
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"⚠️  Warning: Invalid JSON in {file_path}: {e}")
        return None


def safe_json_save(file_path: Path, data: dict) -> bool:
    """
    Safely save JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    import json
    
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not save {file_path}: {e}")
        return False


def with_recovery(message: str) -> Callable:
    """
    Decorator to add recovery message to exceptions.
    
    Args:
        message: Recovery message to display
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, AnoxError):
                    raise
                raise AnoxError(str(e), recovery_hint=message)
        return wrapper
    return decorator
