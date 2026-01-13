"""Initialize project for AI assistance - anox init command."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Optional

from cli.error_handling import (
    handle_command_errors,
    safe_json_save,
    ConfigurationError
)


class ProjectInitializer:
    """Initialize a project for ANOX AI assistance."""
    
    def __init__(self, project_path: Path = None):
        self.project_path = project_path or Path.cwd()
        self.config_file = self.project_path / ".anox" / "config.json"
        
    def is_initialized(self) -> bool:
        """Check if project is already initialized."""
        return self.config_file.exists()
    
    def initialize(self, force: bool = False) -> Dict[str, Any]:
        """
        Initialize project with ANOX configuration.
        
        Args:
            force: Force re-initialization if already initialized
            
        Returns:
            Dictionary with initialization results
        """
        if self.is_initialized() and not force:
            return {
                "success": False,
                "message": "Project already initialized. Use --force to reinitialize.",
                "config_path": str(self.config_file)
            }
        
        try:
            # Create .anox directory
            anox_dir = self.project_path / ".anox"
            anox_dir.mkdir(exist_ok=True)
            
            # Detect project type
            project_type = self._detect_project_type()
            
            # Create default configuration
            config = {
                "version": "1.0",
                "project_name": self.project_path.name,
                "project_type": project_type,
                "initialized_at": self._get_timestamp(),
                "settings": {
                    "auto_fix": False,
                    "auto_review": True,
                    "review_on_commit": False,
                    "excluded_patterns": [
                        "node_modules/**",
                        "venv/**",
                        ".git/**",
                        "*.pyc",
                        "__pycache__/**",
                        "dist/**",
                        "build/**",
                    ]
                }
            }
            
            # Write configuration
            if not safe_json_save(self.config_file, config):
                raise ConfigurationError("Failed to save configuration file")
            
            # Create session directory
            session_dir = anox_dir / "sessions"
            session_dir.mkdir(exist_ok=True)
            
            # Create cache directory
            cache_dir = anox_dir / "cache"
            cache_dir.mkdir(exist_ok=True)
            
            return {
                "success": True,
                "message": f"✓ Project initialized successfully ({project_type})",
                "config_path": str(self.config_file),
                "project_type": project_type,
                "config": config
            }
            
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(f"Initialization failed: {str(e)}")
    
    def _detect_project_type(self) -> str:
        """Detect project type based on files present."""
        if (self.project_path / "package.json").exists():
            return "javascript/typescript"
        elif (self.project_path / "requirements.txt").exists() or (self.project_path / "pyproject.toml").exists():
            return "python"
        elif (self.project_path / "pom.xml").exists() or (self.project_path / "build.gradle").exists():
            return "java"
        elif (self.project_path / "Cargo.toml").exists():
            return "rust"
        elif (self.project_path / "go.mod").exists():
            return "go"
        elif (self.project_path / "composer.json").exists():
            return "php"
        elif (self.project_path / "Gemfile").exists():
            return "ruby"
        else:
            return "unknown"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_config(self) -> Optional[Dict[str, Any]]:
        """Load project configuration."""
        if not self.is_initialized():
            return None
        
        from cli.error_handling import safe_json_load
        return safe_json_load(self.config_file)


@handle_command_errors("init")
def run_init(force: bool = False) -> None:
    """Run the init command."""
    print("🔧 Initializing ANOX for this project...\n")
    
    initializer = ProjectInitializer()
    result = initializer.initialize(force=force)
    
    print(result["message"])
    
    if result["success"]:
        print(f"\n📁 Config saved to: {result['config_path']}")
        print(f"📦 Project type: {result['project_type']}")
        print("\n✨ Next steps:")
        print("  1. Run 'anox analyze' to analyze your code")
        print("  2. Run 'anox review <file>' to review specific files")
        print("  3. Run 'anox fix' to automatically fix issues")
        print("\nTip: Use 'anox status' to see current project status")
