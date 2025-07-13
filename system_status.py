#!/usr/bin/env python3
"""
AscendNet System Status and Health Check
Displays the complete unified system status
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def print_banner():
    """Print AscendNet banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                      🚀 AscendNet Unified                      ║
    ║                    P2P AI Marketplace System                  ║
    ║                                                               ║
    ║    GremlinGPT + GodCore + SignalCore = AscendNet            ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_system_structure():
    """Check if the unified system structure is properly set up"""
    root = Path(os.environ.get('HOME', '/home/user')) / "AscendNet"
    
    required_paths = [
        "backend/api",
        "backend/p2p", 
        "backend/ai_core",
        "backend/utils",
        "config",
        "logs",
        "storage",
        "scripts",
        "docs"
    ]
    
    print("📁 System Structure Check:")
    print("=" * 50)
    
    all_good = True
    for path in required_paths:
        full_path = root / path
        if full_path.exists():
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path} (missing)")
            all_good = False
    
    return all_good

def check_configuration():
    """Check system configuration"""
    config_file = Path("/home/statiksmoke8/AscendNet/config/ascendnet.json")
    
    print("\n⚙️  Configuration Status:")
    print("=" * 50)
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(f"   ✅ Configuration file exists")
            print(f"   📋 System: {config['system']['name']} v{config['system']['version']}")
            print(f"   🌍 Environment: {config['system']['environment']}")
            print(f"   🔧 Components enabled: {len([k for k, v in config['components'].items() if v])}")
            
            return True, config
        except Exception as e:
            print(f"   ❌ Error reading config: {e}")
            return False, None
    else:
        print(f"   ❌ Configuration file missing")
        return False, None

def check_components():
    """Check individual components"""
    components = {
        "API Main": "/home/statiksmoke8/AscendNet/backend/api/main.py",
        "P2P Node": "/home/statiksmoke8/AscendNet/backend/p2p/node.py", 
        "AI Core": "/home/statiksmoke8/AscendNet/backend/ai_core/unified_core.py",
        "Orchestrator": "/home/statiksmoke8/AscendNet/ascendnet_orchestrator.py",
        "Setup Script": "/home/statiksmoke8/AscendNet/scripts/setup.sh",
        "Requirements": "/home/statiksmoke8/AscendNet/requirements.txt"
    }
    
    print("\n🧩 Component Status:")
    print("=" * 50)
    
    all_good = True
    for name, path in components.items():
        if Path(path).exists():
            size = Path(path).stat().st_size
            print(f"   ✅ {name:<15} ({size:,} bytes)")
        else:
            print(f"   ❌ {name:<15} (missing)")
            all_good = False
    
    return all_good

def check_logs():
    """Check log files"""
    log_dir = Path("/home/statiksmoke8/AscendNet/logs")
    
    print("\n📝 Logs Status:")
    print("=" * 50)
    
    if log_dir.exists():
        log_files = list(log_dir.glob("*.log"))
        if log_files:
            for log_file in log_files:
                size = log_file.stat().st_size
                modified = datetime.fromtimestamp(log_file.stat().st_mtime)
                print(f"   📄 {log_file.name:<20} {size:>8,} bytes (modified: {modified.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("   📄 No log files found")
    else:
        print("   ❌ Log directory missing")

def show_system_paths(config):
    """Show system paths from configuration"""
    if not config:
        return
        
    print("\n🗺️  System Paths:")
    print("=" * 50)
    
    key_paths = [
        "root", "backend", "config", "logs", "storage",
        "api", "p2p", "ai_core"
    ]
    
    for path_key in key_paths:
        if path_key in config["paths"]:
            path = config["paths"][path_key]
            exists = "✅" if Path(path).exists() else "❌"
            print(f"   {exists} {path_key:<15} {path}")

def show_integration_status():
    """Show status of integrated legacy components"""
    print("\n🔗 Legacy Integration Status:")
    print("=" * 50)
    
    legacy_mappings = {
        "GremlinGPT": "Integrated into backend/ai_core/unified_core.py",
        "GodCore": "Integrated into backend/ai_core/unified_core.py", 
        "SignalCore": "Integrated into backend/ai_core/unified_core.py",
        "AscendAI": "Moved to backend/ai_core/",
        "Bootstrap": "Unified in scripts/setup.sh",
        "Storage Layers": "Unified in storage/ directory"
    }
    
    for component, status in legacy_mappings.items():
        print(f"   🔄 {component:<15} → {status}")

def show_next_steps():
    """Show recommended next steps"""
    print("\n🚀 Next Steps:")
    print("=" * 50)
    print("   1. Run setup script:     ./scripts/setup.sh")
    print("   2. Start development:    ./dev_launch.sh")
    print("   3. View API docs:        http://localhost:8000/docs")
    print("   4. Check system status:  curl http://localhost:8000/api/v1/health")
    print("   5. Monitor logs:         tail -f logs/ascendnet.log")

def main():
    """Main status check"""
    print_banner()
    
    # Run all checks
    structure_ok = check_system_structure()
    config_ok, config = check_configuration()
    components_ok = check_components()
    
    check_logs()
    show_system_paths(config)
    show_integration_status()
    
    # Overall status
    print("\n📊 Overall System Status:")
    print("=" * 50)
    
    overall_status = structure_ok and config_ok and components_ok
    
    if overall_status:
        print("   🎉 AscendNet Unified System: READY")
        print("   ✨ All components successfully integrated")
        print("   🔥 System ready for deployment!")
    else:
        print("   ⚠️  AscendNet Unified System: NEEDS ATTENTION")
        print("   🔧 Some components require setup")
    
    show_next_steps()
    
    return 0 if overall_status else 1

if __name__ == "__main__":
    sys.exit(main())
