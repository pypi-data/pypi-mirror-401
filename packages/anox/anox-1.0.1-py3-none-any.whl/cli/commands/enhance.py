"""Enhanced analyze command with syntax, security, and optimization analysis.

This command provides comprehensive code analysis including:
- Real-time syntax checking and corrections
- Security vulnerability scanning
- Code efficiency and optimization suggestions
"""

import click
from pathlib import Path
from typing import Optional

from core.syntax_analyzer import SyntaxAnalyzer, get_syntax_suggestions
from core.security_scanner import SecurityScanner
from core.code_optimizer import CodeOptimizer


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--language', '-l', help='Programming language (auto-detected if not specified)')
@click.option('--check', '-c', multiple=True, 
              type=click.Choice(['syntax', 'security', 'optimization', 'all']),
              default=['all'],
              help='Types of checks to perform')
@click.option('--fix', is_flag=True, help='Auto-fix syntax issues where possible')
@click.option('--severity', type=click.Choice(['critical', 'high', 'medium', 'low', 'all']),
              default='all',
              help='Minimum severity level for security issues')
@click.option('--output', '-o', type=click.Path(), help='Output file for the report')
def enhance(file_path: str, language: Optional[str], check: tuple, fix: bool, 
            severity: str, output: Optional[str]):
    """
    Perform comprehensive code analysis with syntax, security, and optimization checks.
    
    Examples:
        anox enhance myfile.py
        anox enhance app.js --check security --severity high
        anox enhance code.java --check optimization --output report.txt
        anox enhance script.py --fix
    """
    file_path_obj = Path(file_path)
    
    # Auto-detect language if not specified
    if not language:
        language = detect_language(file_path_obj)
    
    # Read the file
    try:
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        click.echo(f"❌ Error reading file: {e}", err=True)
        return 1
    
    # Normalize check types
    if 'all' in check:
        check = ('syntax', 'security', 'optimization')
    
    report_parts = []
    report_parts.append(f"\n{'='*70}")
    report_parts.append(f"🔍 ANOX ENHANCED CODE ANALYSIS")
    report_parts.append(f"{'='*70}")
    report_parts.append(f"File: {file_path}")
    report_parts.append(f"Language: {language.upper()}")
    report_parts.append(f"Checks: {', '.join(check).upper()}")
    report_parts.append(f"{'='*70}\n")
    
    # Syntax Analysis
    if 'syntax' in check:
        click.echo("🔤 Running syntax analysis...")
        analyzer = SyntaxAnalyzer()
        issues = analyzer.analyze(code, language)
        
        if issues:
            report_parts.append("\n📝 SYNTAX ISSUES FOUND:")
            report_parts.append("-" * 70)
            
            for issue in issues:
                icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}.get(issue.severity, '•')
                report_parts.append(f"\n{icon} Line {issue.line}:{issue.column} [{issue.severity.upper()}]")
                report_parts.append(f"   {issue.message}")
                if issue.suggestion:
                    report_parts.append(f"   💡 Suggestion: {issue.suggestion}")
            
            # Auto-fix if requested
            if fix:
                click.echo("🔧 Attempting auto-fix...")
                fixed_code, fixes = analyzer.auto_fix(code, language)
                
                if fixes:
                    report_parts.append(f"\n✅ AUTO-FIX APPLIED:")
                    for fix_msg in fixes:
                        report_parts.append(f"   • {fix_msg}")
                    
                    # Write fixed code back to file
                    backup_path = file_path_obj.with_suffix(file_path_obj.suffix + '.backup')
                    file_path_obj.rename(backup_path)
                    
                    with open(file_path_obj, 'w', encoding='utf-8') as f:
                        f.write(fixed_code)
                    
                    report_parts.append(f"\n   Original saved as: {backup_path}")
                    report_parts.append(f"   Fixed code written to: {file_path}")
                else:
                    report_parts.append("\n   No auto-fixable issues found.")
        else:
            report_parts.append("\n✅ No syntax issues found!")
    
    # Security Scan
    if 'security' in check:
        click.echo("🔒 Running security scan...")
        scanner = SecurityScanner()
        vulnerabilities = scanner.scan(code, language, str(file_path))
        
        # Filter by severity if specified
        if severity != 'all':
            severity_order = ['critical', 'high', 'medium', 'low']
            min_index = severity_order.index(severity)
            # Create lookup for efficient filtering
            allowed_severities = set(severity_order[:min_index + 1])
            vulnerabilities = [
                v for v in vulnerabilities 
                if v.severity in allowed_severities
            ]
        
        security_report = scanner.generate_security_report(vulnerabilities)
        report_parts.append(f"\n{security_report}")
        
        # Add secure coding practices
        if vulnerabilities:
            report_parts.append("\n📚 SECURE CODING PRACTICES:")
            report_parts.append("-" * 70)
            practices = scanner.get_secure_coding_practices(language)
            for practice in practices[:5]:  # Show top 5
                report_parts.append(f"  • {practice}")
    
    # Optimization Analysis
    if 'optimization' in check:
        click.echo("⚡ Running optimization analysis...")
        optimizer = CodeOptimizer()
        
        metrics = optimizer.analyze_complexity(code, language)
        suggestions = optimizer.get_optimization_suggestions(code, language)
        
        optimization_report = optimizer.generate_optimization_report(metrics, suggestions)
        report_parts.append(f"\n{optimization_report}")
    
    # Compile and display report
    full_report = '\n'.join(report_parts)
    click.echo(full_report)
    
    # Save to file if requested
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(full_report)
            click.echo(f"\n📄 Report saved to: {output}")
        except Exception as e:
            click.echo(f"❌ Error saving report: {e}", err=True)
    
    # Return exit code based on findings
    if 'security' in check and vulnerabilities:
        critical_or_high = [v for v in vulnerabilities if v.severity in ['critical', 'high']]
        if critical_or_high:
            return 1
    
    return 0


def detect_language(file_path: Path) -> str:
    """Detect programming language from file extension."""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cs': 'csharp',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
    }
    
    suffix = file_path.suffix.lower()
    return extension_map.get(suffix, 'unknown')


if __name__ == '__main__':
    enhance()
