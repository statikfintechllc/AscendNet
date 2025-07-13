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
from loguru import logger

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
    base = Path(os.path.expanduser(CFG["paths"].get("base_dir", "."))).resolve()
    return os.path.expanduser(p.replace("$ROOT", str(base)))


BASE_DIR = resolve_path(CFG["paths"].get("base_dir", "."))
DATA_DIR = resolve_path(CFG["paths"].get("data_dir", "data"))
MODELS_DIR = resolve_path(CFG["paths"].get("models_dir", "models"))
CHECKPOINTS_DIR = resolve_path(CFG["paths"].get("checkpoints_dir", "run/checkpoints"))
LOG_FILE = resolve_path(CFG["paths"].get("log_file", "run/logs/runtime.log"))


# === LOGGER INITIALIZATION ===
logger.add(LOG_FILE, rotation="1 MB", retention="5 days", enqueue=True)
logger.info("[GLOBALS] Configuration loaded and logger initialized.")


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
