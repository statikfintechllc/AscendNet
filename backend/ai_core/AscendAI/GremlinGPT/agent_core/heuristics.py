#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import psutil
import random
import math
from loguru import logger  # type: ignore
from typing import Dict, Any
import json
from backend.globals import CFG


def evaluate_task(task: dict, queue_size: int = 0) -> bool:
    """
    Determines whether to process a task based on system pressure, entropy, and task type.

    Args:
        task (dict): Task dict with at least a 'type' key.
        queue_size (int): Optional backlog pressure input for dynamic control.

    Returns:
        bool: True if execution is approved, False if it should be deferred.
    """

    task_type = task.get("type", "unknown")
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    load = sum(psutil.getloadavg()) / 3
    disk = psutil.disk_usage("/").percent
    entropy = random.random()

    # Load thresholds (configurable)
    cpu_thresh = CFG.get("heuristics", {}).get("cpu", 80)
    mem_thresh = CFG.get("heuristics", {}).get("memory", 85)
    disk_thresh = CFG.get("heuristics", {}).get("disk", 90)
    rng_floor = CFG.get("heuristics", {}).get("entropy_min", 0.05)

    # Task weighting: some task types tolerate more stress
    tolerance_map = {
        "self_train": 0.2,
        "scrape": 0.1,
        "nlp": 0.1,
        "shell": 0.05,
        "trading": 0.15,
        "ask_monday": 0.1,
    }

    entropy_buffer = tolerance_map.get(task_type, 0.0)
    # Remove unused entropy_pass variable

    cpu_count = psutil.cpu_count()
    system_pass = (
        cpu < cpu_thresh
        and mem < mem_thresh
        and disk < disk_thresh
        and (cpu_count is not None and load < cpu_count)
    )

    # Queue overload: if queue is large, reduce rejection chance
    queue_pressure_bonus = math.tanh(queue_size / 10) * 0.1  # Max +10% chance

    decision = system_pass and (entropy + queue_pressure_bonus) > (rng_floor + entropy_buffer)

    logger.debug(
        f"[HEURISTICS] Task={task_type} | CPU={cpu} | MEM={mem} | DISK={disk} | "
        f"LOAD={load:.2f} | Q={queue_size} | RNG={entropy:.2f} + {queue_pressure_bonus:.2f} | "
        f"Decision={decision}"
    )

    return decision
