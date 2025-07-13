#!/usr/bin/env python3
"""
AscendNet Unified System Orchestrator
Unifies all components into one cohesive system using universal pathing
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Universal AscendNet Base Path
ASCENDNET_ROOT = Path(os.environ.get('HOME', '/home/user')) / "AscendNet"

# Unified Component Paths
PATHS = {
    # Core System Paths
    "root": ASCENDNET_ROOT,
    "backend": ASCENDNET_ROOT / "backend",
    "frontend": ASCENDNET_ROOT / "frontend", 
    "docs": ASCENDNET_ROOT / "docs",
    "scripts": ASCENDNET_ROOT / "scripts",
    "smart_contracts": ASCENDNET_ROOT / "smart-contracts",
    
    # Backend Components
    "api": ASCENDNET_ROOT / "backend" / "api",
    "p2p": ASCENDNET_ROOT / "backend" / "p2p",
    "compute": ASCENDNET_ROOT / "backend" / "compute",
    "payments": ASCENDNET_ROOT / "backend" / "payments",
    "storage": ASCENDNET_ROOT / "backend" / "storage",
    "auth": ASCENDNET_ROOT / "backend" / "auth",
    "utils": ASCENDNET_ROOT / "backend" / "utils",
    
    # Legacy Component Integration Paths
    "ascend_ai": ASCENDNET_ROOT / "AscendAI",
    "gremlin_gpt": ASCENDNET_ROOT / "AscendAI" / "GremlinGPT",
    "god_core": ASCENDNET_ROOT / "GodCore",
    "mobile_mirror": ASCENDNET_ROOT / "Mobile-Mirror",
    "signal_core": ASCENDNET_ROOT / "backend" / "ai_core" / "signal_core",
    "quantum_storage": ASCENDNET_ROOT / "backend" / "storage" / "quantum",
    
    # Storage Layers (Unified)
    "cold_storage": ASCENDNET_ROOT / "storage" / "cold",
    "mem_forge": ASCENDNET_ROOT / "storage" / "memory",
    "expansion_pool": ASCENDNET_ROOT / "storage" / "expansion",
    
    # Configuration and Logs
    "config": ASCENDNET_ROOT / "config",
    "logs": ASCENDNET_ROOT / "logs",
    "cache": ASCENDNET_ROOT / "cache",
    
    # Development and Testing
    "tests": ASCENDNET_ROOT / "tests",
    "sandbox": ASCENDNET_ROOT / "sandbox",
    "temp": ASCENDNET_ROOT / "temp"
}

class AscendNetOrchestrator:
    """Unified system orchestrator for AscendNet"""
    
    def __init__(self):
        self.paths = PATHS
        self.config = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup unified logging system"""
        log_dir = self.paths["logs"]
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "ascendnet.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger("AscendNet")
    
    def get_path(self, component: str) -> Path:
        """Get universal path for any component"""
        if component in self.paths:
            return self.paths[component]
        raise ValueError(f"Unknown component: {component}")
    
    def ensure_structure(self):
        """Ensure all required directories exist (internal only)"""
        self.logger.info("Creating unified AscendNet directory structure...")
        
        # Only create internal backend directories, not external component paths
        internal_paths = {
            name: path for name, path in self.paths.items() 
            if not name in ["ascend_ai", "gremlin_gpt", "god_core", "mobile_mirror"]
        }
        
        for name, path in internal_paths.items():
            try:
                path.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Ensured path exists: {name} -> {path}")
            except Exception as e:
                self.logger.error(f"Failed to create path {name}: {e}")
    
    def load_config(self, config_file: Optional[Path] = None) -> Dict[str, Any]:
        """Load unified configuration"""
        if config_file is None:
            config_file = self.paths["config"] / "ascendnet.json"
        
        try:
            with open(str(config_file), 'r') as f:
                self.config = json.load(f)
                self.logger.info(f"Loaded configuration from {config_file}")
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_file}, using defaults")
            self.config = self._default_config()
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            self.config = self._default_config()
        
        return self.config
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for AscendNet"""
        return {
            "system": {
                "name": "AscendNet",
                "version": "1.0.0-alpha",
                "environment": "development"
            },
            "paths": {k: str(v) for k, v in self.paths.items()},
            "components": {
                "api_enabled": True,
                "p2p_enabled": True,
                "compute_enabled": True,
                "payments_enabled": True,
                "ascend_ai_enabled": True,
                "gremlin_gpt_enabled": True,
                "god_core_enabled": True,
                "mobile_mirror_enabled": True,
                "signal_core_enabled": True
            },
            "network": {
                "p2p_port": 8001,
                "api_port": 8000,
                "discovery_enabled": True
            },
            "storage": {
                "ipfs_enabled": True,
                "quantum_compression": True,
                "cache_size_mb": 1024
            }
        }
    
    def save_config(self, config_file: Optional[Path] = None):
        """Save configuration to file"""
        if config_file is None:
            config_file = self.paths["config"] / "ascendnet.json"
        
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(str(config_file), 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info(f"Saved configuration to {config_file}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def initialize_system(self):
        """Initialize the unified AscendNet system"""
        self.logger.info("Initializing AscendNet Unified System...")
        
        # Create directory structure
        self.ensure_structure()
        
        # Load or create configuration
        self.load_config()
        
        # Save current configuration
        self.save_config()
        
        self.logger.info("AscendNet system initialization complete")
        
        return {
            "status": "initialized",
            "paths": {k: str(v) for k, v in self.paths.items()},
            "config": self.config
        }

def main():
    """Main entry point for AscendNet orchestrator"""
    orchestrator = AscendNetOrchestrator()
    result = orchestrator.initialize_system()
    
    print("🚀 AscendNet Unified System Initialized")
    print(f"📁 Root Path: {result['paths']['root']}")
    print(f"⚙️  Configuration saved to: {result['paths']['config']}/ascendnet.json")
    print(f"📝 Logs available at: {result['paths']['logs']}/ascendnet.log")
    
    return result

if __name__ == "__main__":
    main()
