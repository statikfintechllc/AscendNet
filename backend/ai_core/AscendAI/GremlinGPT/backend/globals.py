# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

# backend/globals.py

import os
import toml
import json
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("backend")

# === CONFIGURATION PATHS ===
CONFIG_PATH = "config/config.toml"
MEMORY_JSON = "config/memory.json"


def load_config():
    try:
        return toml.load(CONFIG_PATH)
    except Exception as e:
        logger.critical(f"[GLOBALS] Failed to load TOML config: {e}")
        return {}


def load_memory_config():
    try:
        with open(MEMORY_JSON, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.critical(f"[GLOBALS] Failed to load memory config: {e}")
        return {}


CFG = load_config()
MEM = load_memory_config()


# === PATH MANAGEMENT ===
def resolve_path(p):
    """Expands $ROOT and user home (~) dynamically"""
    if not isinstance(p, str):
        return str(p)
    # Use current script directory as the project root, not the config base_dir
    project_root = Path(__file__).parent.parent.resolve()
    return os.path.expanduser(p.replace("$ROOT", str(project_root)))


BASE_DIR = resolve_path(CFG["paths"].get("base_dir", "."))
DATA_DIR = resolve_path(CFG["paths"].get("data_dir", "data"))
MODELS_DIR = resolve_path(CFG["paths"].get("models_dir", "models"))
CHECKPOINTS_DIR = resolve_path(CFG["paths"].get("checkpoints_dir", "run/checkpoints"))
LOG_FILE = resolve_path(CFG["paths"].get("log_file", "data/logs/runtime.log"))


# === LOGGER INITIALIZATION ===
from utils.logging_config import setup_module_logger

logger = setup_module_logger("backend")


# === HARDWARE PREFERENCES ===
HARDWARE = {
    "use_ram": CFG.get("hardware", {}).get("use_ram", True),
    "use_cpu": CFG.get("hardware", {}).get("use_cpu", True),
    "use_gpu": CFG.get("hardware", {}).get("use_gpu", False),
    "gpu_device": CFG.get("hardware", {}).get("gpu_device", [0]),
    "multi_gpu": CFG.get("hardware", {}).get("multi_gpu", False),
}


# === NLP / EMBEDDING CONFIG ===
NLP = {
    "tokenizer_model": CFG["nlp"].get("tokenizer_model", "bert-base-uncased"),
    "embedder_model": CFG["nlp"].get("embedder_model", "bert-base-uncased"),
    "transformer_model": CFG["nlp"].get("transformer_model", "bert-base-uncased"),
    "embedding_dim": CFG["nlp"].get("embedding_dim", 768),
    "confidence_threshold": CFG["nlp"].get("confidence_threshold", 0.5),
}


# === AGENT TASK SETTINGS ===
AGENT = {
    "max_tasks": CFG["agent"].get("max_tasks", 100),
    "task_retry_limit": CFG["agent"].get("task_retry_limit", 3),
    "log_agent_output": CFG["agent"].get("log_agent_output", True),
}


# === SCRAPER CONFIG ===
SCRAPER = {
    "profile": CFG["scraper"].get("browser_profile", "scraper/profiles/chromium_profile"),
    "interval": CFG["scraper"].get("scrape_interval_sec", 30),
    "max_concurrent": CFG["scraper"].get("max_concurrent_scrapers", 1),
}


# === MEMORY ENGINE SETTINGS ===
MEMORY = {
    "vector_backend": CFG["memory"].get(
        "dashboard_selected_backend", CFG["memory"].get("vector_backend", "faiss")
    ),
    "embedding_format": CFG["memory"].get("embedding_format", "float32"),
    "auto_index": CFG["memory"].get("auto_index", True),
    "index_chunk_size": CFG["memory"].get("index_chunk_size", 128),
}


# === SYSTEM FLAGS ===
SYSTEM = {
    "name": CFG["system"].get("name", "GremlinGPT"),
    "mode": CFG["system"].get("mode", "alpha"),
    "offline": CFG["system"].get("offline", False),
    "debug": CFG["system"].get("debug", False),
    "log_level": CFG["system"].get("log_level", "INFO"),
}


# === LOOP TIMING / CONTROL ===
LOOP = {
    "fsm_tick_delay": CFG.get("loop", {}).get("fsm_tick_delay", 0.5),
    "planner_interval": CFG.get("loop", {}).get("planner_interval", 60),
    "mutation_watch_interval": CFG.get("loop", {}).get("mutation_watch_interval", 10),
    "planner_enabled": CFG.get("loop", {}).get("planner_enabled", True),
    "mutation_enabled": CFG.get("loop", {}).get("mutation_enabled", True),
    "self_training_enabled": CFG.get("loop", {}).get("self_training_enabled", True),
}


# === DASHBOARD BACKEND SELECTION ===
def set_dashboard_backend(backend):
    """Update the dashboard selected backend in config and memory"""
    global MEMORY
    if backend in ["faiss", "chroma"]:
        MEMORY["vector_backend"] = backend
        CFG["memory"]["dashboard_selected_backend"] = backend
        # Also update the config file
        try:
            with open(CONFIG_PATH, "w") as f:
                toml.dump(CFG, f)
            logger.info(f"[GLOBALS] Dashboard backend updated to: {backend}")
            return True
        except Exception as e:
            logger.error(f"[GLOBALS] Failed to update backend: {e}")
            return False
    else:
        logger.error(f"[GLOBALS] Invalid backend: {backend}")
        return False


def get_dashboard_backend():
    """Get the current dashboard selected backend"""
    return MEMORY.get("vector_backend", "faiss")


# === AGENT ROLE ASSIGNMENTS ===
ROLES = CFG.get(
    "roles",
    {
        "planner": "planner_agent",
        "executor": "tool_executor",
        "trainer": "feedback_loop",
        "kernel": "code_mutator",
    },
)
