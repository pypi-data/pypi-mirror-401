"""Quick start guide for first-time ANOX users - anox quickstart command."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from cli.mobile_helpers import (
    is_mobile_environment,
    print_mobile_header,
    get_mobile_input,
    confirm_mobile,
    print_mobile_status,
    get_terminal_width,
)


def print_quickstart_banner() -> None:
    """Print welcome banner for quickstart."""
    if is_mobile_environment():
        print_mobile_header("ANOX Quick Start")
    else:
        width = min(get_terminal_width(), 70)
        print("\n" + "=" * width)
        print("🎯 ANOX QUICK START GUIDE".center(width))
        print("Your AI-Powered Code Assistant".center(width))
        print("=" * width + "\n")


def print_happy_path() -> None:
    """Print the happy path workflow."""
    print("📍 THE HAPPY PATH - What You Should Do First:\n")
    
    steps = [
        ("1️⃣ ", "anox init", "Initialize your project (creates .anox/ config)"),
        ("2️⃣ ", "anox analyze", "Analyze your code for issues"),
        ("3️⃣ ", "anox review <file>", "Review specific files in detail"),
        ("4️⃣ ", "anox fix --apply", "Automatically fix detected issues"),
        ("5️⃣ ", "anox status", "Check your project status anytime"),
    ]
    
    for emoji, cmd, desc in steps:
        print(f"{emoji} {cmd:20} → {desc}")
    
    print("\n💡 Pro tip: Start with 'anox init' - that's always step 1!")


def run_interactive_quickstart() -> None:
    """Run interactive quickstart guide."""
    print_quickstart_banner()
    
    print("Welcome! This guide will help you get started with ANOX.\n")
    print("ANOX is a mobile-first AI code assistant that works offline.")
    print("It helps you analyze, review, and fix code with AI.\n")
    
    # Show the happy path
    print_happy_path()
    
    # Ask if user wants to run the workflow
    print("\n" + "─" * 60)
    
    if not confirm_mobile("Would you like to run the happy path now?", default=True):
        print("\n✨ No problem! Run 'anox init' when you're ready to start.")
        print("💡 Tip: Use 'anox --help' to see all available commands.\n")
        return
    
    # Step 1: Initialize
    print("\n" + "=" * 60)
    print("STEP 1: Initialize Project")
    print("=" * 60 + "\n")
    
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    print(f"📦 Project name: {current_dir.name}\n")
    
    if confirm_mobile("Initialize ANOX in this directory?", default=True):
        from cli.commands.init import run_init
        try:
            run_init(force=False)
            print("\n✅ Step 1 complete!\n")
        except Exception as e:
            print(f"\n❌ Initialization failed: {e}")
            print("💡 Try running 'anox init' manually to see detailed error.\n")
            return
    else:
        print("\n⚠️  Skipped initialization. Run 'anox init' manually when ready.\n")
        return
    
    # Step 2: Analyze
    print("\n" + "=" * 60)
    print("STEP 2: Analyze Your Code")
    print("=" * 60 + "\n")
    
    print("This will scan your code files for potential issues.")
    print("It's safe - no files will be modified.\n")
    
    if confirm_mobile("Run code analysis now?", default=True):
        from cli.commands.analyze import run_analyze
        try:
            run_analyze(paths=None)
            print("\n✅ Step 2 complete!\n")
        except Exception as e:
            print(f"\n⚠️  Analysis encountered an issue: {e}")
            print("💡 You can run 'anox analyze' manually later.\n")
    else:
        print("\n⚠️  Skipped analysis. Run 'anox analyze' when ready.\n")
    
    # Completion
    print("\n" + "=" * 60)
    print("🎉 QUICK START COMPLETE!")
    print("=" * 60 + "\n")
    
    print("✨ What you can do next:\n")
    print("  • anox review <file>  - Get detailed review of specific files")
    print("  • anox fix --apply    - Automatically fix detected issues")
    print("  • anox status         - Check project and session status")
    print("  • anox chat           - Interactive chat with AI")
    print("  • anox --ui           - Open web interface (best for mobile)")
    
    if is_mobile_environment():
        print("\n📱 Mobile Detected! Try these mobile-optimized features:")
        print("  • anox --ui          - Touch-friendly web interface")
        print("  • anox sync          - Offline-first context sync")
        print("  • anox mobile        - Mobile API server")
    
    print("\n📚 Documentation: docs/GETTING_STARTED.md")
    print("❓ Help: anox --help\n")


def print_command_overview() -> None:
    """Print overview of all commands."""
    print("\n📋 COMMAND OVERVIEW\n")
    
    categories = {
        "Core Workflow (The Happy Path 🎯)": [
            ("anox init", "Initialize project for AI assistance"),
            ("anox analyze", "Analyze code for issues"),
            ("anox review <files>", "Review specific files"),
            ("anox fix [--apply]", "Fix issues (dry-run by default)"),
            ("anox status", "Check project status"),
        ],
        "Interactive Modes": [
            ("anox", "Run in terminal (CLI mode)"),
            ("anox chat", "Interactive chat with AI"),
            ("anox --ui", "Web interface (WebSocket-based)"),
        ],
        "Mobile Features": [
            ("anox sync", "Offline-first context sync"),
            ("anox mobile", "Mobile API server"),
        ],
        "System Management": [
            ("anox setup", "Initial system configuration"),
            ("anox login", "Login to ANOX"),
            ("anox logout", "Logout from ANOX"),
            ("anox reset", "Reset local state"),
        ],
    }
    
    for category, commands in categories.items():
        print(f"▸ {category}")
        for cmd, desc in commands:
            print(f"  {cmd:25} - {desc}")
        print()


def run_quickstart(interactive: bool = True, show_help: bool = False) -> None:
    """
    Run quickstart command.
    
    Args:
        interactive: Run interactive guide (default: True)
        show_help: Show command overview instead of running guide
    """
    if show_help:
        print_quickstart_banner()
        print_happy_path()
        print_command_overview()
        print("💡 Run 'anox quickstart' to start the interactive guide.\n")
    elif interactive:
        run_interactive_quickstart()
    else:
        print_quickstart_banner()
        print_happy_path()
        print("\n💡 Run 'anox quickstart' for interactive setup.\n")


if __name__ == "__main__":
    # Test the quickstart
    run_quickstart(interactive=False, show_help=True)
