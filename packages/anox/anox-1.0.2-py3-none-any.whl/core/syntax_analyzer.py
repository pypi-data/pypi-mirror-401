"""Real-time syntax analysis and correction for multiple languages.

This module provides advanced syntax checking and auto-correction capabilities
to handle language complexity challenges developers face.
"""

from __future__ import annotations

import ast
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SyntaxIssueType(Enum):
    """Types of syntax issues that can be detected."""
    MISSING_BRACKET = "missing_bracket"
    MISSING_SEMICOLON = "missing_semicolon"
    INVALID_INDENTATION = "invalid_indentation"
    UNDEFINED_VARIABLE = "undefined_variable"
    TYPE_MISMATCH = "type_mismatch"
    UNUSED_IMPORT = "unused_import"
    DEPRECATED_SYNTAX = "deprecated_syntax"


@dataclass
class SyntaxIssue:
    """Represents a syntax issue found in code."""
    type: SyntaxIssueType
    line: int
    column: int
    message: str
    suggestion: Optional[str] = None
    severity: str = "error"  # error, warning, info


class SyntaxAnalyzer:
    """Analyzes code syntax in real-time and provides corrections."""
    
    def __init__(self):
        """Initialize the syntax analyzer."""
        self.supported_languages = {
            'python': self._analyze_python,
            'javascript': self._analyze_javascript,
            'typescript': self._analyze_typescript,
            'java': self._analyze_java,
            'go': self._analyze_go,
            'rust': self._analyze_rust,
        }
    
    def analyze(self, code: str, language: str) -> List[SyntaxIssue]:
        """
        Analyze code for syntax issues.
        
        Args:
            code: The source code to analyze
            language: Programming language of the code
            
        Returns:
            List of syntax issues found
        """
        language = language.lower()
        
        if language not in self.supported_languages:
            return [SyntaxIssue(
                type=SyntaxIssueType.DEPRECATED_SYNTAX,
                line=0,
                column=0,
                message=f"Language '{language}' not yet supported",
                severity="info"
            )]
        
        analyzer_func = self.supported_languages[language]
        return analyzer_func(code)
    
    def _analyze_python(self, code: str) -> List[SyntaxIssue]:
        """Analyze Python code for syntax issues."""
        issues = []
        
        try:
            # Parse the code with AST
            ast.parse(code)
        except IndentationError as e:
            issues.append(SyntaxIssue(
                type=SyntaxIssueType.INVALID_INDENTATION,
                line=e.lineno or 0,
                column=e.offset or 0,
                message=str(e.msg),
                suggestion="Fix indentation to match Python style (4 spaces)"
            ))
        except TabError as e:
            issues.append(SyntaxIssue(
                type=SyntaxIssueType.INVALID_INDENTATION,
                line=e.lineno or 0,
                column=e.offset or 0,
                message="Inconsistent use of tabs and spaces",
                suggestion="Use consistent indentation (prefer 4 spaces)"
            ))
        except SyntaxError as e:
            issues.append(SyntaxIssue(
                type=SyntaxIssueType.INVALID_INDENTATION 
                     if "indent" in str(e).lower() 
                     else SyntaxIssueType.MISSING_BRACKET,
                line=e.lineno or 0,
                column=e.offset or 0,
                message=str(e.msg),
                suggestion=self._generate_python_fix_suggestion(e)
            ))
        
        # Check for common issues
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for unused imports
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_name = self._extract_import_name(line)
                if import_name and not self._is_import_used(import_name, code):
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.UNUSED_IMPORT,
                        line=i,
                        column=0,
                        message=f"Unused import: {import_name}",
                        suggestion=f"Remove unused import '{import_name}'",
                        severity="warning"
                    ))
        
        return issues
    
    def _analyze_javascript(self, code: str) -> List[SyntaxIssue]:
        """Analyze JavaScript code for syntax issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for missing semicolons
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.endswith((';', '{', '}', ':', ',')):
                if any(keyword in stripped for keyword in ['const ', 'let ', 'var ', 'return ', 'break ', 'continue ']):
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.MISSING_SEMICOLON,
                        line=i,
                        column=len(line),
                        message="Missing semicolon",
                        suggestion=f"{line};",
                        severity="warning"
                    ))
        
        # Check for bracket matching
        bracket_stack = []
        for i, char in enumerate(code):
            if char in '({[':
                bracket_stack.append((char, i))
            elif char in ')}]':
                if not bracket_stack:
                    line_num = code[:i].count('\n') + 1
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.MISSING_BRACKET,
                        line=line_num,
                        column=i - code[:i].rfind('\n'),
                        message=f"Unexpected closing bracket: {char}",
                        severity="error"
                    ))
                else:
                    open_bracket, _ = bracket_stack.pop()
                    if not self._brackets_match(open_bracket, char):
                        line_num = code[:i].count('\n') + 1
                        issues.append(SyntaxIssue(
                            type=SyntaxIssueType.MISSING_BRACKET,
                            line=line_num,
                            column=i - code[:i].rfind('\n'),
                            message=f"Mismatched brackets: {open_bracket} and {char}",
                            severity="error"
                        ))
        
        if bracket_stack:
            open_bracket, pos = bracket_stack[-1]
            line_num = code[:pos].count('\n') + 1
            issues.append(SyntaxIssue(
                type=SyntaxIssueType.MISSING_BRACKET,
                line=line_num,
                column=pos - code[:pos].rfind('\n'),
                message=f"Unclosed bracket: {open_bracket}",
                suggestion=f"Add closing bracket for '{open_bracket}'",
                severity="error"
            ))
        
        return issues
    
    def _analyze_typescript(self, code: str) -> List[SyntaxIssue]:
        """Analyze TypeScript code for syntax issues."""
        # TypeScript includes JavaScript issues plus type checking
        issues = self._analyze_javascript(code)
        
        # Add TypeScript-specific checks
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for missing type annotations
            if re.search(r'function\s+\w+\s*\([^)]*\)\s*{', line):
                if ':' not in line:
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.TYPE_MISMATCH,
                        line=i,
                        column=0,
                        message="Consider adding type annotations",
                        suggestion="Add return type annotation",
                        severity="info"
                    ))
        
        return issues
    
    def _analyze_java(self, code: str) -> List[SyntaxIssue]:
        """Analyze Java code for syntax issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for missing semicolons
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.endswith((';', '{', '}')) and not stripped.startswith(('import ', 'package ', '//', '/*', '*')):
                if any(keyword in stripped for keyword in ['return ', 'break ', 'continue ', 'throw ', 'int ', 'String ', 'boolean ', 'double ', 'float ']):
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.MISSING_SEMICOLON,
                        line=i,
                        column=len(line),
                        message="Missing semicolon",
                        suggestion=f"{line};",
                        severity="error"
                    ))
        
        return issues
    
    def _analyze_go(self, code: str) -> List[SyntaxIssue]:
        """Analyze Go code for syntax issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for unused variables (Go is strict about this)
        var_pattern = re.compile(r'\b(?:var|:=)\s+(\w+)')
        for i, line in enumerate(lines, 1):
            match = var_pattern.search(line)
            if match:
                var_name = match.group(1)
                if not self._is_variable_used(var_name, code, i):
                    issues.append(SyntaxIssue(
                        type=SyntaxIssueType.UNDEFINED_VARIABLE,
                        line=i,
                        column=match.start(1),
                        message=f"Declared and not used: {var_name}",
                        suggestion=f"Remove or use variable '{var_name}'",
                        severity="error"
                    ))
        
        return issues
    
    def _analyze_rust(self, code: str) -> List[SyntaxIssue]:
        """Analyze Rust code for syntax issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for missing lifetime annotations
        for i, line in enumerate(lines, 1):
            if 'fn ' in line and '&' in line and "'" not in line:
                issues.append(SyntaxIssue(
                    type=SyntaxIssueType.TYPE_MISMATCH,
                    line=i,
                    column=0,
                    message="Consider adding lifetime annotations",
                    suggestion="Add lifetime parameter",
                    severity="info"
                ))
        
        return issues
    
    # Helper methods
    
    def _brackets_match(self, open_bracket: str, close_bracket: str) -> bool:
        """Check if opening and closing brackets match."""
        pairs = {'(': ')', '{': '}', '[': ']'}
        return pairs.get(open_bracket) == close_bracket
    
    def _extract_import_name(self, line: str) -> Optional[str]:
        """Extract the imported module/package name from an import statement."""
        match = re.search(r'import\s+(\w+)', line)
        if match:
            return match.group(1)
        match = re.search(r'from\s+(\w+)\s+import', line)
        if match:
            return match.group(1)
        return None
    
    def _is_import_used(self, import_name: str, code: str) -> bool:
        """Check if an imported module is used in the code."""
        # Simple heuristic: check if the import name appears elsewhere
        lines = code.split('\n')
        usage_count = sum(1 for line in lines if import_name in line and not line.strip().startswith(('import ', 'from ')))
        return usage_count > 0
    
    def _is_variable_used(self, var_name: str, code: str, declaration_line: int) -> bool:
        """Check if a variable is used after its declaration."""
        lines = code.split('\n')[declaration_line:]
        return any(var_name in line for line in lines)
    
    def _generate_python_fix_suggestion(self, error: SyntaxError) -> str:
        """Generate a fix suggestion for Python syntax errors."""
        msg = str(error.msg).lower()
        if 'indent' in msg:
            return "Fix indentation to match Python style (4 spaces)"
        elif 'bracket' in msg or 'paren' in msg:
            return "Add missing closing bracket or parenthesis"
        elif 'colon' in msg:
            return "Add missing colon at end of statement"
        return "Review and fix syntax error"
    
    def auto_fix(self, code: str, language: str) -> Tuple[str, List[str]]:
        """
        Automatically fix simple syntax issues.
        
        Args:
            code: The source code to fix
            language: Programming language of the code
            
        Returns:
            Tuple of (fixed_code, list_of_fixes_applied)
        """
        issues = self.analyze(code, language)
        fixes_applied = []
        fixed_code = code
        
        # Sort issues by line number (reverse) to fix from bottom to top
        # This prevents line number shifts
        for issue in sorted(issues, key=lambda x: x.line, reverse=True):
            if issue.severity == "error" and issue.suggestion:
                # Apply fix
                lines = fixed_code.split('\n')
                if 0 < issue.line <= len(lines):
                    if issue.type == SyntaxIssueType.MISSING_SEMICOLON:
                        lines[issue.line - 1] = issue.suggestion
                        fixes_applied.append(f"Line {issue.line}: Added missing semicolon")
                    elif issue.type == SyntaxIssueType.UNUSED_IMPORT:
                        lines[issue.line - 1] = f"# {lines[issue.line - 1]}  # Commented out unused import"
                        fixes_applied.append(f"Line {issue.line}: Commented out unused import")
                
                fixed_code = '\n'.join(lines)
        
        return fixed_code, fixes_applied


def get_syntax_suggestions(code: str, language: str, cursor_position: Tuple[int, int]) -> List[str]:
    """
    Get context-aware syntax suggestions at cursor position.
    
    Args:
        code: The source code
        language: Programming language
        cursor_position: (line, column) tuple
        
    Returns:
        List of suggestions
    """
    suggestions = []
    
    # Basic context-aware suggestions
    lines = code.split('\n')
    line_num, col = cursor_position
    
    if 0 < line_num <= len(lines):
        current_line = lines[line_num - 1][:col]
        
        # Language-specific suggestions
        if language.lower() == 'python':
            if current_line.strip().startswith('def '):
                suggestions.append("Add function docstring")
                suggestions.append("Add type hints")
            elif current_line.strip().startswith('class '):
                suggestions.append("Add class docstring")
                suggestions.append("Add __init__ method")
        
        elif language.lower() in ['javascript', 'typescript']:
            if 'function' in current_line:
                suggestions.append("Convert to arrow function")
                suggestions.append("Add JSDoc comment")
            elif 'const' in current_line or 'let' in current_line:
                suggestions.append("Add type annotation (TypeScript)")
        
        elif language.lower() == 'java':
            if 'class' in current_line:
                suggestions.append("Add JavaDoc comment")
                suggestions.append("Implement Serializable")
            elif 'public' in current_line or 'private' in current_line:
                suggestions.append("Add method documentation")
    
    return suggestions
