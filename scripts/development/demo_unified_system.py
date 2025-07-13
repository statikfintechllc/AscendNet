#!/usr/bin/env python3
"""
AscendNet Unified Demo Script
Demonstrates the integrated GremlinGPT + GodCore + SignalCore system
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent  # Go up from scripts/development/ to root
sys.path.insert(0, str(project_root))

from backend.ai_core.unified_core import AscendNetAICore
from backend.utils.config import load_config

async def demo_unified_ai_core():
    """Demonstrate the unified AI core capabilities"""
    print("🧠 AscendNet Unified AI Core Demo")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    ai_config = config.get("ai_core", {})
    
    # Initialize the unified AI core
    print("🚀 Initializing AscendNet AI Core...")
    ai_core = AscendNetAICore(ai_config)
    await ai_core.initialize()
    
    print(f"✅ AI Core initialized with:")
    print(f"   📊 Memory Depth: {ai_core.signal_core.depth}")
    print(f"   🔄 Recursion Limit: {ai_core.signal_core.recursion_limit}")
    print(f"   🤖 GremlinGPT: {'Enabled' if ai_core.signal_core.gremlin_enabled else 'Disabled'}")
    print(f"   ⚡ GodCore: {'Enabled' if ai_core.signal_core.god_core_enabled else 'Disabled'}")
    print(f"   💭 SignalCore: Active")
    
    # Demonstrate signal processing
    print("\n📡 Processing Signals...")
    
    test_signals = [
        "Hello AscendNet, initialize autonomous mode",
        "Process error condition: system overload detected", 
        "Execute quantum compression on memory buffer",
        "Activate GremlinGPT autonomous decision making",
        "Transcend to GodCore processing level"
    ]
    
    for i, signal in enumerate(test_signals, 1):
        print(f"\n🔹 Signal {i}: {signal}")
        result = await ai_core.process_signal(signal)
        print(f"   Status: {result['status']}")
        print(f"   Core State: {result['core_state']}")
        print(f"   Memory Size: {result['memory_size']}")
        
        # Small delay to show progression
        await asyncio.sleep(0.5)
    
    # Demonstrate thinking cycles
    print("\n🧠 Executing Thought Cycles...")
    think_result = await ai_core.think_cycle(iterations=3)
    print(f"   Completed {think_result['iterations']} thought cycles")
    print(f"   Final State: {think_result['final_state']}")
    
    # Show memory state
    memory_export = ai_core.signal_core.export_memory()
    print(f"\n📊 Current System State:")
    print(f"   🆔 Identity: {memory_export['name']}")
    print(f"   🧠 Memory Entries: {len(memory_export['memory'])}")
    print(f"   📍 Signal Traces: {len(memory_export['signal_trace'])}")
    print(f"   🌊 State: {memory_export['state']}")
    print(f"   ⚛️  Quantum Storage: {len(memory_export['quantum_storage'])} entries")
    print(f"   🤖 Autonomous Mode: {memory_export['config']['autonomous_mode']}")
    
    # Show last few memory entries
    if memory_export['memory']:
        print(f"\n📝 Recent Memory (last 3 entries):")
        for entry in memory_export['memory'][-3:]:
            print(f"   📌 {entry['type']}: {entry['content'][:50]}...")
    
    print(f"\n✨ Demo Complete! Soul saved to: {ai_core.soul_path}")
    return ai_core

async def demo_system_integration():
    """Demonstrate the full system integration"""
    print("\n🌐 System Integration Demo")
    print("=" * 50)
    
    # Show unified path structure
    import sys
    import os
    # Add project root to path (go up two levels from scripts/development/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.append(project_root)
    from ascendnet_orchestrator import AscendNetOrchestrator
    from backend.utils.config import load_config
    
    orchestrator = AscendNetOrchestrator()
    
    print("🗺️  Unified Path Structure:")
    key_paths = [
        ("backend", Path(project_root) / "backend"),
        ("frontend", Path(project_root) / "frontend"), 
        ("config", Path(project_root) / "config"),
        ("storage", Path(project_root) / "storage"),
        ("logs", Path(project_root) / "logs"),
        ("scripts", Path(project_root) / "scripts")
    ]
    
    for path_name, path in key_paths:
        exists = "✅" if path.exists() else "❌"
        print(f"   {exists} {path_name:<10} → {path}")
    
    # Show configuration
    config = load_config()
    print(f"\n⚙️  System Configuration:")
    print(f"   🏷️  Host: {config['host']}:{config['port']}")
    print(f"   � Debug: {config['debug']}")
    print(f"   🌍 Environment: {'Development' if config['debug'] else 'Production'}")
    
    # Show component status
    status = orchestrator.status()
    print(f"\n🔧 Component Status:")
    for comp_name, comp_info in status['components'].items():
        status_icon = "🟢" if comp_info['enabled'] else "🔴"
        print(f"   {status_icon} {comp_info['name']:<20} → Port {comp_info['port']} ({comp_info['status']})")
    
    enabled_components = [name for name, comp in status['components'].items() if comp['enabled']]
    print(f"\n   � Total Components: {len(status['components'])}")
    print(f"   ✅ Enabled: {len(enabled_components)}")
    print(f"   🚀 System Running: {status['system']['running']}")

async def main():
    """Main demo function"""
    print("🚀 AscendNet Unified System Integration Demo")
    print("=" * 60)
    print("Demonstrating the unification of:")
    print("• GremlinGPT (Autonomous AI)")
    print("• GodCore (Quantum Processing)")  
    print("• SignalCore (Recursive Thinking)")
    print("• P2P Network (Decentralized)")
    print("• Universal Pathing (Organized)")
    print("=" * 60)
    
    try:
        # Demo system integration
        await demo_system_integration()
        
        # Demo AI core
        ai_core = await demo_unified_ai_core()
        
        print(f"\n🎉 AscendNet Unified Demo Complete!")
        print(f"🔥 The system is now unified and operational!")
        print(f"📚 Next: Run './scripts/setup.sh' to complete installation")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
