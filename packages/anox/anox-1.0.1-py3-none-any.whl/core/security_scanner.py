"""Security vulnerability scanning and secure coding practices enforcement.

This module provides comprehensive security analysis to identify vulnerabilities
and promote secure coding practices across multiple languages.
"""

from __future__ import annotations

import re
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


class VulnerabilityType(Enum):
    """Types of security vulnerabilities."""
    SQL_INJECTION = "sql_injection"
    XSS = "cross_site_scripting"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    HARDCODED_SECRET = "hardcoded_secret"
    WEAK_CRYPTO = "weak_cryptography"
    INSECURE_RANDOM = "insecure_random"
    UNSAFE_DESERIALIZATION = "unsafe_deserialization"
    MISSING_AUTH = "missing_authentication"
    MISSING_ENCRYPTION = "missing_encryption"
    BUFFER_OVERFLOW = "buffer_overflow"
    RACE_CONDITION = "race_condition"


@dataclass
class Vulnerability:
    """Represents a security vulnerability found in code."""
    type: VulnerabilityType
    severity: str  # critical, high, medium, low
    line: int
    column: int
    description: str
    code_snippet: str
    recommendation: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID
    owasp_category: Optional[str] = None  # OWASP Top 10 category


class SecurityScanner:
    """Scans code for security vulnerabilities and provides remediation advice."""
    
    def __init__(self):
        """Initialize the security scanner."""
        self.patterns = self._initialize_patterns()
        self.secret_patterns = self._initialize_secret_patterns()
    
    def scan(self, code: str, language: str, filename: str = "") -> List[Vulnerability]:
        """
        Scan code for security vulnerabilities.
        
        Args:
            code: The source code to scan
            language: Programming language of the code
            filename: Name of the file being scanned
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        language = language.lower()
        
        # Run all applicable scanners
        vulnerabilities.extend(self._scan_sql_injection(code, language))
        vulnerabilities.extend(self._scan_xss(code, language))
        vulnerabilities.extend(self._scan_command_injection(code, language))
        vulnerabilities.extend(self._scan_path_traversal(code, language))
        vulnerabilities.extend(self._scan_hardcoded_secrets(code))
        vulnerabilities.extend(self._scan_weak_crypto(code, language))
        vulnerabilities.extend(self._scan_insecure_random(code, language))
        vulnerabilities.extend(self._scan_unsafe_deserialization(code, language))
        
        return sorted(vulnerabilities, key=lambda v: (self._severity_order(v.severity), v.line))
    
    def _severity_order(self, severity: str) -> int:
        """Return numeric order for severity sorting."""
        order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        return order.get(severity, 4)
    
    def _initialize_patterns(self) -> Dict[str, List[Dict]]:
        """Initialize vulnerability detection patterns."""
        return {
            'sql_injection': [
                {
                    'pattern': r'execute\s*\(\s*["\'].*?\+',
                    'languages': ['python', 'java', 'javascript', 'typescript'],
                    'description': 'String concatenation in SQL execute'
                },
                {
                    'pattern': r'execute\s*\(\s*.*?\+.*?\)',
                    'languages': ['python', 'java', 'javascript', 'typescript'],
                    'description': 'String concatenation in execute statement'
                },
                {
                    'pattern': r'cursor\.execute\s*\(\s*f["\']',
                    'languages': ['python'],
                    'description': 'f-string used in SQL query'
                },
                {
                    'pattern': r'query\s*=\s*["\'].*?\+',
                    'languages': ['python', 'java', 'javascript', 'typescript'],
                    'description': 'String concatenation in query construction'
                },
                {
                    'pattern': r'["\']SELECT.*?\+',
                    'languages': ['python', 'java', 'javascript', 'typescript'],
                    'description': 'SQL query with string concatenation'
                },
            ],
            'xss': [
                {
                    'pattern': r'innerHTML\s*=\s*[^"\']*(?:user|input|request|param)',
                    'languages': ['javascript', 'typescript'],
                    'description': 'User input assigned to innerHTML'
                },
                {
                    'pattern': r'dangerouslySetInnerHTML\s*=\s*\{\{',
                    'languages': ['javascript', 'typescript'],
                    'description': 'Using dangerouslySetInnerHTML in React'
                },
                {
                    'pattern': r'document\.write\s*\(',
                    'languages': ['javascript', 'typescript'],
                    'description': 'Using document.write (potential XSS)'
                },
            ],
            'command_injection': [
                {
                    'pattern': r'os\.system\s*\(\s*[^"\']*(?:user|input|request|param)',
                    'languages': ['python'],
                    'description': 'User input passed to os.system()'
                },
                {
                    'pattern': r'subprocess\.(call|run|Popen)\s*\(\s*[^"\']*(?:user|input|request)',
                    'languages': ['python'],
                    'description': 'User input passed to subprocess without shell=False'
                },
                {
                    'pattern': r'exec\s*\(\s*[^"\']*(?:user|input|request)',
                    'languages': ['python', 'java', 'javascript'],
                    'description': 'User input passed to exec()'
                },
                {
                    'pattern': r'eval\s*\(\s*[^"\']*(?:user|input|request)',
                    'languages': ['python', 'javascript', 'typescript'],
                    'description': 'User input passed to eval()'
                },
            ],
            'path_traversal': [
                {
                    'pattern': r'open\s*\(\s*[^"\']*(?:user|input|request|param)',
                    'languages': ['python'],
                    'description': 'User input used in file path'
                },
                {
                    'pattern': r'File\s*\(\s*[^"\']*(?:user|input|request)',
                    'languages': ['java'],
                    'description': 'User input used in file path'
                },
                {
                    'pattern': r'fs\.readFile\s*\(\s*[^"\']*(?:user|input|request)',
                    'languages': ['javascript', 'typescript'],
                    'description': 'User input used in file path'
                },
            ],
        }
    
    def _initialize_secret_patterns(self) -> List[Dict]:
        """Initialize patterns for detecting hardcoded secrets."""
        return [
            {
                'pattern': r'(?:password|passwd|pwd)\s*=\s*["\'][^"\']{3,}["\']',
                'description': 'Hardcoded password'
            },
            {
                'pattern': r'(?:api[_-]?key|apikey)\s*=\s*["\'][^"\']{10,}["\']',
                'description': 'Hardcoded API key'
            },
            {
                'pattern': r'(?:secret[_-]?key|secretkey)\s*=\s*["\'][^"\']{10,}["\']',
                'description': 'Hardcoded secret key'
            },
            {
                'pattern': r'(?:access[_-]?token|accesstoken)\s*=\s*["\'][^"\']{10,}["\']',
                'description': 'Hardcoded access token'
            },
            {
                'pattern': r'(?:private[_-]?key|privatekey)\s*=\s*["\'][^"\']{10,}["\']',
                'description': 'Hardcoded private key'
            },
            {
                'pattern': r'-----BEGIN (?:RSA |)PRIVATE KEY-----',
                'description': 'Private key in code'
            },
            {
                'pattern': r'aws_secret_access_key\s*=\s*["\'][^"\']+["\']',
                'description': 'Hardcoded AWS secret key'
            },
        ]
    
    def _scan_sql_injection(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for SQL injection vulnerabilities."""
        vulnerabilities = []
        
        for pattern_info in self.patterns['sql_injection']:
            if language not in pattern_info['languages']:
                continue
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.SQL_INJECTION,
                        severity='critical',
                        line=i,
                        column=0,
                        description=f"Potential SQL injection: {pattern_info['description']}",
                        code_snippet=line.strip(),
                        recommendation="Use parameterized queries or prepared statements instead of string concatenation",
                        cwe_id="CWE-89",
                        owasp_category="A03:2021 – Injection"
                    ))
        
        return vulnerabilities
    
    def _scan_xss(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for Cross-Site Scripting (XSS) vulnerabilities."""
        vulnerabilities = []
        
        for pattern_info in self.patterns['xss']:
            if language not in pattern_info['languages']:
                continue
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern_info['pattern'], line):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.XSS,
                        severity='high',
                        line=i,
                        column=0,
                        description=f"Potential XSS vulnerability: {pattern_info['description']}",
                        code_snippet=line.strip(),
                        recommendation="Sanitize and escape user input before rendering. Use textContent or safe rendering methods",
                        cwe_id="CWE-79",
                        owasp_category="A03:2021 – Injection"
                    ))
        
        return vulnerabilities
    
    def _scan_command_injection(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for command injection vulnerabilities."""
        vulnerabilities = []
        
        for pattern_info in self.patterns['command_injection']:
            if language not in pattern_info['languages']:
                continue
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern_info['pattern'], line):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.COMMAND_INJECTION,
                        severity='critical',
                        line=i,
                        column=0,
                        description=f"Potential command injection: {pattern_info['description']}",
                        code_snippet=line.strip(),
                        recommendation="Avoid passing user input to system commands. Use allowlists or safer alternatives",
                        cwe_id="CWE-78",
                        owasp_category="A03:2021 – Injection"
                    ))
        
        return vulnerabilities
    
    def _scan_path_traversal(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for path traversal vulnerabilities."""
        vulnerabilities = []
        
        for pattern_info in self.patterns['path_traversal']:
            if language not in pattern_info['languages']:
                continue
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(pattern_info['pattern'], line):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.PATH_TRAVERSAL,
                        severity='high',
                        line=i,
                        column=0,
                        description=f"Potential path traversal: {pattern_info['description']}",
                        code_snippet=line.strip(),
                        recommendation="Validate and sanitize file paths. Use allowlists or resolve to canonical paths",
                        cwe_id="CWE-22",
                        owasp_category="A01:2021 – Broken Access Control"
                    ))
        
        return vulnerabilities
    
    def _scan_hardcoded_secrets(self, code: str) -> List[Vulnerability]:
        """Scan for hardcoded secrets and credentials."""
        vulnerabilities = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith(('#', '//', '/*', '*')):
                continue
            
            for pattern_info in self.secret_patterns:
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.HARDCODED_SECRET,
                        severity='critical',
                        line=i,
                        column=0,
                        description=f"Hardcoded secret detected: {pattern_info['description']}",
                        code_snippet=line.strip()[:50] + "...",  # Truncate for safety
                        recommendation="Use environment variables or secure vaults (e.g., AWS Secrets Manager, HashiCorp Vault)",
                        cwe_id="CWE-798",
                        owasp_category="A07:2021 – Identification and Authentication Failures"
                    ))
        
        return vulnerabilities
    
    def _scan_weak_crypto(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for weak cryptographic practices."""
        vulnerabilities = []
        
        weak_algorithms = ['md5', 'sha1', 'des', 'rc4']
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for algo in weak_algorithms:
                if re.search(rf'\b{algo}\b', line, re.IGNORECASE):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.WEAK_CRYPTO,
                        severity='high',
                        line=i,
                        column=0,
                        description=f"Weak cryptographic algorithm detected: {algo.upper()}",
                        code_snippet=line.strip(),
                        recommendation=f"Replace {algo.upper()} with stronger algorithms like SHA-256, SHA-3, or AES-256",
                        cwe_id="CWE-327",
                        owasp_category="A02:2021 – Cryptographic Failures"
                    ))
        
        return vulnerabilities
    
    def _scan_insecure_random(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for insecure random number generation."""
        vulnerabilities = []
        
        insecure_patterns = {
            'python': [r'random\.random\(', r'random\.randint\('],
            'javascript': [r'Math\.random\('],
            'java': [r'new Random\(', r'Math\.random\('],
        }
        
        if language not in insecure_patterns:
            return vulnerabilities
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in insecure_patterns[language]:
                if re.search(pattern, line):
                    # Check if it's used in security context
                    if any(keyword in line.lower() for keyword in ['token', 'key', 'password', 'secret', 'auth', 'session']):
                        vulnerabilities.append(Vulnerability(
                            type=VulnerabilityType.INSECURE_RANDOM,
                            severity='medium',
                            line=i,
                            column=0,
                            description="Insecure random number generation for security-sensitive context",
                            code_snippet=line.strip(),
                            recommendation="Use cryptographically secure random generators (e.g., secrets module in Python, crypto.randomBytes in Node.js)",
                            cwe_id="CWE-338",
                            owasp_category="A02:2021 – Cryptographic Failures"
                        ))
        
        return vulnerabilities
    
    def _scan_unsafe_deserialization(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for unsafe deserialization practices."""
        vulnerabilities = []
        
        unsafe_patterns = {
            'python': [
                r'pickle\.loads?\(',
                # Check for yaml.load without SafeLoader
                # This pattern looks for yaml.load( but not followed by SafeLoader on same line
                r'yaml\.load\([^)]*\)(?!.*SafeLoader)'
            ],
            'java': [r'ObjectInputStream', r'readObject\('],
            'javascript': [r'JSON\.parse\(.*(?:user|input|request)'],
        }
        
        if language not in unsafe_patterns:
            return vulnerabilities
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in unsafe_patterns[language]:
                if re.search(pattern, line):
                    vulnerabilities.append(Vulnerability(
                        type=VulnerabilityType.UNSAFE_DESERIALIZATION,
                        severity='high',
                        line=i,
                        column=0,
                        description="Potentially unsafe deserialization detected",
                        code_snippet=line.strip(),
                        recommendation="Validate and sanitize deserialized data. Use safe deserializers or implement integrity checks",
                        cwe_id="CWE-502",
                        owasp_category="A08:2021 – Software and Data Integrity Failures"
                    ))
        
        return vulnerabilities
    
    def generate_security_report(self, vulnerabilities: List[Vulnerability]) -> str:
        """
        Generate a comprehensive security report.
        
        Args:
            vulnerabilities: List of detected vulnerabilities
            
        Returns:
            Formatted security report
        """
        if not vulnerabilities:
            return "✅ No security vulnerabilities detected!\n"
        
        # Group by severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for vuln in vulnerabilities:
            by_severity[vuln.severity].append(vuln)
        
        report = "🔒 SECURITY SCAN REPORT\n"
        report += "=" * 60 + "\n\n"
        
        # Summary
        total = len(vulnerabilities)
        report += f"Total vulnerabilities found: {total}\n"
        for severity in ['critical', 'high', 'medium', 'low']:
            count = len(by_severity[severity])
            if count > 0:
                icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                report += f"  {icon} {severity.upper()}: {count}\n"
        
        report += "\n" + "=" * 60 + "\n\n"
        
        # Detailed findings
        for severity in ['critical', 'high', 'medium', 'low']:
            if by_severity[severity]:
                report += f"\n{severity.upper()} SEVERITY ISSUES:\n"
                report += "-" * 60 + "\n"
                
                for vuln in by_severity[severity]:
                    report += f"\n📍 Line {vuln.line}: {vuln.type.value}\n"
                    report += f"   Description: {vuln.description}\n"
                    report += f"   Code: {vuln.code_snippet}\n"
                    report += f"   Recommendation: {vuln.recommendation}\n"
                    if vuln.cwe_id:
                        report += f"   CWE: {vuln.cwe_id}\n"
                    if vuln.owasp_category:
                        report += f"   OWASP: {vuln.owasp_category}\n"
        
        report += "\n" + "=" * 60 + "\n"
        report += "\n💡 Remember: Security is an ongoing process. Regular scans and code reviews are essential.\n"
        
        return report
    
    def get_secure_coding_practices(self, language: str) -> List[str]:
        """
        Get secure coding practices for a specific language.
        
        Args:
            language: Programming language
            
        Returns:
            List of secure coding practices
        """
        general_practices = [
            "Validate and sanitize all user inputs",
            "Use parameterized queries for database operations",
            "Implement proper authentication and authorization",
            "Use HTTPS for all network communications",
            "Keep dependencies up to date",
            "Implement proper error handling without exposing sensitive information",
            "Use secure random number generators for cryptographic operations",
            "Store secrets in environment variables or secure vaults",
            "Implement rate limiting and throttling",
            "Log security events for monitoring and forensics",
        ]
        
        language_specific = {
            'python': [
                "Use secrets module for cryptographic random numbers",
                "Avoid using pickle with untrusted data",
                "Use yaml.safe_load() instead of yaml.load()",
                "Set shell=False in subprocess calls",
            ],
            'javascript': [
                "Use Content Security Policy (CSP) headers",
                "Sanitize data before setting innerHTML",
                "Use crypto.randomBytes() for cryptographic operations",
                "Validate JSON schemas",
            ],
            'java': [
                "Use PreparedStatement for SQL queries",
                "Implement proper input validation using Bean Validation",
                "Use SecureRandom for cryptographic operations",
                "Avoid using reflection with untrusted data",
            ],
        }
        
        practices = general_practices.copy()
        if language.lower() in language_specific:
            practices.extend(language_specific[language.lower()])
        
        return practices
