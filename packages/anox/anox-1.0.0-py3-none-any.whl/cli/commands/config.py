"""API configuration command for managing API keys."""

import sys
from workspace import get_api_key_manager


def run_config(subcommand: str = None, args: list = None) -> int:
    """Run configuration commands.
    
    Args:
        subcommand: The subcommand (api, etc.)
        args: Additional arguments
        
    Returns:
        Exit code.
    """
    if subcommand == 'api':
        return run_api_config(args or [])
    else:
        print_config_help()
        return 0


def run_api_config(args: list) -> int:
    """Manage API keys.
    
    Args:
        args: Command arguments
        
    Returns:
        Exit code.
    """
    if not args or args[0] in {'-h', '--help', 'help'}:
        print_api_help()
        return 0
    
    manager = get_api_key_manager()
    command = args[0]
    
    if command == 'list':
        return cmd_list(manager, args[1:])
    elif command == 'add':
        return cmd_add(manager, args[1:])
    elif command == 'edit':
        return cmd_edit(manager, args[1:])
    elif command == 'delete':
        return cmd_delete(manager, args[1:])
    elif command == 'import':
        return cmd_import(manager, args[1:])
    else:
        print(f"❌ Unknown command: {command}")
        print_api_help()
        return 1


def cmd_list(manager, args: list) -> int:
    """List API keys."""
    provider = None
    if args and not args[0].startswith('-'):
        provider = args[0]
    
    keys = manager.list(provider=provider, enabled_only=False)
    
    if not keys:
        print("No API keys configured.")
        print("\nAdd a key with: anox config api add <api-key>")
        return 0
    
    print("╭" + "─" * 78 + "╮")
    print("│" + " Configured API Keys".center(78) + "│")
    print("╰" + "─" * 78 + "╯\n")
    
    for key in keys:
        status = "✅" if key['enabled'] else "❌"
        print(f"{status} {key['id']}")
        print(f"   Provider: {key['provider']}")
        print(f"   Name: {key['name']}")
        print(f"   Model: {key['model']}")
        print(f"   Key: {key['api_key_masked']}")
        if key['created_at']:
            print(f"   Created: {key['created_at'][:10]}")
        print()
    
    return 0


def cmd_add(manager, args: list) -> int:
    """Add a new API key."""
    if not args:
        print("❌ Error: API key required")
        print("\nUsage: anox config api add <api-key> [options]")
        print("\nOptions:")
        print("  --name <name>       Custom name for this key")
        print("  --provider <name>   Provider (auto-detected if not specified)")
        print("  --model <model>     Default model to use")
        return 1
    
    api_key = args[0]
    name = None
    provider = None
    model = None
    
    i = 1
    while i < len(args):
        if args[i] == '--name' and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == '--provider' and i + 1 < len(args):
            provider = args[i + 1]
            i += 2
        elif args[i] == '--model' and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        else:
            i += 1
    
    try:
        # Auto-detect provider if not specified
        if provider is None:
            detected = manager.detect_provider(api_key)
            if detected == 'unknown':
                print("❌ Could not auto-detect provider.")
                print("   Please specify with --provider <name>")
                return 1
            provider = detected
        
        key_id = manager.add(api_key=api_key, name=name, provider=provider, model=model)
        
        print("✅ API key added successfully!")
        print(f"   ID: {key_id}")
        print(f"   Provider: {provider}")
        if name:
            print(f"   Name: {name}")
        print(f"\nUse 'anox config api list' to view all keys")
        return 0
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def cmd_edit(manager, args: list) -> int:
    """Edit an existing API key."""
    if not args:
        print("❌ Error: Key ID required")
        print("\nUsage: anox config api edit <key-id> [options]")
        print("\nOptions:")
        print("  --name <name>       New name")
        print("  --key <api-key>     New API key")
        print("  --model <model>     New default model")
        print("  --enable            Enable the key")
        print("  --disable           Disable the key")
        return 1
    
    key_id = args[0]
    new_key = None
    name = None
    model = None
    enabled = None
    
    i = 1
    while i < len(args):
        if args[i] == '--name' and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == '--key' and i + 1 < len(args):
            new_key = args[i + 1]
            i += 2
        elif args[i] == '--model' and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        elif args[i] == '--enable':
            enabled = True
            i += 1
        elif args[i] == '--disable':
            enabled = False
            i += 1
        else:
            i += 1
    
    try:
        success = manager.edit(
            key_id=key_id,
            api_key=new_key,
            name=name,
            model=model,
            enabled=enabled
        )
        
        if success:
            print(f"✅ API key '{key_id}' updated successfully!")
            return 0
        else:
            print(f"❌ Key ID '{key_id}' not found")
            return 1
            
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def cmd_delete(manager, args: list) -> int:
    """Delete an API key."""
    if not args:
        print("❌ Error: Key ID required")
        print("\nUsage: anox config api delete <key-id>")
        return 1
    
    key_id = args[0]
    
    # Confirm deletion
    if '--yes' not in args and '-y' not in args:
        response = input(f"Delete API key '{key_id}'? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 0
    
    success = manager.delete(key_id)
    
    if success:
        print(f"✅ API key '{key_id}' deleted successfully!")
        return 0
    else:
        print(f"❌ Key ID '{key_id}' not found")
        return 1


def cmd_import(manager, args: list) -> int:
    """Import API keys from environment variables."""
    imported = manager.import_from_env()
    
    if not imported:
        print("No API keys found in environment variables.")
        print("\nSupported environment variables:")
        print("  - ANTHROPIC_API_KEY")
        print("  - OPENAI_API_KEY")
        print("  - GOOGLE_API_KEY")
        print("  - COHERE_API_KEY")
        print("  - HUGGINGFACE_API_KEY")
        return 0
    
    print(f"✅ Imported {len(imported)} API key(s):")
    for provider, key_id in imported.items():
        print(f"   - {provider}: {key_id}")
    
    print(f"\nUse 'anox config api list' to view all keys")
    return 0


def print_config_help():
    """Print config command help."""
    print("""Usage: anox config <subcommand>

Configuration Management:

  anox config api <command>    Manage API keys

Use 'anox config api help' for more information on API key management.
""")


def print_api_help():
    """Print API config help."""
    print("""Usage: anox config api <command> [options]

API Key Management:

Commands:
  list [provider]              List all API keys (optionally filter by provider)
  add <api-key> [options]      Add a new API key
  edit <key-id> [options]      Edit an existing API key
  delete <key-id>              Delete an API key
  import                       Import API keys from environment variables

Add Options:
  --name <name>                Custom name for this key
  --provider <provider>        Provider (auto-detected if not specified)
  --model <model>              Default model to use

Edit Options:
  --name <name>                New name
  --key <api-key>              New API key value
  --model <model>              New default model
  --enable                     Enable the key
  --disable                    Disable the key

Examples:
  # Add a key (auto-detects provider)
  anox config api add sk-ant-xxxxx

  # Add with custom name
  anox config api add sk-xxxxx --name "My OpenAI Key"

  # List all keys
  anox config api list

  # Edit a key
  anox config api edit anthropic_1 --name "Production Key"

  # Delete a key
  anox config api delete openai_1

  # Import from environment
  anox config api import

Supported Providers:
  - Anthropic Claude (sk-ant-...)
  - OpenAI (sk-...)
  - Google Gemini (AIza...)
  - Cohere (co-...)
  - HuggingFace (hf_...)

The system automatically detects the provider from the API key format.
""")


if __name__ == '__main__':
    sys.exit(run_config('api', sys.argv[1:]))
