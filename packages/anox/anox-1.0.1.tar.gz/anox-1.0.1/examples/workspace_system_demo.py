#!/usr/bin/env python3
"""Example: Complete Anox Workspace System Usage

This example demonstrates the complete workspace system including:
1. WorkspaceCore - Single active workspace management
2. Backend API - Clean separation of concerns
3. UI Adapter - State management for UI
4. WebSocket Protocol - Remote client support
5. Event-driven architecture
"""

import tempfile
import os
from pathlib import Path
import json

# Import workspace components
from workspace import (
    # Core components
    get_workspace_core,
    BackendAPIFacade,
    FileOperation,
    
    # UI components
    get_ui_adapter,
    
    # Protocol
    WorkspaceProtocol,
    WebSocketMessage,
    WorkspaceAction,
    
    # Events
    get_event_bus,
    EventType,
)


def example_1_workspace_core():
    """Example 1: Using WorkspaceCore for workspace management."""
    print("\n" + "="*60)
    print("Example 1: WorkspaceCore - Single Active Workspace")
    print("="*60)
    
    # Get workspace core
    core = get_workspace_core()
    
    # Create temp workspace
    tmpdir = tempfile.mkdtemp()
    print(f"✅ Created temp workspace: {tmpdir}")
    
    # Set as active workspace
    config = core.set_workspace_root(tmpdir, name="My Project")
    print(f"✅ Set active workspace: {config.name}")
    print(f"   Root: {config.root_path}")
    
    # Update workspace settings
    core.update_workspace_settings({
        'editor.fontSize': 14,
        'theme': 'dark',
        'git.enabled': True
    })
    print(f"✅ Updated workspace settings")
    
    # Get settings
    font_size = core.get_workspace_setting('editor.fontSize')
    theme = core.get_workspace_setting('theme')
    print(f"   Font Size: {font_size}")
    print(f"   Theme: {theme}")
    
    # Get workspace info
    info = core.get_workspace_info()
    print(f"✅ Workspace active: {info['active']}")
    print(f"   Settings: {info['settings']}")


def example_2_backend_api():
    """Example 2: Using Backend API for file operations."""
    print("\n" + "="*60)
    print("Example 2: Backend API - File Operations")
    print("="*60)
    
    # Create temp workspace
    tmpdir = Path(tempfile.mkdtemp())
    
    # Initialize backend
    backend = BackendAPIFacade(tmpdir)
    print(f"✅ Initialized backend for: {tmpdir}")
    
    # Write a file
    operation = FileOperation(
        operation='write',
        path='hello.py',
        content='print("Hello, Anox!")'
    )
    result = backend.execute_file_operation(operation)
    
    if result.success:
        print(f"✅ Created file: hello.py")
    
    # Read the file
    operation = FileOperation(operation='read', path='hello.py')
    result = backend.execute_file_operation(operation)
    
    if result.success:
        print(f"✅ Read file content:")
        print(f"   {result.data}")
    
    # List files
    operation = FileOperation(operation='list', path='')
    result = backend.execute_file_operation(operation)
    
    if result.success:
        print(f"✅ Files in workspace:")
        for file in result.data:
            print(f"   - {file.name} ({file.size} bytes)")
    
    # Try to access outside workspace (should fail)
    operation = FileOperation(operation='read', path='../../etc/passwd')
    result = backend.execute_file_operation(operation)
    
    if not result.success:
        print(f"✅ Security check passed:")
        print(f"   Blocked access outside workspace")


def example_3_ui_adapter():
    """Example 3: Using UI Adapter for state management."""
    print("\n" + "="*60)
    print("Example 3: UI Adapter - State Management")
    print("="*60)
    
    # Create temp workspace
    tmpdir = tempfile.mkdtemp()
    core = get_workspace_core()
    core.set_workspace_root(tmpdir)
    
    # Get UI adapter
    ui = get_ui_adapter()
    
    # Get UI state
    state = ui.get_state()
    print(f"✅ UI State:")
    print(f"   Workspace: {state.workspace_root}")
    print(f"   Active: {state.workspace_active}")
    print(f"   Focus: {state.current_focus}")
    print(f"   Panels: {list(state.panels.keys())}")
    
    # Create a test file
    test_file = Path(tmpdir) / 'test.txt'
    test_file.write_text('Hello, UI!')
    
    # Open file through UI adapter
    result = ui.handle_open_file('test.txt')
    if result.success:
        print(f"✅ Opened file through UI:")
        print(f"   Content: {result.data}")
    
    # Toggle panel
    ui.handle_toggle_panel('terminal')
    state = ui.get_state()
    print(f"✅ Toggled terminal visibility:")
    print(f"   Visible: {state.panels['terminal']['visible']}")
    
    # Focus panel
    ui.handle_focus_panel('editor')
    state = ui.get_state()
    print(f"✅ Focused editor:")
    print(f"   Current focus: {state.current_focus}")


def example_4_websocket_protocol():
    """Example 4: Using WebSocket Protocol for remote clients."""
    print("\n" + "="*60)
    print("Example 4: WebSocket Protocol - Remote Communication")
    print("="*60)
    
    # Create temp workspace
    tmpdir = tempfile.mkdtemp()
    core = get_workspace_core()
    core.set_workspace_root(tmpdir)
    
    # Create test file
    test_file = Path(tmpdir) / 'app.py'
    test_file.write_text('def main():\n    print("Hello")\n')
    
    # Initialize protocol
    protocol = WorkspaceProtocol()
    print(f"✅ Initialized WebSocket protocol")
    
    # Example: Get workspace state
    message = WebSocketMessage(
        type='request',
        action=WorkspaceAction.GET_STATE.value,
        data={},
        id='req-1'
    )
    response = protocol.handle_message(message)
    print(f"✅ Get State Request:")
    print(f"   Success: {response.data['success']}")
    print(f"   Workspace Root: {response.data['state']['workspace_root']}")
    
    # Example: Open file
    message = WebSocketMessage(
        type='request',
        action=WorkspaceAction.OPEN_FILE.value,
        data={'path': 'app.py'},
        id='req-2'
    )
    response = protocol.handle_message(message)
    print(f"✅ Open File Request:")
    print(f"   Success: {response.data['success']}")
    print(f"   Content preview: {response.data['content'][:30]}...")
    
    # Example: Save file
    message = WebSocketMessage(
        type='request',
        action=WorkspaceAction.SAVE_FILE.value,
        data={
            'path': 'new_file.py',
            'content': '# New file\nprint("Created via protocol")'
        },
        id='req-3'
    )
    response = protocol.handle_message(message)
    print(f"✅ Save File Request:")
    print(f"   Success: {response.data['success']}")
    
    # Example: Using JSON strings (for real WebSocket)
    json_request = json.dumps({
        'type': 'request',
        'action': 'list_files',
        'data': {'directory': ''},
        'id': 'req-4'
    })
    json_response = protocol.handle_message_json(json_request)
    response_data = json.loads(json_response)
    print(f"✅ List Files Request (JSON):")
    print(f"   Success: {response_data['data']['success']}")
    print(f"   Files: {len(response_data['data']['files'])}")


def example_5_events():
    """Example 5: Event-driven architecture."""
    print("\n" + "="*60)
    print("Example 5: Event System - Reactive Updates")
    print("="*60)
    
    # Get event bus
    event_bus = get_event_bus()
    
    # Create temp workspace
    tmpdir = tempfile.mkdtemp()
    
    # Track events
    events_received = []
    
    def on_workspace_changed(event):
        events_received.append(event)
        print(f"🔔 Event: Workspace root changed")
        print(f"   Old: {event.data.get('old_root')}")
        print(f"   New: {event.data.get('new_root')}")
    
    def on_layout_changed(event):
        events_received.append(event)
        print(f"🔔 Event: Layout changed")
        print(f"   Panel: {event.data.get('panel')}")
    
    # Subscribe to events
    event_bus.subscribe(EventType.WORKSPACE_ROOT_CHANGED, on_workspace_changed)
    event_bus.subscribe(EventType.LAYOUT_CHANGED, on_layout_changed)
    print(f"✅ Subscribed to workspace events")
    
    # Trigger workspace change
    core = get_workspace_core()
    core.set_workspace_root(tmpdir)
    
    # Trigger layout change
    ui = get_ui_adapter()
    ui.handle_toggle_panel('explorer')
    
    print(f"✅ Total events received: {len(events_received)}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Anox Workspace System - Complete Examples")
    print("="*60)
    
    try:
        example_1_workspace_core()
        example_2_backend_api()
        example_3_ui_adapter()
        example_4_websocket_protocol()
        example_5_events()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        print("\nKey Takeaways:")
        print("1. WorkspaceCore manages single active workspace")
        print("2. Backend API provides clean separation of concerns")
        print("3. UI Adapter bridges state and rendering")
        print("4. WebSocket Protocol enables remote clients")
        print("5. Event system makes everything reactive")
        print("\n💡 This architecture is:")
        print("   - Clean and maintainable")
        print("   - Mobile-friendly")
        print("   - Testable and secure")
        print("   - Production-ready")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
