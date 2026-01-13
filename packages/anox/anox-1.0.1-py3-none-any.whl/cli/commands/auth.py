"""Authentication and session management commands."""

from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class AuthManager:
    """Manages user authentication and sessions."""

    def __init__(self, session_file: Path = Path("session/auth.json")):
        self.session_file = session_file
        self.session_file.parent.mkdir(parents=True, exist_ok=True)

    def login(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        model_type: Optional[str] = None,
        model_api_key: Optional[str] = None,
    ) -> bool:
        """
        Login user and create session with model configuration.
        
        Args:
            username: Username (if not provided, will prompt)
            password: Password (if not provided, will prompt)
            model_type: Model type ('offline' or 'online')
            model_api_key: API key for online model
        
        Returns:
            True if login successful
        """
        if not username:
            username = input("Username: ").strip()
        
        if not username:
            print("❌ Username is required")
            return False
        
        if not password:
            import getpass
            password = getpass.getpass("Password: ").strip()
        
        if not password:
            print("❌ Password is required")
            return False
        
        # Model selection
        if not model_type:
            print("\n╭─ Model Selection " + "─" * 60 + "╮")
            print("│                                                                              │")
            print("│  Select model type:                                                          │")
            print("│    1. Offline - Local models (no internet required)                         │")
            print("│    2. Online  - Cloud models (requires API key)                             │")
            print("│                                                                              │")
            print("╰" + "─" * 78 + "╯")
            
            choice = input("\nChoice (1/2): ").strip()
            if choice == "1":
                model_type = "offline"
            elif choice == "2":
                model_type = "online"
            else:
                print("❌ Invalid choice")
                return False
        
        # If online model, require API key
        if model_type == "online" and not model_api_key:
            print("\n╭─ Online Model Configuration " + "─" * 48 + "╮")
            print("│                                                                              │")
            print("│  Select provider:                                                            │")
            print("│    1. OpenAI (GPT-4, GPT-3.5)                                                │")
            print("│    2. Anthropic (Claude)                                                     │")
            print("│    3. Google (Gemini)                                                        │")
            print("│    4. Custom (Any other provider)                                            │")
            print("│                                                                              │")
            print("╰" + "─" * 78 + "╯")
            
            provider_choice = input("\nProvider (1/2/3/4): ").strip()
            provider_map = {
                "1": ("openai", "OpenAI"),
                "2": ("anthropic", "Anthropic"),
                "3": ("google", "Google"),
                "4": ("custom", "Custom"),
            }
            
            if provider_choice not in provider_map:
                print("❌ Invalid provider choice")
                return False
            
            provider, provider_name = provider_map[provider_choice]
            
            # For custom provider, ask for provider name
            if provider_choice == "4":
                custom_provider = input("\nEnter provider name (e.g., 'azure', 'cohere', 'huggingface'): ").strip()
                if not custom_provider:
                    print("❌ Provider name is required")
                    return False
                # Store both lowercase (for internal use) and title case (for display)
                provider = custom_provider.lower()
                provider_name = custom_provider.lower().title()
            
            import getpass
            model_api_key = getpass.getpass(f"\n{provider_name} API Key: ").strip()
            
            if not model_api_key:
                print("❌ API key is required for online models")
                return False
        else:
            provider = None
        
        # Generate AXON API key
        axon_api_key = self._generate_axon_key()
        
        # Create session
        session_data = {
            "username": username,
            "password_hash": self._hash_password(password),
            "model_type": model_type,
            "model_provider": provider if model_type == "online" else None,
            "model_api_key": model_api_key if model_type == "online" else None,
            "axon_api_key": axon_api_key,
            "login_time": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=30)).isoformat(),
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Display success message with Qodo-style formatting
            print("\n" + "╭" + "─" * 78 + "╮")
            print("│" + " ✓ Login Successful".ljust(78) + "│")
            print("│" + "".ljust(78) + "│")
            print("│" + f" User: {username}".ljust(78) + "│")
            print("│" + f" Model: {model_type}".ljust(78) + "│")
            if provider:
                print("│" + f" Provider: {provider}".ljust(78) + "│")
            print("│" + f" Session expires: {session_data['expires'][:10]}".ljust(78) + "│")
            print("│" + "".ljust(78) + "│")
            print("│" + " Your ANOX API Key (save this for API access):".ljust(78) + "│")
            print("│" + f" {axon_api_key}".ljust(78) + "│")
            print("│" + "".ljust(78) + "│")
            print("│" + " You can now use:".ljust(78) + "│")
            print("│" + "   anox chat       - Interactive chat".ljust(78) + "│")
            print("│" + "   anox --ui       - Web interface".ljust(78) + "│")
            print("│" + "   anox status     - Check session".ljust(78) + "│")
            print("│" + "".ljust(78) + "│")
            print("╰" + "─" * 78 + "╯\n")
            
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def _generate_axon_key(self) -> str:
        """Generate a unique ANOX API key."""
        # Use os.urandom and base64 to avoid conflict with local secrets package
        random_bytes = os.urandom(32)
        token = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
        return f"anox_{token}"

    def _hash_password(self, password: str) -> str:
        """Simple password hashing (in production, use proper hashing)."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def logout(self) -> bool:
        """
        Logout user and clear session.
        
        Returns:
            True if logout successful
        """
        if not self.session_file.exists():
            print("⚠️  No active session")
            return False
        
        try:
            # Read current session for confirmation
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            username = session_data.get("username", "unknown")
            
            # Delete session file
            self.session_file.unlink()
            
            print("\n" + "╭" + "─" * 78 + "╮")
            print("│" + f" ✓ Logged out: {username}".ljust(78) + "│")
            print("│" + " Session cleared".ljust(78) + "│")
            print("╰" + "─" * 78 + "╯\n")
            return True
        except Exception as e:
            print(f"❌ Logout failed: {e}")
            return False

    def get_session(self) -> Optional[dict]:
        """
        Get current session if valid.
        
        Returns:
            Session data if valid, None otherwise
        """
        if not self.session_file.exists():
            return None
        
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session expired
            expires = datetime.fromisoformat(session_data.get("expires", ""))
            if datetime.now() > expires:
                print("⚠️  Session expired. Please login again.")
                self.session_file.unlink()
                return None
            
            return session_data
        except Exception:
            return None

    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.get_session() is not None

    def get_username(self) -> Optional[str]:
        """Get current username."""
        session = self.get_session()
        return session.get("username") if session else None

    def get_api_key(self) -> Optional[str]:
        """Get AXON API key from session."""
        session = self.get_session()
        if session and session.get("axon_api_key"):
            return session["axon_api_key"]
        
        return None

    def get_model_api_key(self) -> Optional[str]:
        """Get model provider API key from session."""
        session = self.get_session()
        if session and session.get("model_api_key"):
            return session["model_api_key"]
        
        # Fallback to environment variables
        model_type = session.get("model_type") if session else None
        provider = session.get("model_provider") if session else None
        
        if model_type == "online" and provider:
            env_var_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GOOGLE_API_KEY",
            }
            
            # For predefined providers, use the map
            if provider in env_var_map:
                return os.environ.get(env_var_map[provider])
            
            # For custom providers, try common patterns
            # E.g., 'azure' -> 'AZURE_API_KEY', 'cohere' -> 'COHERE_API_KEY'
            custom_env_var = f"{provider.upper()}_API_KEY"
            return os.environ.get(custom_env_var)
        
        return None


def run_login(username: Optional[str] = None, password: Optional[str] = None) -> None:
    """Run login command."""
    print("\n" + "╭" + "─" * 78 + "╮")
    print("│" + " ANOX Login".center(78) + "│")
    print("╰" + "─" * 78 + "╯")
    
    auth = AuthManager()
    
    # Check if already logged in
    if auth.is_logged_in():
        current_user = auth.get_username()
        response = input(f"\nAlready logged in as '{current_user}'. Login as different user? (y/N): ").strip().lower()
        if response != 'y':
            print("\nLogin cancelled.\n")
            return
        auth.logout()
    
    # Perform login
    auth.login(username, password)


def run_logout() -> None:
    """Run logout command."""
    print("\n" + "╭" + "─" * 78 + "╮")
    print("│" + " ANOX Logout".center(78) + "│")
    print("╰" + "─" * 78 + "╯")
    
    auth = AuthManager()
    
    if not auth.is_logged_in():
        print("\n⚠️  Not logged in\n")
        return
    
    # Confirm logout
    username = auth.get_username()
    response = input(f"\nLogout '{username}'? (y/N): ").strip().lower()
    if response == 'y':
        auth.logout()
    else:
        print("\nLogout cancelled.\n")


def check_auth() -> bool:
    """Check authentication status."""
    auth = AuthManager()
    
    if auth.is_logged_in():
        session = auth.get_session()
        
        print("\n" + "╭" + "─" * 78 + "╮")
        print("│" + " Session Status".center(78) + "│")
        print("│" + "".ljust(78) + "│")
        print("│" + f" ✓ Logged in as: {session.get('username')}".ljust(78) + "│")
        print("│" + f" Model Type: {session.get('model_type')}".ljust(78) + "│")
        
        if session.get('model_provider'):
            print("│" + f" Provider: {session.get('model_provider')}".ljust(78) + "│")
        
        print("│" + f" Session expires: {session.get('expires', '')[:10]}".ljust(78) + "│")
        print("│" + "".ljust(78) + "│")
        
        if session.get('axon_api_key'):
            key = session.get('axon_api_key')
            masked_key = key[:8] + "..." + key[-4:] if len(key) > 12 else key
            print("│" + f" ANOX API Key: {masked_key}".ljust(78) + "│")
        
        print("│" + "".ljust(78) + "│")
        print("╰" + "─" * 78 + "╯\n")
        return True
    else:
        print("\n" + "╭" + "─" * 78 + "╮")
        print("│" + " ⚠️  Not logged in".ljust(78) + "│")
        print("│" + " Run 'anox login' to authenticate".ljust(78) + "│")
        print("╰" + "─" * 78 + "╯\n")
        return False
