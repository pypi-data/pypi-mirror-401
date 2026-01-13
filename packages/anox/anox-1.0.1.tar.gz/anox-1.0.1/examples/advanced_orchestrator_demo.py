#!/usr/bin/env python3
"""
Example: Advanced Orchestrator Brain Integration

This example demonstrates how to use the advanced orchestrator brain
with the universal model adapter to create a GitHub Copilot-like system.
"""

import os
import time
from pathlib import Path

# Import advanced orchestrator
from core.brain_orchestrator import (
    AdvancedOrchestratorBrain,
    TaskContext,
    TaskType,
    TaskComplexity,
)

# Import universal adapter
from models.universal_adapter import (
    create_from_file,
    create_from_api,
    create_from_ollama,
    UniversalModelAdapter,
    ModelFormat,
)


def setup_models():
    """
    Setup models using universal adapter.
    
    This example shows how to configure multiple models of different types.
    """
    models = {}
    
    # 1. Local GGUF model (if available)
    local_model_path = os.environ.get('AXON_LOCAL_MODEL_PATH')
    if local_model_path and Path(local_model_path).exists():
        print(f"✓ Loading local model: {local_model_path}")
        models['local_llama'] = create_from_file(
            local_model_path,
            n_ctx=4096,
            n_gpu_layers=35,  # Use GPU if available
        )
    
    # 2. Ollama models (if running)
    try:
        print("✓ Checking Ollama...")
        ollama_model = create_from_ollama('llama2')
        if ollama_model.health_check():
            models['ollama_llama'] = ollama_model
            print("✓ Ollama available")
    except:
        print("⚠️  Ollama not available")
    
    # 3. OpenAI API (if key provided)
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        print("✓ OpenAI API available")
        models['gpt35'] = create_from_api('openai', openai_key, 'gpt-3.5-turbo')
        models['gpt4'] = create_from_api('openai', openai_key, 'gpt-4')
    
    # 4. Anthropic Claude (if key provided)
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    if anthropic_key:
        print("✓ Anthropic Claude available")
        models['claude'] = create_from_api('anthropic', anthropic_key, 'claude-3-opus-20240229')
    
    # 5. Google Gemini (if key provided)
    google_key = os.environ.get('GOOGLE_API_KEY')
    if google_key:
        print("✓ Google Gemini available")
        models['gemini'] = create_from_api('google', google_key, 'gemini-pro')
    
    # If no models available, create a mock model
    if not models:
        print("⚠️  No real models available, using mock mode")
        models['mock'] = UniversalModelAdapter(
            ModelFormat.CUSTOM_HTTP,
            {'base_url': 'http://mock'},
            name='Mock Model'
        )
    
    return models


def demonstrate_task_completion(brain, models, user_id='demo_user'):
    """Demonstrate code completion task."""
    print("\n" + "="*60)
    print("🎯 Task: Code Completion")
    print("="*60)
    
    prompt = """
def fibonacci(n):
    # Complete this function to return the nth Fibonacci number
    """
    
    context = TaskContext(
        task_type=TaskType.CODE_COMPLETION,
        complexity=TaskComplexity.SIMPLE,
        language='python',
        code_size=len(prompt),
        requires_speed=True,
    )
    
    start_time = time.time()
    selected_model_id = brain.select_optimal_model(context, user_id)
    selection_time = time.time() - start_time
    
    print(f"✓ Selected model: {selected_model_id} (in {selection_time:.3f}s)")
    
    model = models[selected_model_id]
    
    start_time = time.time()
    response = model.generate(prompt)
    response_time = time.time() - start_time
    
    print(f"✓ Response time: {response_time:.3f}s")
    print(f"\nResponse:\n{response[:200]}...")
    
    # Record performance
    brain.record_performance(
        model_id=selected_model_id,
        task_type=TaskType.CODE_COMPLETION,
        response_time=response_time,
        success=True,
        accuracy_score=0.85,
    )
    
    return selected_model_id


def demonstrate_code_review(brain, models, user_id='demo_user'):
    """Demonstrate code review task."""
    print("\n" + "="*60)
    print("🎯 Task: Code Review")
    print("="*60)
    
    code = """
def process_data(data):
    result = []
    for item in data:
        if item != None:
            result.append(item * 2)
    return result
"""
    
    prompt = f"Review this Python code and suggest improvements:\n\n{code}"
    
    context = TaskContext(
        task_type=TaskType.CODE_REVIEW,
        complexity=TaskComplexity.MODERATE,
        language='python',
        code_size=len(code),
        requires_accuracy=True,
    )
    
    start_time = time.time()
    selected_model_id = brain.select_optimal_model(context, user_id)
    selection_time = time.time() - start_time
    
    print(f"✓ Selected model: {selected_model_id} (in {selection_time:.3f}s)")
    
    model = models[selected_model_id]
    
    start_time = time.time()
    response = model.generate(prompt)
    response_time = time.time() - start_time
    
    print(f"✓ Response time: {response_time:.3f}s")
    print(f"\nResponse:\n{response[:300]}...")
    
    # Record performance
    brain.record_performance(
        model_id=selected_model_id,
        task_type=TaskType.CODE_REVIEW,
        response_time=response_time,
        success=True,
        accuracy_score=0.92,
    )
    
    return selected_model_id


def demonstrate_learning(brain):
    """Demonstrate learning and optimization."""
    print("\n" + "="*60)
    print("📊 Learning & Optimization")
    print("="*60)
    
    # Get statistics
    stats = brain.get_stats()
    print(f"\nStatistics:")
    print(f"  Total models: {stats['total_models']}")
    print(f"  Healthy models: {stats['healthy_models']}")
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Tracked users: {stats['tracked_users']}")
    
    # Get model recommendations for different tasks
    print(f"\n🏆 Model Recommendations:")
    
    for task_type in [TaskType.CODE_COMPLETION, TaskType.CODE_REVIEW, TaskType.TEST_GENERATION]:
        recommendations = brain.get_model_recommendations(task_type)
        print(f"\n  {task_type.value}:")
        for model_id, score in recommendations[:3]:  # Top 3
            print(f"    {model_id}: {score:.3f}")
    
    # Get optimization report
    print(f"\n🔧 Optimization Report:")
    report = brain.optimize_model_selection()
    print(f"  Analysis timestamp: {report['timestamp']}")
    print(f"  Total executions analyzed: {report['total_executions']}")
    
    if report['optimizations']:
        print(f"\n  Recommendations:")
        for opt in report['optimizations']:
            print(f"    - {opt['type']}: {opt['recommendation']}")
    else:
        print(f"  No optimization recommendations at this time")
    
    print(f"\n  Best model-task pairings:")
    for task, pairing in list(report['best_pairings'].items())[:5]:
        print(f"    {task}: {pairing['model']} (score: {pairing['score']:.3f})")


def main():
    """Main demonstration."""
    print("="*60)
    print("🧠 AXON Advanced Orchestrator Brain - Demonstration")
    print("="*60)
    
    # Setup models
    print("\n📦 Setting up models...")
    models = setup_models()
    print(f"\n✓ {len(models)} model(s) available:")
    for model_id, model in models.items():
        info = model.get_info()
        print(f"  - {model_id}: {info['format']}")
    
    # Initialize brain
    print("\n🧠 Initializing orchestrator brain...")
    brain = AdvancedOrchestratorBrain(
        models,
        performance_log_path=Path('logs/demo_performance.jsonl'),
        usage_pattern_path=Path('logs/demo_usage_patterns.json'),
    )
    print("✓ Brain initialized")
    
    # Demonstrate different tasks
    user_id = 'demo_user'
    
    # Task 1: Code completion (fast task)
    model1 = demonstrate_task_completion(brain, models, user_id)
    
    # Task 2: Code review (accuracy-critical task)
    model2 = demonstrate_code_review(brain, models, user_id)
    
    # Notice: Brain might select different models for different tasks
    if model1 != model2:
        print(f"\n✨ Note: Brain selected different models for different tasks!")
        print(f"   Completion: {model1} (requires speed)")
        print(f"   Review: {model2} (requires accuracy)")
    
    # Demonstrate learning
    demonstrate_learning(brain)
    
    print("\n" + "="*60)
    print("✅ Demonstration complete!")
    print("="*60)
    print("\nThe orchestrator brain has:")
    print("  ✓ Selected optimal models for each task")
    print("  ✓ Recorded performance metrics")
    print("  ✓ Learned user preferences")
    print("  ✓ Generated optimization recommendations")
    print("\nThis data will be used to improve future selections!")
    print("\nLogs saved to:")
    print("  - logs/demo_performance.jsonl")
    print("  - logs/demo_usage_patterns.json")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
