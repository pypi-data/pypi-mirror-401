#!/usr/bin/env python3
"""
Multi-Provider AI Model System Demo

Demonstrates how Anox supports AI models from all vendors,
both offline and online, with automatic fallback.
"""

import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workspace.ai_models import (
    ModelType, ModelProvider, ModelConfig, ModelManager,
    create_provider, create_model_manager_with_defaults,
    get_available_models
)


def demo_1_basic_usage():
    """Demo 1: Basic usage with default configuration."""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic Usage (Offline-First)")
    print("=" * 70)
    
    # Create manager with defaults (offline models)
    manager = create_model_manager_with_defaults()
    
    # List available providers
    print("\n📋 Available Providers:")
    for info in manager.list_providers():
        status = "✅" if info['available'] else "❌"
        active = "⭐" if info['is_active'] else "  "
        print(f"{active} {status} {info['name']}: {info['info']['model_name']}")
    
    # Generate text
    print("\n🤖 Generating text...")
    try:
        response = manager.generate("Explain what recursion is in one sentence")
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")
        print(f"Provider: {response.provider}")
        print(f"Tokens: {response.tokens_used}")
    except Exception as e:
        print(f"Note: {e}")
        print("(This is expected if offline models aren't set up)")


def demo_2_online_models():
    """Demo 2: Configure online models (OpenAI, Anthropic, Google)."""
    print("\n" + "=" * 70)
    print("DEMO 2: Online Models Configuration")
    print("=" * 70)
    
    manager = ModelManager()
    
    # Configure multiple online providers
    online_models = [
        {
            'name': 'gpt4',
            'config': ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4",
                model_type=ModelType.ONLINE,
                api_key="sk-test-key",  # Replace with real key
                capabilities=['chat', 'code', 'completion']
            )
        },
        {
            'name': 'claude',
            'config': ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name="claude-3-opus",
                model_type=ModelType.ONLINE,
                api_key="sk-ant-test-key",  # Replace with real key
                capabilities=['chat', 'analysis', 'code']
            )
        },
        {
            'name': 'gemini',
            'config': ModelConfig(
                provider=ModelProvider.GOOGLE,
                model_name="gemini-pro",
                model_type=ModelType.ONLINE,
                api_key="AIza-test-key",  # Replace with real key
                capabilities=['chat', 'multimodal']
            )
        }
    ]
    
    print("\n🌐 Configuring online models...")
    for model_info in online_models:
        provider = create_provider(model_info['config'])
        if manager.register_provider(model_info['name'], provider):
            print(f"✅ Registered: {model_info['name']} ({model_info['config'].model_name})")
    
    # Show capabilities
    print("\n📊 Model Capabilities:")
    for info in manager.list_providers():
        caps = ", ".join(info['info']['capabilities'])
        print(f"  {info['name']}: {caps}")
    
    # Generate with different models
    print("\n🎯 Generating with different models...")
    for provider_name in ['gpt4', 'claude', 'gemini']:
        manager.set_active_provider(provider_name)
        try:
            response = manager.generate("Write a hello world function")
            print(f"  {provider_name}: {response.content[:60]}...")
        except Exception as e:
            print(f"  {provider_name}: {str(e)[:60]}...")


def demo_3_offline_models():
    """Demo 3: Configure offline models (Ollama, Llama.cpp, Transformers)."""
    print("\n" + "=" * 70)
    print("DEMO 3: Offline Models Configuration")
    print("=" * 70)
    
    manager = ModelManager()
    
    # Configure multiple offline providers
    offline_models = [
        {
            'name': 'ollama_llama2',
            'config': ModelConfig(
                provider=ModelProvider.OLLAMA,
                model_name="llama2",
                model_type=ModelType.OFFLINE,
                base_url="http://localhost:11434",
                capabilities=['chat', 'code']
            )
        },
        {
            'name': 'ollama_mistral',
            'config': ModelConfig(
                provider=ModelProvider.OLLAMA,
                model_name="mistral",
                model_type=ModelType.OFFLINE,
                base_url="http://localhost:11434",
                capabilities=['chat', 'code', 'completion']
            )
        },
        {
            'name': 'llama_cpp',
            'config': ModelConfig(
                provider=ModelProvider.LLAMA_CPP,
                model_name="llama-7b",
                model_type=ModelType.OFFLINE,
                model_path="./models/llama-7b.gguf",
                capabilities=['chat', 'code']
            )
        }
    ]
    
    print("\n💾 Configuring offline models...")
    for model_info in offline_models:
        provider = create_provider(model_info['config'])
        if manager.register_provider(model_info['name'], provider):
            available = "✅" if provider.is_available() else "⚠️ (not running)"
            print(f"{available} Registered: {model_info['name']}")
    
    # Show offline advantages
    print("\n✨ Offline Model Advantages:")
    print("  1. ✅ Works without internet")
    print("  2. ✅ Free (no API costs)")
    print("  3. ✅ Private (data never leaves device)")
    print("  4. ✅ Fast (no network latency)")
    print("  5. ✅ Unlimited usage")
    
    # Try generating
    print("\n🎯 Testing offline generation...")
    for provider_name in manager.providers.keys():
        manager.set_active_provider(provider_name)
        try:
            response = manager.generate("Explain AI in simple terms")
            print(f"  {provider_name}: {response.content[:60]}...")
        except Exception as e:
            print(f"  {provider_name}: Note - {str(e)[:50]}...")


def demo_4_automatic_fallback():
    """Demo 4: Automatic fallback between providers."""
    print("\n" + "=" * 70)
    print("DEMO 4: Automatic Fallback (Online → Offline)")
    print("=" * 70)
    
    manager = ModelManager()
    
    # Add both online and offline providers
    providers = [
        ('gpt4', ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4",
            model_type=ModelType.ONLINE,
            api_key="test"
        )),
        ('claude', ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3",
            model_type=ModelType.ONLINE,
            api_key="test"
        )),
        ('ollama', ModelConfig(
            provider=ModelProvider.OLLAMA,
            model_name="llama2",
            model_type=ModelType.OFFLINE
        ))
    ]
    
    print("\n🔄 Setting up fallback chain...")
    for name, config in providers:
        provider = create_provider(config)
        manager.register_provider(name, provider)
        print(f"  Added: {name} ({config.model_type.value})")
    
    # Set fallback order
    fallback_order = ['gpt4', 'claude', 'ollama']
    manager.set_fallback_order(fallback_order)
    
    print(f"\n📋 Fallback order: {' → '.join(fallback_order)}")
    print("   (Tries GPT-4 first, falls back to Claude, then Ollama)")
    
    # Test fallback
    print("\n🎯 Testing fallback mechanism...")
    try:
        response = manager.generate("Test prompt", use_fallback=True)
        print(f"  ✅ Responded with: {response.provider}")
        print(f"  Content: {response.content[:60]}...")
    except Exception as e:
        print(f"  ⚠️ All providers failed: {e}")
    
    print("\n💡 Use Cases:")
    print("  • Internet down → Automatically uses offline model")
    print("  • API quota exceeded → Falls back to alternative")
    print("  • Cost control → Try free models first")
    print("  • Privacy → Prefer offline when possible")


def demo_5_mobile_optimization():
    """Demo 5: Mobile-optimized configuration."""
    print("\n" + "=" * 70)
    print("DEMO 5: Mobile Optimization")
    print("=" * 70)
    
    def get_connection_type():
        """Simulate connection detection."""
        return "4g"  # Could be: wifi, 5g, 4g, 3g, offline
    
    def select_optimal_provider(connection):
        """Select best provider based on connection."""
        if connection in ['wifi', '5g']:
            return 'gpt4', 'Fast connection - use best model'
        elif connection == '4g':
            return 'gpt-3.5', 'Good connection - balanced model'
        elif connection == '3g':
            return 'ollama', 'Slow connection - use offline'
        else:
            return 'ollama', 'No connection - use offline'
    
    connection = get_connection_type()
    provider, reason = select_optimal_provider(connection)
    
    print(f"\n📱 Mobile Device Detected")
    print(f"  Connection: {connection}")
    print(f"  Selected: {provider}")
    print(f"  Reason: {reason}")
    
    print("\n🔋 Battery Optimization:")
    print("  • Offline models - No network radio usage")
    print("  • Response caching - Avoid repeated API calls")
    print("  • Batch requests - Reduce wake-ups")
    print("  • Lazy loading - Load only when needed")
    
    print("\n📊 Bandwidth Optimization:")
    print("  • State deltas - Send only changes")
    print("  • Compression - Reduce data transfer")
    print("  • Model selection - Smaller models on slow connections")
    print("  • Local caching - Reuse previous responses")
    
    print("\n💰 Cost Optimization:")
    print("  • Free offline models for development")
    print("  • Cheaper models (GPT-3.5) for routine tasks")
    print("  • Premium models (GPT-4) only for critical tasks")
    print("  • Track token usage to stay within budget")


def demo_6_available_models():
    """Demo 6: List all available models."""
    print("\n" + "=" * 70)
    print("DEMO 6: Available Models")
    print("=" * 70)
    
    models = get_available_models()
    
    print("\n🌐 Online Models (Cloud API):")
    for model in models['online']:
        print(f"  • {model}")
    
    print("\n💾 Offline Models (Local):")
    for model in models['offline']:
        print(f"  • {model}")
    
    print(f"\nTotal: {len(models['online'])} online + {len(models['offline'])} offline = {len(models['online']) + len(models['offline'])} models")


def demo_7_practical_example():
    """Demo 7: Practical workspace integration."""
    print("\n" + "=" * 70)
    print("DEMO 7: Practical Workspace Integration")
    print("=" * 70)
    
    print("\n🎯 Real-world scenario:")
    print("  You're developing a Python web app on your laptop")
    print("  Internet is spotty, budget is limited")
    
    print("\n⚙️ Optimal configuration:")
    
    # Create manager with smart fallback
    manager = ModelManager()
    
    configs = [
        ('ollama_primary', ModelConfig(
            provider=ModelProvider.OLLAMA,
            model_name="codellama",
            model_type=ModelType.OFFLINE,
            capabilities=['code']
        )),
        ('gpt35_backup', ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-3.5-turbo",
            model_type=ModelType.ONLINE,
            api_key="sk-...",
            capabilities=['chat', 'code']
        )),
        ('gpt4_final', ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4",
            model_type=ModelType.ONLINE,
            api_key="sk-...",
            capabilities=['chat', 'code', 'completion']
        ))
    ]
    
    for name, config in configs:
        provider = create_provider(config)
        manager.register_provider(name, provider)
    
    manager.set_fallback_order(['ollama_primary', 'gpt35_backup', 'gpt4_final'])
    
    print("\n1️⃣ Coding (95% of time):")
    print("   → Use: ollama_primary (CodeLlama)")
    print("   → Why: Free, fast, offline, good for code")
    
    print("\n2️⃣ Complex logic (4% of time):")
    print("   → Use: gpt35_backup (GPT-3.5)")
    print("   → Why: Cheap ($0.001/1K tokens), good reasoning")
    
    print("\n3️⃣ Critical review (1% of time):")
    print("   → Use: gpt4_final (GPT-4)")
    print("   → Why: Best quality for important decisions")
    
    print("\n💰 Cost estimate:")
    print("   • 95% offline: $0/month")
    print("   • 4% GPT-3.5: ~$2/month")
    print("   • 1% GPT-4: ~$5/month")
    print("   • Total: ~$7/month vs $200+ with GPT-4 only")
    
    print("\n✨ Benefits:")
    print("   ✅ Works offline (airplane coding!)")
    print("   ✅ 95% free (save money)")
    print("   ✅ Fast responses (no network latency)")
    print("   ✅ Private (code never leaves device)")
    print("   ✅ Always available (no API quotas)")


def main():
    """Run all demos."""
    print("=" * 70)
    print("🤖 ANOX MULTI-PROVIDER AI SYSTEM DEMO")
    print("=" * 70)
    print("\nThis demo shows how Anox supports AI models from ALL vendors:")
    print("  • Online: OpenAI, Anthropic, Google, Cohere, Mistral")
    print("  • Offline: Ollama, Llama.cpp, Transformers, ONNX")
    print("\nFeatures:")
    print("  ✅ Unified interface for all models")
    print("  ✅ Automatic fallback (online → offline)")
    print("  ✅ Mobile-optimized (bandwidth, battery, cost)")
    print("  ✅ Privacy-first (offline models for sensitive code)")
    
    demos = [
        demo_1_basic_usage,
        demo_2_online_models,
        demo_3_offline_models,
        demo_4_automatic_fallback,
        demo_5_mobile_optimization,
        demo_6_available_models,
        demo_7_practical_example
    ]
    
    for demo in demos:
        try:
            demo()
            input("\nPress Enter to continue to next demo...")
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n⚠️ Error in demo: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("🎉 DEMO COMPLETE")
    print("=" * 70)
    print("\n📚 Learn more:")
    print("  • Documentation: docs/MULTI_PROVIDER_AI.md")
    print("  • Tests: python3 test_ai_models.py")
    print("  • Code: workspace/ai_models.py")
    print("\n🚀 Get started:")
    print("  from workspace.ai_models import create_model_manager_with_defaults")
    print("  manager = create_model_manager_with_defaults()")
    print("  response = manager.generate('Your prompt here')")


if __name__ == "__main__":
    main()
