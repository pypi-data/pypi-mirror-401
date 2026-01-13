"""Launch mobile API server command."""

from __future__ import annotations


def launch_mobile_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Launch the mobile-friendly API server.
    
    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: 8000)
    """
    print("\n=== AXON Mobile API Server ===\n")
    print("Starting mobile-friendly API server...")
    print("This server provides REST endpoints for mobile applications.\n")
    
    try:
        from api.mobile_server import start_mobile_api_server
        start_mobile_api_server(host=host, port=port)
    except ImportError as e:
        print(f"❌ Failed to import mobile server: {e}")
        print("\nMake sure you have installed required dependencies:")
        print("  pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
