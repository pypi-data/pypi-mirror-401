"""Code intelligence module for analysis, review, and testing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from models.base import BaseModel


@dataclass
class CodeAnalysisResult:
    """Result of code analysis."""
    file_path: str
    language: str
    issues: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    suggestions: List[str]


@dataclass
class CodeReviewResult:
    """Result of code review."""
    file_path: str
    comments: List[Dict[str, Any]]
    overall_score: float
    summary: str


@dataclass
class TestGenerationResult:
    """Result of test generation."""
    test_code: str
    test_cases: List[str]
    coverage_targets: List[str]


class CodeIntelligence:
    """
    Code intelligence engine providing:
    - Code analysis
    - Code review
    - Test generation
    - Code completion
    - Vulnerability detection
    """

    def __init__(self, model: BaseModel) -> None:
        self.model = model
        self._supported_languages = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "java": [".java"],
            "cpp": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
            "go": [".go"],
            "rust": [".rs"],
            "ruby": [".rb"],
            "php": [".php"],
        }

    def analyze_code(self, code: str, language: str, file_path: str = "") -> CodeAnalysisResult:
        """
        Analyze code for quality, bugs, and improvements.
        
        Args:
            code: Source code to analyze
            language: Programming language
            file_path: Optional file path for context
            
        Returns:
            CodeAnalysisResult with issues and suggestions
        """
        prompt = self._build_analysis_prompt(code, language, file_path)
        context = {
            "task_type": "code_analysis",
            "intent_domain": "dev",
            "identity_role": "code_analyzer",
            "language": language,
        }

        response = self.model.generate(prompt, context)
        
        # Parse response into structured result
        return self._parse_analysis_response(response, file_path, language)

    def review_code(
        self,
        code: str,
        language: str,
        file_path: str = "",
        context_files: Optional[List[str]] = None,
    ) -> CodeReviewResult:
        """
        Review code and provide feedback.
        
        Args:
            code: Source code to review
            language: Programming language
            file_path: Optional file path for context
            context_files: Optional list of related files for context
            
        Returns:
            CodeReviewResult with comments and score
        """
        prompt = self._build_review_prompt(code, language, file_path, context_files)
        context = {
            "task_type": "code_review",
            "intent_domain": "dev",
            "identity_role": "code_reviewer",
            "language": language,
        }

        response = self.model.generate(prompt, context)
        
        return self._parse_review_response(response, file_path)

    def generate_tests(
        self,
        code: str,
        language: str,
        test_framework: Optional[str] = None,
    ) -> TestGenerationResult:
        """
        Generate test cases for the given code.
        
        Args:
            code: Source code to generate tests for
            language: Programming language
            test_framework: Optional test framework (pytest, jest, junit, etc.)
            
        Returns:
            TestGenerationResult with test code and cases
        """
        prompt = self._build_test_generation_prompt(code, language, test_framework)
        context = {
            "task_type": "test_generation",
            "intent_domain": "dev",
            "identity_role": "test_generator",
            "language": language,
            "test_framework": test_framework,
        }

        response = self.model.generate(prompt, context)
        
        return self._parse_test_generation_response(response)

    def complete_code(
        self,
        code_prefix: str,
        code_suffix: str,
        language: str,
        file_path: str = "",
    ) -> str:
        """
        Complete code based on prefix and suffix.
        
        Args:
            code_prefix: Code before cursor
            code_suffix: Code after cursor
            language: Programming language
            file_path: Optional file path for context
            
        Returns:
            Completed code snippet
        """
        prompt = self._build_completion_prompt(code_prefix, code_suffix, language, file_path)
        context = {
            "task_type": "code_completion",
            "intent_domain": "dev",
            "identity_role": "code_completer",
            "language": language,
            "max_tokens": 256,
            "temperature": 0.3,
        }

        response = self.model.generate(prompt, context)
        
        return self._parse_completion_response(response)

    def scan_vulnerabilities(self, code: str, language: str) -> List[Dict[str, Any]]:
        """
        Scan code for security vulnerabilities.
        
        Args:
            code: Source code to scan
            language: Programming language
            
        Returns:
            List of vulnerability findings
        """
        prompt = self._build_vulnerability_scan_prompt(code, language)
        context = {
            "task_type": "vulnerability_scan",
            "intent_domain": "cyber",
            "identity_role": "security_analyst",
            "language": language,
        }

        response = self.model.generate(prompt, context)
        
        return self._parse_vulnerability_response(response)

    # Private helper methods for building prompts

    def _build_analysis_prompt(self, code: str, language: str, file_path: str) -> str:
        """Build prompt for code analysis."""
        return f"""Analyze the following {language} code for quality issues, bugs, and improvements.

File: {file_path or 'unknown'}

Code:
```{language}
{code}
```

Please provide:
1. List of issues found (bugs, code smells, anti-patterns)
2. Code quality metrics assessment
3. Specific suggestions for improvement

Format your response with clear sections."""

    def _build_review_prompt(
        self,
        code: str,
        language: str,
        file_path: str,
        context_files: Optional[List[str]],
    ) -> str:
        """Build prompt for code review."""
        context_info = ""
        if context_files:
            context_info = f"\nRelated files: {', '.join(context_files)}"

        return f"""Review the following {language} code as a senior developer would.

File: {file_path or 'unknown'}{context_info}

Code:
```{language}
{code}
```

Please provide:
1. Line-by-line comments for improvements
2. Overall code quality assessment (score 1-10)
3. Summary of key findings
4. Prioritized recommendations

Be constructive and specific in your feedback."""

    def _build_test_generation_prompt(
        self,
        code: str,
        language: str,
        test_framework: Optional[str],
    ) -> str:
        """Build prompt for test generation."""
        framework_info = f" using {test_framework}" if test_framework else ""
        
        return f"""Generate comprehensive test cases for the following {language} code{framework_info}.

Code:
```{language}
{code}
```

Please provide:
1. Complete test code with multiple test cases
2. Coverage of edge cases and error conditions
3. Clear test case descriptions
4. Setup and teardown if needed

Ensure tests are thorough and follow best practices."""

    def _build_completion_prompt(
        self,
        code_prefix: str,
        code_suffix: str,
        language: str,
        file_path: str,
    ) -> str:
        """Build prompt for code completion."""
        return f"""Complete the {language} code at the cursor position (marked with <CURSOR>).

File: {file_path or 'unknown'}

Code:
```{language}
{code_prefix}<CURSOR>{code_suffix}
```

Provide only the code that should be inserted at the cursor position.
Be concise and follow the existing code style."""

    def _build_vulnerability_scan_prompt(self, code: str, language: str) -> str:
        """Build prompt for vulnerability scanning."""
        return f"""Scan the following {language} code for security vulnerabilities.

Code:
```{language}
{code}
```

Please identify:
1. SQL injection vulnerabilities
2. Cross-site scripting (XSS) risks
3. Authentication/authorization issues
4. Insecure cryptography
5. Input validation problems
6. Other security concerns

For each finding, provide:
- Severity (critical/high/medium/low)
- Location (line number if possible)
- Description of the issue
- Recommended fix"""

    # Private helper methods for parsing responses

    def _parse_analysis_response(
        self,
        response: str,
        file_path: str,
        language: str,
    ) -> CodeAnalysisResult:
        """Parse analysis response into structured result."""
        # Simple parsing - in production, use more sophisticated parsing
        issues = []
        suggestions = []
        
        lines = response.split("\n")
        for line in lines:
            if "issue" in line.lower() or "bug" in line.lower():
                issues.append({"description": line.strip(), "severity": "medium"})
            elif "suggest" in line.lower() or "improve" in line.lower():
                suggestions.append(line.strip())

        metrics = {
            "total_issues": len(issues),
            "total_suggestions": len(suggestions),
        }

        return CodeAnalysisResult(
            file_path=file_path,
            language=language,
            issues=issues,
            metrics=metrics,
            suggestions=suggestions,
        )

    def _parse_review_response(self, response: str, file_path: str) -> CodeReviewResult:
        """Parse review response into structured result."""
        comments = []
        overall_score = 7.0  # Default
        
        # Extract score if present
        if "score" in response.lower():
            for line in response.split("\n"):
                if "score" in line.lower():
                    try:
                        score_str = "".join(c for c in line if c.isdigit() or c == ".")
                        if score_str:
                            overall_score = float(score_str)
                    except ValueError:
                        pass

        # Extract comments
        for line in response.split("\n"):
            if line.strip() and len(line) > 20:
                comments.append({
                    "line": 0,  # Would need more sophisticated parsing
                    "comment": line.strip(),
                })

        return CodeReviewResult(
            file_path=file_path,
            comments=comments,
            overall_score=overall_score,
            summary=response[:200] + "..." if len(response) > 200 else response,
        )

    def _parse_test_generation_response(self, response: str) -> TestGenerationResult:
        """Parse test generation response."""
        # Extract code blocks
        test_code = response
        if "```" in response:
            parts = response.split("```")
            if len(parts) >= 3:
                test_code = parts[1]
                if test_code.startswith("python") or test_code.startswith("javascript"):
                    test_code = "\n".join(test_code.split("\n")[1:])

        # Extract test case names
        test_cases = []
        for line in response.split("\n"):
            if "def test_" in line or "test(" in line or "it(" in line:
                test_cases.append(line.strip())

        return TestGenerationResult(
            test_code=test_code.strip(),
            test_cases=test_cases,
            coverage_targets=["main_function"],  # Would need more sophisticated parsing
        )

    def _parse_completion_response(self, response: str) -> str:
        """Parse completion response."""
        # Extract code from response
        if "```" in response:
            parts = response.split("```")
            if len(parts) >= 3:
                code = parts[1]
                if code.startswith("python") or code.startswith("javascript"):
                    code = "\n".join(code.split("\n")[1:])
                return code.strip()
        
        return response.strip()

    def _parse_vulnerability_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse vulnerability scan response."""
        vulnerabilities = []
        
        current_vuln = {}
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                if current_vuln:
                    vulnerabilities.append(current_vuln)
                    current_vuln = {}
                continue
                
            if "severity" in line.lower():
                for severity in ["critical", "high", "medium", "low"]:
                    if severity in line.lower():
                        current_vuln["severity"] = severity
                        break
            elif "line" in line.lower() and any(c.isdigit() for c in line):
                current_vuln["line"] = line
            else:
                if "description" not in current_vuln:
                    current_vuln["description"] = line
                else:
                    current_vuln["description"] += " " + line

        if current_vuln:
            vulnerabilities.append(current_vuln)

        return vulnerabilities

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension."""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for language, extensions in self._supported_languages.items():
            if ext in extensions:
                return language
        
        return None

    def is_supported_language(self, language: str) -> bool:
        """Check if language is supported."""
        return language.lower() in self._supported_languages
