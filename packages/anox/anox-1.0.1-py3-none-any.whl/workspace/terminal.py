"""Terminal - Integrated terminal tied to workspace root."""

import os
import subprocess
import shlex
from pathlib import Path
from typing import Dict, Any, Optional, List
from .events import get_event_bus, EventType


class Terminal:
    """Terminal component for executing commands in workspace context.
    
    Terminal is the SOURCE OF TRUTH for workspace state.
    When terminal changes directory, the entire workspace follows.
    """
    
    def __init__(self, root_path: Path, emit_events: bool = True):
        """Initialize terminal.
        
        Args:
            root_path: Workspace root directory.
            emit_events: Whether to emit events to the event bus.
        """
        self.root_path = root_path
        self._cwd = root_path
        self._env = os.environ.copy()
        self._history: List[Dict[str, Any]] = []
        self._emit_events = emit_events
        
        if emit_events:
            self.event_bus = get_event_bus()
    
    def execute(self, command: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """Execute a command in the workspace context.
        
        Args:
            command: Command to execute.
            timeout: Command timeout in seconds.
            
        Returns:
            Dictionary with stdout, stderr, return_code, and cwd.
        """
        try:
            # Parse command for cd operations
            if command.strip().startswith('cd '):
                return self._handle_cd(command)
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self._cwd),
                env=self._env,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                'command': command,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'cwd': str(self._cwd),
                'success': result.returncode == 0
            }
            
            # Add to history
            self._history.append(output)
            
            # Parse errors if command failed
            if result.returncode != 0 and result.stderr:
                errors = self.parse_error_output(result.stderr)
                output['parsed_errors'] = errors
                
                # Emit ERROR_DETECTED event for auto-jump to editor
                if self._emit_events and errors:
                    self.event_bus.emit(
                        EventType.ERROR_DETECTED,
                        {
                            'command': command,
                            'errors': errors,
                            'stderr': result.stderr,
                            'cwd': str(self._cwd)
                        },
                        'terminal'
                    )
            
            # Emit command executed event
            if self._emit_events:
                self.event_bus.emit(
                    EventType.COMMAND_EXECUTED,
                    {
                        'command': command,
                        'cwd': str(self._cwd),
                        'success': result.returncode == 0,
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    },
                    'terminal'
                )
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                'command': command,
                'stdout': '',
                'stderr': f'Command timed out after {timeout} seconds',
                'return_code': -1,
                'cwd': str(self._cwd),
                'success': False,
                'error': 'timeout'
            }
        except Exception as e:
            return {
                'command': command,
                'stdout': '',
                'stderr': str(e),
                'return_code': -1,
                'cwd': str(self._cwd),
                'success': False,
                'error': str(e)
            }
    
    def _handle_cd(self, command: str) -> Dict[str, Any]:
        """Handle cd command to change working directory.
        
        Args:
            command: cd command string.
            
        Returns:
            Result dictionary.
        """
        try:
            # Parse target directory
            parts = shlex.split(command)
            if len(parts) < 2:
                target = str(self.root_path)
            else:
                target = parts[1]
            
            # Resolve target path
            if target == '~':
                new_cwd = Path.home()
            elif target.startswith('~'):
                new_cwd = Path.home() / target[2:]
            elif Path(target).is_absolute():
                new_cwd = Path(target)
            else:
                new_cwd = self._cwd / target
            
            new_cwd = new_cwd.resolve()
            
            # Security check: stay within or below workspace root
            try:
                new_cwd.relative_to(self.root_path)
                allow_cd = True
            except ValueError:
                # Allow cd to parent directories of workspace
                allow_cd = self.root_path.is_relative_to(new_cwd)
            
            if allow_cd and new_cwd.exists() and new_cwd.is_dir():
                old_cwd = self._cwd
                self._cwd = new_cwd
                
                # Emit CWD changed event (Terminal = source of truth)
                if self._emit_events:
                    self.event_bus.emit(
                        EventType.CWD_CHANGED,
                        {
                            'old_cwd': str(old_cwd),
                            'new_cwd': str(new_cwd),
                            'workspace_root': str(self.root_path)
                        },
                        'terminal'
                    )
                
                return {
                    'command': command,
                    'stdout': str(new_cwd),
                    'stderr': '',
                    'return_code': 0,
                    'cwd': str(self._cwd),
                    'success': True
                }
            else:
                error_msg = f"cd: {target}: Directory not accessible or outside workspace"
                return {
                    'command': command,
                    'stdout': '',
                    'stderr': error_msg,
                    'return_code': 1,
                    'cwd': str(self._cwd),
                    'success': False
                }
        except Exception as e:
            return {
                'command': command,
                'stdout': '',
                'stderr': f"cd: {str(e)}",
                'return_code': 1,
                'cwd': str(self._cwd),
                'success': False
            }
    
    def get_cwd(self) -> str:
        """Get current working directory.
        
        Returns:
            Current working directory path.
        """
        return str(self._cwd)
    
    def reset_cwd(self) -> None:
        """Reset working directory to workspace root."""
        self._cwd = self.root_path
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get command history.
        
        Args:
            limit: Maximum number of history entries to return.
            
        Returns:
            List of command results.
        """
        if limit:
            return self._history[-limit:]
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear command history."""
        self._history.clear()
    
    def parse_error_output(self, stderr: str) -> List[Dict[str, Any]]:
        """Parse error output to extract file paths and line numbers.
        
        Args:
            stderr: Error output from command.
            
        Returns:
            List of parsed errors with file, line, and message.
        """
        import re
        
        errors = []
        
        # Common error patterns
        patterns = [
            # Python traceback: File "path", line N
            r'File "([^"]+)", line (\d+)',
            # GCC/Clang: path:line:column: error
            r'([^:]+):(\d+):(\d+): (?:error|warning)',
            # JavaScript/TypeScript: path(line,column)
            r'([^\(]+)\((\d+),(\d+)\)',
            # Ruby: path:line:in
            r'([^:]+):(\d+):in',
            # Go: path:line:column:
            r'([^:]+):(\d+):(\d+):',
        ]
        
        for line in stderr.split('\n'):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    file_path = match.group(1)
                    line_num = int(match.group(2))
                    
                    # Try to resolve file path relative to workspace
                    try:
                        full_path = (self._cwd / file_path).resolve()
                        rel_path = full_path.relative_to(self.root_path)
                        file_path = str(rel_path)
                    except (ValueError, OSError):
                        pass
                    
                    errors.append({
                        'file': file_path,
                        'line': line_num,
                        'column': int(match.group(3)) if len(match.groups()) >= 3 and match.group(3) else 0,
                        'message': line.strip(),
                        'raw_line': line
                    })
                    break
        
        return errors
