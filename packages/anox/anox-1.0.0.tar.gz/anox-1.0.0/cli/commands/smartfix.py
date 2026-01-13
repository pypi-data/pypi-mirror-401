"""Smart Fix Command - Vibe-driven killer loop for mobile bug fixing.

This is the "One Killer Loop" implementation:
  Error/Bug → AI Fix → Patch + Explanation (vibe-based) → Ready to Commit

Designed to create the "Moment of Wow" on mobile.

Each vibe mode produces MEANINGFULLY DIFFERENT results:
- CHILL: Ultra-conservative, only critical errors, max 1 file
- FOCUS: Targeted bug fixes, efficient, max 3 files
- HACKER: Aggressive refactoring allowed, max 10 files
- EXPLAIN: Analysis only, NO code changes
"""

from __future__ import annotations

import json
import shlex
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from cli.commands.init import ProjectInitializer
from cli.error_handling import (
    handle_command_errors,
    validate_project_initialized,
    safe_json_load,
    safe_json_save,
    FixError,
)
from core.vibe import VibePolicy, VibeMode, get_vibe_description


# Constants
MAX_FILES_TO_SCAN = 20  # Maximum number of files to scan for errors


class SmartFixer:
    """Smart code fixer with vibe-driven behavior."""
    
    def __init__(self, vibe: str = "focus"):
        """Initialize smart fixer with vibe policy.
        
        Args:
            vibe: Vibe mode (chill, focus, hacker, explain)
        """
        self.project_path = Path.cwd().resolve()  # Resolve to absolute path for safety
        # Validate project path is within safe bounds (not root, not system dirs)
        self._validate_project_path()
        self.initializer = ProjectInitializer(self.project_path)
        self.vibe_policy = VibePolicy.from_string(vibe)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _validate_project_path(self) -> None:
        """Validate that project path is safe to work with."""
        # Don't allow root directory
        if self.project_path == Path('/'):
            raise FixError("Cannot run in root directory for safety reasons")
        
        # Don't allow system directories
        system_dirs = ['/bin', '/boot', '/dev', '/etc', '/lib', '/proc', '/root', '/sbin', '/sys', '/usr']
        for sys_dir in system_dirs:
            if self.project_path == Path(sys_dir) or sys_dir in str(self.project_path):
                raise FixError(f"Cannot run in system directory: {sys_dir}")
    
    def auto_detect_and_fix(self, target: Optional[str] = None) -> Dict[str, Any]:
        """
        Automatically detect errors and fix them (killer loop).
        
        This is the ONE KILLER LOOP:
        1. Auto-detect errors/bugs
        2. Generate fix with AI (vibe-aware)
        3. Create patch + explanation
        4. Generate commit message
        5. Ready to apply
        
        Args:
            target: Optional specific file or error to target
            
        Returns:
            Dictionary with fix results, patch, and commit message
        """
        validate_project_initialized(self.project_path)
        
        print(f"🎯 Smart Fix Mode: {self.vibe_policy.mode.value.upper()}")
        print(f"   {get_vibe_description(self.vibe_policy.mode)}")
        print(f"   Max files: {self.vibe_policy.get_max_files_changed()} | Confidence: {self.vibe_policy.get_confidence_level()}\n")
        
        # Step 1: Auto-detect errors
        print("🔍 Step 1/4: Detecting errors...")
        errors = self._auto_detect_errors(target)
        
        if not errors:
            return {
                "success": True,
                "message": "✓ No errors detected! Code looks good.",
                "errors_found": 0,
            }
        
        print(f"   Found {len(errors)} error(s)\n")
        
        # Step 2: Generate fixes (vibe-aware)
        print("🤖 Step 2/4: Generating fixes...")
        fixes = self._generate_vibe_aware_fixes(errors)
        
        # Check vibe policy constraints
        if not self._check_vibe_constraints(fixes):
            return {
                "success": False,
                "message": f"❌ Fixes exceed {self.vibe_policy.mode.value} vibe limits",
                "vibe": self.vibe_policy.mode.value,
                "constraint_violated": True,
            }
        
        print(f"   Generated {len(fixes)} fix(es)\n")
        
        # Step 3: Create patch + explanation
        print("📝 Step 3/4: Creating patch...")
        patch_data = self._create_patch_with_explanation(fixes)
        print("   Patch ready\n")
        
        # Step 4: Generate commit message
        print("💬 Step 4/4: Generating commit message...")
        commit_msg = self._generate_commit_message(fixes)
        print(f"   Message: {commit_msg.split(chr(10))[0]}...\n")
        
        # Save session
        self._save_session(errors, fixes, patch_data, commit_msg)
        
        # Display results
        self._display_results(errors, fixes, patch_data, commit_msg)
        
        return {
            "success": True,
            "message": "✓ Smart fix complete",
            "vibe": self.vibe_policy.mode.value,
            "errors_found": len(errors),
            "fixes_generated": len(fixes),
            "patch": patch_data,
            "commit_message": commit_msg,
            "session_id": self.session_id,
        }
    
    def _auto_detect_errors(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        """Auto-detect errors in code.
        
        Args:
            target: Optional specific file to check
            
        Returns:
            List of detected errors
        """
        errors = []
        
        # Try to detect errors from multiple sources
        # 1. Python syntax errors
        errors.extend(self._detect_python_errors(target))
        
        # 2. Linter errors (if available)
        errors.extend(self._detect_linter_errors(target))
        
        # 3. Analysis results (if available)
        errors.extend(self._detect_from_analysis(target))
        
        # 4. Git status (uncommitted changes that might have issues)
        if self.vibe_policy.mode == VibeMode.HACKER:
            errors.extend(self._detect_from_git_diff())
        
        return errors[:10]  # Limit to top 10 errors
    
    def _detect_python_errors(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        """Detect Python syntax errors."""
        errors = []
        
        # Validate and sanitize target path
        if target:
            target_path = Path(target).resolve()
            # Ensure target is within project path
            try:
                target_path.relative_to(self.project_path)
            except ValueError:
                # Target is outside project, skip
                return errors
        
        # Find Python files
        if target and target_path.exists():
            py_files = [target_path] if target.endswith('.py') else []
        else:
            py_files = list(self.project_path.glob("**/*.py"))
            # Exclude .anox and common directories
            py_files = [f for f in py_files if '.anox' not in str(f) and 'venv' not in str(f)]
        
        for py_file in py_files[:MAX_FILES_TO_SCAN]:
            try:
                code = py_file.read_text(encoding='utf-8')
                compile(code, str(py_file), 'exec')
            except SyntaxError as e:
                errors.append({
                    "type": "syntax_error",
                    "file": str(py_file.relative_to(self.project_path)),
                    "line": e.lineno or 0,
                    "message": str(e.msg),
                    "severity": "high",
                })
            except Exception:
                pass
        
        return errors
    
    def _detect_linter_errors(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        """Detect linter errors using pylint."""
        errors = []
        
        # Validate target path if provided
        if target:
            target_path = Path(target).resolve()
            try:
                target_path.relative_to(self.project_path)
            except ValueError:
                # Target is outside project, skip
                return errors
            # Use relative path for safety
            target_arg = str(target_path.relative_to(self.project_path))
        else:
            target_arg = "."
        
        # Only check if pylint is available
        try:
            # Quick check for common issues
            # Use the validated target_arg which is already relative to project_path
            result = subprocess.run(
                ['python', '-m', 'pylint', '--errors-only', '--output-format=json', target_arg],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            
            if result.stdout:
                try:
                    pylint_results = json.loads(result.stdout)
                    for issue in pylint_results[:5]:  # Top 5
                        errors.append({
                            "type": "linter_error",
                            "file": issue.get("path", "unknown"),
                            "line": issue.get("line", 0),
                            "message": issue.get("message", ""),
                            "severity": "medium",
                        })
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        
        return errors
    
    def _detect_from_analysis(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        """Detect errors from previous analysis."""
        errors = []
        
        analysis_file = self.project_path / ".anox" / "analysis" / "latest.json"
        if analysis_file.exists():
            analysis_data = safe_json_load(analysis_file)
            if analysis_data:
                results = analysis_data.get("results", [])
                for result in results:
                    file_path = result.get("file_path", "")
                    if target and target not in file_path:
                        continue
                    
                    for issue in result.get("issues", [])[:3]:  # Top 3 per file
                        if issue.get("severity") in ["high", "error"]:
                            errors.append({
                                "type": "analysis_issue",
                                "file": file_path,
                                "line": issue.get("line", 0),
                                "message": issue.get("message", ""),
                                "severity": issue.get("severity", "medium"),
                            })
        
        return errors
    
    def _detect_from_git_diff(self) -> List[Dict[str, Any]]:
        """Detect potential issues from git diff (hacker mode only)."""
        errors = []
        
        try:
            result = subprocess.run(
                ['git', 'diff', '--unified=0'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=2,
            )
            
            # Look for common mistake patterns in diff
            if result.stdout:
                # Simple heuristic: lines with "TODO", "FIXME", "XXX", "BUG"
                for line in result.stdout.split('\n'):
                    if any(marker in line.upper() for marker in ['TODO', 'FIXME', 'XXX', 'BUG']):
                        errors.append({
                            "type": "todo_marker",
                            "file": "git-diff",
                            "line": 0,
                            "message": f"Marker found: {line.strip()[:60]}",
                            "severity": "low",
                        })
        except Exception:
            pass
        
        return errors[:3]  # Limit to 3
    
    def _generate_vibe_aware_fixes(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate fixes based on vibe policy.
        
        This is where vibes ACTUALLY MATTER - different vibes produce
        fundamentally different fix strategies.
        
        Args:
            errors: List of detected errors
            
        Returns:
            List of generated fixes
        """
        fixes = []
        confidence = self.vibe_policy.get_confidence_level()
        
        # Sort errors by severity and vibe preference
        sorted_errors = self._prioritize_errors_by_vibe(errors)
        
        for error in sorted_errors:
            # Generate fix with vibe-specific strategy
            fix = self._generate_fix_with_vibe_strategy(error, confidence)
            
            if fix and self._is_fix_allowed_by_vibe(fix):
                fixes.append(fix)
                
                # CHILL mode: Stop after first fix (ultra-conservative)
                if self.vibe_policy.mode == VibeMode.CHILL:
                    break
        
        return fixes
    
    def _prioritize_errors_by_vibe(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize errors based on vibe mode.
        
        Different vibes care about different things:
        - CHILL: Only critical errors
        - FOCUS: High-severity bugs first
        - HACKER: Everything, including refactor opportunities
        - EXPLAIN: All errors for analysis
        """
        if self.vibe_policy.mode == VibeMode.CHILL:
            # Only highest severity
            return [e for e in errors if e.get("severity") == "high"]
        
        elif self.vibe_policy.mode == VibeMode.FOCUS:
            # High and medium severity, sorted by severity
            filtered = [e for e in errors if e.get("severity") in ["high", "medium"]]
            return sorted(filtered, key=lambda e: {"high": 0, "medium": 1}.get(e.get("severity", "medium"), 2))
        
        elif self.vibe_policy.mode == VibeMode.HACKER:
            # Everything, including low severity
            return errors
        
        else:  # EXPLAIN mode
            # All errors for analysis
            return errors
    
    def _generate_fix_with_vibe_strategy(self, error: Dict[str, Any], confidence: str) -> Optional[Dict[str, Any]]:
        """Generate fix using vibe-specific strategy.
        
        This makes vibes REAL - each vibe generates fundamentally different fixes:
        - CHILL: Minimal, surgical changes only
        - FOCUS: Direct bug fixes, no extras
        - HACKER: May refactor entire sections
        - EXPLAIN: No fixes, detailed analysis only
        """
        # EXPLAIN mode: No fixes, only explanation
        if self.vibe_policy.mode == VibeMode.EXPLAIN:
            return {
                "error": error,
                "file": error["file"],
                "line": error["line"],
                "type": "analysis",
                "change": "No changes (explain mode)",
                "explanation": self._generate_explanation(error),
                "risk": "NONE",
                "analysis": self._generate_deep_analysis(error),
            }
        
        fix_type = self._determine_fix_type(error)
        
        # Use confidence to determine strategy
        if confidence == "cautious":
            # CHILL mode: Most conservative fix possible
            change = self._generate_minimal_fix(error)
        elif confidence == "balanced":
            # FOCUS mode: Direct, efficient fix
            change = self._generate_direct_fix(error)
        elif confidence == "aggressive":
            # HACKER mode: Aggressive, may refactor
            change = self._generate_aggressive_fix(error)
        else:  # analytical (EXPLAIN mode, shouldn't reach here)
            change = self._generate_explanation(error)
        
        explanation = self._generate_explanation(error)
        
        return {
            "error": error,
            "file": error["file"],
            "line": error["line"],
            "type": fix_type,
            "change": change,
            "explanation": explanation,
            "risk": self._assess_risk(error),
            "confidence": confidence,
        }
    
    def _generate_minimal_fix(self, error: Dict[str, Any]) -> str:
        """Generate the most minimal fix possible (CHILL mode)."""
        error_msg = error.get("message", "").lower()
        
        if "undefined" in error_msg or "not defined" in error_msg:
            return "Add minimal import or define variable with placeholder"
        elif "syntax" in error_msg:
            return "Fix only the syntax error, change nothing else"
        elif "unused" in error_msg:
            return "Prefix with underscore to mark as intentionally unused"
        else:
            return f"Minimal fix: {error.get('message', '')[:40]}"
    
    def _generate_direct_fix(self, error: Dict[str, Any]) -> str:
        """Generate direct, efficient fix (FOCUS mode)."""
        error_msg = error.get("message", "").lower()
        
        if "undefined" in error_msg or "not defined" in error_msg:
            return "Import required module or define missing variable"
        elif "syntax" in error_msg:
            return "Fix syntax error completely"
        elif "unused" in error_msg:
            return "Remove unused code if safe, otherwise mark with underscore"
        else:
            return f"Fix: {error.get('message', '')}"
    
    def _generate_aggressive_fix(self, error: Dict[str, Any]) -> str:
        """Generate aggressive fix that may refactor (HACKER mode)."""
        error_msg = error.get("message", "").lower()
        
        if "undefined" in error_msg or "not defined" in error_msg:
            return "Refactor imports organization, add proper typing, and ensure all dependencies are explicit"
        elif "syntax" in error_msg:
            return "Fix syntax and improve code style, add type hints if missing"
        elif "unused" in error_msg:
            return "Remove all unused code, clean up imports, refactor if needed"
        else:
            return f"Refactor to fix: {error.get('message', '')} and improve surrounding code"
    
    def _generate_deep_analysis(self, error: Dict[str, Any]) -> str:
        """Generate deep analysis (EXPLAIN mode).
        
        Note: This is a simplified analysis. In production with AI model integration,
        this would provide more detailed context-aware analysis.
        """
        error_type = error.get('type', 'unknown')
        severity = error.get('severity', 'unknown')
        message = error.get('message', 'Unknown error')
        
        return f"""
Deep Analysis:
  Error Type: {error_type}
  Severity: {severity}
  Location: {error['file']}:{error['line']}
  
  Root Cause: {message}
  
  Possible Solutions:
  1. Direct fix at error location
  2. Refactor surrounding code
  3. Add proper error handling
  
  Impact Analysis:
  - Risk of fix: Depends on code context (syntax errors are low risk)
  - Alternatives: Multiple approaches possible depending on context
  - Trade-offs: Speed vs. safety vs. maintainability
  
  Note: With AI model integration, this analysis would be much more detailed
  and context-aware, providing specific recommendations based on code structure.
"""
    
    def _determine_fix_type(self, error: Dict[str, Any]) -> str:
        """Determine type of fix needed."""
        error_type = error.get("type", "")
        
        if error_type == "syntax_error":
            return "syntax_correction"
        elif error_type == "linter_error":
            return "code_improvement"
        elif error_type == "analysis_issue":
            return "bug_fix"
        else:
            return "minor_fix"
    
    def _generate_fix_for_error(self, error: Dict[str, Any]) -> str:
        """Generate fix code for an error.
        
        This is a simplified implementation. In production, would use
        AI model to generate actual fix.
        """
        error_msg = error.get("message", "")
        
        # Simple fix suggestions based on common patterns
        if "undefined" in error_msg.lower() or "not defined" in error_msg.lower():
            return "Add missing import or variable definition"
        elif "syntax" in error_msg.lower():
            return "Fix syntax error (check parentheses, colons, indentation)"
        elif "unused" in error_msg.lower():
            return "Remove unused code or mark with underscore prefix"
        else:
            return f"Fix: {error_msg}"
    
    def _generate_explanation(self, error: Dict[str, Any]) -> str:
        """Generate explanation based on vibe verbosity."""
        verbosity = self.vibe_policy.get_verbosity()
        error_msg = error.get("message", "")
        
        if verbosity == "minimal":
            return error_msg[:50]
        elif verbosity == "normal":
            return f"{error['type']}: {error_msg}"
        elif verbosity == "detailed":
            return f"{error['type']} at {error['file']}:{error['line']}\n{error_msg}\nSeverity: {error.get('severity', 'unknown')}"
        else:  # verbose
            return f"""
Error Details:
  Type: {error['type']}
  File: {error['file']}
  Line: {error['line']}
  Message: {error_msg}
  Severity: {error.get('severity', 'unknown')}
  
This error should be fixed to improve code quality.
"""
    
    def _assess_risk(self, error: Dict[str, Any]) -> str:
        """Assess risk level of fixing this error."""
        severity = error.get("severity", "medium")
        error_type = error.get("type", "")
        
        if error_type == "syntax_error":
            return "LOW"  # Syntax fixes are usually safe
        elif severity == "high":
            return "MEDIUM"
        else:
            return "LOW"
    
    def _is_fix_allowed_by_vibe(self, fix: Dict[str, Any]) -> bool:
        """Check if fix is allowed by current vibe policy."""
        # Check risk level
        max_risk = self.vibe_policy.get_max_risk()
        fix_risk = fix["risk"]
        
        risk_order = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}
        
        if max_risk == "NONE":
            return False  # EXPLAIN mode - no fixes
        
        if risk_order.get(fix_risk, 0) > risk_order.get(max_risk, 0):
            return False
        
        return True
    
    def _check_vibe_constraints(self, fixes: List[Dict[str, Any]]) -> bool:
        """Check if fixes meet vibe policy constraints.
        
        This is a HARD ENFORCEMENT - vibes actually block changes that
        violate their policies.
        """
        # Count unique files
        unique_files = set(fix["file"] for fix in fixes)
        
        # Analyze what the fixes would do
        needs_refactor = any(
            "refactor" in fix.get("change", "").lower() 
            for fix in fixes
        )
        needs_new_files = any(
            fix.get("type") == "new_file" 
            for fix in fixes
        )
        needs_delete = any(
            "remove" in fix.get("change", "").lower() or "delete" in fix.get("change", "").lower()
            for fix in fixes
        )
        
        # Use vibe policy enforcement
        enforcement_result = self.vibe_policy.enforce_limits({
            "files_to_modify": list(unique_files),
            "needs_refactor": needs_refactor,
            "needs_new_files": needs_new_files,
            "needs_delete": needs_delete,
        })
        
        if not enforcement_result["allowed"]:
            print(f"   ⚠️  Vibe constraint: {enforcement_result['reason']}")
            return False
        
        return True
    
    def _create_patch_with_explanation(self, fixes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create patch data with explanation."""
        return {
            "vibe": self.vibe_policy.mode.value,
            "fixes": fixes,
            "summary": self._create_fix_summary(fixes),
            "files_changed": len(set(fix["file"] for fix in fixes)),
            "total_fixes": len(fixes),
        }
    
    def _create_fix_summary(self, fixes: List[Dict[str, Any]]) -> str:
        """Create summary of fixes."""
        if not fixes:
            return "No fixes"
        
        fix_types = {}
        for fix in fixes:
            fix_type = fix["type"]
            fix_types[fix_type] = fix_types.get(fix_type, 0) + 1
        
        summary_parts = [f"{count} {ftype}" for ftype, count in fix_types.items()]
        return f"Applied {', '.join(summary_parts)}"
    
    def _generate_commit_message(self, fixes: List[Dict[str, Any]]) -> str:
        """Generate commit message based on fixes and vibe."""
        if not self.vibe_policy.should_auto_commit():
            return ""
        
        # Create commit message based on vibe
        vibe_prefixes = {
            VibeMode.CHILL: "fix: ",
            VibeMode.FOCUS: "fix: ",
            VibeMode.HACKER: "refactor: ",
            VibeMode.EXPLAIN: "",
        }
        
        prefix = vibe_prefixes.get(self.vibe_policy.mode, "fix: ")
        summary = self._create_fix_summary(fixes)
        
        if self.vibe_policy.get_verbosity() in ["detailed", "verbose"]:
            # Detailed commit message
            message_lines = [f"{prefix}{summary}", ""]
            for fix in fixes[:5]:  # Top 5 fixes
                message_lines.append(f"- {fix['file']}: {fix['change']}")
            
            message_lines.append("")
            message_lines.append(f"Vibe: {self.vibe_policy.mode.value}")
            return "\n".join(message_lines)
        else:
            # Simple commit message
            return f"{prefix}{summary}"
    
    def _save_session(
        self,
        errors: List[Dict[str, Any]],
        fixes: List[Dict[str, Any]],
        patch_data: Dict[str, Any],
        commit_msg: str,
    ) -> None:
        """Save fix session data."""
        session_dir = self.project_path / ".anox" / "smartfix"
        session_dir.mkdir(parents=True, exist_ok=True)
        
        session_file = session_dir / f"{self.session_id}.json"
        
        data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "vibe": self.vibe_policy.mode.value,
            "errors_detected": errors,
            "fixes_generated": fixes,
            "patch": patch_data,
            "commit_message": commit_msg,
        }
        
        safe_json_save(session_file, data)
        
        # Also save as latest
        latest_file = session_dir / "latest.json"
        safe_json_save(latest_file, data)
    
    def _display_results(
        self,
        errors: List[Dict[str, Any]],
        fixes: List[Dict[str, Any]],
        patch_data: Dict[str, Any],
        commit_msg: str,
    ) -> None:
        """Display results in mobile-friendly format."""
        print("\n" + "=" * 60)
        print("🎉 SMART FIX COMPLETE")
        print("=" * 60)
        
        # Show vibe impact clearly
        vibe_emoji = {
            "chill": "🌊",
            "focus": "🎯", 
            "hacker": "⚡",
            "explain": "📚"
        }
        confidence = self.vibe_policy.get_confidence_level()
        
        print(f"\n📊 Summary:")
        print(f"   Vibe: {vibe_emoji.get(self.vibe_policy.mode.value, '')} {self.vibe_policy.mode.value.upper()} (confidence: {confidence})")
        print(f"   Max files allowed: {self.vibe_policy.get_max_files_changed()}")
        print(f"   Errors found: {len(errors)}")
        print(f"   Fixes generated: {len(fixes)}")
        print(f"   Files affected: {patch_data['files_changed']}")
        
        # Show what vibe allowed/blocked
        if self.vibe_policy.mode.value == "chill":
            print(f"   🌊 CHILL mode: Ultra-conservative, only critical fixes")
        elif self.vibe_policy.mode.value == "focus":
            print(f"   🎯 FOCUS mode: Targeted bug fixes, no refactoring")
        elif self.vibe_policy.mode.value == "hacker":
            print(f"   ⚡ HACKER mode: Aggressive fixes, refactoring allowed")
        elif self.vibe_policy.mode.value == "explain":
            print(f"   📚 EXPLAIN mode: Analysis only, no code changes")
        
        if fixes:
            print(f"\n🔧 Fixes:")
            for i, fix in enumerate(fixes[:5], 1):
                print(f"   {i}. {fix['file']}")
                print(f"      {fix['change']}")
                if self.vibe_policy.should_show_reasoning():
                    print(f"      Risk: {fix['risk']} | Confidence: {fix.get('confidence', 'N/A')}")
        
        if commit_msg:
            print(f"\n💬 Commit Message:")
            for line in commit_msg.split('\n')[:5]:
                print(f"   {line}")
        
        print(f"\n💾 Session saved: {self.session_id}")
        
        # Vibe-specific next steps
        if self.vibe_policy.mode.value == "explain":
            print(f"\n💡 Next steps (EXPLAIN mode):")
            print(f"   - Review analysis in .anox/smartfix/{self.session_id}.json")
            print(f"   - No changes to apply (explain mode)")
        else:
            print(f"\n💡 Next steps:")
            print(f"   - Review fixes in .anox/smartfix/{self.session_id}.json")
            print(f"   - Apply with: anox smartfix --apply {self.session_id}")
            print(f"   - Or review and commit manually")


@handle_command_errors("smartfix")
def run_smartfix(
    vibe: str = "focus",
    target: Optional[str] = None,
    apply: bool = False,
    session_id: Optional[str] = None,
) -> None:
    """Run smart fix command.
    
    Args:
        vibe: Vibe mode (chill, focus, hacker, explain)
        target: Optional specific file or error to target
        apply: Whether to apply fixes immediately
        session_id: Session ID to apply (if applying previous session)
    """
    if session_id:
        print(f"📂 Applying session: {session_id}")
        print("⚠️  Apply functionality not yet implemented")
        return
    
    print(f"🚀 Starting Smart Fix (vibe: {vibe})\n")
    
    try:
        fixer = SmartFixer(vibe=vibe)
        result = fixer.auto_detect_and_fix(target=target)
        
        if not result["success"]:
            print(f"\n❌ {result['message']}")
            return
        
        if result.get("errors_found", 0) == 0:
            print(result["message"])
            return
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nAvailable vibes: chill, focus, hacker, explain")
        print("Example: anox smartfix --vibe=focus")
