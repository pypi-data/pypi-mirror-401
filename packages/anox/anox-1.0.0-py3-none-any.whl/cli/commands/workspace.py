"""Workspace command - Launch Anox workspace interface."""

import sys
import os
from pathlib import Path

from workspace import Workspace, AnoxCopilot


def run_workspace(root_path: str = None, ui_mode: bool = True) -> int:
    """Launch Anox workspace.
    
    Args:
        root_path: Workspace root directory. Defaults to current directory.
        ui_mode: Whether to launch web UI (True) or CLI mode (False).
        
    Returns:
        Exit code.
    """
    try:
        # Initialize workspace
        workspace = Workspace(root_path)
        
        print("╭──────────────────────────────────────────────────╮")
        print("│              🚀 Anox Workspace                   │")
        print("│         VS Code-style + Personal Copilot        │")
        print("╰──────────────────────────────────────────────────╯")
        print()
        print(f"📁 Workspace: {workspace.get_root()}")
        print()
        
        # Initialize Copilot (with BYOK support)
        import os
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if api_key:
            copilot = AnoxCopilot(workspace.get_root(), api_key=api_key)
            print("🧠 Copilot: Enabled (Claude Sonnet)")
            
            # Index codebase
            print("📚 Indexing codebase...")
            files = workspace.list_files(recursive=True)
            file_paths = [f['path'] for f in files if f['is_file']]
            copilot.index_codebase(file_paths)
            print(f"✓ Indexed {len(file_paths)} files")
        else:
            copilot = None
            print("🧠 Copilot: Disabled (No API key found)")
            print("   Set ANTHROPIC_API_KEY to enable")
        
        print()
        
        if ui_mode:
            print("🌐 Launching web interface...")
            print("   Access at: http://localhost:3000")
            print()
            print("Workspace Features:")
            print("  ├─ 📁 File Explorer - Browse all files")
            print("  ├─ ✏️  Editor - Edit with syntax highlighting")
            print("  ├─ 💻 Terminal - Integrated terminal")
            print("  └─ 🔍 Search - Project-wide search")
            
            if copilot:
                print()
                print("Copilot Features:")
                print("  ├─ 🔍 Code Analysis - Real-time warnings")
                print("  ├─ 🔧 Auto-fix - Confident fixes only")
                print("  ├─ 🐛 Error Parsing - Terminal error analysis")
                print("  └─ 💰 Cost Control - Token limits & BYOK")
            
            # Launch web UI with workspace support
            from cli.commands.ui import launch_ui
            return launch_ui(workspace=workspace, copilot=copilot)
        else:
            # CLI mode
            print("💬 CLI Mode - Interactive workspace")
            print("Type 'help' for available commands")
            return _run_cli_mode(workspace, copilot)
        
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def _run_cli_mode(workspace: Workspace, copilot: AnoxCopilot = None) -> int:
    """Run workspace in CLI mode.
    
    Args:
        workspace: Workspace instance.
        copilot: Copilot instance (optional).
        
    Returns:
        Exit code.
    """
    print()
    
    while True:
        try:
            command = input("anox> ").strip()
            
            if not command:
                continue
            
            if command in ('exit', 'quit', 'q'):
                break
            
            if command == 'help':
                _print_help()
                continue
            
            if command == 'info':
                info = workspace.get_workspace_info()
                print(f"Root: {info['root']}")
                print(f"Total files: {info['total_files']}")
                print(f"Open files: {len(info['open_files'])}")
                if copilot:
                    usage = copilot.get_usage()
                    print(f"Copilot tokens: {usage['total_tokens']}")
                continue
            
            if command.startswith('ls'):
                parts = command.split(maxsplit=1)
                path = parts[1] if len(parts) > 1 else None
                files = workspace.list_files(path)
                for f in files:
                    icon = "📁" if f['is_directory'] else "📄"
                    print(f"{icon} {f['name']}")
                continue
            
            if command.startswith('search '):
                query = command[7:]
                results = workspace.search_files(query)
                print(f"Found {len(results)} matches:")
                for r in results[:20]:  # Limit to 20
                    print(f"  {r['file']}:{r['line']} - {r['content'][:60]}")
                continue
            
            # Execute as terminal command
            result = workspace.execute_command(command)
            if result['stdout']:
                print(result['stdout'])
            if result['stderr']:
                print(result['stderr'], file=sys.stderr)
                
                # Parse errors with copilot
                if copilot and not result['success']:
                    errors = copilot.parse_terminal_error(
                        result['stderr'],
                        workspace.get_workspace_info()
                    )
                    if errors:
                        print("\n🧠 Copilot Analysis:")
                        for err in errors:
                            print(f"  {err.get('file', '?')}:{err.get('line', '?')}")
                            print(f"  → {err.get('suggestion', 'No suggestion')}")
            
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            break
    
    return 0


def _print_help():
    """Print CLI help."""
    print("""
Anox Workspace Commands:

  ls [path]          List files
  search <query>     Search in files
  info               Show workspace info
  help               Show this help
  exit, quit, q      Exit workspace

Any other command is executed in the terminal.
""")


def run_workspace_test():
    """Run workspace tests."""
    print("\n🧪 Running Workspace Tests...")
    print("=" * 60)
    
    # Import and run tests
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    try:
        # Run the simple test without pytest
        import test_workspace_v1_simple
        exit_code = test_workspace_v1_simple.main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_workspace_validate():
    """Run workspace DoD validation."""
    print("\n✅ Running Workspace v1 Validation...")
    print("=" * 60)
    
    # Import and run validation
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    try:
        import validate_workspace_v1
        success = validate_workspace_v1.validate_dod()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error running validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_workspace_examples():
    """Run workspace usage examples."""
    print("\n📚 Running Workspace Examples...")
    print("=" * 60)
    
    # Import and run examples
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    try:
        import workspace_examples
        workspace_examples.main()
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(run_workspace())
