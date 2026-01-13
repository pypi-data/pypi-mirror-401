#!/usr/bin/env python3
"""Example: Using Anthropic Claude with Anox

This example demonstrates how to use Anthropic Claude for various AI tasks.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from models.factory import ModelFactory, create_default_router


def example_1_simple_generation():
    """Example 1: Simple text generation."""
    print("\n" + "=" * 60)
    print("Example 1: Simple Text Generation")
    print("=" * 60)
    
    try:
        # Create router (uses Anthropic if configured)
        router = create_default_router()
        model = router.select_worker()
        
        print(f"Using model: {model.name}")
        
        # Simple prompt
        prompt = "Write a Python function to calculate factorial."
        
        print(f"\nPrompt: {prompt}")
        print("\nGenerating response...")
        
        response = model.generate(prompt, context={
            "max_tokens": 512,
            "temperature": 0.7,
            "task_type": "code_generation"
        })
        
        print("\nResponse:")
        print(response)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure to configure your API key with:")
        print("  anox config api add sk-ant-...")


def example_2_code_review():
    """Example 2: Code review and analysis."""
    print("\n" + "=" * 60)
    print("Example 2: Code Review")
    print("=" * 60)
    
    code = """
def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
"""
    
    try:
        factory = ModelFactory()
        
        # Try to create Anthropic model
        try:
            model = factory.create_anthropic_model()
            print("Using: Anthropic Claude")
        except:
            print("Anthropic not configured, using default")
            router = factory.create_model_router()
            model = router.select_worker()
        
        prompt = f"""Review this Python code and provide:
1. What it does
2. Any bugs or issues
3. Suggestions for improvement

Code:
{code}
"""
        
        print(f"\nAnalyzing code...")
        
        response = model.generate(prompt, context={
            "max_tokens": 1024,
            "temperature": 0.7,
            "task_type": "code_review"
        })
        
        print("\nReview:")
        print(response)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_3_explain_code():
    """Example 3: Explain complex code."""
    print("\n" + "=" * 60)
    print("Example 3: Code Explanation")
    print("=" * 60)
    
    code = """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
"""
    
    try:
        router = create_default_router()
        model = router.select_worker()
        
        prompt = f"""Explain this code in simple terms for a beginner:

{code}

Include:
1. What algorithm this is
2. How it works step by step
3. Time complexity
"""
        
        print("Generating explanation...")
        
        response = model.generate(prompt, context={
            "max_tokens": 1024,
            "temperature": 0.7,
            "task_type": "explanation"
        })
        
        print("\nExplanation:")
        print(response)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_4_usage_tracking():
    """Example 4: View usage statistics."""
    print("\n" + "=" * 60)
    print("Example 4: Usage Statistics")
    print("=" * 60)
    
    try:
        from models.usage_tracker import get_usage_tracker
        
        tracker = get_usage_tracker()
        
        # Get total usage
        total = tracker.get_total_usage()
        
        print("\nCurrent Usage:")
        print(f"  Total Calls: {total['total_calls']}")
        print(f"  Total Tokens: {total['total_tokens']:,}")
        print(f"  Estimated Cost: ${total['total_cost']:.4f}")
        
        # Check limits
        limits = tracker.check_limits()
        print(f"\nLimits:")
        print(f"  Used: {limits['percentage']:.1f}%")
        print(f"  Soft Limit: {limits['soft_limit']:,} tokens")
        print(f"  Hard Limit: {limits['hard_limit']:,} tokens")
        
        if limits['soft_limit_reached']:
            print("  ⚠️  Soft limit reached!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_5_model_info():
    """Example 5: Get model information."""
    print("\n" + "=" * 60)
    print("Example 5: Model Information")
    print("=" * 60)
    
    try:
        router = create_default_router()
        info = router.get_model_info()
        
        print("\nRouter Configuration:")
        print(f"  Prefer Online: {info['prefer_online']}")
        print(f"  Auto Fallback: {info['auto_fallback']}")
        
        print("\nOffline Model:")
        print(f"  Name: {info['offline_model']['name']}")
        
        if info['online_model']:
            print("\nOnline Model:")
            print(f"  Name: {info['online_model']['name']}")
            
            # Get detailed model info
            model = router.select_worker()
            model_info = model.get_info()
            
            print(f"  Provider: {model_info.get('provider', 'N/A')}")
            print(f"  Model: {model_info.get('model', 'N/A')}")
            print(f"  Type: {model_info.get('type', 'N/A')}")
            
            if 'usage' in model_info:
                usage = model_info['usage']
                print(f"\n  Usage Statistics:")
                print(f"    Calls: {usage['total_calls']}")
                print(f"    Tokens: {usage['total_tokens']:,}")
                print(f"    Cost: ${usage['total_cost']:.4f}")
        else:
            print("\n⚠️  No online model configured")
            print("   Add API key with: anox config api add sk-ant-...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Anthropic Claude with Anox - Examples")
    print("=" * 60)
    
    print("\nThese examples demonstrate using Anthropic Claude for:")
    print("  1. Simple text generation")
    print("  2. Code review and analysis")
    print("  3. Code explanation")
    print("  4. Usage tracking")
    print("  5. Model information")
    
    # Check if API key is configured
    try:
        from workspace.api_keys import get_api_key_manager
        manager = get_api_key_manager()
        anthropic_key = manager.get_active_key("anthropic")
        
        if not anthropic_key:
            print("\n⚠️  Warning: No Anthropic API key configured")
            print("   Examples will use offline mock model")
            print("\nTo configure Anthropic:")
            print("  1. Get API key from https://console.anthropic.com/")
            print("  2. Run: anox config api add sk-ant-...")
            print("  3. Or set: export ANTHROPIC_API_KEY=sk-ant-...")
    except:
        pass
    
    # Run examples
    example_1_simple_generation()
    example_2_code_review()
    example_3_explain_code()
    example_4_usage_tracking()
    example_5_model_info()
    
    print("\n" + "=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print("\nFor more information:")
    print("  - See docs/ANTHROPIC_INTEGRATION.md")
    print("  - Run: python test_anthropic_integration.py")
    print("  - Use: anox usage show")


if __name__ == "__main__":
    main()
