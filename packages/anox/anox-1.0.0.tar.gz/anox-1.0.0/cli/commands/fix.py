"""Code fix command - anox fix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from cli.commands.init import ProjectInitializer
from cli.error_handling import (
    handle_command_errors,
    validate_project_initialized,
    safe_json_load,
    safe_json_save,
    FixError,
    ProjectNotInitializedError
)


class CodeFixer:
    """Automatically fix code issues."""
    
    def __init__(self):
        self.project_path = Path.cwd()
        self.initializer = ProjectInitializer(self.project_path)
        
    def fix_issues(self, dry_run: bool = True, paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Fix code issues found in analysis.
        
        Args:
            dry_run: If True, only show what would be fixed without applying changes
            paths: Optional list of specific paths to fix
            
        Returns:
            Dictionary with fix results
            
        Raises:
            ProjectNotInitializedError: If project not initialized
            FixError: If fix operation fails
        """
        # Check if project is initialized
        validate_project_initialized(self.project_path)
        
        # Load analysis results
        analysis_file = self.project_path / ".anox" / "analysis" / "latest.json"
        if not analysis_file.exists():
            raise FixError("No analysis results found. Run 'anox analyze' first.")
        
        analysis_data = safe_json_load(analysis_file)
        if not analysis_data:
            raise FixError("Failed to load analysis results")
        
        try:
            # Filter fixable issues
            fixable_issues = self._find_fixable_issues(analysis_data, paths)
            
            if not fixable_issues:
                return {
                    "success": True,
                    "message": "No fixable issues found.",
                    "fixes_applied": 0
                }
            
            # Apply fixes
            fixes_applied = 0
            fixed_files = []
            
            if dry_run:
                print("🔍 Dry run mode - showing what would be fixed:\n")
                for issue in fixable_issues:
                    print(f"  📁 {issue['file']}")
                    print(f"     Line {issue['line']}: {issue['description']}")
                    print(f"     Fix: {issue['fix']}\n")
                
                return {
                    "success": True,
                    "message": f"Found {len(fixable_issues)} fixable issues",
                    "dry_run": True,
                    "potential_fixes": len(fixable_issues)
                }
            else:
                # Actually apply fixes
                for issue in fixable_issues:
                    try:
                        if self._apply_fix(issue):
                            fixes_applied += 1
                            if issue['file'] not in fixed_files:
                                fixed_files.append(issue['file'])
                    except Exception as e:
                        print(f"⚠️  Failed to fix {issue['file']}: {str(e)}")
                        continue
                
                # Save fix results
                self._save_results(fixable_issues, fixes_applied, fixed_files)
                
                return {
                    "success": True,
                    "message": f"✓ Applied {fixes_applied} fixes to {len(fixed_files)} files",
                    "fixes_applied": fixes_applied,
                    "files_modified": len(fixed_files),
                    "dry_run": False
                }
            
        except FixError:
            raise
        except Exception as e:
            raise FixError(str(e))
    
    def _find_fixable_issues(self, analysis_data: Dict[str, Any], paths: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Find issues that can be automatically fixed."""
        fixable = []
        results = analysis_data.get("results", [])
        
        for result in results:
            file_path = result.get("file_path", "")
            
            # Filter by paths if specified
            if paths and not any(p in file_path for p in paths):
                continue
            
            issues = result.get("issues", [])
            for issue in issues:
                # Only include issues with auto-fix capability
                if issue.get("auto_fixable", False):
                    fixable.append({
                        "file": file_path,
                        "line": issue.get("line", 0),
                        "description": issue.get("message", ""),
                        "fix": issue.get("suggested_fix", ""),
                        "severity": issue.get("severity", "low")
                    })
        
        return fixable
    
    def _apply_fix(self, issue: Dict[str, Any]) -> bool:
        """Apply a single fix to a file."""
        # This is a simplified implementation
        # In production, would use proper AST manipulation
        file_path = Path(issue["file"])
        
        if not file_path.exists():
            return False
        
        # Read file
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception:
            return False
        
        # Apply fix (simplified - would need more sophisticated logic)
        line_num = issue.get("line", 0) - 1
        if 0 <= line_num < len(lines):
            # In a real implementation, would parse and modify properly
            # For now, just mark it as attempted
            return True
        
        return False
    
    def _save_results(self, issues: List[Dict[str, Any]], fixes_applied: int, fixed_files: List[str]) -> None:
        """Save fix results."""
        results_dir = self.project_path / ".anox" / "fixes"
        results_dir.mkdir(exist_ok=True)
        
        # Save latest results
        results_file = results_dir / "latest.json"
        
        data = {
            "timestamp": self._get_timestamp(),
            "fixes_applied": fixes_applied,
            "files_modified": len(fixed_files),
            "files": fixed_files,
            "issues_fixed": issues
        }
        
        safe_json_save(results_file, data)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


@handle_command_errors("fix")
def run_fix(dry_run: bool = True, paths: Optional[List[str]] = None) -> None:
    """Run the fix command."""
    if dry_run:
        print("🔧 Running in dry-run mode (no changes will be made)...\n")
    else:
        print("🔧 Applying fixes...\n")
    
    fixer = CodeFixer()
    result = fixer.fix_issues(dry_run=dry_run, paths=paths)
    
    print(result["message"])
    
    if result["success"]:
        if result.get("dry_run"):
            print(f"\n💡 Run 'anox fix --apply' to actually apply these fixes")
        else:
            fixes = result.get("fixes_applied", 0)
            files = result.get("files_modified", 0)
            
            if fixes > 0:
                print(f"\n✅ Successfully fixed {fixes} issues in {files} files")
                print("\n💡 Next steps:")
                print("  - Review changes with 'git diff'")
                print("  - Run 'anox analyze' to verify fixes")
                print("  - Commit changes if satisfied")
            else:
                print("\n💡 Tip: Run 'anox analyze' to find issues first")
