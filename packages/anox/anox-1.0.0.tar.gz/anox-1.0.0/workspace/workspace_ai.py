"""Context-Aware AI Assistant for Anox Workspace.

This module implements a workspace-embedded AI assistant that:
1. Always knows the current workspace root
2. Reads files and understands project structure
3. References terminal output for error detection
4. Proactively warns about issues
5. Provides explainable and reversible actions
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import re

from .workspace_core import get_workspace_core
from .backend_api import BackendAPIFacade, FileOperation
from .events import get_event_bus, EventType


@dataclass
class AIWarning:
    """Warning detected by AI assistant."""
    
    severity: str  # 'error', 'warning', 'info'
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    confidence: float = 0.0


@dataclass
class AIAction:
    """Action proposed by AI assistant."""
    
    action_type: str  # 'fix', 'refactor', 'add_import', 'create_file', etc.
    description: str
    target_file: str
    changes: List[Dict[str, Any]]
    reversible: bool
    confidence: float
    explanation: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'action_type': self.action_type,
            'description': self.description,
            'target_file': self.target_file,
            'changes': self.changes,
            'reversible': self.reversible,
            'confidence': self.confidence,
            'explanation': self.explanation,
        }


class WorkspaceAwareAI:
    """Context-aware AI assistant embedded in workspace.
    
    This AI assistant:
    - Always tracks workspace root
    - Indexes project structure
    - Monitors file changes
    - Watches terminal output
    - Provides proactive warnings
    - Suggests fixes with explanations
    - All actions are reversible
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize workspace-aware AI.
        
        Args:
            workspace_root: Workspace root (uses current workspace if None)
        """
        self.workspace_core = get_workspace_core()
        self.event_bus = get_event_bus()
        
        # Get workspace root from core or parameter
        if workspace_root is None:
            workspace_root = self.workspace_core.get_current_root()
        
        if workspace_root is None:
            raise ValueError("No active workspace. Set workspace root first.")
        
        self.workspace_root = workspace_root
        self.backend = BackendAPIFacade(workspace_root)
        
        # Context tracking
        self._project_structure: Dict[str, Any] = {}
        self._file_cache: Dict[str, str] = {}
        self._terminal_history: List[Dict[str, Any]] = []
        self._warnings: List[AIWarning] = []
        self._suggested_actions: List[AIAction] = []
        
        # Configuration
        self._monitoring_enabled = True
        self._proactive_warnings = True
        self._auto_fix_threshold = 0.9  # Only auto-fix with 90%+ confidence
        
        # Subscribe to workspace events
        self._subscribe_to_events()
        
        # Initial project scan
        self._scan_project_structure()
    
    def _subscribe_to_events(self) -> None:
        """Subscribe to workspace events for monitoring."""
        # File changes
        self.event_bus.subscribe(EventType.FILE_SAVED, self._on_file_saved)
        self.event_bus.subscribe(EventType.FILE_OPENED, self._on_file_opened)
        
        # Terminal events
        self.event_bus.subscribe(EventType.COMMAND_EXECUTED, self._on_command_executed)
        self.event_bus.subscribe(EventType.ERROR_DETECTED, self._on_error_detected)
        
        # Workspace changes
        self.event_bus.subscribe(
            EventType.WORKSPACE_ROOT_CHANGED,
            self._on_workspace_changed
        )
    
    def _scan_project_structure(self) -> None:
        """Scan and index project structure."""
        try:
            operation = FileOperation(
                operation='list',
                path='',
                options={'recursive': True}
            )
            result = self.backend.execute_file_operation(operation)
            
            if result.success:
                files = result.data
                
                # Build project structure
                self._project_structure = {
                    'total_files': len(files),
                    'files_by_type': self._categorize_files(files),
                    'potential_entry_points': self._find_entry_points(files),
                    'config_files': self._find_config_files(files),
                    'dependencies': self._extract_dependencies(files),
                    'last_scan': datetime.now().isoformat(),
                }
                
                print(f"✅ AI: Indexed {len(files)} files in workspace")
            else:
                print(f"⚠️  AI: Could not scan project - {result.error}")
        except Exception as e:
            print(f"⚠️  AI: Error scanning project - {e}")
    
    def _categorize_files(self, files: List[Any]) -> Dict[str, List[str]]:
        """Categorize files by type."""
        categories: Dict[str, List[str]] = {
            'python': [],
            'javascript': [],
            'typescript': [],
            'html': [],
            'css': [],
            'json': [],
            'markdown': [],
            'yaml': [],
            'other': []
        }
        
        for file_info in files:
            if file_info.is_dir:
                continue
            
            name = file_info.name.lower()
            path = file_info.path
            
            if name.endswith('.py'):
                categories['python'].append(path)
            elif name.endswith(('.js', '.jsx')):
                categories['javascript'].append(path)
            elif name.endswith(('.ts', '.tsx')):
                categories['typescript'].append(path)
            elif name.endswith('.html'):
                categories['html'].append(path)
            elif name.endswith('.css'):
                categories['css'].append(path)
            elif name.endswith('.json'):
                categories['json'].append(path)
            elif name.endswith('.md'):
                categories['markdown'].append(path)
            elif name.endswith(('.yml', '.yaml')):
                categories['yaml'].append(path)
            else:
                categories['other'].append(path)
        
        return categories
    
    def _find_entry_points(self, files: List[Any]) -> List[str]:
        """Find potential entry point files."""
        entry_points = []
        
        common_names = [
            'main.py', 'app.py', '__main__.py',
            'index.js', 'index.ts', 'main.js',
            'server.py', 'server.js',
            'cli.py', 'run.py'
        ]
        
        for file_info in files:
            if file_info.is_dir:
                continue
            
            if file_info.name.lower() in common_names:
                entry_points.append(file_info.path)
        
        return entry_points
    
    def _find_config_files(self, files: List[Any]) -> List[str]:
        """Find configuration files."""
        config_files = []
        
        config_patterns = [
            'package.json', 'requirements.txt', 'setup.py',
            'pyproject.toml', 'Pipfile', 'poetry.lock',
            'tsconfig.json', 'webpack.config.js',
            '.env', '.env.example', 'config.py', 'config.json'
        ]
        
        for file_info in files:
            if file_info.is_dir:
                continue
            
            name = file_info.name
            if name in config_patterns or name.startswith('.'):
                config_files.append(file_info.path)
        
        return config_files
    
    def _extract_dependencies(self, files: List[Any]) -> Dict[str, List[str]]:
        """Extract project dependencies from config files."""
        dependencies = {
            'python': [],
            'javascript': [],
            'unknown': []
        }
        
        # This would be enhanced to actually read and parse config files
        # For now, just identify which dependency files exist
        
        for file_info in files:
            if file_info.is_dir:
                continue
            
            if file_info.name == 'requirements.txt':
                dependencies['python'].append('requirements.txt detected')
            elif file_info.name == 'package.json':
                dependencies['javascript'].append('package.json detected')
        
        return dependencies
    
    # Event handlers
    
    def _on_file_saved(self, event: Any) -> None:
        """Handle file saved event - analyze for issues."""
        if not self._monitoring_enabled:
            return
        
        file_path = event.data.get('path')
        if not file_path:
            return
        
        # Read file content
        operation = FileOperation(operation='read', path=file_path)
        result = self.backend.execute_file_operation(operation)
        
        if result.success:
            content = result.data
            self._file_cache[file_path] = content
            
            # Analyze for issues
            if self._proactive_warnings:
                warnings = self._analyze_file_for_issues(file_path, content)
                self._warnings.extend(warnings)
                
                # Emit warnings to UI
                if warnings:
                    self._emit_warnings(warnings)
    
    def _on_file_opened(self, event: Any) -> None:
        """Handle file opened event - provide context."""
        file_path = event.data.get('path')
        if not file_path:
            return
        
        # Check if there are existing warnings for this file
        file_warnings = [w for w in self._warnings if w.file_path == file_path]
        if file_warnings:
            print(f"⚠️  AI: {len(file_warnings)} warning(s) for {file_path}")
    
    def _on_command_executed(self, event: Any) -> None:
        """Handle command executed event - track terminal history."""
        command = event.data.get('command')
        output = event.data.get('output')
        success = event.data.get('success', True)
        
        self._terminal_history.append({
            'command': command,
            'output': output,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 50 commands
        if len(self._terminal_history) > 50:
            self._terminal_history = self._terminal_history[-50:]
    
    def _on_error_detected(self, event: Any) -> None:
        """Handle error detected in terminal - parse and suggest fixes."""
        errors = event.data.get('errors', [])
        
        for error in errors:
            file_path = error.get('file')
            line = error.get('line')
            message = error.get('message')
            
            if file_path and line:
                # Create warning
                warning = AIWarning(
                    severity='error',
                    message=f"Terminal error: {message}",
                    file_path=file_path,
                    line_number=line,
                    suggestion=self._suggest_fix_for_error(error),
                    auto_fixable=False,
                    confidence=0.7
                )
                
                self._warnings.append(warning)
                print(f"🔴 AI: Error in {file_path}:{line} - {message}")
    
    def _on_workspace_changed(self, event: Any) -> None:
        """Handle workspace root changed - rescan project."""
        new_root = event.data.get('new_root')
        if new_root:
            self.workspace_root = Path(new_root)
            self.backend = BackendAPIFacade(self.workspace_root)
            self._scan_project_structure()
            
            # Clear cached data
            self._file_cache.clear()
            self._warnings.clear()
            self._suggested_actions.clear()
    
    # Analysis methods
    
    def _analyze_file_for_issues(self, file_path: str, 
                                  content: str) -> List[AIWarning]:
        """Analyze file content for potential issues.
        
        This is a simplified version. In production, this would use
        actual AI models to analyze code.
        """
        warnings = []
        
        # Check for common issues (simplified pattern matching)
        issues = self._check_common_issues(file_path, content)
        
        for issue in issues:
            warning = AIWarning(
                severity=issue['severity'],
                message=issue['message'],
                file_path=file_path,
                line_number=issue.get('line'),
                suggestion=issue.get('suggestion'),
                auto_fixable=issue.get('auto_fixable', False),
                confidence=issue.get('confidence', 0.5)
            )
            warnings.append(warning)
        
        return warnings
    
    def _check_common_issues(self, file_path: str, 
                            content: str) -> List[Dict[str, Any]]:
        """Check for common code issues using pattern matching."""
        issues = []
        lines = content.split('\n')
        
        # Python-specific checks
        if file_path.endswith('.py'):
            # Check for missing imports
            if 'import ' not in content and 'from ' not in content:
                if any(keyword in content for keyword in ['os.', 'sys.', 'json.', 'Path(']):
                    issues.append({
                        'severity': 'warning',
                        'message': 'Missing import statements detected',
                        'line': 1,
                        'suggestion': 'Add necessary import statements at top of file',
                        'auto_fixable': True,
                        'confidence': 0.8
                    })
            
            # Check for unused imports (simplified)
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    module = line.split()[1].split('.')[0]
                    if module not in '\n'.join(lines[i:]):  # Very basic check
                        issues.append({
                            'severity': 'info',
                            'message': f'Potentially unused import: {module}',
                            'line': i,
                            'suggestion': 'Remove if not needed',
                            'auto_fixable': True,
                            'confidence': 0.6
                        })
        
        # JavaScript/TypeScript checks
        if file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            # Check for console.log (common debug leftover)
            for i, line in enumerate(lines, 1):
                if 'console.log' in line and not line.strip().startswith('//'):
                    issues.append({
                        'severity': 'info',
                        'message': 'Console.log statement found (debug code?)',
                        'line': i,
                        'suggestion': 'Remove before production deployment',
                        'auto_fixable': True,
                        'confidence': 0.7
                    })
        
        # Check for long files
        if len(lines) > 500:
            issues.append({
                'severity': 'info',
                'message': f'Large file ({len(lines)} lines) - consider refactoring',
                'suggestion': 'Split into smaller modules for better maintainability',
                'auto_fixable': False,
                'confidence': 0.5
            })
        
        return issues
    
    def _suggest_fix_for_error(self, error: Dict[str, Any]) -> str:
        """Suggest a fix for terminal error."""
        message = error.get('message', '')
        
        # Common error patterns and suggestions
        if 'ModuleNotFoundError' in message or 'ImportError' in message:
            module = self._extract_module_name(message)
            return f"Install missing module: pip install {module}"
        
        elif 'SyntaxError' in message:
            return "Check syntax at indicated line - missing colon, parenthesis, or quote?"
        
        elif 'NameError' in message:
            var_name = self._extract_variable_name(message)
            return f"Variable '{var_name}' not defined - check spelling or add definition"
        
        elif 'FileNotFoundError' in message:
            return "File not found - check path and ensure file exists"
        
        else:
            return "Review error message and check documentation"
    
    def _extract_module_name(self, error_message: str) -> str:
        """Extract module name from error message."""
        match = re.search(r"No module named '(\w+)'", error_message)
        if match:
            return match.group(1)
        return "unknown-module"
    
    def _extract_variable_name(self, error_message: str) -> str:
        """Extract variable name from error message."""
        match = re.search(r"name '(\w+)' is not defined", error_message)
        if match:
            return match.group(1)
        return "unknown-variable"
    
    def _emit_warnings(self, warnings: List[AIWarning]) -> None:
        """Emit warnings to UI via event system."""
        for warning in warnings:
            self.event_bus.emit(
                EventType.WORKSPACE_STATE_CHANGED,
                {
                    'type': 'ai_warning',
                    'warning': {
                        'severity': warning.severity,
                        'message': warning.message,
                        'file': warning.file_path,
                        'line': warning.line_number,
                        'suggestion': warning.suggestion,
                        'auto_fixable': warning.auto_fixable,
                        'confidence': warning.confidence
                    }
                },
                source='workspace_ai'
            )
    
    # Public API
    
    def get_workspace_context(self) -> Dict[str, Any]:
        """Get current workspace context for AI operations.
        
        Returns:
            Complete workspace context including structure, files, terminal history
        """
        return {
            'workspace_root': str(self.workspace_root),
            'project_structure': self._project_structure,
            'open_files': list(self._file_cache.keys()),
            'terminal_history': self._terminal_history[-10:],  # Last 10 commands
            'active_warnings': [
                {
                    'severity': w.severity,
                    'message': w.message,
                    'file': w.file_path,
                    'line': w.line_number
                }
                for w in self._warnings
            ],
            'suggested_actions': [a.to_dict() for a in self._suggested_actions]
        }
    
    def get_warnings(self, file_path: Optional[str] = None) -> List[AIWarning]:
        """Get warnings, optionally filtered by file.
        
        Args:
            file_path: Optional file path to filter by
            
        Returns:
            List of warnings
        """
        if file_path:
            return [w for w in self._warnings if w.file_path == file_path]
        return self._warnings.copy()
    
    def get_file_context(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get context about a specific file.
        
        Args:
            file_path: Path to file
            
        Returns:
            File context or None if not found
        """
        # Check if file is in cache
        content = self._file_cache.get(file_path)
        
        if content is None:
            # Try to read from filesystem
            operation = FileOperation(operation='read', path=file_path)
            result = self.backend.execute_file_operation(operation)
            
            if result.success:
                content = result.data
                self._file_cache[file_path] = content
            else:
                return None
        
        # Build context
        warnings = [w for w in self._warnings if w.file_path == file_path]
        
        return {
            'path': file_path,
            'content': content,
            'size': len(content),
            'lines': len(content.split('\n')),
            'warnings': [
                {
                    'severity': w.severity,
                    'message': w.message,
                    'line': w.line_number,
                    'suggestion': w.suggestion
                }
                for w in warnings
            ],
            'language': self._detect_language(file_path),
        }
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        if file_path.endswith('.py'):
            return 'python'
        elif file_path.endswith(('.js', '.jsx')):
            return 'javascript'
        elif file_path.endswith(('.ts', '.tsx')):
            return 'typescript'
        elif file_path.endswith('.html'):
            return 'html'
        elif file_path.endswith('.css'):
            return 'css'
        elif file_path.endswith('.json'):
            return 'json'
        else:
            return 'unknown'
    
    def clear_warnings(self, file_path: Optional[str] = None) -> None:
        """Clear warnings, optionally for specific file.
        
        Args:
            file_path: Optional file path to clear warnings for
        """
        if file_path:
            self._warnings = [w for w in self._warnings if w.file_path != file_path]
        else:
            self._warnings.clear()
    
    def rescan_workspace(self) -> Dict[str, Any]:
        """Rescan workspace structure.
        
        Returns:
            Scan result
        """
        self._scan_project_structure()
        return {
            'success': True,
            'files_indexed': self._project_structure.get('total_files', 0),
            'last_scan': self._project_structure.get('last_scan')
        }
    
    def explain_action(self, action: AIAction) -> str:
        """Get detailed explanation of proposed action.
        
        Args:
            action: Action to explain
            
        Returns:
            Detailed explanation
        """
        explanation = f"Action: {action.action_type}\n"
        explanation += f"Target: {action.target_file}\n"
        explanation += f"Description: {action.description}\n"
        explanation += f"Reversible: {'Yes' if action.reversible else 'No'}\n"
        explanation += f"Confidence: {action.confidence:.1%}\n\n"
        explanation += f"Explanation: {action.explanation}\n\n"
        explanation += f"Changes:\n"
        
        for i, change in enumerate(action.changes, 1):
            explanation += f"  {i}. {change.get('description', 'No description')}\n"
        
        return explanation


# Global instance
_global_workspace_ai: Optional[WorkspaceAwareAI] = None


def get_workspace_ai() -> WorkspaceAwareAI:
    """Get the global workspace-aware AI instance.
    
    Returns:
        Global WorkspaceAwareAI instance
    """
    global _global_workspace_ai
    if _global_workspace_ai is None:
        _global_workspace_ai = WorkspaceAwareAI()
    return _global_workspace_ai


def reset_workspace_ai() -> None:
    """Reset the global workspace AI instance (for testing)."""
    global _global_workspace_ai
    _global_workspace_ai = None
