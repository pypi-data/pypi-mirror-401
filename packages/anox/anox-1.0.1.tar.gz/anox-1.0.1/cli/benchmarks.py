"""Benchmark framework for measuring ANOX intelligence and performance."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

from cli.commands.init import ProjectInitializer
from cli.commands.analyze import CodeAnalyzer
from cli.commands.review import CodeReviewer


@dataclass
class BenchmarkResult:
    """Result of a benchmark test."""
    name: str
    success: bool
    duration_ms: float
    metrics: Dict[str, Any]
    timestamp: str
    error: Optional[str] = None


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results."""
    suite_name: str
    results: List[BenchmarkResult]
    total_duration_ms: float
    success_rate: float
    timestamp: str


class BenchmarkRunner:
    """Run benchmarks to measure ANOX performance."""
    
    def __init__(self, benchmark_dir: Path = None):
        self.benchmark_dir = benchmark_dir or Path(".anox") / "benchmarks"
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)
        
    def run_benchmark(self, name: str, func: Callable, **kwargs) -> BenchmarkResult:
        """
        Run a single benchmark test.
        
        Args:
            name: Name of the benchmark
            func: Function to benchmark
            **kwargs: Arguments to pass to function
            
        Returns:
            BenchmarkResult with timing and metrics
        """
        start_time = time.time()
        error = None
        success = False
        metrics = {}
        
        try:
            result = func(**kwargs)
            success = result.get("success", False) if isinstance(result, dict) else bool(result)
            metrics = result if isinstance(result, dict) else {"result": str(result)}
        except Exception as e:
            error = str(e)
            success = False
        
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        
        return BenchmarkResult(
            name=name,
            success=success,
            duration_ms=duration_ms,
            metrics=metrics,
            timestamp=datetime.now().isoformat(),
            error=error
        )
    
    def run_suite(self, suite_name: str, benchmarks: List[tuple]) -> BenchmarkSuite:
        """
        Run a suite of benchmarks.
        
        Args:
            suite_name: Name of the benchmark suite
            benchmarks: List of (name, func, kwargs) tuples
            
        Returns:
            BenchmarkSuite with all results
        """
        suite_start = time.time()
        results = []
        
        for name, func, kwargs in benchmarks:
            print(f"  Running: {name}...")
            result = self.run_benchmark(name, func, **kwargs)
            results.append(result)
            
            status = "✓" if result.success else "✗"
            print(f"    {status} {result.duration_ms:.2f}ms")
        
        suite_end = time.time()
        total_duration_ms = (suite_end - suite_start) * 1000
        
        success_count = sum(1 for r in results if r.success)
        success_rate = (success_count / len(results)) * 100 if results else 0
        
        suite = BenchmarkSuite(
            suite_name=suite_name,
            results=results,
            total_duration_ms=total_duration_ms,
            success_rate=success_rate,
            timestamp=datetime.now().isoformat()
        )
        
        # Save results
        self._save_suite(suite)
        
        return suite
    
    def _save_suite(self, suite: BenchmarkSuite) -> None:
        """Save benchmark suite results."""
        suite_file = self.benchmark_dir / f"{suite.suite_name}.json"
        
        data = {
            "suite_name": suite.suite_name,
            "timestamp": suite.timestamp,
            "total_duration_ms": suite.total_duration_ms,
            "success_rate": suite.success_rate,
            "results": [asdict(r) for r in suite.results]
        }
        
        with open(suite_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def run_command_benchmarks(self, project_path: Path) -> BenchmarkSuite:
        """
        Run benchmarks for all core commands.
        
        Args:
            project_path: Path to test project
            
        Returns:
            BenchmarkSuite with command benchmark results
        """
        print("\n🏃 Running Command Benchmarks...")
        
        benchmarks = [
            ("init", self._benchmark_init, {"project_path": project_path}),
            ("analyze", self._benchmark_analyze, {"project_path": project_path}),
            ("review", self._benchmark_review, {"project_path": project_path}),
            ("status", self._benchmark_status, {"project_path": project_path}),
        ]
        
        return self.run_suite("command_benchmarks", benchmarks)
    
    def _benchmark_init(self, project_path: Path) -> Dict[str, Any]:
        """Benchmark init command."""
        initializer = ProjectInitializer(project_path)
        result = initializer.initialize(force=True)
        return result
    
    def _benchmark_analyze(self, project_path: Path) -> Dict[str, Any]:
        """Benchmark analyze command."""
        analyzer = CodeAnalyzer()
        analyzer.project_path = project_path
        analyzer.initializer = ProjectInitializer(project_path)
        
        # Create a test file if not exists
        test_file = project_path / "test.py"
        if not test_file.exists():
            test_file.write_text("def test(): pass")
        
        result = analyzer.analyze_project()
        return result
    
    def _benchmark_review(self, project_path: Path) -> Dict[str, Any]:
        """Benchmark review command."""
        reviewer = CodeReviewer()
        reviewer.project_path = project_path
        reviewer.initializer = ProjectInitializer(project_path)
        
        # Create a test file if not exists
        test_file = project_path / "test.py"
        if not test_file.exists():
            test_file.write_text("def test(): pass")
        
        result = reviewer.review_files([str(test_file)])
        return result
    
    def _benchmark_status(self, project_path: Path) -> Dict[str, Any]:
        """Benchmark status command."""
        from cli.commands.status import get_project_status
        import os
        
        old_cwd = os.getcwd()
        try:
            os.chdir(project_path)
            status = get_project_status()
            return {"success": True, "status": status}
        finally:
            os.chdir(old_cwd)
    
    def run_intelligence_benchmarks(self) -> BenchmarkSuite:
        """
        Run benchmarks to measure AI intelligence quality.
        
        Returns:
            BenchmarkSuite with intelligence benchmark results
        """
        print("\n🧠 Running Intelligence Benchmarks...")
        
        benchmarks = [
            ("code_understanding", self._benchmark_code_understanding, {}),
            ("issue_detection", self._benchmark_issue_detection, {}),
            ("suggestion_quality", self._benchmark_suggestion_quality, {}),
        ]
        
        return self.run_suite("intelligence_benchmarks", benchmarks)
    
    def _benchmark_code_understanding(self) -> Dict[str, Any]:
        """Benchmark code understanding capability."""
        # Mock test - in production would use real model
        test_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""
        
        # Simulate analysis
        time.sleep(0.1)  # Mock processing time
        
        return {
            "success": True,
            "understood_structure": True,
            "identified_purpose": True,
            "complexity_score": 5
        }
    
    def _benchmark_issue_detection(self) -> Dict[str, Any]:
        """Benchmark issue detection capability."""
        # Mock test - in production would use real model
        test_code = """
def unsafe_function(user_input):
    eval(user_input)  # Security issue
    x = 1 / 0  # Logic error
"""
        
        # Simulate analysis
        time.sleep(0.1)  # Mock processing time
        
        return {
            "success": True,
            "security_issues_found": 1,
            "logic_issues_found": 1,
            "total_issues": 2
        }
    
    def _benchmark_suggestion_quality(self) -> Dict[str, Any]:
        """Benchmark suggestion quality."""
        # Mock test - in production would use real model
        time.sleep(0.1)  # Mock processing time
        
        return {
            "success": True,
            "suggestions_count": 5,
            "actionable_suggestions": 4,
            "quality_score": 0.8
        }
    
    def generate_report(self, suite: BenchmarkSuite) -> str:
        """
        Generate a human-readable report from benchmark results.
        
        Args:
            suite: BenchmarkSuite to report on
            
        Returns:
            Formatted report string
        """
        lines = []
        lines.append(f"\n{'=' * 60}")
        lines.append(f"Benchmark Report: {suite.suite_name}")
        lines.append(f"{'=' * 60}")
        lines.append(f"Timestamp: {suite.timestamp}")
        lines.append(f"Total Duration: {suite.total_duration_ms:.2f}ms")
        lines.append(f"Success Rate: {suite.success_rate:.1f}%")
        lines.append(f"")
        
        lines.append("Results:")
        for result in suite.results:
            status = "✓ PASS" if result.success else "✗ FAIL"
            lines.append(f"  {status} - {result.name} ({result.duration_ms:.2f}ms)")
            
            if result.error:
                lines.append(f"       Error: {result.error}")
            
            # Show key metrics
            if result.metrics:
                for key, value in list(result.metrics.items())[:3]:
                    if isinstance(value, (int, float, bool, str)):
                        lines.append(f"       {key}: {value}")
        
        lines.append(f"{'=' * 60}\n")
        
        return "\n".join(lines)


def run_all_benchmarks(project_path: Path = None) -> None:
    """Run all benchmark suites."""
    import tempfile
    
    # Use temporary directory if no project path provided
    if project_path is None:
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
    
    runner = BenchmarkRunner()
    
    # Run command benchmarks
    cmd_suite = runner.run_command_benchmarks(project_path)
    print(runner.generate_report(cmd_suite))
    
    # Run intelligence benchmarks
    intel_suite = runner.run_intelligence_benchmarks()
    print(runner.generate_report(intel_suite))
    
    print(f"\n💾 Benchmark results saved to: {runner.benchmark_dir}")
    print(f"\n📊 Summary:")
    print(f"  Commands: {cmd_suite.success_rate:.1f}% success")
    print(f"  Intelligence: {intel_suite.success_rate:.1f}% success")


if __name__ == "__main__":
    run_all_benchmarks()
