"""ANOX main entry point - CLI and WebSocket interface."""

from __future__ import annotations

import sys

# Core interactive commands
from cli.commands.chat import launch_chat
from cli.commands.ui import launch_ui
from cli.commands.auth import run_login, run_logout

# Configuration commands
from cli.commands.config import run_config
from cli.commands.usage import run_usage_command

# Development workflow commands
from cli.commands.init import run_init
from cli.commands.analyze import run_analyze
from cli.commands.review import run_review
from cli.commands.fix import run_fix
from cli.commands.smartfix import run_smartfix
from cli.commands.status import run_status

# Test commands
from cli.commands.test import run_test_command

# Command menu
from cli.commands.cmd import run_cmd_menu

# Workspace commands
from cli.commands.workspace import (
    run_workspace,
    run_workspace_test,
    run_workspace_validate,
    run_workspace_examples
)

# Mobile & sync commands
from cli.commands.mobile import launch_mobile_server
from cli.commands.sync import run_sync

# Other commands
from cli.commands.setup import run_setup
from cli.commands.quickstart import run_quickstart
from cli.commands.reset import reset_state
from cli.commands.run import run_brain_cli

from core.sentry_config import init_sentry, capture_exception
from cli.mobile_helpers import is_mobile_environment, print_mobile_help, mobile_welcome


def print_usage() -> None:
    """Display the 5 main commands only / แสดงคำสั่งหลัก 5 คำสั่งเท่านั้น"""
    # Show mobile-specific help if on mobile
    if is_mobile_environment():
        print_mobile_help()
        return
    
    print(
        """
╭──────────────────────────────────────────────────────────────╮
│                    ANOX - AI Assistant                       │
│              Simple. Powerful. Command-line first.           │
╰──────────────────────────────────────────────────────────────╯

คำสั่งหลัก (Main Commands):
  
  anox login              เข้าสู่ระบบ/สมัครสมาชิก
  anox chat               แชทกับ AI ผ่าน CLI
  anox --ui               เปิด Workspace (VS Code style)
  anox cmd                แสดงคำสั่งขั้นสูงทั้งหมด
  anox --help             แสดงความช่วยเหลือ

💡 เริ่มต้น: anox chat
📚 คำสั่งเพิ่มเติม: anox cmd
"""
    )


def main() -> None:
    # Initialize Sentry error tracking
    init_sentry()
    
    # Show mobile welcome if on mobile and no args
    if is_mobile_environment() and len(sys.argv) == 1:
        mobile_welcome()
    
    try:
        args = sys.argv[1:]
        if not args:
            # Default behavior: show main 5 commands
            print_usage()
            return

        command = args[0].lower()
        
        # Authentication commands
        if command == "login":
            run_login()
        elif command == "logout":
            run_logout()
        
        # Configuration commands
        elif command == "config":
            subcommand = args[1] if len(args) > 1 else None
            remaining_args = args[2:] if len(args) > 2 else []
            run_config(subcommand, remaining_args)
        
        # Usage tracking
        elif command == "usage":
            subcommand = args[1] if len(args) > 1 else None
            remaining_args = args[2:] if len(args) > 2 else []
            sys.exit(run_usage_command([subcommand] + remaining_args if subcommand else remaining_args))
        
        # Interactive interfaces
        elif command == "chat":
            launch_chat()
        elif command in {"--ui", "ui"}:
            # WebSocket-based web interface
            ws_port = 3456
            webapp_port = 3000
            
            for arg in args:
                if arg.startswith("--ws-port="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        try:
                            ws_port = int(parts[1])
                        except ValueError:
                            print(f"❌ Error: Invalid ws-port value: {parts[1]}")
                            sys.exit(1)
                    else:
                        print("❌ Error: --ws-port requires a value")
                        sys.exit(1)
                elif arg.startswith("--webapp-port="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        try:
                            webapp_port = int(parts[1])
                        except ValueError:
                            print(f"❌ Error: Invalid webapp-port value: {parts[1]}")
                            sys.exit(1)
                    else:
                        print("❌ Error: --webapp-port requires a value")
                        sys.exit(1)
            
            launch_ui(
                webapp_port=webapp_port,
                ws_port=ws_port,
            )
        
        # Development workflow commands
        elif command == "init":
            force = "--force" in args
            run_init(force=force)
        
        elif command == "analyze":
            # Parse paths and flags
            paths = [arg for arg in args[1:] if not arg.startswith("-")]
            verbose = "--verbose" in args or "-v" in args
            run_analyze(paths or None, verbose=verbose)
        
        elif command == "review":
            # Parse file paths
            paths = [arg for arg in args[1:] if not arg.startswith("-")]
            verbose = "--verbose" in args or "-v" in args
            if not paths:
                print("❌ Error: No files specified for review")
                print("\nUsage: anox review <file1> [file2] ...")
                print("Example: anox review main.py src/utils.py")
                sys.exit(1)
            run_review(paths, verbose=verbose)
        
        elif command == "fix":
            # Parse flags
            dry_run = "--apply" not in args
            paths = [arg for arg in args[1:] if not arg.startswith("-")]
            run_fix(dry_run=dry_run, paths=paths or None)
        
        elif command == "smartfix":
            # Parse smartfix options
            vibe = "focus"
            target = None
            apply = False
            session_id = None
            
            for arg in args[1:]:
                if arg.startswith("--vibe="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        vibe = parts[1]
                    else:
                        print("❌ Error: --vibe requires a value")
                        sys.exit(1)
                elif arg.startswith("--target="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        target = parts[1]
                    else:
                        print("❌ Error: --target requires a value")
                        sys.exit(1)
                elif arg == "--apply":
                    apply = True
                elif arg.startswith("--session="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        session_id = parts[1]
                    else:
                        print("❌ Error: --session requires a value")
                        sys.exit(1)
                elif arg in {"-h", "--help"}:
                    print("Usage: anox smartfix [options]")
                    print("\nOptions:")
                    print("  --vibe=MODE     Set vibe mode (chill, focus, hacker, explain)")
                    print("  --target=PATH   Target specific file or directory")
                    print("  --apply         Apply fixes immediately")
                    print("  --session=ID    Apply previous session")
                    print("\nVibes:")
                    print("  chill    🌊 Ultra-safe (max 1 file)")
                    print("  focus    🎯 Balanced (max 3 files, default)")
                    print("  hacker   ⚡ Aggressive (max 10 files)")
                    print("  explain  📚 Read-only (0 files)")
                    return
            
            run_smartfix(vibe=vibe, target=target, apply=apply, session_id=session_id)
        
        elif command == "status":
            run_status()
        
        # Mobile & sync commands
        elif command == "mobile":
            # Parse mobile server options
            host = "0.0.0.0"
            port = 8000
            
            for arg in args[1:]:
                if arg.startswith("--host="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        host = parts[1]
                    else:
                        print("❌ Error: --host requires a value")
                        sys.exit(1)
                elif arg.startswith("--port="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        try:
                            port = int(parts[1])
                        except ValueError:
                            print(f"❌ Error: Invalid port value: {parts[1]}")
                            sys.exit(1)
                    else:
                        print("❌ Error: --port requires a value")
                        sys.exit(1)
            
            launch_mobile_server(host=host, port=port)
        
        elif command == "sync":
            # Parse sync options
            show_status = "--status" in args
            clear_queue = "--clear" in args
            force = "--force" in args
            run_sync(show_status=show_status, clear_queue=clear_queue, force=force)
        
        # Setup & utility commands
        elif command == "setup":
            profile = None
            for arg in args[1:]:
                if arg.startswith("--profile="):
                    parts = arg.split("=", 1)
                    if len(parts) == 2 and parts[1]:
                        profile = parts[1]
                    else:
                        print("❌ Error: --profile requires a value")
                        sys.exit(1)
            run_setup(profile=profile)
        
        elif command == "quickstart":
            interactive = "--no-interactive" not in args
            show_help = "--help" in args or "-h" in args
            run_quickstart(interactive=interactive, show_help=show_help)
        
        elif command == "reset":
            reset_state()
        
        elif command == "run":
            run_brain_cli()
        
        # Test command
        elif command == "test":
            subcommand = args[1] if len(args) > 1 else None
            run_test_command(subcommand)
        
        # Workspace command
        elif command == "workspace":
            subcommand = args[1] if len(args) > 1 else None
            
            if subcommand == "test":
                run_workspace_test()
            elif subcommand == "validate":
                run_workspace_validate()
            elif subcommand == "examples":
                run_workspace_examples()
            elif subcommand in {"help", "-h", "--help", None}:
                print("""
Usage: anox workspace <command>

Workspace v1 Commands:
  test        Run workspace tests
  validate    Validate all Definition of Done criteria
  examples    Run usage examples
  help        Show this help message

Examples:
  anox workspace test       # Run all workspace tests
  anox workspace validate   # Validate DoD criteria
  anox workspace examples   # Run usage examples
""")
            else:
                print(f"❌ Error: Unknown workspace command '{subcommand}'")
                print("\nRun 'anox workspace help' for available commands")
                sys.exit(1)
        
        # Command menu
        elif command == "cmd":
            run_cmd_menu()
        
        # Help command - shows comprehensive command reference
        elif command in {"-h", "--help", "help"}:
            run_cmd_menu()
        
        else:
            print(f"❌ Unknown command: {command}")
            print("\nRun 'anox --help' to see all available commands")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 ANOX terminated by user")
        sys.exit(0)
    except Exception as e:
        # Capture exception in Sentry
        capture_exception(e, context={'command': ' '.join(sys.argv)})
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
