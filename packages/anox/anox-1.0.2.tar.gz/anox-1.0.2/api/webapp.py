"""WebSocket server for real-time ANOX web interface."""

from __future__ import annotations

import asyncio
import json
import os
import uuid
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False


class WebSocketServer:
    """WebSocket server for ANOX web interface."""
    
    # Supported online providers
    ONLINE_PROVIDERS = ["openai", "anthropic", "google", "cohere", "huggingface"]
    
    # Supported offline model types
    OFFLINE_TYPES = ["llama", "phi", "mistral", "codellama", "ollama"]

    def __init__(self, port: int = 3456):
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.sessions: Dict[str, dict] = {}
        self._orchestrator = None
        self._model_router = None

    def _init_orchestrator(self):
        """Initialize orchestrator lazily."""
        if self._orchestrator:
            return
        
        try:
            from core.orchestrator_factory import create_orchestrator
            from models.config import ModelConfigManager
            from models.offline_llama import OfflineLlamaAdapter
            from models.online_api import OnlineAPIAdapter
            from models.router import ModelRouter
            
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

            # Use factory to create orchestrator
            self._orchestrator = create_orchestrator(
                model_router=model_router,
                log_file="logs/websocket.log"
            )
            print("✅ Orchestrator initialized")
        except Exception as e:
            print(f"⚠️  Could not initialize orchestrator: {e}")
            print("   WebSocket will run in echo mode")

    async def register(self, websocket: WebSocketServerProtocol) -> str:
        """Register a new WebSocket client."""
        self.clients.add(websocket)
        session_id = datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())
        self.sessions[session_id] = {
            "websocket": websocket,
            "created_at": datetime.now().isoformat(),
        }
        print(f"🔗 New WebSocket connection established")
        print(f"🔗 WebSocket connected to session {session_id} ({len(self.clients)} total)")
        return session_id

    async def unregister(self, websocket: WebSocketServerProtocol):
        """Unregister a WebSocket client."""
        self.clients.discard(websocket)
        # Remove from sessions
        for session_id, session in list(self.sessions.items()):
            if session["websocket"] == websocket:
                del self.sessions[session_id]
                print(f"🔌 WebSocket disconnected from session {session_id}")
                break

    async def handle_message(self, websocket: WebSocketServerProtocol, message: str, session_id: str):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "chat":
                # Handle chat message
                user_message = data.get("message", "")
                response = await self.process_chat(user_message, session_id)
                await websocket.send(json.dumps({
                    "type": "response",
                    "session_id": session_id,
                    "message": response,
                }))
            elif command == "status":
                # Return status with model info
                model_info = self.get_model_info()
                await websocket.send(json.dumps({
                    "type": "status",
                    "session_id": session_id,
                    "clients": len(self.clients),
                    "version": "1.0.0",
                }))
                # Send model info separately
                await websocket.send(json.dumps({
                    "type": "model_info",
                    **model_info
                }))
            elif command == "switch_model":
                # Handle model switching
                model_id = data.get("model_id")
                result = await self.switch_model(model_id)
                await websocket.send(json.dumps({
                    "type": "model_info" if result["success"] else "error",
                    "message": result.get("message", ""),
                    **result.get("model_info", {})
                }))
            elif command == "list_models":
                # List available models
                models = self.list_available_models()
                await websocket.send(json.dumps({
                    "type": "model_list",
                    "models": models
                }))
            elif command == "configure_model":
                # Configure a model provider
                provider = data.get("provider")
                config = data.get("config", {})
                result = await self.configure_model(provider, config)
                await websocket.send(json.dumps({
                    "type": "response" if result["success"] else "error",
                    "message": result["message"]
                }))
            
            # Workspace commands
            elif command == "workspace_info":
                # Return workspace information
                workspace_root = os.getcwd()
                await websocket.send(json.dumps({
                    "type": "workspace_info",
                    "session_id": session_id,
                    "root": workspace_root,
                    "copilot_enabled": self._orchestrator is not None
                }))
            
            elif command == "list_files":
                # List files in workspace
                path = data.get("path", ".")
                recursive = data.get("recursive", False)
                try:
                    files = self._list_directory(path, recursive)
                    await websocket.send(json.dumps({
                        "type": "file_tree",
                        "tree": files
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error listing files: {str(e)}"
                    }))
            
            elif command == "open_file":
                # Open a file and return its content
                file_path = data.get("file", "")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    await websocket.send(json.dumps({
                        "type": "file_content",
                        "file": file_path,
                        "content": content
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error opening file: {str(e)}"
                    }))
            
            elif command == "save_file":
                # Save file content
                file_path = data.get("file", "")
                content = data.get("content", "")
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    await websocket.send(json.dumps({
                        "type": "response",
                        "message": f"File saved: {file_path}"
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error saving file: {str(e)}"
                    }))
            
            elif command == "create_file":
                # Create a new file
                file_path = data.get("file", "")
                content = data.get("content", "")
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    await websocket.send(json.dumps({
                        "type": "response",
                        "message": f"File created: {file_path}"
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error creating file: {str(e)}"
                    }))
            
            elif command == "search":
                # Search in files
                query = data.get("query", "")
                pattern = data.get("pattern", "*")
                case_sensitive = data.get("caseSensitive", False)
                use_regex = data.get("useRegex", False)
                try:
                    results = self._search_files(query, pattern, case_sensitive, use_regex)
                    await websocket.send(json.dumps({
                        "type": "search_results",
                        "results": results
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error searching: {str(e)}"
                    }))
            
            elif command == "execute_command":
                # Execute terminal command
                cmd = data.get("command", "")
                try:
                    import subprocess
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    output = result.stdout + result.stderr
                    has_errors = result.returncode != 0
                    
                    # Parse errors from output
                    error_info = None
                    if has_errors:
                        error_info = self._parse_error(output)
                    
                    await websocket.send(json.dumps({
                        "type": "terminal_output",
                        "output": output,
                        "has_errors": has_errors,
                        "error_info": error_info
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error executing command: {str(e)}"
                    }))
            
            elif command == "copilot_status":
                # Return copilot status
                await websocket.send(json.dumps({
                    "type": "copilot_usage",
                    "total_tokens": 0,
                    "estimated_cost_usd": 0.0
                }))
            
            elif command == "copilot_analyze":
                # Analyze file with copilot
                file_path = data.get("file", "")
                content = data.get("content", "")
                await websocket.send(json.dumps({
                    "type": "copilot_analysis",
                    "warnings": []
                }))
            
            elif command == "copilot_index":
                # Index codebase
                await websocket.send(json.dumps({
                    "type": "response",
                    "message": "Indexing started..."
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON",
            }))

    async def process_chat(self, message: str, session_id: str) -> str:
        """Process chat message through orchestrator."""
        # Initialize orchestrator if not done yet
        if not self._orchestrator:
            self._init_orchestrator()
        
        # If orchestrator is available, use it
        if self._orchestrator:
            try:
                decision = self._orchestrator.execute_pipeline(
                    raw_input=message,
                    source="human",  # Changed from "websocket" to valid source
                    role="developer",  # Changed from "user" to valid role
                    subject_id=session_id,
                )
                
                if decision.response:
                    return decision.response
                elif decision.decision == "REFUSE":
                    return f"❌ Request refused: {decision.veto_reason or 'Policy restriction.'}"
                else:
                    return f"Decision: {decision.decision}, Risk: {decision.risk_level}"
            except Exception as e:
                return f"Error processing message: {e}"
        
        # Fallback to echo mode
        return f"Echo: {message} (Session: {session_id})"

    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information."""
        if self._model_router:
            try:
                info = self._model_router.get_model_info()
                current_model = self._model_router.select_worker()
                return {
                    "model_type": getattr(current_model, "type", "unknown"),
                    "provider": getattr(current_model, "provider", "N/A"),
                    "health": "ready" if current_model.health_check() else "error",
                    "model_name": getattr(current_model, "name", "Unknown"),
                }
            except Exception as e:
                return {
                    "model_type": "offline",
                    "provider": "default",
                    "health": "offline",
                    "model_name": "Default",
                }
        return {
            "model_type": "offline",
            "provider": "default",
            "health": "offline",
            "model_name": "Default (No router)",
        }

    async def switch_model(self, model_id: str) -> Dict[str, Any]:
        """Switch to a different model."""
        try:
            # Determine model type from ID
            is_online = any(provider in model_id for provider in self.ONLINE_PROVIDERS)
            model_type = "online" if is_online else "offline"
            provider = model_id.split("_")[0] if "_" in model_id else model_id
            
            # Here we would implement actual model switching logic
            # For now, return success with model info
            return {
                "success": True,
                "message": f"Switched to model: {model_id}",
                "model_info": {
                    "model_type": model_type,
                    "provider": provider,
                    "health": "loading",
                    "model_name": model_id,
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to switch model: {e}",
            }

    def list_available_models(self) -> List[Dict[str, Any]]:
        """List all available models."""
        models = []
        
        # Add offline models
        models.extend([
            {"id": "offline_default", "name": "Default Offline", "type": "offline", "available": True},
            {"id": "offline_llama", "name": "LLaMA", "type": "offline", "available": False},
            {"id": "offline_phi", "name": "Phi-3", "type": "offline", "available": False},
            {"id": "offline_mistral", "name": "Mistral", "type": "offline", "available": False},
            {"id": "ollama", "name": "Ollama", "type": "offline", "available": False},
        ])
        
        # Add online models
        models.extend([
            {"id": "openai_gpt35", "name": "OpenAI GPT-3.5", "type": "online", "available": False},
            {"id": "openai_gpt4", "name": "OpenAI GPT-4", "type": "online", "available": False},
            {"id": "anthropic_claude", "name": "Anthropic Claude", "type": "online", "available": False},
            {"id": "google_gemini", "name": "Google Gemini", "type": "online", "available": False},
            {"id": "cohere", "name": "Cohere", "type": "online", "available": False},
        ])
        
        return models

    async def configure_model(self, provider: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Configure a model provider."""
        try:
            # Here we would save the configuration and potentially reload models
            # For now, just acknowledge receipt
            return {
                "success": True,
                "message": f"Configuration saved for {provider}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to configure {provider}: {e}"
            }
    
    def _list_directory(self, path: str, recursive: bool = False) -> Dict[str, Any]:
        """List files and directories."""
        import os
        from pathlib import Path
        
        target_path = Path(path)
        if not target_path.exists():
            return {"name": path, "children": []}
        
        result = {
            "name": target_path.name or str(target_path),
            "path": str(target_path),
            "is_directory": target_path.is_dir(),
            "children": []
        }
        
        if target_path.is_dir():
            try:
                items = sorted(target_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                for item in items:
                    # Skip hidden files and common ignored directories
                    if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', '.git']:
                        continue
                    
                    child = {
                        "name": item.name,
                        "path": str(item),
                        "is_directory": item.is_dir()
                    }
                    
                    if recursive and item.is_dir():
                        child.update(self._list_directory(str(item), recursive))
                    
                    result["children"].append(child)
            except PermissionError:
                pass
        
        return result
    
    def _search_files(self, query: str, pattern: str, case_sensitive: bool, use_regex: bool) -> List[Dict[str, Any]]:
        """Search for text in files."""
        import re
        import glob
        from pathlib import Path
        
        results = []
        
        # Find files matching pattern
        files = glob.glob(pattern, recursive=True)
        
        # Search in each file
        for file_path in files:
            try:
                path = Path(file_path)
                if not path.is_file():
                    continue
                
                # Skip binary files and large files
                if path.suffix in ['.pyc', '.so', '.dll', '.exe', '.bin', '.jpg', '.png', '.gif']:
                    continue
                if path.stat().st_size > 1024 * 1024:  # Skip files > 1MB
                    continue
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if use_regex:
                            flags = 0 if case_sensitive else re.IGNORECASE
                            if re.search(query, line, flags):
                                results.append({
                                    "file": file_path,
                                    "line": line_num,
                                    "content": line.strip(),
                                    "match": query
                                })
                        else:
                            search_line = line if case_sensitive else line.lower()
                            search_query = query if case_sensitive else query.lower()
                            if search_query in search_line:
                                results.append({
                                    "file": file_path,
                                    "line": line_num,
                                    "content": line.strip(),
                                    "match": query
                                })
            except Exception:
                continue
        
        return results[:100]  # Limit to 100 results
    
    def _parse_error(self, output: str) -> Optional[Dict[str, Any]]:
        """Parse error information from command output."""
        import re
        
        # Common error patterns
        patterns = [
            # Python errors: File "file.py", line 42
            r'File "([^"]+)", line (\d+)',
            # Node.js errors: at /path/file.js:42:10
            r'at ([^\s:]+):(\d+):',
            # Generic: file.ext:42:
            r'([^\s:]+):(\d+):',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                return {
                    "file": match.group(1),
                    "line": int(match.group(2)),
                    "message": output.split('\n')[0] if '\n' in output else output
                }
        
        return None

    async def handler(self, websocket: WebSocketServerProtocol):
        """Handle WebSocket connection."""
        session_id = await self.register(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message, session_id)
        finally:
            await self.unregister(websocket)

    async def start(self):
        """Start the WebSocket server."""
        if not WEBSOCKETS_AVAILABLE:
            print("❌ websockets library not installed")
            print("   Install with: pip install websockets")
            return
        
        print(f"🔌 Starting WebSocket server on port {self.port}")
        
        # Initialize orchestrator in background
        self._init_orchestrator()
        
        async with websockets.serve(self.handler, "0.0.0.0", self.port):
            print(f"✅ WebSocket server listening on ws://localhost:{self.port}")
            await asyncio.Future()  # Run forever


def create_web_interface(webapp_port: int = 3000, ws_port: int = 3456) -> None:
    """
    Create ANOX web interface with WebSocket support.
    
    Args:
        webapp_port: Port for web app
        ws_port: Port for WebSocket server
    """
    print(f"\n🚀 Starting WebApp on webapp port: {webapp_port}, ws port: {ws_port}")
    
    # Check for agent configuration
    config_files = ["agent.toml", "agent.yaml", "agent.yml"]
    has_config = any(Path(f).exists() for f in config_files)
    
    if not has_config:
        print("No agent configuration file (agent.toml, agent.yaml, or agent.yml) found in the current directory or any parent directory.")
    
    # Start WebSocket server
    server = WebSocketServer(port=ws_port)
    
    print(f"🌐 Opening browser at: http://localhost:{webapp_port}?wsPort={ws_port}")
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n\n🛑 WebSocket server stopped")


def start_webapp(webapp_port: int = 3000, ws_port: int = 3456):
    """Start the web application with HTTP server and WebSocket."""
    print(f"🚀 Web app running on http://localhost:{webapp_port}")
    
    # Start both HTTP server and WebSocket server
    try:
        import threading
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        
        # Change to static directory
        static_dir = Path(__file__).parent / "static"
        if not static_dir.exists():
            print(f"❌ Static directory not found: {static_dir}")
            return
        
        os.chdir(static_dir)
        
        class CustomHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                # Suppress default logging
                pass
            
            def do_GET(self):
                if self.path == '/':
                    self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        
        # Start HTTP server in a separate thread
        httpd = HTTPServer(('0.0.0.0', webapp_port), CustomHandler)
        http_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        http_thread.start()
        
        print(f"✅ HTTP server listening on http://localhost:{webapp_port}")
        
        # Open browser
        webbrowser.open(f"http://localhost:{webapp_port}?wsPort={ws_port}")
        
        # Start WebSocket server (blocking)
        create_web_interface(webapp_port, ws_port)
        
    except Exception as e:
        print(f"❌ Failed to start web app: {e}")
        import traceback
        traceback.print_exc()
