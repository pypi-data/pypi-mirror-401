"""Chat command for interactive conversation with ANOX."""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from cli.commands.auth import AuthManager
from control.setup import SetupController
from core.orchestrator import DecisionOrchestrator
from core.orchestrator_factory import create_orchestrator
from models.config import ModelConfigManager
from models.offline_llama import OfflineLlamaAdapter
from models.online_api import OnlineAPIAdapter
from models.router import ModelRouter


class ChatInterface:
    """Interactive chat interface for ANOX with Qodo-style UI."""

    def __init__(self) -> None:
        self._orchestrator: Optional[DecisionOrchestrator] = None
        self._running: bool = False
        self._model_router: Optional[ModelRouter] = None
        self._session_id: str = datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())
        self._version: str = "1.0.0"
        self._auth_manager = AuthManager()

    def initialize(self) -> None:
        """Initialize the chat system."""
        controller = SetupController()
        profile = controller.run()
        
        # Load model configuration
        model_config_manager = ModelConfigManager()
        
        # Initialize models
        offline_config = model_config_manager.get_default_offline_model()
        online_config = model_config_manager.get_default_online_model()
        
        if offline_config and offline_config.model_path:
            offline_model = OfflineLlamaAdapter(
                model_path=offline_config.model_path,
                name=offline_config.name,
                **offline_config.options
            )
        else:
            from models.offline_adapter import OfflineModelAdapter
            offline_model = OfflineModelAdapter()
        
        online_model = None
        if online_config:
            online_model = OnlineAPIAdapter(
                provider=online_config.provider,
                model_name=online_config.model_name,
                api_key=online_config.api_key,
                name=online_config.name,
            )
        
        router_config = model_config_manager.get_router_config()
        model_router = ModelRouter(
            offline_model=offline_model,
            online_model=online_model,
            prefer_online=router_config.prefer_online,
            auto_fallback=router_config.auto_fallback,
        )
        self._model_router = model_router

        # Use factory to create orchestrator (eliminates duplication)
        self._orchestrator = create_orchestrator(
            model_router=model_router,
            log_file="logs/chat.log"
        )

    def start(self) -> None:
        """Start the chat interface with Qodo-style UI."""
        if not self._orchestrator:
            self.initialize()

        # Check authentication
        session = self._auth_manager.get_session()
        username = session.get("username", "Guest") if session else "Guest"
        
        self._running = True
        
        # Display welcome banner (Qodo-style)
        self._display_welcome_banner(username)
        
        # Get model info
        model_info = self._get_current_model_info()
        
        print(f"\n{'─' * 80}")
        print(f" Model: {model_info}")
        print(f" Status: ● Connected")
        print(f" Pipeline: Intent → Policy → Risk → Plan → Execute → Response")
        print(f"{'─' * 80}\n")

        while self._running:
            try:
                # Qodo-style prompt
                user_input = input("\n> Your wish is my command\n  ").strip()
            except KeyboardInterrupt:
                print("\n\n[Ctrl+C] Use /exit to quit properly")
                continue
            except EOFError:
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                self._handle_command(user_input)
                continue

            # Process user input through orchestrator
            try:
                decision = self._orchestrator.execute_pipeline(
                    raw_input=user_input,
                    source="human",  # Changed from "chat" to valid source
                    role="developer",  # Changed from "user" to valid role
                    subject_id=username,
                )

                if decision.response:
                    print(f"\n┌─ ANOX Response")
                    print(f"│")
                    for line in decision.response.split('\n'):
                        print(f"│ {line}")
                    print(f"└{'─' * 78}")
                    
                    # Show execution info if available
                    if decision.execution_result and decision.execution_result.success:
                        result = decision.execution_result
                        print(f"\n✓ Executed {len(result.results)} tasks successfully")
                        
                elif decision.decision == "REFUSE":
                    print(f"\n❌ Request refused: {decision.veto_reason or 'Policy restriction.'}")
                elif decision.decision == "REQUIRE_CONFIRMATION":
                    print(f"\n⚠️  This action requires confirmation.")
                    print(f"   Reason: High-risk operation or domain restriction")
                    print(f"   Risk Level: {decision.risk_level}")
                else:
                    print(f"\n[Decision: {decision.decision}, Risk: {decision.risk_level}]")
                    
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def _display_welcome_banner(self, username: str) -> None:
        """Display Qodo-style welcome banner."""
        banner_width = 80
        print("\n" + "╭" + "─" * (banner_width - 2) + "╮")
        print("│" + " Welcome to ANOX Command".center(banner_width - 2) + "│")
        print("│" + f" Session ID: {self._session_id}".ljust(banner_width - 2) + "│")
        print("│" + f" Version: {self._version} (latest)".ljust(banner_width - 2) + "│")
        print("│" + f" User: {username}".ljust(banner_width - 2) + "│")
        
        # Check if logged in
        if self._auth_manager.is_logged_in():
            session = self._auth_manager.get_session()
            expires = session.get("expires", "")[:10] if session else ""
            print("│" + f" Session expires: {expires}".ljust(banner_width - 2) + "│")
        else:
            print("│" + " ⚠️  Not logged in - Limited features".ljust(banner_width - 2) + "│")
        
        print("╰" + "─" * (banner_width - 2) + "╯")
        
        # Tip box
        print("\n╭" + "─" * (banner_width - 2) + "╮")
        print("│" + " Tip: Type /help for commands • [Ctrl+C] to cancel • /exit to quit".ljust(banner_width - 2) + "│")
        print("╰" + "─" * (banner_width - 2) + "╯")

    def _get_current_model_info(self) -> str:
        """Get current model information."""
        if not self._model_router:
            return "No model loaded"
        
        info = self._model_router.get_model_info()
        offline = info.get("offline_model", {})
        online = info.get("online_model", {})
        
        if info.get("prefer_online") and online:
            return f"{online.get('provider', 'unknown')}/{online.get('model', 'unknown')}"
        else:
            return f"offline/{offline.get('name', 'unknown')}"

    def _handle_command(self, command: str) -> None:
        """Handle chat commands."""
        cmd = command.lower().strip()
        
        if cmd == "/exit" or cmd == "/quit":
            print("\n" + "─" * 80)
            print(" Goodbye! Session saved.")
            print("─" * 80 + "\n")
            self._running = False
        elif cmd == "/help" or cmd == "/?":
            self._show_help()
        elif cmd == "/clear":
            if self._orchestrator:
                self._orchestrator.short_term_memory.clear()
                print("\n✓ Conversation history cleared.\n")
        elif cmd == "/models":
            self._show_models()
        elif cmd == "/switch":
            self._switch_model()
        elif cmd == "/status":
            self._show_status()
        elif cmd == "/key":
            self._show_api_key()
        else:
            print(f"\n❌ Unknown command: {command}")
            print("   Type /help for available commands.\n")

    def _show_help(self) -> None:
        """Show help with Qodo-style formatting."""
        print("\n╭─ Available Commands " + "─" * 57 + "╮")
        print("│                                                                              │")
        print("│  /help, /?       Show this help message                                     │")
        print("│  /clear          Clear conversation history                                 │")
        print("│  /models         Show available models                                      │")
        print("│  /switch         Switch between online/offline models                       │")
        print("│  /status         Show session and model status                              │")
        print("│  /key            Show your AXON API key                                     │")
        print("│  /exit, /quit    Exit chat                                                  │")
        print("│                                                                              │")
        print("╰" + "─" * 78 + "╯\n")

    def _show_models(self) -> None:
        """Show available models."""
        if not self._model_router:
            print("\n❌ No models available.\n")
            return
        
        info = self._model_router.get_model_info()
        print("\n╭─ Available Models " + "─" * 59 + "╮")
        print("│                                                                              │")
        
        print("│  Offline Model:                                                              │")
        offline = info.get("offline_model", {})
        print(f"│    Name: {offline.get('name', 'Unknown'):<64} │")
        print(f"│    Type: {offline.get('type', 'Unknown'):<64} │")
        print(f"│    Mock Mode: {str(offline.get('mock_mode', False)):<60} │")
        print("│                                                                              │")
        
        if info.get("online_model"):
            print("│  Online Model:                                                               │")
            online = info.get("online_model", {})
            print(f"│    Name: {online.get('name', 'Unknown'):<64} │")
            print(f"│    Provider: {online.get('provider', 'Unknown'):<60} │")
            print(f"│    Mock Mode: {str(online.get('mock_mode', False)):<60} │")
        else:
            print("│  Online Model: Not configured                                                │")
        
        print("│                                                                              │")
        print("│  Router Settings:                                                            │")
        print(f"│    Prefer Online: {str(info.get('prefer_online', False)):<59} │")
        print(f"│    Auto Fallback: {str(info.get('auto_fallback', True)):<59} │")
        print("│                                                                              │")
        print("╰" + "─" * 78 + "╯\n")

    def _switch_model(self) -> None:
        """Switch between online and offline models."""
        if not self._model_router:
            print("\n❌ Model router not available.\n")
            return
        
        current_prefer = self._model_router.prefer_online
        self._model_router.prefer_online = not current_prefer
        
        mode = "online" if self._model_router.prefer_online else "offline"
        print(f"\n✓ Switched to prefer {mode} models.\n")

    def _show_status(self) -> None:
        """Show current status."""
        print("\n╭─ Session Status " + "─" * 60 + "╮")
        print("│                                                                              │")
        
        # Session info
        if self._auth_manager.is_logged_in():
            session = self._auth_manager.get_session()
            if session:
                print(f"│  User: {session.get('username', 'Unknown'):<68} │")
                print(f"│  Session ID: {self._session_id:<62} │")
                expires = session.get("expires", "")[:10]
                print(f"│  Expires: {expires:<67} │")
                if session.get('api_key'):
                    print("│  API Key: ● Configured                                                       │")
        else:
            print("│  Status: ⚠️  Not logged in                                                    │")
        
        print("│                                                                              │")
        
        # Model info
        model_info = self._get_current_model_info()
        print(f"│  Current Model: {model_info:<61} │")
        print("│  Connection: ● Connected                                                     │")
        print("│                                                                              │")
        print("╰" + "─" * 78 + "╯\n")

    def _show_api_key(self) -> None:
        """Show ANOX API key."""
        api_key = self._auth_manager.get_api_key()
        
        print("\n╭─ ANOX API Key " + "─" * 62 + "╮")
        print("│                                                                              │")
        
        if api_key:
            # Mask the key for security
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else api_key
            print(f"│  Key: {masked_key:<70} │")
            print("│                                                                              │")
            print("│  Use this key to authenticate with ANOX API:                                │")
            print("│    curl -H 'X-API-Key: YOUR_KEY' http://localhost:8000/api/v1/...           │")
        else:
            print("│  ⚠️  No API key configured                                                   │")
            print("│                                                                              │")
            print("│  Run 'anox login' to set up your API key                                    │")
        
        print("│                                                                              │")
        print("╰" + "─" * 78 + "╯\n")


def launch_chat() -> None:
    """Launch the chat interface."""
    try:
        chat = ChatInterface()
        chat.start()
    except KeyboardInterrupt:
        print("\n\n" + "─" * 80)
        print(" Session interrupted. Goodbye!")
        print("─" * 80 + "\n")
    except Exception as e:
        print(f"\n❌ Error starting chat: {e}\n")
