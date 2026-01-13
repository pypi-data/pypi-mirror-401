"""Code analysis tool implementation."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.base_tool import Tool


class AnalysisTools(Tool):
    """
    Tool for code analysis operations.
    
    Provides basic linting, syntax checking, and code quality analysis.
    """
    
    tool_id = "analysis_tools"
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        Initialize AnalysisTools.
        
        Args:
            workspace_root: Root directory for analysis (defaults to cwd)
        """
        self.workspace_root = Path(workspace_root or ".").resolve()
    
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute analysis operation based on payload.
        
        Args:
            payload: Dictionary with:
                - operation: str (lint, syntax_check, complexity)
                - path: str (file or directory to analyze)
                - language: str (python, javascript, etc.)
                
        Returns:
            Dictionary with analysis result
        """
        operation = payload.get("operation")
        
        if operation == "lint":
            return self.lint_code(payload["path"], payload.get("language"))
        elif operation == "syntax_check":
            return self.check_syntax(payload["path"], payload.get("language"))
        elif operation == "detect_language":
            return self.detect_language(payload["path"])
        else:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}",
            }
    
    def detect_language(self, path: str) -> Dict[str, Any]:
        """
        Detect programming language from file extension.
        
        Args:
            path: File path
            
        Returns:
            Dictionary with detected language
        """
        file_path = Path(path)
        extension = file_path.suffix.lower()
        
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "c",
            ".hpp": "cpp",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".sh": "bash",
        }
        
        language = language_map.get(extension, "unknown")
        
        return {
            "success": True,
            "path": path,
            "language": language,
            "extension": extension,
        }
    
    def check_syntax(self, path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Check file syntax.
        
        Args:
            path: File path
            language: Programming language (auto-detected if not provided)
            
        Returns:
            Dictionary with syntax check results
        """
        try:
            file_path = self.workspace_root / path
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {path}",
                }
            
            # Detect language if not provided
            if not language:
                lang_result = self.detect_language(path)
                language = lang_result.get("language", "unknown")
            
            # Check syntax based on language
            if language == "python":
                return self._check_python_syntax(file_path)
            elif language in ["javascript", "typescript"]:
                return self._check_js_syntax(file_path)
            else:
                return {
                    "success": True,
                    "path": path,
                    "language": language,
                    "valid": True,
                    "note": f"Syntax checking not implemented for {language}",
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def _check_python_syntax(self, file_path: Path) -> Dict[str, Any]:
        """Check Python file syntax using ast module."""
        import ast
        
        try:
            content = file_path.read_text(encoding="utf-8")
            ast.parse(content, filename=str(file_path))
            
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "language": "python",
                "valid": True,
                "errors": [],
            }
        except SyntaxError as e:
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "language": "python",
                "valid": False,
                "errors": [{
                    "line": e.lineno,
                    "column": e.offset,
                    "message": e.msg,
                    "text": e.text.strip() if e.text else "",
                }],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def _check_js_syntax(self, file_path: Path) -> Dict[str, Any]:
        """Check JavaScript/TypeScript syntax using node if available."""
        try:
            # Try using node's --check flag
            result = subprocess.run(
                ["node", "--check", str(file_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "path": str(file_path.relative_to(self.workspace_root)),
                    "language": "javascript",
                    "valid": True,
                    "errors": [],
                }
            else:
                # Parse error message
                errors = self._parse_js_errors(result.stderr)
                return {
                    "success": True,
                    "path": str(file_path.relative_to(self.workspace_root)),
                    "language": "javascript",
                    "valid": False,
                    "errors": errors,
                }
        except FileNotFoundError:
            # Node not available
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "language": "javascript",
                "valid": True,
                "note": "Node.js not available for syntax checking",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def _parse_js_errors(self, error_output: str) -> List[Dict[str, Any]]:
        """Parse JavaScript error output."""
        errors = []
        
        # Pattern: file:line:column: message
        pattern = r"^([^:]+):(\d+):(\d+):\s*(.+)$"
        
        for line in error_output.split("\n"):
            match = re.match(pattern, line)
            if match:
                errors.append({
                    "line": int(match.group(2)),
                    "column": int(match.group(3)),
                    "message": match.group(4),
                })
        
        return errors
    
    def lint_code(self, path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Lint code file.
        
        Args:
            path: File path
            language: Programming language (auto-detected if not provided)
            
        Returns:
            Dictionary with linting results
        """
        try:
            file_path = self.workspace_root / path
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {path}",
                }
            
            # Detect language if not provided
            if not language:
                lang_result = self.detect_language(path)
                language = lang_result.get("language", "unknown")
            
            # Lint based on language
            if language == "python":
                return self._lint_python(file_path)
            else:
                return {
                    "success": True,
                    "path": path,
                    "language": language,
                    "issues": [],
                    "note": f"Linting not implemented for {language}",
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def _lint_python(self, file_path: Path) -> Dict[str, Any]:
        """Lint Python file using basic checks."""
        issues = []
        
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            
            # Basic checks
            for i, line in enumerate(lines, 1):
                # Check line length
                if len(line) > 120:
                    issues.append({
                        "line": i,
                        "type": "style",
                        "message": f"Line too long ({len(line)} > 120 characters)",
                    })
                
                # Check trailing whitespace
                if line.endswith(" ") or line.endswith("\t"):
                    issues.append({
                        "line": i,
                        "type": "style",
                        "message": "Trailing whitespace",
                    })
            
            return {
                "success": True,
                "path": str(file_path.relative_to(self.workspace_root)),
                "language": "python",
                "issues": issues,
                "issue_count": len(issues),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
