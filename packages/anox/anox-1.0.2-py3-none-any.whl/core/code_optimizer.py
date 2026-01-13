"""Code efficiency and optimization analysis.

This module provides algorithm complexity analysis, performance profiling,
and optimization recommendations for cleaner, more efficient code.
"""

from __future__ import annotations

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ComplexityClass(Enum):
    """Algorithm complexity classes."""
    O_1 = "O(1)"  # Constant
    O_LOG_N = "O(log n)"  # Logarithmic
    O_N = "O(n)"  # Linear
    O_N_LOG_N = "O(n log n)"  # Linearithmic
    O_N2 = "O(n²)"  # Quadratic
    O_N3 = "O(n³)"  # Cubic
    O_2N = "O(2ⁿ)"  # Exponential
    O_NF = "O(n!)"  # Factorial


@dataclass
class OptimizationSuggestion:
    """Represents a code optimization suggestion."""
    line: int
    issue_type: str
    current_complexity: str
    description: str
    suggestion: str
    potential_improvement: str
    priority: str  # high, medium, low
    code_snippet: str


@dataclass
class PerformanceMetric:
    """Performance metrics for code analysis."""
    function_name: str
    time_complexity: ComplexityClass
    space_complexity: ComplexityClass
    nested_loops: int
    recursive_calls: int
    memory_allocations: int
    suggestions: List[str]


class CodeOptimizer:
    """Analyzes code for efficiency and provides optimization recommendations."""
    
    def __init__(self):
        """Initialize the code optimizer."""
        self.anti_patterns = self._initialize_anti_patterns()
    
    def analyze_complexity(self, code: str, language: str) -> List[PerformanceMetric]:
        """
        Analyze algorithmic complexity of functions in the code.
        
        Args:
            code: The source code to analyze
            language: Programming language of the code
            
        Returns:
            List of performance metrics for each function
        """
        metrics = []
        
        if language.lower() == 'python':
            metrics = self._analyze_python_complexity(code)
        elif language.lower() in ['javascript', 'typescript']:
            metrics = self._analyze_javascript_complexity(code)
        elif language.lower() == 'java':
            metrics = self._analyze_java_complexity(code)
        
        return metrics
    
    def get_optimization_suggestions(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """
        Get optimization suggestions for the code.
        
        Args:
            code: The source code to analyze
            language: Programming language of the code
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        # Check for common anti-patterns
        suggestions.extend(self._check_nested_loops(code, language))
        suggestions.extend(self._check_inefficient_operations(code, language))
        suggestions.extend(self._check_memory_issues(code, language))
        suggestions.extend(self._check_string_operations(code, language))
        suggestions.extend(self._check_data_structure_usage(code, language))
        
        return sorted(suggestions, key=lambda s: self._priority_order(s.priority))
    
    def _priority_order(self, priority: str) -> int:
        """Return numeric order for priority sorting."""
        order = {'high': 0, 'medium': 1, 'low': 2}
        return order.get(priority, 3)
    
    def _initialize_anti_patterns(self) -> Dict:
        """Initialize common anti-patterns to detect."""
        return {
            'nested_loops': {
                'description': 'Multiple nested loops detected',
                'impact': 'Increases time complexity exponentially'
            },
            'repeated_operations': {
                'description': 'Repeated operations in loop',
                'impact': 'Unnecessary computation overhead'
            },
            'inefficient_search': {
                'description': 'Linear search in loop',
                'impact': 'Could use hash table for O(1) lookup'
            },
            'string_concatenation': {
                'description': 'String concatenation in loop',
                'impact': 'Creates new string objects repeatedly'
            },
            'premature_optimization': {
                'description': 'Overly complex optimization',
                'impact': 'Reduces readability without significant gains'
            },
        }
    
    def _analyze_python_complexity(self, code: str) -> List[PerformanceMetric]:
        """Analyze complexity of Python code."""
        metrics = []
        
        # Find all function definitions
        function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        functions = re.finditer(function_pattern, code)
        
        for func_match in functions:
            func_name = func_match.group(1)
            func_start = func_match.start()
            
            # Extract function body (simplified)
            lines = code[func_start:].split('\n')
            func_body = []
            indent_level = None
            
            for line in lines[1:]:  # Skip function definition line
                if line.strip() and indent_level is None:
                    indent_level = len(line) - len(line.lstrip())
                
                if indent_level is not None:
                    current_indent = len(line) - len(line.lstrip())
                    if line.strip() and current_indent < indent_level:
                        break
                    func_body.append(line)
            
            func_code = '\n'.join(func_body)
            
            # Analyze the function
            nested_loops = self._count_nested_loops(func_code)
            recursive_calls = func_code.count(f'{func_name}(')
            memory_allocs = self._count_memory_allocations(func_code, 'python')
            
            # Estimate time complexity
            time_complexity = self._estimate_time_complexity(
                nested_loops, recursive_calls, func_code
            )
            
            # Estimate space complexity
            space_complexity = self._estimate_space_complexity(
                memory_allocs, recursive_calls
            )
            
            # Generate suggestions
            suggestions = []
            if nested_loops >= 2:
                suggestions.append("Consider using dynamic programming or memoization to reduce nested loops")
            if recursive_calls > 0 and 'memo' not in func_code.lower():
                suggestions.append("Add memoization to recursive function to avoid redundant calculations")
            if func_code.count('append(') > 10:
                suggestions.append("Consider list comprehension instead of repeated append() calls")
            if '.sort()' in func_code and 'for' in func_code:
                suggestions.append("Sorting in a loop can be optimized - consider sorting once outside the loop")
            
            metrics.append(PerformanceMetric(
                function_name=func_name,
                time_complexity=time_complexity,
                space_complexity=space_complexity,
                nested_loops=nested_loops,
                recursive_calls=recursive_calls,
                memory_allocations=memory_allocs,
                suggestions=suggestions
            ))
        
        return metrics
    
    def _analyze_javascript_complexity(self, code: str) -> List[PerformanceMetric]:
        """Analyze complexity of JavaScript/TypeScript code."""
        metrics = []
        
        # Find all function definitions
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*function\s*\([^)]*\)',
        ]
        
        for pattern in function_patterns:
            functions = re.finditer(pattern, code)
            
            for func_match in functions:
                func_name = func_match.group(1)
                func_start = func_match.start()
                
                # Extract function body (simplified)
                brace_count = 0
                func_end = func_start
                found_start = False
                
                for i, char in enumerate(code[func_start:], func_start):
                    if char == '{':
                        found_start = True
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if found_start and brace_count == 0:
                            func_end = i
                            break
                
                func_code = code[func_start:func_end]
                
                # Analyze the function
                nested_loops = self._count_nested_loops(func_code)
                recursive_calls = func_code.count(f'{func_name}(')
                memory_allocs = self._count_memory_allocations(func_code, 'javascript')
                
                time_complexity = self._estimate_time_complexity(
                    nested_loops, recursive_calls, func_code
                )
                
                space_complexity = self._estimate_space_complexity(
                    memory_allocs, recursive_calls
                )
                
                suggestions = []
                if nested_loops >= 2:
                    suggestions.append("Consider using Map or Set for O(1) lookups instead of nested loops")
                if '.forEach(' in func_code and '.map(' in func_code:
                    suggestions.append("Chain array methods or use a single iteration to improve performance")
                if 'new Array' in func_code or 'Array(' in func_code:
                    suggestions.append("Consider using array literals [] for better performance")
                
                metrics.append(PerformanceMetric(
                    function_name=func_name,
                    time_complexity=time_complexity,
                    space_complexity=space_complexity,
                    nested_loops=nested_loops,
                    recursive_calls=recursive_calls,
                    memory_allocations=memory_allocs,
                    suggestions=suggestions
                ))
        
        return metrics
    
    def _analyze_java_complexity(self, code: str) -> List[PerformanceMetric]:
        """Analyze complexity of Java code."""
        metrics = []
        
        # Find all method definitions
        method_pattern = r'(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{'
        methods = re.finditer(method_pattern, code)
        
        for method_match in methods:
            method_name = method_match.group(1)
            method_start = method_match.start()
            
            # Extract method body
            brace_count = 0
            method_end = method_start
            found_start = False
            
            for i, char in enumerate(code[method_start:], method_start):
                if char == '{':
                    found_start = True
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if found_start and brace_count == 0:
                        method_end = i
                        break
            
            method_code = code[method_start:method_end]
            
            nested_loops = self._count_nested_loops(method_code)
            recursive_calls = method_code.count(f'{method_name}(')
            memory_allocs = self._count_memory_allocations(method_code, 'java')
            
            time_complexity = self._estimate_time_complexity(
                nested_loops, recursive_calls, method_code
            )
            
            space_complexity = self._estimate_space_complexity(
                memory_allocs, recursive_calls
            )
            
            suggestions = []
            if 'new ' in method_code and 'for' in method_code:
                suggestions.append("Object creation in loop detected - consider object pooling")
            if 'Collections.sort' in method_code and nested_loops > 0:
                suggestions.append("Sorting in loop detected - optimize by sorting once")
            
            metrics.append(PerformanceMetric(
                function_name=method_name,
                time_complexity=time_complexity,
                space_complexity=space_complexity,
                nested_loops=nested_loops,
                recursive_calls=recursive_calls,
                memory_allocations=memory_allocs,
                suggestions=suggestions
            ))
        
        return metrics
    
    def _count_nested_loops(self, code: str) -> int:
        """Count the maximum depth of nested loops."""
        max_depth = 0
        current_depth = 0
        
        # Match for, while loops
        loop_keywords = ['for', 'while', 'foreach']
        
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            
            # Check if line starts a loop
            if any(stripped.startswith(keyword) for keyword in loop_keywords):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            
            # Simple heuristic: decrease depth when indentation decreases significantly
            # This is simplified and may not be 100% accurate
            if stripped.startswith('}') or (stripped and len(line) - len(line.lstrip()) == 0):
                current_depth = max(0, current_depth - 1)
        
        return max_depth
    
    def _count_memory_allocations(self, code: str, language: str) -> int:
        """Count memory allocation operations."""
        count = 0
        
        if language == 'python':
            # Lists, dicts, sets, objects
            count += code.count('[')
            count += code.count('{')
            count += code.count('list(')
            count += code.count('dict(')
            count += code.count('set(')
        elif language in ['javascript', 'typescript']:
            count += code.count('new ')
            count += code.count('[')
            count += code.count('{')
        elif language == 'java':
            count += code.count('new ')
            count += code.count('ArrayList')
            count += code.count('HashMap')
        
        return count
    
    def _estimate_time_complexity(self, nested_loops: int, recursive_calls: int, code: str) -> ComplexityClass:
        """Estimate time complexity based on code analysis."""
        # This is a simplified heuristic
        if nested_loops >= 3:
            return ComplexityClass.O_N3
        elif nested_loops == 2:
            return ComplexityClass.O_N2
        elif nested_loops == 1:
            if 'sort' in code.lower():
                return ComplexityClass.O_N_LOG_N
            return ComplexityClass.O_N
        elif recursive_calls > 0:
            if 'memo' in code.lower() or 'cache' in code.lower():
                return ComplexityClass.O_N
            if recursive_calls > 1:
                return ComplexityClass.O_2N
            return ComplexityClass.O_N
        else:
            return ComplexityClass.O_1
    
    def _estimate_space_complexity(self, memory_allocs: int, recursive_calls: int) -> ComplexityClass:
        """Estimate space complexity based on code analysis."""
        if recursive_calls > 1:
            return ComplexityClass.O_2N
        elif recursive_calls == 1:
            return ComplexityClass.O_N
        elif memory_allocs > 5:
            return ComplexityClass.O_N
        else:
            return ComplexityClass.O_1
    
    def _check_nested_loops(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """Check for nested loops that could be optimized."""
        suggestions = []
        lines = code.split('\n')
        
        loop_stack = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Detect loop start
            if any(keyword in stripped for keyword in ['for ', 'while ', 'foreach']):
                indent = len(line) - len(line.lstrip())
                loop_stack.append((i, indent))
                
                # Check if nested
                if len(loop_stack) >= 2:
                    suggestions.append(OptimizationSuggestion(
                        line=i,
                        issue_type='nested_loops',
                        current_complexity='O(n²) or worse',
                        description=f'{len(loop_stack)}-level nested loops detected',
                        suggestion='Consider: 1) Using hash tables for O(1) lookup, 2) Preprocessing data, 3) Using built-in functions, 4) Algorithm redesign',
                        potential_improvement=f'Could reduce from O(n{len(loop_stack)}) to O(n) or O(n log n)',
                        priority='high',
                        code_snippet=line.strip()
                    ))
            
            # Detect loop end (simplified)
            if stripped.startswith('}') or (indent := len(line) - len(line.lstrip())) == 0:
                loop_stack = [l for l in loop_stack if l[1] < indent]
        
        return suggestions
    
    def _check_inefficient_operations(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """Check for inefficient operations."""
        suggestions = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for linear search in loop
            if 'in ' in line and any(keyword in line for keyword in ['for ', 'while ']):
                suggestions.append(OptimizationSuggestion(
                    line=i,
                    issue_type='inefficient_search',
                    current_complexity='O(n²)',
                    description='Linear search within loop',
                    suggestion='Use Set or Map for O(1) lookup instead of linear search',
                    potential_improvement='Reduce from O(n²) to O(n)',
                    priority='high',
                    code_snippet=line.strip()
                ))
            
            # Check for repeated function calls
            func_calls = re.findall(r'(\w+)\(', line)
            if len(func_calls) > 3 and len(set(func_calls)) < len(func_calls):
                suggestions.append(OptimizationSuggestion(
                    line=i,
                    issue_type='repeated_operations',
                    current_complexity='Multiple calls',
                    description='Repeated function calls detected',
                    suggestion='Cache function results in a variable',
                    potential_improvement='Reduce redundant computations',
                    priority='medium',
                    code_snippet=line.strip()
                ))
        
        return suggestions
    
    def _check_memory_issues(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """Check for memory inefficiencies."""
        suggestions = []
        lines = code.split('\n')
        
        in_loop = False
        for i, line in enumerate(lines, 1):
            if any(keyword in line for keyword in ['for ', 'while ']):
                in_loop = True
            
            if in_loop:
                # Check for object creation in loop
                if 'new ' in line or (language == 'python' and ('[' in line or '{' in line)):
                    suggestions.append(OptimizationSuggestion(
                        line=i,
                        issue_type='memory_allocation',
                        current_complexity='O(n) space per iteration',
                        description='Memory allocation inside loop',
                        suggestion='Preallocate or reuse objects outside loop',
                        potential_improvement='Reduce memory allocations and GC pressure',
                        priority='medium',
                        code_snippet=line.strip()
                    ))
            
            if line.strip().startswith('}'):
                in_loop = False
        
        return suggestions
    
    def _check_string_operations(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """Check for inefficient string operations."""
        suggestions = []
        lines = code.split('\n')
        
        # Language-specific suggestions
        language_suggestions = {
            'python': 'Use list and join(), or io.StringIO',
            'javascript': 'Use array and join()',
            'java': 'Use StringBuilder'
        }
        suggestion_text = language_suggestions.get(language, 'Use string builder pattern')
        
        in_loop = False
        for i, line in enumerate(lines, 1):
            if any(keyword in line for keyword in ['for ', 'while ']):
                in_loop = True
            
            if in_loop and ('+=' in line or '+ ' in line) and ("'" in line or '"' in line):
                suggestions.append(OptimizationSuggestion(
                    line=i,
                    issue_type='string_concatenation',
                    current_complexity='O(n²) for string building',
                    description='String concatenation in loop',
                    suggestion=suggestion_text,
                    potential_improvement='Reduce from O(n²) to O(n)',
                    priority='high',
                    code_snippet=line.strip()
                ))
            
            if line.strip().startswith('}'):
                in_loop = False
        
        return suggestions
    
    def _check_data_structure_usage(self, code: str, language: str) -> List[OptimizationSuggestion]:
        """Check for suboptimal data structure usage."""
        suggestions = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for list when set would be better
            if language == 'python':
                if '[' in line and 'in ' in code:
                    if 'unique' in code.lower() or 'duplicate' in code.lower():
                        suggestions.append(OptimizationSuggestion(
                            line=i,
                            issue_type='data_structure',
                            current_complexity='O(n) for membership test',
                            description='Using list for membership testing',
                            suggestion='Use set for O(1) membership tests when checking uniqueness',
                            potential_improvement='Improve lookup from O(n) to O(1)',
                            priority='medium',
                            code_snippet=line.strip()
                        ))
        
        return suggestions
    
    def generate_optimization_report(self, metrics: List[PerformanceMetric], 
                                    suggestions: List[OptimizationSuggestion]) -> str:
        """
        Generate a comprehensive optimization report.
        
        Args:
            metrics: Performance metrics
            suggestions: Optimization suggestions
            
        Returns:
            Formatted optimization report
        """
        report = "⚡ CODE OPTIMIZATION REPORT\n"
        report += "=" * 60 + "\n\n"
        
        # Complexity Analysis
        if metrics:
            report += "COMPLEXITY ANALYSIS:\n"
            report += "-" * 60 + "\n"
            
            for metric in metrics:
                report += f"\n📊 Function: {metric.function_name}\n"
                report += f"   Time Complexity: {metric.time_complexity.value}\n"
                report += f"   Space Complexity: {metric.space_complexity.value}\n"
                report += f"   Nested Loops: {metric.nested_loops}\n"
                report += f"   Recursive Calls: {metric.recursive_calls}\n"
                
                if metric.suggestions:
                    report += "   Suggestions:\n"
                    for suggestion in metric.suggestions:
                        report += f"     • {suggestion}\n"
            
            report += "\n"
        
        # Optimization Suggestions
        if suggestions:
            report += "OPTIMIZATION SUGGESTIONS:\n"
            report += "-" * 60 + "\n"
            
            # Group by priority
            by_priority = {'high': [], 'medium': [], 'low': []}
            for suggestion in suggestions:
                by_priority[suggestion.priority].append(suggestion)
            
            for priority in ['high', 'medium', 'low']:
                if by_priority[priority]:
                    icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
                    report += f"\n{icon} {priority.upper()} PRIORITY:\n"
                    
                    for suggestion in by_priority[priority]:
                        report += f"\n  Line {suggestion.line}: {suggestion.issue_type}\n"
                        report += f"  Current: {suggestion.current_complexity}\n"
                        report += f"  Issue: {suggestion.description}\n"
                        report += f"  Suggestion: {suggestion.suggestion}\n"
                        report += f"  Improvement: {suggestion.potential_improvement}\n"
        
        if not metrics and not suggestions:
            report += "✅ No obvious optimization opportunities found!\n"
            report += "Code appears to be reasonably efficient.\n"
        
        report += "\n" + "=" * 60 + "\n"
        report += "\n💡 Remember: Premature optimization is the root of all evil.\n"
        report += "   Focus on readability first, optimize bottlenecks later.\n"
        
        return report
