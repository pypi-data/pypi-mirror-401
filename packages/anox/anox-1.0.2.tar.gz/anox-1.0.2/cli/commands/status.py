"""Status command - show project and system status."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from cli.commands.init import ProjectInitializer
from cli.commands.auth import AuthManager


def get_project_status() -> Dict[str, Any]:
    """Get current project status."""
    project_path = Path.cwd()
    initializer = ProjectInitializer(project_path)
    
    status = {
        "project_initialized": initializer.is_initialized(),
        "project_path": str(project_path),
    }
    
    if status["project_initialized"]:
        config = initializer.get_config()
        if config:
            status["project_name"] = config.get("project_name", "unknown")
            status["project_type"] = config.get("project_type", "unknown")
            status["initialized_at"] = config.get("initialized_at", "unknown")
        
        # Check for analysis results
        analysis_file = project_path / ".anox" / "analysis" / "latest.json"
        if analysis_file.exists():
            try:
                with open(analysis_file, 'r') as f:
                    analysis = json.load(f)
                    summary = analysis.get("summary", {})
                    status["last_analysis"] = {
                        "timestamp": analysis.get("timestamp", "unknown"),
                        "files": summary.get("total_files", 0),
                        "issues": summary.get("total_issues", 0)
                    }
            except Exception:
                pass
        
        # Check for review results
        review_file = project_path / ".anox" / "reviews" / "latest.json"
        if review_file.exists():
            try:
                with open(review_file, 'r') as f:
                    review = json.load(f)
                    summary = review.get("summary", {})
                    status["last_review"] = {
                        "timestamp": review.get("timestamp", "unknown"),
                        "files": summary.get("total_files", 0),
                        "score": summary.get("average_score", 0)
                    }
            except Exception:
                pass
    
    return status


def get_session_status() -> Dict[str, Any]:
    """Get session status."""
    try:
        auth_manager = AuthManager()
        session = auth_manager.get_session()
        
        if session:
            return {
                "logged_in": True,
                "username": session.get("username", "unknown"),
            }
    except Exception:
        pass
    
    return {"logged_in": False}


def run_status() -> None:
    """Run the status command."""
    print("📊 ANOX Status\n")
    
    # Session status
    session_status = get_session_status()
    print("🔐 Session:")
    if session_status.get("logged_in"):
        print(f"  Status: ✅ Logged in")
        print(f"  User: {session_status.get('username', 'unknown')}")
    else:
        print(f"  Status: ❌ Not logged in")
        print(f"  Tip: Run 'anox login' to log in")
    
    # Project status
    project_status = get_project_status()
    print("\n📁 Project:")
    
    if project_status.get("project_initialized"):
        print(f"  Status: ✅ Initialized")
        print(f"  Name: {project_status.get('project_name', 'unknown')}")
        print(f"  Type: {project_status.get('project_type', 'unknown')}")
        
        # Analysis status
        if "last_analysis" in project_status:
            analysis = project_status["last_analysis"]
            print(f"\n  Last Analysis:")
            print(f"    Files: {analysis['files']}")
            print(f"    Issues: {analysis['issues']}")
        
        # Review status
        if "last_review" in project_status:
            review = project_status["last_review"]
            print(f"\n  Last Review:")
            print(f"    Files: {review['files']}")
            print(f"    Score: {review['score']}/10")
    else:
        print(f"  Status: ❌ Not initialized")
        print(f"  Path: {project_status.get('project_path', 'unknown')}")
        print(f"\n  💡 Run 'anox init' to initialize this project")
    
    print()
