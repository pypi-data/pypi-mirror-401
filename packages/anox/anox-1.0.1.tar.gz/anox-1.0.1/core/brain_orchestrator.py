"""
Advanced Orchestrator Brain - Context-Aware Model Management System

This module implements an intelligent orchestrator that acts as a "brain" controlling
models, similar to GitHub Copilot, rather than just a chatbot. It provides:

1. Advanced orchestrator brain (context-aware model management)
2. Task-specific model specialization
3. Performance monitoring and auto-optimization
4. Dynamic model switching based on task complexity
5. Learning from usage patterns
6. Universal model adapter (support ANY model format)
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from models.base import BaseModel


class TaskType(Enum):
    """Types of tasks the orchestrator can handle."""
    CODE_COMPLETION = "code_completion"
    CODE_REVIEW = "code_review"
    CODE_ANALYSIS = "code_analysis"
    TEST_GENERATION = "test_generation"
    BUG_DETECTION = "bug_detection"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    SECURITY_SCAN = "security_scan"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ARCHITECTURE_DESIGN = "architecture_design"
    GENERAL_CHAT = "general_chat"


class TaskComplexity(Enum):
    """Complexity levels for tasks."""
    TRIVIAL = 1
    SIMPLE = 2
    MODERATE = 3
    COMPLEX = 4
    VERY_COMPLEX = 5


@dataclass
class TaskContext:
    """Contextual information about a task."""
    task_type: TaskType
    complexity: TaskComplexity
    language: Optional[str] = None
    file_type: Optional[str] = None
    code_size: int = 0
    requires_accuracy: bool = False
    requires_speed: bool = False
    user_preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetric:
    """Performance metrics for a model on a task."""
    model_id: str
    task_type: TaskType
    response_time: float
    success: bool
    accuracy_score: float
    user_satisfaction: Optional[float] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class UsagePattern:
    """Usage pattern learned from user behavior."""
    user_id: str
    task_type: TaskType
    preferred_model: str
    avg_complexity: float
    frequency: int
    last_used: float = field(default_factory=time.time)


class AdvancedOrchestratorBrain:
    """
    Advanced orchestrator brain that intelligently manages models.
    
    This is NOT a chatbot - it's a control system that orchestrates models
    to provide GitHub Copilot-like capabilities across any platform and
    with support for unlimited model types.
    """
    
    def __init__(
        self,
        models: Dict[str, BaseModel],
        performance_log_path: Optional[Path] = None,
        usage_pattern_path: Optional[Path] = None,
    ) -> None:
        """
        Initialize the orchestrator brain.
        
        Args:
            models: Dictionary of available models by ID
            performance_log_path: Path to store performance metrics
            usage_pattern_path: Path to store usage patterns
        """
        self.models = models
        self.performance_log_path = performance_log_path or Path("logs/performance.jsonl")
        self.usage_pattern_path = usage_pattern_path or Path("logs/usage_patterns.json")
        
        # Performance monitoring
        self.performance_history: List[PerformanceMetric] = []
        self.model_scores: Dict[str, Dict[TaskType, float]] = {}
        
        # Usage patterns
        self.usage_patterns: Dict[str, Dict[TaskType, UsagePattern]] = {}
        
        # Model specializations
        self.model_specializations: Dict[str, List[TaskType]] = self._initialize_specializations()
        
        # Load historical data
        self._load_performance_history()
        self._load_usage_patterns()
    
    def _initialize_specializations(self) -> Dict[str, List[TaskType]]:
        """
        Initialize model specializations based on known capabilities.
        
        This maps models to task types they excel at.
        """
        specializations = {}
        
        for model_id, model in self.models.items():
            model_type = getattr(model, 'model_type', 'general')
            
            if 'codex' in model_id.lower() or 'code' in model_id.lower():
                specializations[model_id] = [
                    TaskType.CODE_COMPLETION,
                    TaskType.CODE_REVIEW,
                    TaskType.TEST_GENERATION,
                ]
            elif 'gpt-4' in model_id.lower() or 'claude' in model_id.lower():
                specializations[model_id] = [
                    TaskType.CODE_ANALYSIS,
                    TaskType.ARCHITECTURE_DESIGN,
                    TaskType.REFACTORING,
                    TaskType.SECURITY_SCAN,
                ]
            elif 'fast' in model_id.lower() or 'turbo' in model_id.lower():
                specializations[model_id] = [
                    TaskType.CODE_COMPLETION,
                    TaskType.BUG_DETECTION,
                ]
            else:
                # General purpose
                specializations[model_id] = list(TaskType)
        
        return specializations
    
    def select_optimal_model(self, context: TaskContext, user_id: Optional[str] = None) -> str:
        """
        Select the optimal model for a given task context.
        
        This is the core intelligence - it considers:
        1. Task type and complexity
        2. Model specializations
        3. Performance history
        4. User preferences and patterns
        5. Real-time model health
        
        Args:
            context: Task context information
            user_id: Optional user identifier for personalization
            
        Returns:
            Selected model ID
        """
        # Step 1: Filter models by availability and health
        available_models = self._get_healthy_models()
        
        if not available_models:
            raise RuntimeError("No healthy models available")
        
        # Step 2: Check user preferences and patterns
        if user_id and user_id in self.usage_patterns:
            user_pattern = self.usage_patterns[user_id].get(context.task_type)
            if user_pattern and user_pattern.preferred_model in available_models:
                # Use user's preferred model if performance is acceptable
                model_id = user_pattern.preferred_model
                if self._get_model_score(model_id, context.task_type) > 0.7:
                    self._update_usage_pattern(user_id, context, model_id)
                    return model_id
        
        # Step 3: Score models based on multiple factors
        model_scores = {}
        for model_id in available_models:
            score = self._calculate_model_score(model_id, context)
            model_scores[model_id] = score
        
        # Step 4: Select highest scoring model
        best_model = max(model_scores, key=model_scores.get)
        
        # Step 5: Update usage patterns
        if user_id:
            self._update_usage_pattern(user_id, context, best_model)
        
        return best_model
    
    def _calculate_model_score(self, model_id: str, context: TaskContext) -> float:
        """
        Calculate a comprehensive score for a model given a task context.
        
        Factors:
        - Specialization match (40%)
        - Historical performance (30%)
        - Complexity appropriateness (20%)
        - User requirements (10%)
        """
        score = 0.0
        
        # Specialization match (40%)
        if context.task_type in self.model_specializations.get(model_id, []):
            score += 0.4
        else:
            score += 0.1  # Partial credit for general models
        
        # Historical performance (30%)
        historical_score = self._get_model_score(model_id, context.task_type)
        score += 0.3 * historical_score
        
        # Complexity appropriateness (20%)
        model = self.models[model_id]
        model_capacity = getattr(model, 'capacity_level', 3)  # 1-5 scale
        
        if abs(model_capacity - context.complexity.value) <= 1:
            score += 0.2
        elif abs(model_capacity - context.complexity.value) == 2:
            score += 0.1
        
        # User requirements (10%)
        if context.requires_speed:
            # Prefer models with faster response times
            avg_time = self._get_avg_response_time(model_id, context.task_type)
            if avg_time < 1.0:  # Under 1 second
                score += 0.1
            elif avg_time < 3.0:  # Under 3 seconds
                score += 0.05
        
        if context.requires_accuracy:
            # Prefer models with high accuracy
            accuracy = self._get_avg_accuracy(model_id, context.task_type)
            if accuracy > 0.9:
                score += 0.1
            elif accuracy > 0.75:
                score += 0.05
        
        return score
    
    def _get_healthy_models(self) -> List[str]:
        """Get list of models that are currently healthy and available."""
        healthy = []
        for model_id, model in self.models.items():
            try:
                if model.health_check():
                    healthy.append(model_id)
            except Exception:
                # Model health check failed, skip it
                pass
        return healthy
    
    def _get_model_score(self, model_id: str, task_type: TaskType) -> float:
        """Get the performance score for a model on a task type."""
        if model_id not in self.model_scores:
            return 0.5  # Default neutral score
        
        if task_type not in self.model_scores[model_id]:
            return 0.5  # Default neutral score
        
        return self.model_scores[model_id][task_type]
    
    def _get_avg_response_time(self, model_id: str, task_type: TaskType) -> float:
        """Get average response time for a model on a task type."""
        relevant_metrics = [
            m for m in self.performance_history
            if m.model_id == model_id and m.task_type == task_type
        ]
        
        if not relevant_metrics:
            return 2.0  # Default estimate
        
        return sum(m.response_time for m in relevant_metrics) / len(relevant_metrics)
    
    def _get_avg_accuracy(self, model_id: str, task_type: TaskType) -> float:
        """Get average accuracy for a model on a task type."""
        relevant_metrics = [
            m for m in self.performance_history
            if m.model_id == model_id and m.task_type == task_type and m.success
        ]
        
        if not relevant_metrics:
            return 0.75  # Default estimate
        
        return sum(m.accuracy_score for m in relevant_metrics) / len(relevant_metrics)
    
    def record_performance(
        self,
        model_id: str,
        task_type: TaskType,
        response_time: float,
        success: bool,
        accuracy_score: float = 0.8,
        user_satisfaction: Optional[float] = None,
    ) -> None:
        """
        Record performance metrics for a model execution.
        
        This enables learning and optimization over time.
        """
        metric = PerformanceMetric(
            model_id=model_id,
            task_type=task_type,
            response_time=response_time,
            success=success,
            accuracy_score=accuracy_score,
            user_satisfaction=user_satisfaction,
        )
        
        self.performance_history.append(metric)
        
        # Update model scores
        if model_id not in self.model_scores:
            self.model_scores[model_id] = {}
        
        # Calculate new score (exponential moving average)
        old_score = self.model_scores[model_id].get(task_type, 0.5)
        new_score = accuracy_score if success else 0.0
        alpha = 0.2  # Learning rate
        updated_score = alpha * new_score + (1 - alpha) * old_score
        
        self.model_scores[model_id][task_type] = updated_score
        
        # Persist to disk
        self._save_performance_metric(metric)
    
    def _update_usage_pattern(
        self,
        user_id: str,
        context: TaskContext,
        model_id: str,
    ) -> None:
        """Update usage patterns based on user behavior."""
        if user_id not in self.usage_patterns:
            self.usage_patterns[user_id] = {}
        
        if context.task_type not in self.usage_patterns[user_id]:
            pattern = UsagePattern(
                user_id=user_id,
                task_type=context.task_type,
                preferred_model=model_id,
                avg_complexity=context.complexity.value,
                frequency=1,
            )
            self.usage_patterns[user_id][context.task_type] = pattern
        else:
            pattern = self.usage_patterns[user_id][context.task_type]
            pattern.preferred_model = model_id
            pattern.frequency += 1
            pattern.avg_complexity = (
                0.8 * pattern.avg_complexity + 0.2 * context.complexity.value
            )
            pattern.last_used = time.time()
        
        # Periodically save patterns
        if len(self.usage_patterns) % 10 == 0:
            self._save_usage_patterns()
    
    def infer_task_complexity(self, context: Dict[str, Any]) -> TaskComplexity:
        """
        Infer task complexity from context.
        
        This uses heuristics and learned patterns to estimate complexity.
        """
        # Code size heuristic
        code_size = context.get('code_size', 0)
        if code_size > 10000:
            return TaskComplexity.VERY_COMPLEX
        elif code_size > 5000:
            return TaskComplexity.COMPLEX
        elif code_size > 1000:
            return TaskComplexity.MODERATE
        elif code_size > 100:
            return TaskComplexity.SIMPLE
        else:
            return TaskComplexity.TRIVIAL
    
    def get_model_recommendations(self, task_type: TaskType) -> List[Tuple[str, float]]:
        """
        Get ranked model recommendations for a task type.
        
        Returns:
            List of (model_id, score) tuples, sorted by score descending
        """
        recommendations = []
        
        for model_id in self.models:
            context = TaskContext(
                task_type=task_type,
                complexity=TaskComplexity.MODERATE,
            )
            score = self._calculate_model_score(model_id, context)
            recommendations.append((model_id, score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations
    
    def optimize_model_selection(self) -> Dict[str, Any]:
        """
        Analyze performance history and optimize model selection strategies.
        
        Returns:
            Optimization report with suggestions
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_executions': len(self.performance_history),
            'models_analyzed': len(self.models),
            'optimizations': [],
        }
        
        # Identify underperforming models
        for model_id, scores in self.model_scores.items():
            avg_score = sum(scores.values()) / len(scores) if scores else 0
            if avg_score < 0.5:
                report['optimizations'].append({
                    'type': 'low_performance',
                    'model_id': model_id,
                    'avg_score': avg_score,
                    'recommendation': 'Consider removing or retraining this model',
                })
        
        # Identify optimal model-task pairings
        best_pairings = {}
        for task_type in TaskType:
            recommendations = self.get_model_recommendations(task_type)
            if recommendations:
                best_model, best_score = recommendations[0]
                best_pairings[task_type.value] = {
                    'model': best_model,
                    'score': best_score,
                }
        
        report['best_pairings'] = best_pairings
        
        return report
    
    def _save_performance_metric(self, metric: PerformanceMetric) -> None:
        """Save a performance metric to disk."""
        self.performance_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.performance_log_path, 'a') as f:
            f.write(json.dumps({
                'model_id': metric.model_id,
                'task_type': metric.task_type.value,
                'response_time': metric.response_time,
                'success': metric.success,
                'accuracy_score': metric.accuracy_score,
                'user_satisfaction': metric.user_satisfaction,
                'timestamp': metric.timestamp,
            }) + '\n')
    
    def _load_performance_history(self) -> None:
        """Load performance history from disk."""
        if not self.performance_log_path.exists():
            return
        
        try:
            with open(self.performance_log_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    metric = PerformanceMetric(
                        model_id=data['model_id'],
                        task_type=TaskType(data['task_type']),
                        response_time=data['response_time'],
                        success=data['success'],
                        accuracy_score=data['accuracy_score'],
                        user_satisfaction=data.get('user_satisfaction'),
                        timestamp=data['timestamp'],
                    )
                    self.performance_history.append(metric)
            
            # Rebuild model scores from history
            for metric in self.performance_history:
                if metric.model_id not in self.model_scores:
                    self.model_scores[metric.model_id] = {}
                
                old_score = self.model_scores[metric.model_id].get(metric.task_type, 0.5)
                new_score = metric.accuracy_score if metric.success else 0.0
                alpha = 0.2
                self.model_scores[metric.model_id][metric.task_type] = (
                    alpha * new_score + (1 - alpha) * old_score
                )
        except Exception as e:
            print(f"⚠️  Failed to load performance history: {e}")
    
    def _save_usage_patterns(self) -> None:
        """Save usage patterns to disk."""
        self.usage_pattern_path.parent.mkdir(parents=True, exist_ok=True)
        
        patterns_data = {}
        for user_id, user_patterns in self.usage_patterns.items():
            patterns_data[user_id] = {}
            for task_type, pattern in user_patterns.items():
                patterns_data[user_id][task_type.value] = {
                    'preferred_model': pattern.preferred_model,
                    'avg_complexity': pattern.avg_complexity,
                    'frequency': pattern.frequency,
                    'last_used': pattern.last_used,
                }
        
        with open(self.usage_pattern_path, 'w') as f:
            json.dump(patterns_data, f, indent=2)
    
    def _load_usage_patterns(self) -> None:
        """Load usage patterns from disk."""
        if not self.usage_pattern_path.exists():
            return
        
        try:
            with open(self.usage_pattern_path, 'r') as f:
                patterns_data = json.load(f)
            
            for user_id, user_patterns in patterns_data.items():
                self.usage_patterns[user_id] = {}
                for task_type_str, pattern_data in user_patterns.items():
                    task_type = TaskType(task_type_str)
                    pattern = UsagePattern(
                        user_id=user_id,
                        task_type=task_type,
                        preferred_model=pattern_data['preferred_model'],
                        avg_complexity=pattern_data['avg_complexity'],
                        frequency=pattern_data['frequency'],
                        last_used=pattern_data['last_used'],
                    )
                    self.usage_patterns[user_id][task_type] = pattern
        except Exception as e:
            print(f"⚠️  Failed to load usage patterns: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the orchestrator."""
        return {
            'total_models': len(self.models),
            'healthy_models': len(self._get_healthy_models()),
            'total_executions': len(self.performance_history),
            'tracked_users': len(self.usage_patterns),
            'model_scores': {
                model_id: {task.value: score for task, score in scores.items()}
                for model_id, scores in self.model_scores.items()
            },
        }
