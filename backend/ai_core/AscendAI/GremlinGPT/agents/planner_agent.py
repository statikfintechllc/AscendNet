#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: agents/planner_agent.py

from agent_core.task_queue import enqueue_task, reprioritize, dump
from tools.reward_model import top_rewarded_tasks
from memory.vector_store import embedder
import logging
logger = logging.getLogger("GremlinGPT.TaskQueue")
from backend.utils.git_ops import archive_json_log, auto_commit
from datetime import datetime
import random
import os

AGENT_NAME = "planner_agent"


def inspect_task_queue():
    current = dump()
    logger.info(f"[{AGENT_NAME}] Found {sum(len(current[level]) for level in current)} task(s) in queue.")
    return current


def analyze_rewards(threshold=0.4):
    top = top_rewarded_tasks(n=10)
    logger.info(f"[{AGENT_NAME}] Top reward signals:")
    for t in top:
        logger.info(f"  - {t['task']} [Score: {t['reward']}] Reason: {t['reason']}")
    weak_signals = [t for t in top if t["reward"] < threshold]
    return top, weak_signals


def adjust_priorities(weak_signals):
    queue = dump()
    affected_types = {w["task"] for w in weak_signals}
    count = 0
    for level in queue:
        for task in queue[level]:
            tid = task.get("id")
            if task["type"] in affected_types:
                if reprioritize(tid, "high"):
                    logger.debug(f"[{AGENT_NAME}] Boosted priority of task {tid}")
                    count += 1
    if count:
        logger.info(
            f"[{AGENT_NAME}] Reprioritized {count} tasks due to low confidence."
        )


def plan_next_task():
    try:
        top, weak = analyze_rewards()
        adjust_priorities(weak)

        if weak:
            choice = weak[0]["task"]
            reason = "reprocessing_low_confidence"
        elif top:
            choice = random.choices(
                [t["task"] for t in top], weights=[t["reward"] for t in top], k=1
            )[0]
            reason = "reward_guided"
        else:
            choice = "scrape"
            reason = "fallback_scrape"

        planned = {
            "type": choice,
            "meta": {
                "source": AGENT_NAME,
                "timestamp": datetime.utcnow().isoformat(),
                "strategy": reason,
            },
        }

        desc = f"Planned task: {choice} via {reason}"
        vector = embedder.embed_text(desc)
        embedder.package_embedding(
            text=desc,
            vector=vector,
            meta={
                "agent": AGENT_NAME,
                "task_type": choice,
                "reason": reason,
                "timestamp": planned["meta"]["timestamp"],
                "watermark": "source:GremlinGPT",
            },
        )

        embedder.inject_watermark(origin=AGENT_NAME)

        # Archive NLP dataset if exists
        nlp_set = "data/nlp_training_sets/auto_generated.jsonl"
        if os.path.exists(nlp_set):
            archive_path = archive_json_log(nlp_set, prefix="planlog")
            if archive_path:
                auto_commit(archive_path, message="[autocommit] Planner log update")

        logger.info(f"[{AGENT_NAME}] Planned next task: {choice} [{reason}]")
        return planned
    except Exception as e:
        logger.error(f"[{AGENT_NAME}] Failed planning next task: {e}")
        # Emergency fallback
        return {
            "type": "scrape",
            "meta": {
                "source": AGENT_NAME,
                "timestamp": datetime.utcnow().isoformat(),
                "strategy": "error_fallback",
                "error": str(e),
            },
        }


def enqueue_next():
    task = plan_next_task()
    enqueue_task(task)
    logger.info(f"[{AGENT_NAME}] Enqueued task: {task['type']}")


def planner_loop(cycles=3):
    logger.info(f"[{AGENT_NAME}] Starting planner loop with {cycles} cycles.")
    for _ in range(cycles):
        enqueue_next()


if __name__ == "__main__":
    planner_loop(3)
