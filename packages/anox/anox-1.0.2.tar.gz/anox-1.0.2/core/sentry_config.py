"""Sentry error tracking configuration for AXON."""

from __future__ import annotations

import os
import logging
from typing import Optional

# Lazy import flag - we'll import sentry_sdk only when needed
SENTRY_AVAILABLE = None


def _check_sentry_available():
    """Check if sentry_sdk is available and can be imported safely."""
    global SENTRY_AVAILABLE
    if SENTRY_AVAILABLE is not None:
        return SENTRY_AVAILABLE
    
    try:
        import sentry_sdk  # noqa: F401
        SENTRY_AVAILABLE = True
    except (ImportError, AttributeError, ModuleNotFoundError) as e:
        # Catch AttributeError for eventlet/trio compatibility issues
        # Catch ImportError/ModuleNotFoundError when sentry_sdk is not installed
        SENTRY_AVAILABLE = False
        if not isinstance(e, ImportError):
            # Log non-import errors as they may indicate compatibility issues
            logging.debug('Sentry SDK import failed due to compatibility issue: %s', e)
    
    return SENTRY_AVAILABLE


def init_sentry(
    dsn: Optional[str] = None,
    environment: Optional[str] = None,
    traces_sample_rate: float = 1.0,
    profiles_sample_rate: float = 1.0,
    send_default_pii: bool = True,
    enable_tracing: bool = True,
) -> bool:
    """
    Initialize Sentry error tracking.
    
    Args:
        dsn: Sentry DSN (Data Source Name). If not provided, reads from SENTRY_DSN env var.
        environment: Environment name (e.g., 'production', 'development')
        traces_sample_rate: Percentage of transactions to trace (0.0 to 1.0)
        profiles_sample_rate: Percentage of transactions to profile (0.0 to 1.0)
        send_default_pii: Add data like request headers and IP for users
        enable_tracing: Enable tracing for performance monitoring
    
    Returns:
        True if Sentry was initialized successfully, False otherwise
    """
    if not _check_sentry_available():
        # Silently skip if Sentry is not available or has compatibility issues
        return False
    
    # Get DSN from parameter or environment variable
    # Default DSN for the project
    default_dsn = "https://fb6269384565414e9c125beef9fa3787@o4510683697840128.ingest.us.sentry.io/4510683710357504"
    sentry_dsn = dsn or os.getenv('SENTRY_DSN') or default_dsn
    
    if not sentry_dsn:
        print("ℹ️  Sentry DSN not configured. Error tracking is disabled.")
        print("   Set SENTRY_DSN environment variable to enable error tracking.")
        return False
    
    # Determine environment
    if environment is None:
        environment = os.getenv('SENTRY_ENVIRONMENT', 'development')
    
    # Initialize Sentry - import here to avoid early import issues
    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment,
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            send_default_pii=send_default_pii,
            enable_tracing=enable_tracing,
            integrations=[
                LoggingIntegration(
                    level=logging.INFO,  # Capture info and above for better logging
                    event_level=logging.ERROR,  # Send errors as events
                ),
            ],
            # Set release version if available
            release=os.getenv('SENTRY_RELEASE', 'axon@1.0.0'),
            # Additional options
            attach_stacktrace=True,
            before_send=before_send_filter,
        )
        print(f"✅ Sentry error tracking initialized (environment: {environment})")
        return True
    except Exception as e:
        print(f"⚠️  Failed to initialize Sentry: {e}")
        return False


def before_send_filter(event, hint):
    """
    Filter events before sending to Sentry.
    
    This function allows filtering out certain events or modifying them
    before they are sent to Sentry.
    """
    # Don't send events for expected errors
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        
        # Filter out keyboard interrupts
        if exc_type.__name__ == 'KeyboardInterrupt':
            return None
        
        # Filter out expected connection errors during development
        if 'ConnectionRefusedError' in str(exc_type):
            return None
    
    return event


def capture_exception(error: Exception, context: Optional[dict] = None) -> Optional[str]:
    """
    Capture an exception and send it to Sentry.
    
    Args:
        error: The exception to capture
        context: Additional context to include with the error
    
    Returns:
        Event ID if successful, None otherwise
    """
    if not _check_sentry_available():
        return None
    
    try:
        import sentry_sdk
        
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                return sentry_sdk.capture_exception(error)
        else:
            return sentry_sdk.capture_exception(error)
    except Exception:
        # Silently fail if Sentry capture fails
        return None


def capture_message(message: str, level: str = 'info', context: Optional[dict] = None) -> Optional[str]:
    """
    Capture a message and send it to Sentry.
    
    Args:
        message: The message to capture
        level: Message level ('debug', 'info', 'warning', 'error', 'fatal')
        context: Additional context to include with the message
    
    Returns:
        Event ID if successful, None otherwise
    """
    if not _check_sentry_available():
        return None
    
    try:
        import sentry_sdk
        
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                return sentry_sdk.capture_message(message, level=level)
        else:
            return sentry_sdk.capture_message(message, level=level)
    except Exception:
        # Silently fail if Sentry capture fails
        return None


def set_user_context(user_id: str, username: Optional[str] = None, email: Optional[str] = None):
    """
    Set user context for error tracking.
    
    Args:
        user_id: Unique user identifier
        username: Username (optional)
        email: Email address (optional)
    """
    if not _check_sentry_available():
        return
    
    try:
        import sentry_sdk
        
        sentry_sdk.set_user({
            'id': user_id,
            'username': username,
            'email': email,
        })
    except Exception:
        pass


def add_breadcrumb(message: str, category: str = 'default', level: str = 'info', data: Optional[dict] = None):
    """
    Add a breadcrumb to track user actions leading to an error.
    
    Args:
        message: Breadcrumb message
        category: Category of the breadcrumb
        level: Level of the breadcrumb ('debug', 'info', 'warning', 'error')
        data: Additional data for the breadcrumb
    """
    if not _check_sentry_available():
        return
    
    try:
        import sentry_sdk
        
        sentry_sdk.add_breadcrumb(
            message=message,
            category=category,
            level=level,
            data=data or {},
        )
    except Exception:
        pass


def start_profiler():
    """
    Manually start the Sentry profiler.
    
    This allows you to profile specific sections of code by calling start_profiler()
    before the code and stop_profiler() after.
    
    Example:
        start_profiler()
        # Your code to profile
        stop_profiler()
    """
    if not _check_sentry_available():
        return
    
    try:
        import sentry_sdk
        sentry_sdk.profiler.start_profiler()
    except Exception:
        pass


def stop_profiler():
    """
    Manually stop the Sentry profiler.
    
    Note: Calls to stop_profiler are optional - if you don't stop the profiler,
    it will keep profiling your application until the process exits or stop_profiler is called.
    """
    if not _check_sentry_available():
        return
    
    try:
        import sentry_sdk
        sentry_sdk.profiler.stop_profiler()
    except Exception:
        pass
