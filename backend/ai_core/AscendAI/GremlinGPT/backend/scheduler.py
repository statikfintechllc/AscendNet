#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import schedule
import time
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("backend")
import threading
from backend.globals import CFG

# Thread-safe LOOP access
_LOOP = None
_LOOP_LOCK = threading.Lock()


def get_loop():
    global _LOOP
    with _LOOP_LOCK:
        return _LOOP


def set_loop(loop_obj):
    global _LOOP
    with _LOOP_LOCK:
        _LOOP = loop_obj


from self_training.trainer import trigger_retrain
from agents.planner_agent import enqueue_next
from self_mutation_watcher.watcher import scan_and_diff


def start_scheduler():
    LOOP = get_loop()
    if not isinstance(LOOP, dict):
        logger.error("[SCHEDULER] LOOP is not defined or not a dict. Scheduler will not start.")
        return
    retrain_interval = LOOP.get("self_train_interval_min", 15)
    plan_interval = LOOP.get("planner_interval_sec", 10)
    mutation_interval = LOOP.get("mutation_watch_interval_sec", 5)

    logger.info("[SCHEDULER] Initializing GremlinGPT scheduler...")

    import signal

    running = True

    def shutdown_handler(signum, frame):
        nonlocal running
        logger.warning(f"[SCHEDULER] Received signal {signum} — shutting down gracefully.")
        running = False

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    if LOOP.get("self_training_enabled", True):
        schedule.every(retrain_interval).minutes.do(trigger_retrain)
        logger.success("[SCHEDULER] Self-training scheduled.")
    if LOOP.get("planner_enabled", True):
        schedule.every(plan_interval).seconds.do(enqueue_next)
        logger.success("[SCHEDULER] Planner agent scheduled.")
    if LOOP.get("mutation_watch_enabled", True):
        schedule.every(mutation_interval).seconds.do(scan_and_diff)
        logger.success("[SCHEDULER] Mutation watcher scheduled.")

    while running:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("[SCHEDULER] Manual interrupt — halting.")
            break
        except Exception as e:
            import traceback

            logger.error(f"[SCHEDULER] Scheduler encountered error: {e}\n{traceback.format_exc()}")
            time.sleep(3)
    logger.info("[SCHEDULER] Scheduler stopped.")
