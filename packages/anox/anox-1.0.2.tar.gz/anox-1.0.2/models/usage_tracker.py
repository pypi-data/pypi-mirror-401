"""Token usage tracking and cost estimation for AI models."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class UsageEntry:
    """Single usage tracking entry."""
    timestamp: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: float
    task_type: str = "general"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CostConfig:
    """Cost configuration for a provider/model."""
    provider: str
    model: str
    input_cost_per_1k: float  # Cost per 1000 input tokens
    output_cost_per_1k: float  # Cost per 1000 output tokens


# Cost configurations for different models (prices in USD)
DEFAULT_COSTS = {
    "anthropic": {
        "claude-3-5-sonnet-20241022": CostConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            input_cost_per_1k=0.003,
            output_cost_per_1k=0.015,
        ),
        "claude-3-sonnet-20240229": CostConfig(
            provider="anthropic",
            model="claude-3-sonnet-20240229",
            input_cost_per_1k=0.003,
            output_cost_per_1k=0.015,
        ),
        "claude-3-opus-20240229": CostConfig(
            provider="anthropic",
            model="claude-3-opus-20240229",
            input_cost_per_1k=0.015,
            output_cost_per_1k=0.075,
        ),
        "claude-3-haiku-20240307": CostConfig(
            provider="anthropic",
            model="claude-3-haiku-20240307",
            input_cost_per_1k=0.00025,
            output_cost_per_1k=0.00125,
        ),
    },
    "openai": {
        "gpt-4-turbo-preview": CostConfig(
            provider="openai",
            model="gpt-4-turbo-preview",
            input_cost_per_1k=0.01,
            output_cost_per_1k=0.03,
        ),
        "gpt-4": CostConfig(
            provider="openai",
            model="gpt-4",
            input_cost_per_1k=0.03,
            output_cost_per_1k=0.06,
        ),
        "gpt-3.5-turbo": CostConfig(
            provider="openai",
            model="gpt-3.5-turbo",
            input_cost_per_1k=0.0005,
            output_cost_per_1k=0.0015,
        ),
    },
    "google": {
        "gemini-pro": CostConfig(
            provider="google",
            model="gemini-pro",
            input_cost_per_1k=0.00025,
            output_cost_per_1k=0.0005,
        ),
    },
}


class TokenUsageTracker:
    """Track token usage and estimate costs."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize usage tracker.
        
        Args:
            storage_path: Path to store usage data. Defaults to ~/.anox/usage.json
        """
        if storage_path is None:
            config_dir = Path.home() / '.anox'
            config_dir.mkdir(parents=True, exist_ok=True)
            storage_path = config_dir / 'usage.json'
        
        self.storage_path = storage_path
        self._entries: List[UsageEntry] = []
        self._load()
    
    def _load(self) -> None:
        """Load usage data from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self._entries = [UsageEntry(**entry) for entry in data]
            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️  Failed to load usage data: {e}")
    
    def _save(self) -> None:
        """Save usage data to storage."""
        data = [entry.to_dict() for entry in self._entries]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_usage(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_type: str = "general"
    ) -> UsageEntry:
        """Track a usage event.
        
        Args:
            provider: AI provider name.
            model: Model name.
            input_tokens: Number of input tokens.
            output_tokens: Number of output tokens.
            task_type: Type of task performed.
            
        Returns:
            UsageEntry with calculated cost.
        """
        total_tokens = input_tokens + output_tokens
        estimated_cost = self._estimate_cost(provider, model, input_tokens, output_tokens)
        
        entry = UsageEntry(
            timestamp=datetime.utcnow().isoformat(),
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            task_type=task_type,
        )
        
        self._entries.append(entry)
        self._save()
        
        return entry
    
    def _estimate_cost(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estimate cost for token usage.
        
        Args:
            provider: AI provider name.
            model: Model name.
            input_tokens: Number of input tokens.
            output_tokens: Number of output tokens.
            
        Returns:
            Estimated cost in USD.
        """
        # Get cost config
        cost_config = None
        if provider in DEFAULT_COSTS and model in DEFAULT_COSTS[provider]:
            cost_config = DEFAULT_COSTS[provider][model]
        
        if not cost_config:
            # Default fallback (assume GPT-3.5 pricing)
            input_cost = (input_tokens / 1000) * 0.0005
            output_cost = (output_tokens / 1000) * 0.0015
            return input_cost + output_cost
        
        input_cost = (input_tokens / 1000) * cost_config.input_cost_per_1k
        output_cost = (output_tokens / 1000) * cost_config.output_cost_per_1k
        
        return input_cost + output_cost
    
    def get_total_usage(self, provider: Optional[str] = None) -> Dict:
        """Get total usage statistics.
        
        Args:
            provider: Filter by provider. Returns all if None.
            
        Returns:
            Dictionary with usage statistics.
        """
        entries = self._entries
        if provider:
            entries = [e for e in entries if e.provider == provider]
        
        if not entries:
            return {
                "total_calls": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
            }
        
        return {
            "total_calls": len(entries),
            "total_input_tokens": sum(e.input_tokens for e in entries),
            "total_output_tokens": sum(e.output_tokens for e in entries),
            "total_tokens": sum(e.total_tokens for e in entries),
            "total_cost": sum(e.estimated_cost for e in entries),
        }
    
    def get_usage_by_model(self) -> Dict[str, Dict]:
        """Get usage statistics grouped by model.
        
        Returns:
            Dictionary mapping model names to usage statistics.
        """
        models = {}
        
        for entry in self._entries:
            key = f"{entry.provider}/{entry.model}"
            if key not in models:
                models[key] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "cost": 0.0,
                }
            
            models[key]["calls"] += 1
            models[key]["input_tokens"] += entry.input_tokens
            models[key]["output_tokens"] += entry.output_tokens
            models[key]["total_tokens"] += entry.total_tokens
            models[key]["cost"] += entry.estimated_cost
        
        return models
    
    def get_recent_usage(self, days: int = 7) -> List[UsageEntry]:
        """Get usage entries from the last N days.
        
        Args:
            days: Number of days to look back.
            
        Returns:
            List of recent usage entries.
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        recent = []
        for entry in self._entries:
            try:
                entry_time = datetime.fromisoformat(entry.timestamp)
                if entry_time >= cutoff:
                    recent.append(entry)
            except ValueError:
                continue
        
        return recent
    
    def check_limits(
        self,
        soft_limit: int = 100000,
        hard_limit: int = 500000
    ) -> Dict[str, any]:
        """Check if usage is approaching limits.
        
        Args:
            soft_limit: Warning threshold for total tokens.
            hard_limit: Hard stop threshold for total tokens.
            
        Returns:
            Dictionary with limit check results.
        """
        total = self.get_total_usage()
        total_tokens = total["total_tokens"]
        
        return {
            "total_tokens": total_tokens,
            "soft_limit": soft_limit,
            "hard_limit": hard_limit,
            "soft_limit_reached": total_tokens >= soft_limit,
            "hard_limit_reached": total_tokens >= hard_limit,
            "percentage": (total_tokens / hard_limit) * 100 if hard_limit > 0 else 0,
        }
    
    def reset_usage(self) -> None:
        """Reset all usage data."""
        self._entries = []
        self._save()
    
    def print_summary(self, provider: Optional[str] = None) -> None:
        """Print usage summary.
        
        Args:
            provider: Filter by provider. Shows all if None.
        """
        total = self.get_total_usage(provider)
        
        print("=" * 60)
        print(f"Token Usage Summary{' - ' + provider if provider else ''}")
        print("=" * 60)
        print(f"Total API Calls: {total['total_calls']}")
        print(f"Input Tokens: {total['total_input_tokens']:,}")
        print(f"Output Tokens: {total['total_output_tokens']:,}")
        print(f"Total Tokens: {total['total_tokens']:,}")
        print(f"Estimated Cost: ${total['total_cost']:.4f}")
        print()
        
        # By model breakdown
        by_model = self.get_usage_by_model()
        if by_model:
            print("Breakdown by Model:")
            print("-" * 60)
            for model, stats in by_model.items():
                print(f"\n{model}:")
                print(f"  Calls: {stats['calls']}")
                print(f"  Tokens: {stats['total_tokens']:,}")
                print(f"  Cost: ${stats['cost']:.4f}")


# Global instance
_tracker_instance: Optional[TokenUsageTracker] = None


def get_usage_tracker() -> TokenUsageTracker:
    """Get the global usage tracker instance."""
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = TokenUsageTracker()
    return _tracker_instance
