"""ANOX UI launcher - Workspace-enabled WebSocket interface."""

from __future__ import annotations

import os
from typing import Optional


def launch_ui(
    webapp_port: int = 3000,
    ws_port: int = 3456,
    workspace = None,
    copilot = None,
) -> None:
    """
    Launch the WebSocket-based web UI with integrated workspace.
    
    Args:
        webapp_port: Port for web app (default: 3000)
        ws_port: Port for WebSocket server (default: 3456)
        workspace: Optional Workspace instance (auto-created if None)
        copilot: Optional Copilot instance (auto-created if API key available)
    """
    # Initialize workspace if not provided
    if workspace is None:
        from workspace import Workspace
        import os
        workspace = Workspace(os.getcwd())
        print(f"📁 Workspace initialized: {workspace.get_root()}")
    
    # Initialize copilot if not provided and API key available
    if copilot is None:
        from workspace import AnoxCopilot, get_api_key_manager
        from pathlib import Path
        
        # Try to get API key from manager first
        api_manager = get_api_key_manager()
        
        # Import from environment if not already configured
        imported = api_manager.import_from_env()
        if imported:
            print(f"📥 Imported {len(imported)} API key(s) from environment")
        
        # Get active API key
        active_key = api_manager.get_active_key()
        
        if active_key:
            key_id, key_config = active_key
            copilot = AnoxCopilot(
                workspace.get_root(), 
                api_key=key_config.api_key, 
                provider=key_config.provider,
                model=key_config.model
            )
            print(f"🧠 Copilot enabled: {key_config.provider} ({key_config.name})")
        else:
            print("🧠 Copilot disabled: No API key configured")
            print("   Use 'anox config api add <key>' or set environment variable")
    
    # Launch WebSocket-based web app
    print("\n╭" + "─" * 78 + "╮")
    print("│" + " Anox Workspace + Web Interface".center(78) + "│")
    print("│" + " VS Code-style with Multi-Provider AI Copilot".center(78) + "│")
    print("╰" + "─" * 78 + "╯\n")
    
    # Note: workspace and copilot instances will be created within webapp
    # This is for display/logging purposes only
    from api.webapp import start_webapp
    start_webapp(
        webapp_port=webapp_port, 
        ws_port=ws_port
    )
