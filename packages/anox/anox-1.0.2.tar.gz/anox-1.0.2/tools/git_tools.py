"""Git operations tool implementation."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.base_tool import Tool


class GitTools(Tool):
    """
    Tool for Git operations.
    
    Provides safe Git operations like status, diff, add, commit.
    All operations are executed in the workspace directory.
    """
    
    tool_id = "git_tools"
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize GitTools.
        
        Args:
            workspace_root: Root directory for Git operations (defaults to cwd)
        """
        self.workspace_root = Path(workspace_root or ".").resolve()
    
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Git operation based on payload.
        
        Args:
            payload: Dictionary with:
                - operation: str (status, diff, add, commit, log)
                - files: List[str] (for add operation)
                - message: str (for commit operation)
                - args: List[str] (additional arguments)
                
        Returns:
            Dictionary with operation result
        """
        operation = payload.get("operation")
        
        if operation == "status":
            return self.status(payload.get("args", []))
        elif operation == "diff":
            return self.diff(payload.get("files"), payload.get("args", []))
        elif operation == "add":
            return self.add(payload.get("files", []))
        elif operation == "commit":
            return self.commit(payload.get("message", ""), payload.get("args", []))
        elif operation == "log":
            return self.log(payload.get("args", []))
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
            }
    
    def _run_git_command(self, args: List[str]) -> Dict[str, Any]:
        """
        Run a Git command safely.
        
        Args:
            args: Git command arguments (without 'git' prefix)
            
        Returns:
            Dictionary with command output or error
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Git command timed out after 30 seconds",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def status(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get Git repository status.
        
        Args:
            args: Additional arguments for git status
            
        Returns:
            Dictionary with status information
        """
        cmd_args = ["status", "--porcelain"] + (args or [])
        result = self._run_git_command(cmd_args)
        
        if not result["success"]:
            return result
        
        # Parse porcelain output
        lines = result["stdout"].split("\n") if result["stdout"] else []
        
        modified = []
        added = []
        deleted = []
        untracked = []
        
        for line in lines:
            if not line:
                continue
            
            status_code = line[:2]
            file_path = line[3:]
            
            if status_code.startswith("M"):
                modified.append(file_path)
            elif status_code.startswith("A"):
                added.append(file_path)
            elif status_code.startswith("D"):
                deleted.append(file_path)
            elif status_code.startswith("?"):
                untracked.append(file_path)
        
        return {
            "success": True,
            "modified": modified,
            "added": added,
            "deleted": deleted,
            "untracked": untracked,
            "clean": len(lines) == 0,
        }
    
    def diff(self, files: Optional[List[str]] = None, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get Git diff.
        
        Args:
            files: Specific files to diff (None for all)
            args: Additional arguments for git diff
            
        Returns:
            Dictionary with diff output
        """
        cmd_args = ["diff"] + (args or [])
        if files:
            cmd_args.extend(["--"] + files)
        
        result = self._run_git_command(cmd_args)
        
        if not result["success"]:
            return result
        
        return {
            "success": True,
            "diff": result["stdout"],
            "has_changes": bool(result["stdout"]),
        }
    
    def add(self, files: List[str]) -> Dict[str, Any]:
        """
        Stage files for commit.
        
        Args:
            files: List of files to add
            
        Returns:
            Dictionary with operation result
        """
        if not files:
            return {
                "success": False,
                "error": "No files specified",
            }
        
        cmd_args = ["add"] + files
        result = self._run_git_command(cmd_args)
        
        if not result["success"]:
            return result
        
        return {
            "success": True,
            "files_added": files,
            "count": len(files),
        }
    
    def commit(self, message: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a Git commit.
        
        Args:
            message: Commit message
            args: Additional arguments for git commit
            
        Returns:
            Dictionary with commit result
        """
        if not message:
            return {
                "success": False,
                "error": "Commit message is required",
            }
        
        cmd_args = ["commit", "-m", message] + (args or [])
        result = self._run_git_command(cmd_args)
        
        if not result["success"]:
            return result
        
        # Extract commit hash from output
        commit_hash = None
        if result["stdout"]:
            # Output format: "[branch hash] message"
            parts = result["stdout"].split()
            if len(parts) >= 2:
                commit_hash = parts[1].strip("[]")
        
        return {
            "success": True,
            "message": message,
            "commit_hash": commit_hash,
            "output": result["stdout"],
        }
    
    def log(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get Git log.
        
        Args:
            args: Additional arguments for git log
            
        Returns:
            Dictionary with log entries
        """
        # Use oneline format for easier parsing
        cmd_args = ["log", "--oneline", "-n", "10"] + (args or [])
        result = self._run_git_command(cmd_args)
        
        if not result["success"]:
            return result
        
        # Parse log entries
        lines = result["stdout"].split("\n") if result["stdout"] else []
        commits = []
        
        for line in lines:
            if not line:
                continue
            
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                commits.append({
                    "hash": parts[0],
                    "message": parts[1],
                })
        
        return {
            "success": True,
            "commits": commits,
            "count": len(commits),
        }
