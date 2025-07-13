#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import subprocess
import shlex
import shutil
import json
from datetime import datetime
from pathlib import Path
from memory.vector_store.embedder import package_embedding
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("executors")

# --- Import encode for embedding shell logs ---
try:
    from nlp_engine.transformer_core import encode
except ImportError:
    import numpy as np

    def encode(text):
        return np.zeros(384, dtype="float32")


LOG_PATH = Path("data/logs/shell_log.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

SAFE_COMMANDS = {
    "ls",
    "pwd",
    "whoami",
    "echo",
    "ps",
    "top",
    "df",
    "free",
    "uptime",
    "uname",
    "cat",
    "grep",
    "find",
}


def run_shell_command(cmd: str) -> str:
    parsed = shlex.split(cmd)

    if not parsed:
        logger.warning("[SHELL] Empty or invalid command.")
        return "[DENIED] Empty command"

    base_cmd = parsed[0]

    if base_cmd not in SAFE_COMMANDS:
        logger.warning(f"[SHELL] Unsafe command blocked: {base_cmd}")
        return f"[DENIED] Unsafe command: {base_cmd}"

    if not shutil.which(base_cmd):
        logger.warning(f"[SHELL] Command not found: {base_cmd}")
        return f"[DENIED] Command not found: {base_cmd}"

    try:
        result = subprocess.run(parsed, capture_output=True, text=True, timeout=10)

        output = result.stdout.strip() or result.stderr.strip() or "[NO OUTPUT]"

        meta = {
            "origin": "shell_executor",
            "command": cmd,
            "timestamp": datetime.utcnow().isoformat(),
            "watermark": "source:GremlinGPT",
        }

        vector = encode(f"{cmd}\n{output}")
        package_embedding(f"{cmd}\n{output}", vector, meta=meta)

        with open(LOG_PATH, "a") as log:
            log.write(
                json.dumps({"timestamp": meta["timestamp"], "command": cmd, "output": output})
                + "\n"
            )

        logger.info(f"[SHELL] Executed: {cmd}")
        return output

    except subprocess.TimeoutExpired:
        logger.error(f"[SHELL] Command timed out: {cmd}")
        return "[ERROR] Command timed out."

    except Exception as e:
        logger.error(f"[SHELL] Execution error: {e}")
        return f"[ERROR] {e}"
