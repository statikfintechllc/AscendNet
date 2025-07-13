"""
AscendNet Unified Configuration Management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from environment and config files"""

    # Base configuration
    config = {
        "host": os.getenv("ASCENDNET_HOST", "0.0.0.0"),
        "port": int(os.getenv("ASCENDNET_PORT", "8000")),
        "debug": os.getenv("ASCENDNET_DEBUG", "false").lower() == "true",
        "cors_origins": ["*"],
        "allowed_hosts": ["*"],
        # P2P Configuration
        "p2p": {
            "port": int(os.getenv("P2P_PORT", "8001")),
            "bootstrap_nodes": os.getenv("P2P_BOOTSTRAP_NODES", "").split(","),
            "node_id": os.getenv("P2P_NODE_ID", None),
            "discovery_enabled": True,
        },
        # Storage Configuration
        "storage": {
            "ipfs_api": os.getenv("IPFS_API", "/ip4/127.0.0.1/tcp/5001"),
            "cache_dir": os.getenv("CACHE_DIR", "/tmp/ascendnet"),
            "quantum_compression": True,
        },
        # Payment Configuration
        "payments": {
            "ethereum_rpc": os.getenv("ETHEREUM_RPC", ""),
            "solana_rpc": os.getenv("SOLANA_RPC", ""),
            "fee_percentage": float(os.getenv("FEE_PERCENTAGE", "3.0")),
        },
        # AI Core Configuration
        "ai_core": {
            "ascend_ai_enabled": True,
            "gremlin_gpt_enabled": True,
            "signal_core_enabled": True,
            "god_core_enabled": True,
            "mobile_mirror_enabled": True,
            "memory_depth": int(os.getenv("MEMORY_DEPTH", "2048")),
            "recursion_limit": int(os.getenv("RECURSION_LIMIT", "512")),
        },
    }

    # Load from config file if exists
    config_file = (
        Path(os.environ.get("HOME", "/home/user")) / "AscendNet" / "config" / "ascendnet.json"
    )
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)

                # Replace any hardcoded paths in the config with universal ones
                if "paths" in file_config:
                    home_dir = os.environ.get("HOME", "/home/user")
                    ascendnet_root = f"{home_dir}/AscendNet"

                    # Update all paths to use the current user's home directory
                    for key, path in file_config["paths"].items():
                        if isinstance(path, str) and "/home/statiksmoke8/AscendNet" in path:
                            file_config["paths"][key] = path.replace(
                                "/home/statiksmoke8/AscendNet", ascendnet_root
                            )

                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")

    return config
