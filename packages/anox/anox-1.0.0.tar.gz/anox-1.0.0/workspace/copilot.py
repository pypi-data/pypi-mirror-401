"""Anox Copilot - Always-on AI assistant with multi-provider support."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


class AnoxCopilot:
    """AI Copilot that assists with code analysis and fixes.
    
    Features:
    - Always-on but non-intrusive
    - Reads entire project codebase
    - Provides inline warnings
    - Auto-fixes with confidence threshold
    - Parses terminal errors and points to files/lines
    - Supports multiple AI providers (Claude, GPT, Gemini, etc.)
    """
    
    def __init__(self, workspace_root: Path, api_key: Optional[str] = None,
                 model: str = "auto", provider: str = "auto", 
                 confidence_threshold: float = 0.8):
        """Initialize Anox Copilot.
        
        Args:
            workspace_root: Root path of the workspace.
            api_key: API key for the chosen provider (BYOK - Bring Your Own Key).
            model: Model to use (default: auto - uses model router).
            provider: AI provider (auto, openai, anthropic, google, etc.).
            confidence_threshold: Minimum confidence for auto-fix (0.0-1.0).
        """
        self.workspace_root = workspace_root
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.confidence_threshold = confidence_threshold
        
        # Track usage for cost control
        self._usage = {
            'total_tokens': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'api_calls': 0
        }
        
        # Limits for cost control
        self._limits = {
            'soft_limit_tokens': 100000,  # Warning threshold
            'hard_limit_tokens': 500000,  # Hard stop
            'enabled': True
        }
        
        # Context cache for codebase awareness
        self._codebase_context: Dict[str, Any] = {}
        self._inline_warnings: List[Dict[str, Any]] = []
    
    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze a file for potential issues.
        
        Args:
            file_path: Path to file relative to workspace.
            content: File content.
            
        Returns:
            Analysis result with warnings and suggestions.
        """
        if not self._check_limits():
            return {'error': 'API limit reached. Please add credits or wait.'}
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(file_path, content)
        
        # Call AI API (supports multiple providers)
        result = self._call_ai_api(prompt, task='analyze')
        
        return {
            'file': file_path,
            'warnings': result.get('warnings', []),
            'suggestions': result.get('suggestions', []),
            'issues': result.get('issues', []),
            'confidence': result.get('confidence', 0.0)
        }
    
    def auto_fix(self, file_path: str, content: str, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Automatically fix an issue if confidence is high enough.
        
        Args:
            file_path: Path to file.
            content: Current file content.
            issue: Issue to fix.
            
        Returns:
            Fix result with new content if confidence threshold met, None otherwise.
        """
        if not self._check_limits():
            return None
        
        # Build fix prompt
        prompt = self._build_fix_prompt(file_path, content, issue)
        
        # Call AI API
        result = self._call_ai_api(prompt, task='fix')
        
        confidence = result.get('confidence', 0.0)
        
        # Only auto-fix if confidence is above threshold
        if confidence >= self.confidence_threshold:
            return {
                'success': True,
                'new_content': result.get('fixed_content'),
                'explanation': result.get('explanation'),
                'confidence': confidence,
                'changes': result.get('changes', [])
            }
        
        return {
            'success': False,
            'reason': f'Confidence {confidence:.2f} below threshold {self.confidence_threshold}',
            'suggestion': result.get('suggestion'),
            'confidence': confidence
        }
    
    def parse_terminal_error(self, stderr: str, workspace_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse terminal error output and provide context.
        
        Args:
            stderr: Error output from terminal.
            workspace_context: Context about the workspace state.
            
        Returns:
            List of parsed errors with file/line info and suggestions.
        """
        if not self._check_limits():
            return []
        
        prompt = self._build_error_analysis_prompt(stderr, workspace_context)
        
        result = self._call_ai_api(prompt, task='error_analysis')
        
        return result.get('errors', [])
    
    def get_inline_warnings(self, file_path: str) -> List[Dict[str, Any]]:
        """Get inline warnings for a file.
        
        Args:
            file_path: Path to file.
            
        Returns:
            List of inline warnings with line numbers and messages.
        """
        return [w for w in self._inline_warnings if w.get('file') == file_path]
    
    def index_codebase(self, file_list: List[str]) -> Dict[str, Any]:
        """Index codebase for context-aware assistance.
        
        Args:
            file_list: List of files to index.
            
        Returns:
            Indexing result.
        """
        # Build lightweight index of codebase structure
        self._codebase_context = {
            'files': file_list,
            'total_files': len(file_list),
            'indexed_at': self._get_timestamp()
        }
        
        return {
            'success': True,
            'files_indexed': len(file_list),
            'context_ready': True
        }
    
    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics.
        
        Returns:
            Usage statistics including tokens and costs.
        """
        # Cost estimate (varies by provider and model)
        # Note: Prices may change. Check your provider's pricing page for current rates.
        # Default estimates based on common pricing (circa 2024):
        # - Claude Sonnet: Input $3/1M, Output $15/1M tokens
        # - GPT-4: Input $30/1M, Output $60/1M tokens  
        # - GPT-3.5: Input $0.5/1M, Output $1.5/1M tokens
        # TODO: Implement provider-specific pricing
        input_cost_per_token = 0.000003  # Default estimate
        output_cost_per_token = 0.000015  # Default estimate
        
        input_cost = self._usage['input_tokens'] * input_cost_per_token
        output_cost = self._usage['output_tokens'] * output_cost_per_token
        total_cost = input_cost + output_cost
        
        return {
            **self._usage,
            'estimated_cost_usd': total_cost,
            'limits': self._limits,
            'percentage_used': (self._usage['total_tokens'] / self._limits['hard_limit_tokens'] * 100),
            'provider': self.provider,
            'model': self.model
        }
    
    def set_limits(self, soft_limit: Optional[int] = None, 
                   hard_limit: Optional[int] = None) -> None:
        """Set usage limits.
        
        Args:
            soft_limit: Soft limit for tokens (warning).
            hard_limit: Hard limit for tokens (stop).
        """
        if soft_limit is not None:
            self._limits['soft_limit_tokens'] = soft_limit
        if hard_limit is not None:
            self._limits['hard_limit_tokens'] = hard_limit
    
    def _check_limits(self) -> bool:
        """Check if usage is within limits.
        
        Returns:
            True if within limits, False if hard limit reached.
        """
        if not self._limits['enabled']:
            return True
        
        if self._usage['total_tokens'] >= self._limits['hard_limit_tokens']:
            return False
        
        if self._usage['total_tokens'] >= self._limits['soft_limit_tokens']:
            print(f"⚠️  Warning: Approaching token limit. "
                  f"Used {self._usage['total_tokens']}/{self._limits['hard_limit_tokens']}")
        
        return True
    
    def _call_ai_api(self, prompt: str, task: str = 'general') -> Dict[str, Any]:
        """Call AI API (supports multiple providers).
        
        Args:
            prompt: Prompt to send.
            task: Task type for tracking.
            
        Returns:
            API response.
        """
        # This is a placeholder. In real implementation, this would:
        # 1. Detect provider from self.provider and self.model
        # 2. Use model router to select appropriate model
        # 3. Make actual API call (OpenAI, Anthropic, Google, etc.)
        # 4. Track token usage
        # 5. Handle errors and rate limits
        
        # For now, return mock response
        self._usage['api_calls'] += 1
        self._usage['input_tokens'] += len(prompt.split())
        self._usage['output_tokens'] += 100  # Mock
        self._usage['total_tokens'] = self._usage['input_tokens'] + self._usage['output_tokens']
        
        return {
            'success': True,
            'task': task,
            'warnings': [],
            'suggestions': [],
            'confidence': 0.9,
            'mock': True,
            'provider': self.provider,
            'model': self.model
        }
    
    def _build_analysis_prompt(self, file_path: str, content: str) -> str:
        """Build prompt for file analysis."""
        return f"""Analyze this code file for potential issues.

File: {file_path}

```
{content}
```

Provide:
1. Any bugs or errors
2. Security vulnerabilities
3. Code quality issues
4. Performance concerns
5. Suggestions for improvement

Format as JSON with confidence scores."""
    
    def _build_fix_prompt(self, file_path: str, content: str, issue: Dict[str, Any]) -> str:
        """Build prompt for auto-fix."""
        return f"""Fix this specific issue in the code.

File: {file_path}
Issue: {issue.get('message', 'Unknown')}
Line: {issue.get('line', 'Unknown')}

Current code:
```
{content}
```

Provide:
1. Fixed code
2. Explanation of changes
3. Confidence score (0.0-1.0)

Only suggest a fix if you are confident it's correct."""
    
    def _build_error_analysis_prompt(self, stderr: str, context: Dict[str, Any]) -> str:
        """Build prompt for error analysis."""
        return f"""Analyze this error output and provide actionable guidance.

Error output:
```
{stderr}
```

Workspace context:
{json.dumps(context, indent=2)}

Provide:
1. File and line number of the error
2. Root cause explanation
3. Suggested fix
4. Related files that might be involved"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
