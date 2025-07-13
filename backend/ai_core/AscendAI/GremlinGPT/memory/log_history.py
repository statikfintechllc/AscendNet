#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import json
from pathlib import Path
from datetime import datetime
from backend.globals import logger

HISTORY_DIR = Path("data/logs/history/")
HISTORY_FILE = HISTORY_DIR / "gremlin_exec_log.jsonl"


def log_event(event_type, task_type, details, status="ok", meta=None):
    """
    Stores an event in the Gremlin execution history log with semantic metadata.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "task": task_type,
        "status": status,
        "details": details,
        "meta": meta or {},
    }

    try:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.error(f"[HISTORY] Failed to log: {e}")


def load_history(n=50):
    """
    Loads the last n historical events from memory.
    """
    try:
        from collections import deque

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = deque(f, maxlen=n)
        return [json.loads(line) for line in lines]
        return []
    except Exception as e:
        logger.error(f"[HISTORY] Load failed: {e}")
        return []


# === CLI Test Harness ===
if __name__ == "__main__":
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    log_event("exec", "scrape", {"outcome": "5 tickers pulled"}, status="success")
    log_event("exec", "nlp", {"answer": "support/resistance identified"}, status="ok")
    print(load_history(2))
