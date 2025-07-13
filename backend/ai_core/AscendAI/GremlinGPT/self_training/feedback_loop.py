# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# self_training/feedback_loop.py

import json
import os
from datetime import datetime
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("self_training")
from memory.vector_store.embedder import inject_watermark, package_embedding

# Paths
LOG_PATH = Path("data/logs/")
TRIGGER_FILE = Path("run/checkpoints/retrain_trigger.json")
ARCHIVE_DIR = Path("docs/feedback_triggers/")
LOG_PATH.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def inject_feedback():
    logger.info("[FEEDBACK] Mutation event detected — scheduling retrain.")

    trigger = {
        "trigger": "mutation_watcher",
        "time": datetime.utcnow().isoformat(),
        "note": "Auto-diff-based training cycle",
        "watermark": "source:GremlinGPT",
        "context": "Feedback loop triggered by mutation event",
    }

    try:
        with open(TRIGGER_FILE, "w") as f:
            json.dump(trigger, f, indent=2)
        logger.success(f"[FEEDBACK] Retrain trigger saved → {TRIGGER_FILE}")

        # Inject into vector memory
        inject_watermark(origin="feedback_loop")

        # Archive trigger for traceable memory lineage
        archive_trigger(trigger)

        # Autocommit if git settings permit
        auto_commit_push()

    except Exception as e:
        logger.error(f"[FEEDBACK] Failed to save retrain trigger: {e}")


def archive_trigger(trigger):
    try:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        out_path = ARCHIVE_DIR / f"trigger_{ts}.json"
        with open(out_path, "w") as f:
            json.dump(trigger, f, indent=2)
        logger.debug(f"[FEEDBACK] Trigger archived → {out_path}")
    except Exception as e:
        logger.warning(f"[FEEDBACK] Trigger archive failed: {e}")


def auto_commit_push():
    try:
        os.system(f"git add {ARCHIVE_DIR}")
        os.system('git commit -m "[autocommit] Feedback trigger archived"')
        branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
        os.system(f"git push origin {branch}")
        logger.info("[FEEDBACK] Trigger autocommitted and pushed.")
    except Exception as e:
        logger.warning(f"[FEEDBACK] Git push failed: {e}")


def check_trigger():
    exists = TRIGGER_FILE.exists()
    logger.debug(f"[FEEDBACK] Trigger file exists: {exists}")
    return exists


def clear_trigger():
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()
        logger.info("[FEEDBACK] Retrain trigger cleared.")


def tag_event(tag, meta=None):
    """Tag an event for feedback, traceability, and cross-module signaling."""
    event = {
        "tag": tag,
        "meta": meta or {},
        "timestamp": datetime.utcnow().isoformat(),
        "watermark": "source:GremlinGPT",
    }
    try:
        # Log to feedback log
        log_path = LOG_PATH / "tagged_events.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        # Archive for traceability
        archive_trigger(event)
        logger.info(f"[FEEDBACK] Event tagged: {tag} | {meta}")
    except Exception as e:
        logger.error(f"[FEEDBACK] Failed to tag event: {e}")


__all__ = [
    "inject_feedback",
    "archive_trigger",
    "auto_commit_push",
    "check_trigger",
    "clear_trigger",
    "tag_event",
]
