"""CLI command to view and manage token usage statistics."""

import sys
from models.usage_tracker import get_usage_tracker


def run_usage_command(args: list = None) -> int:
    """View and manage token usage statistics.
    
    Args:
        args: Command arguments
        
    Returns:
        Exit code.
    """
    args = args or []
    
    if not args or args[0] in {'-h', '--help', 'help'}:
        print_help()
        return 0
    
    command = args[0]
    
    if command == 'show':
        return cmd_show(args[1:])
    elif command == 'summary':
        return cmd_summary(args[1:])
    elif command == 'reset':
        return cmd_reset(args[1:])
    else:
        print(f"❌ Unknown command: {command}")
        print_help()
        return 1


def cmd_show(args: list) -> int:
    """Show detailed usage information."""
    tracker = get_usage_tracker()
    
    # Filter by provider if specified
    provider = None
    if args and not args[0].startswith('-'):
        provider = args[0]
    
    tracker.print_summary(provider=provider)
    
    # Check limits
    limits = tracker.check_limits()
    
    print("\n" + "=" * 60)
    print("Limit Check")
    print("=" * 60)
    print(f"Total Tokens: {limits['total_tokens']:,}")
    print(f"Soft Limit: {limits['soft_limit']:,} {'⚠️  REACHED' if limits['soft_limit_reached'] else '✓'}")
    print(f"Hard Limit: {limits['hard_limit']:,} {'❌ REACHED' if limits['hard_limit_reached'] else '✓'}")
    print(f"Usage: {limits['percentage']:.1f}%")
    
    if limits['hard_limit_reached']:
        print("\n⚠️  WARNING: Hard limit reached! Consider adding more credits or resetting usage.")
    elif limits['soft_limit_reached']:
        print("\n⚠️  WARNING: Soft limit reached. Approaching hard limit.")
    
    return 0


def cmd_summary(args: list) -> int:
    """Show quick summary."""
    tracker = get_usage_tracker()
    
    total = tracker.get_total_usage()
    
    print("Quick Usage Summary:")
    print(f"  Total Calls: {total['total_calls']}")
    print(f"  Total Tokens: {total['total_tokens']:,}")
    print(f"  Estimated Cost: ${total['total_cost']:.4f}")
    
    return 0


def cmd_reset(args: list) -> int:
    """Reset usage statistics."""
    # Confirm reset
    if '--yes' not in args and '-y' not in args:
        response = input("Reset all usage statistics? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 0
    
    tracker = get_usage_tracker()
    tracker.reset_usage()
    
    print("✅ Usage statistics reset successfully!")
    return 0


def print_help():
    """Print usage command help."""
    print("""Usage: anox usage <command> [options]

Token Usage Tracking:

Commands:
  show [provider]              Show detailed usage information
                               Optionally filter by provider (anthropic, openai, etc.)
  summary                      Show quick usage summary
  reset                        Reset all usage statistics

Examples:
  # Show all usage
  anox usage show

  # Show Anthropic usage only
  anox usage show anthropic

  # Quick summary
  anox usage summary

  # Reset statistics
  anox usage reset --yes

Cost Control:
  - Soft limit: 100,000 tokens (warning)
  - Hard limit: 500,000 tokens (stop)
  - Usage is tracked per model and provider
  - Costs are estimated based on published pricing
""")


if __name__ == '__main__':
    sys.exit(run_usage_command(sys.argv[1:]))
