"""Code review command - anox review."""

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
    ReviewError,
    ProjectNotInitializedError
)
from intel.code_intelligence import CodeIntelligence
from models.offline_adapter import OfflineModelAdapter


# Configuration constants
MAX_FILES_TO_REVIEW = 20  # Limit for prototype phase


class CodeReviewer:
    """Review code and provide feedback."""
    
    def __init__(self):
        self.project_path = Path.cwd()
        self.initializer = ProjectInitializer(self.project_path)
        self.model = OfflineModelAdapter()
        self.intelligence = CodeIntelligence(self.model)
        
    def review_files(self, paths: List[str]) -> Dict[str, Any]:
        """
        Review specific files.
        
        Args:
            paths: List of file paths to review
            
        Returns:
            Dictionary with review results
            
        Raises:
            ProjectNotInitializedError: If project not initialized
            ReviewError: If review fails
        """
        # Check if project is initialized
        validate_project_initialized(self.project_path)
        
        try:
            # Resolve paths
            files_to_review = self._resolve_paths(paths)
            
            if not files_to_review:
                return {
                    "success": False,
                    "message": "No valid files found to review."
                }
            
            # Review files
            reviews = []
            total_comments = 0
            
            for file_path in files_to_review:
                try:
                    review = self._review_file(file_path)
                    if review:
                        reviews.append(review)
                        total_comments += len(review.comments)
                except Exception as e:
                    print(f"⚠️  Skipped {file_path}: {str(e)}")
                    continue
            
            # Create summary
            summary = self._create_summary(reviews)
            
            # Save results
            self._save_results(reviews, summary)
            
            return {
                "success": True,
                "message": f"✓ Reviewed {len(reviews)} files",
                "files_reviewed": len(reviews),
                "total_comments": total_comments,
                "summary": summary,
                "reviews": reviews
            }
            
        except ReviewError:
            raise
        except Exception as e:
            raise ReviewError(str(e))
    
    def _resolve_paths(self, paths: List[str]) -> List[Path]:
        """Resolve provided paths to actual files."""
        files = []
        for path_str in paths:
            path = Path(path_str)
            if path.is_file():
                files.append(path)
            elif path.is_dir():
                # Get all code files in directory
                files.extend(self._get_code_files_in_dir(path))
        return files
    
    def _get_code_files_in_dir(self, directory: Path) -> List[Path]:
        """Get all code files in a directory."""
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.rb', '.php']
        files = []
        for ext in extensions:
            for file_path in directory.rglob(f"*{ext}"):
                if len(files) >= MAX_FILES_TO_REVIEW:
                    return files
                files.append(file_path)
        return files
    
    def _review_file(self, file_path: Path):
        """Review a single file."""
        # Read file
        code = safe_file_read(file_path)
        if code is None:
            return None
        
        # Detect language
        language = self.intelligence.detect_language(str(file_path))
        
        # Review
        review = self.intelligence.review_code(code, language, str(file_path))
        return review
    
    def _create_summary(self, reviews: List) -> Dict[str, Any]:
        """Create review summary."""
        if not reviews:
            return {}
        
        total_comments = sum(len(r.comments) for r in reviews)
        avg_score = sum(r.overall_score for r in reviews) / len(reviews) if reviews else 0
        
        return {
            "total_files": len(reviews),
            "total_comments": total_comments,
            "average_score": round(avg_score, 2),
            "needs_improvement": avg_score < 7.0
        }
    
    def _save_results(self, reviews: List, summary: Dict[str, Any]) -> None:
        """Save review results."""
        results_dir = self.project_path / ".anox" / "reviews"
        results_dir.mkdir(exist_ok=True)
        
        # Save latest results
        results_file = results_dir / "latest.json"
        
        data = {
            "timestamp": self._get_timestamp(),
            "summary": summary,
            "reviews": [self._serialize_review(r) for r in reviews]
        }
        
        safe_json_save(results_file, data)
    
    def _serialize_review(self, review) -> Dict[str, Any]:
        """Serialize review result."""
        return {
            "file_path": review.file_path,
            "comments": review.comments,
            "overall_score": review.overall_score,
            "summary": review.summary
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


@handle_command_errors("review")
def run_review(paths: List[str], verbose: bool = False) -> None:
    """Run the review command."""
    if not paths:
        print("❌ Error: No files specified for review")
        print("\nUsage: anox review <file1> [file2] ...")
        print("Example: anox review main.py src/utils.py")
        return
    
    print(f"📝 Reviewing {len(paths)} file(s)...\n")
    
    reviewer = CodeReviewer()
    result = reviewer.review_files(paths)
    
    print(result["message"])
    
    if result["success"]:
        summary = result.get("summary", {})
        
        print(f"\n📊 Review Summary:")
        print(f"  Files reviewed: {summary.get('total_files', 0)}")
        print(f"  Total comments: {summary.get('total_comments', 0)}")
        print(f"  Average score: {summary.get('average_score', 0)}/10")
        
        if summary.get("needs_improvement"):
            print("\n⚠️  Code quality below threshold - improvements recommended")
        else:
            print("\n✅ Code quality looks good!")
        
        # Show sample comments
        reviews = result.get("reviews", [])
        if reviews and verbose:
            print("\n💬 Sample Comments:")
            for review in reviews[:3]:
                print(f"\n  📁 {review.file_path}")
                for comment in review.comments[:3]:
                    line = comment.get("line", "?")
                    text = comment.get("text", "")
                    print(f"    L{line}: {text}")
        
        print("\n💡 Next steps:")
        print("  - Check .anox/reviews/latest.json for detailed feedback")
        print("  - Run 'anox fix' to automatically fix issues")
