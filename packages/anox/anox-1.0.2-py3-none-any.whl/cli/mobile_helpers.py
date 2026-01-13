"""Mobile-friendly CLI helpers for Termux and touch-based terminals."""

from __future__ import annotations

import os
import sys


def is_mobile_environment() -> bool:
    """
    Detect if running in a mobile environment (Termux, etc.).
    
    Returns:
        True if running on mobile, False otherwise
    """
    # Check for Termux environment variable
    prefix = os.environ.get('PREFIX', '')
    if prefix and ('com.termux' in prefix or prefix.endswith('com.termux')):
        return True
    
    # Check for Termux-specific paths
    if os.path.exists('/data/data/com.termux'):
        return True
    
    # Check TERMUX_VERSION environment variable
    if os.environ.get('TERMUX_VERSION'):
        return True
    
    return False


def get_terminal_width() -> int:
    """
    Get terminal width, with mobile-friendly defaults.
    
    Returns:
        Terminal width in characters
    """
    try:
        columns = os.get_terminal_size().columns
        # On mobile, limit to reasonable width for touch typing
        if is_mobile_environment() and columns > 80:
            return 80
        return columns
    except (AttributeError, ValueError, OSError):
        # Default mobile-friendly width
        return 60 if is_mobile_environment() else 80


def print_mobile_header(title: str = "AXON") -> None:
    """
    Print mobile-friendly header.
    
    Args:
        title: Header title
    """
    width = get_terminal_width()
    border = "─" * min(width - 2, 50)
    
    print(f"\n╭{border}╮")
    print(f"│ {title.center(len(border) - 2)} │")
    print(f"╰{border}╯\n")


def print_mobile_menu(options: list[tuple[str, str]], title: str = "Menu") -> None:
    """
    Print mobile-friendly menu with large touch targets.
    
    Args:
        options: List of (key, description) tuples
        title: Menu title
    """
    width = get_terminal_width()
    
    print(f"\n📱 {title}")
    print("─" * min(width, 40))
    
    for key, desc in options:
        # Make the key more visible and touch-friendly
        print(f"  [{key}]  {desc}")
    
    print("─" * min(width, 40))


def print_mobile_help() -> None:
    """Print mobile-specific help with touch-friendly shortcuts."""
    print_mobile_header("AXON Mobile Help")
    
    print("🔥 KILLER LOOP (NEW v2.0!):\n")
    print("  anox smartfix          - 🔥 Auto-fix bugs in one command!")
    print("    --vibe=focus         -    Quick & precise (DEFAULT)")
    print("    --vibe=chill         -    Safe mode for critical code")
    print("    --vibe=hacker        -    Aggressive refactoring")
    print("    --vibe=explain       -    Learn without changing code")
    
    print("\n🎯 Quick Commands (optimized for touch):\n")
    
    # Main commands with clear descriptions
    commands = [
        ("anox quickstart", "🎯 First-time guide (START HERE!)"),
        ("anox init", "🏠 Initialize your project"),
        ("anox sync", "📱 Offline-first sync (mobile wow!)"),
        ("anox chat", "💬 Chat with AI assistant"),
        ("anox --ui", "🌐 Web interface (best for mobile)"),
        ("anox mobile", "📡 Mobile API server"),
        ("anox -h", "❓ Show help menu"),
    ]
    
    for cmd, desc in commands:
        print(f"  {cmd:18} - {desc}")
    
    print("\n✨ Mobile 'Wow' Features:")
    features = [
        "• anox smartfix - One command fixes everything! < 30 sec",
        "• anox sync - Works offline, syncs when back online!",
        "• Vibe control - 4 behavior modes for different needs",
        "• Survives network drops - never lose your context",
        "• Bandwidth-aware - adapts to poor connections",
        "• Quick resume - pick up where you left off",
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n📍 Mobile Tips:")
    tips = [
        "• Use web UI (anox --ui) for best mobile experience",
        "• Swipe keyboard for faster typing",
        "• Use volume up/down as arrow keys in Termux",
        "• Long-press for copy/paste",
        "• Ctrl+C to stop any command",
    ]
    
    for tip in tips:
        print(f"  {tip}")
    
    print("\n📲 Termux-specific:")
    termux_tips = [
        "• Install: pkg install python git",
        "• Storage: termux-setup-storage",
        "• Keyboard: Install Hacker's Keyboard app",
        "• Shortcuts: Create widget shortcuts",
    ]
    
    for tip in termux_tips:
        print(f"  {tip}")
    
    print()


def get_mobile_input(prompt: str = "Choice", default: str = "") -> str:
    """
    Get input with mobile-friendly prompt.
    
    Args:
        prompt: Input prompt text
        default: Default value if user just presses enter
    
    Returns:
        User input string
    """
    if default:
        prompt_text = f"➤ {prompt} [{default}]: "
    else:
        prompt_text = f"➤ {prompt}: "
    
    try:
        result = input(prompt_text).strip()
        return result if result else default
    except (KeyboardInterrupt, EOFError):
        print("\n")
        return default


def confirm_mobile(prompt: str = "Continue?", default: bool = True) -> bool:
    """
    Get yes/no confirmation with mobile-friendly interface.
    
    Args:
        prompt: Confirmation prompt
        default: Default value if user just presses enter
    
    Returns:
        True for yes, False for no
    """
    default_text = "Y/n" if default else "y/N"
    response = get_mobile_input(f"{prompt} ({default_text})", "y" if default else "n")
    
    return response.lower() in ['y', 'yes', '1', 'true']


def clear_screen() -> None:
    """Clear screen in a mobile-friendly way."""
    if is_mobile_environment():
        # On mobile, just add some newlines instead of clearing
        # This preserves scroll history
        print("\n" * 5)
    else:
        # On desktop, clear normally
        os.system('cls' if os.name == 'nt' else 'clear')


def print_mobile_shortcuts() -> None:
    """Print available keyboard shortcuts for mobile."""
    print_mobile_header("⌨️ Keyboard Shortcuts")
    
    shortcuts = [
        ("Ctrl+C", "Cancel/Stop current operation"),
        ("Ctrl+D", "Exit/Logout"),
        ("Ctrl+L", "Clear screen (on some terminals)"),
        ("Vol ↑/↓", "Scroll up/down (Termux)"),
        ("Vol ↑+Q", "Show extra keys (Termux)"),
    ]
    
    for key, desc in shortcuts:
        print(f"  {key:12} → {desc}")
    
    print()


def format_mobile_output(text: str, max_width: int = None) -> str:
    """
    Format text for mobile display with appropriate line breaks.
    
    Args:
        text: Text to format
        max_width: Maximum width (defaults to terminal width)
    
    Returns:
        Formatted text
    """
    if max_width is None:
        max_width = get_terminal_width()
    
    # Simple word wrap for mobile
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > max_width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                # Word is too long, break it
                lines.append(word)
                current_length = 0
        else:
            current_line.append(word)
            current_length += word_length
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)


def print_mobile_status(status: str, message: str) -> None:
    """
    Print status message with mobile-friendly formatting.
    
    Args:
        status: Status type ('success', 'error', 'warning', 'info')
        message: Status message
    """
    icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'loading': '⏳',
    }
    
    icon = icons.get(status, '•')
    formatted_msg = format_mobile_output(message, get_terminal_width() - 4)
    
    print(f"{icon} {formatted_msg}\n")


# Convenience functions for common mobile patterns
def mobile_welcome() -> None:
    """Show mobile-optimized welcome screen."""
    if is_mobile_environment():
        print_mobile_header("AXON AI Brain v2.0")
        print("📱 Mobile Mode Detected\n")
        print("🔥 NEW: The Killer Loop!")
        print("  anox smartfix --vibe=focus   (< 30 sec bug fix!)")
        print("\n🎯 First time? Run: anox quickstart")
        print("\nFor best mobile experience, try:")
        print("  • anox smartfix  (One-command auto-fix)")
        print("  • anox sync      (Offline-first sync)")
        print("  • anox --ui      (Touch-friendly web UI)")
        print("  • anox chat      (Chat mode)")
        print("\nType 'anox -h' for mobile help\n")


def mobile_command_menu() -> str:
    """
    Show mobile-optimized command menu and get selection.
    
    Returns:
        Selected command
    """
    options = [
        ("1", "💬 Chat with AI"),
        ("2", "🌐 Open Web UI"),
        ("3", "📱 Start Mobile API"),
        ("4", "⚙️ Setup/Config"),
        ("5", "❓ Help"),
        ("6", "🚪 Exit"),
    ]
    
    print_mobile_menu(options, "Quick Commands")
    
    choice = get_mobile_input("Select option (1-6)", "1")
    
    command_map = {
        "1": "chat",
        "2": "ui",
        "3": "mobile",
        "4": "setup",
        "5": "help",
        "6": "exit",
    }
    
    return command_map.get(choice, "help")


if __name__ == "__main__":
    # Demo/test mobile helpers
    print(f"Mobile environment: {is_mobile_environment()}")
    print(f"Terminal width: {get_terminal_width()}")
    print()
    
    mobile_welcome()
    print_mobile_help()
    print_mobile_shortcuts()
