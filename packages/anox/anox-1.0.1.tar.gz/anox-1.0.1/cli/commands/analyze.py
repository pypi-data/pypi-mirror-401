"""Code analysis command - anox analyze."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from cli.commands.init import ProjectInitializer
from cli.error_handling import (
    handle_command_errors,
    validate_project_initialized,
    safe_file_read,
    safe_json_save,
    AnalysisError,
    ProjectNotInitializedError
)
from intel.code_intelligence import CodeIntelligence
from models.offline_adapter import OfflineModelAdapter


# Configuration constants
MAX_FILES_TO_ANALYZE = 50  # Limit for prototype phase


class CodeAnalyzer:
    """Analyze code for issues, bugs, and improvements."""
    
    def __init__(self):
        self.project_path = Path.cwd()
        self.initializer = ProjectInitializer(self.project_path)
        self.model = OfflineModelAdapter()
        self.intelligence = CodeIntelligence(self.model)
        
    def analyze_project(self, paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze project or specific paths.
        
        Args:
            paths: Optional list of specific paths to analyze
            
        Returns:
            Dictionary with analysis results
            
        Raises:
            ProjectNotInitializedError: If project not initialized
            AnalysisError: If analysis fails
        """
        # Check if project is initialized
        validate_project_initialized(self.project_path)
        
        config = self.initializer.get_config()
        if not config:
            raise AnalysisError("Failed to load project configuration")
        
        try:
            # Get files to analyze
            if paths:
                files_to_analyze = self._resolve_paths(paths)
            else:
                files_to_analyze = self._discover_files(config)
            
            if not files_to_analyze:
                return {
                    "success": False,
                    "message": "No files found to analyze."
                }
            
            # Analyze files
            results = []
            total_issues = 0
            
            for file_path in files_to_analyze:
                try:
                    result = self._analyze_file(file_path)
                    if result:
                        results.append(result)
                        total_issues += len(result.issues)
                except Exception as e:
                    print(f"⚠️  Skipped {file_path}: {str(e)}")
                    continue
            
            # Create summary
            summary = self._create_summary(results, total_issues)
            
            # Save results
            self._save_results(results, summary)
            
            return {
                "success": True,
                "message": f"✓ Analyzed {len(results)} files",
                "files_analyzed": len(results),
                "total_issues": total_issues,
                "summary": summary,
                "results": results
            }
            
        except AnalysisError:
            raise
        except Exception as e:
            raise AnalysisError(str(e))
    
    def _resolve_paths(self, paths: List[str]) -> List[Path]:
        """Resolve provided paths to actual files."""
        files = []
        for path_str in paths:
            path = Path(path_str)
            if path.is_file():
                files.append(path)
            elif path.is_dir():
                files.extend(self._get_code_files_in_dir(path))
        return files
    
    def _discover_files(self, config: Dict[str, Any]) -> List[Path]:
        """Discover all code files in project."""
        excluded = config.get("settings", {}).get("excluded_patterns", [])
        return self._get_code_files_in_dir(self.project_path, excluded)
    
    def _get_code_files_in_dir(self, directory: Path, excluded: List[str] = None) -> List[Path]:
        """Get all code files in a directory."""
        excluded = excluded or []
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.rb', '.php']
        
        files = []
        for ext in extensions:
            for file_path in directory.rglob(f"*{ext}"):
                # Check limit first to avoid unnecessary work
                if len(files) >= MAX_FILES_TO_ANALYZE:
                    return files
                
                # Skip excluded patterns
                if any(file_path.match(pattern) for pattern in excluded):
                    continue
                files.append(file_path)
        
        return files
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single file."""
        # Read file
        code = safe_file_read(file_path)
        if code is None:
            return None
        
        # Detect language
        language = self.intelligence.detect_language(str(file_path))
        
        # Analyze
        result = self.intelligence.analyze_code(code, language, str(file_path))
        return result
    
    def _create_summary(self, results: List, total_issues: int) -> Dict[str, Any]:
        """Create analysis summary."""
        if not results:
            return {}
        
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        
        for result in results:
            for issue in result.issues:
                severity = issue.get("severity", "low")
                if severity in severity_counts:
                    severity_counts[severity] += 1
        
        return {
            "total_files": len(results),
            "total_issues": total_issues,
            "by_severity": severity_counts,
            "requires_attention": severity_counts["high"] > 0
        }
    
    def _save_results(self, results: List, summary: Dict[str, Any]) -> None:
        """Save analysis results."""
        results_dir = self.project_path / ".anox" / "analysis"
        results_dir.mkdir(exist_ok=True)
        
        # Save latest results
        results_file = results_dir / "latest.json"
        
        data = {
            "timestamp": self._get_timestamp(),
            "summary": summary,
            "results": [self._serialize_result(r) for r in results]
        }
        
        safe_json_save(results_file, data)
    
    def _serialize_result(self, result) -> Dict[str, Any]:
        """Serialize analysis result."""
        return {
            "file_path": result.file_path,
            "language": result.language,
            "issues": result.issues,
            "metrics": result.metrics,
            "suggestions": result.suggestions
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


@handle_command_errors("analyze")
def run_analyze(paths: Optional[List[str]] = None, verbose: bool = False) -> None:
    """Run the analyze command."""
    print("🔍 Analyzing code...\n")
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_project(paths)
    
    print(result["message"])
    
    if result["success"]:
        summary = result.get("summary", {})
        
        print(f"\n📊 Analysis Summary:")
        print(f"  Files analyzed: {summary.get('total_files', 0)}")
        print(f"  Total issues: {summary.get('total_issues', 0)}")
        
        severity = summary.get("by_severity", {})
        if severity:
            print(f"\n  By Severity:")
            print(f"    🔴 High: {severity.get('high', 0)}")
            print(f"    🟡 Medium: {severity.get('medium', 0)}")
            print(f"    🟢 Low: {severity.get('low', 0)}")
        
        if summary.get("requires_attention"):
            print("\n⚠️  High-severity issues found - review recommended")
        
        print("\n💡 Next steps:")
        print("  - Run 'anox review <file>' to review specific files")
        print("  - Run 'anox fix' to automatically fix issues")
        print("  - Check .anox/analysis/latest.json for detailed results")
