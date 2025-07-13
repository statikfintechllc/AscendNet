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
from backend.globals import CFG, logger
from datetime import datetime

STATE_FILE = Path(CFG["paths"].get("checkpoints_dir", "run/checkpoints/")) / "state_snapshot.json"
# Directory creation deferred to save_state()


def load_state():
    """
    Loads the state snapshot from the state file if it exists.

    Returns:
        dict: The loaded state as a dictionary if the file exists and is valid, otherwise an empty dictionary.
    """
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                logger.debug(f"[STATE] Loaded state snapshot with keys: {list(state.keys())}")
                return state
        except Exception as e:
            logger.error(f"[STATE] Failed to load snapshot: {e}")
    return {}


def save_state(state):
    """
    Save the current application state to a JSON file.

    Args:
        state (dict): The state dictionary to be saved.
    """
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        # Use datetime.now(timezone.utc) if you want UTC, or datetime.utcnow() for naive UTC
        logger.info(f"[STATE] Snapshot saved @ {datetime.utcnow().isoformat()} UTC")
    except Exception as e:
        logger.error(f"[STATE] Failed to save snapshot: {e}")
