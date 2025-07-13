#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: agent_core/task_queue.py

from collections import deque, defaultdict
import uuid
import json
from pathlib import Path
import logging

logger = logging.getLogger("GremlinGPT.TaskQueue")
from datetime import datetime, timedelta

QUEUE_FILE = Path("run/checkpoints/task_queue.json")
ESCALATION_THRESHOLD_SEC = 120


class TaskQueue:
    """
    Production-ready prioritized task queue for FSM and agents.
    """

    def __init__(self):
        self.task_queue = {"high": deque(), "normal": deque(), "low": deque()}
        self.task_status = {}
        self.task_meta = defaultdict(dict)
        self._load_snapshot()

    def enqueue_task(self, task):
        task_id = str(uuid.uuid4())
        task["id"] = task_id
        priority = task.get("priority", "normal").lower()
        if priority not in self.task_queue:
            logger.warning(f"[TaskQueue] Invalid priority '{priority}', defaulting to normal.")
            priority = "normal"
        self.task_queue[priority].append(task)
        self.task_status[task_id] = "queued"
        self.task_meta[task_id] = {
            "type": task["type"],
            "priority": priority,
            "timestamp": datetime.utcnow().isoformat(),
            "retries": 0,
        }
        logger.debug(f"[TaskQueue] Enqueued ({priority}): {task['type']} ({task_id})")
        self._save_snapshot()

    def fetch_task(self, task_type=None):
        for level in ["high", "normal", "low"]:
            for _ in range(len(self.task_queue[level])):
                task = self.task_queue[level].popleft()
                if not task_type or task["type"] == task_type:
                    self.task_status[task["id"]] = "running"
                    return task
                self.task_queue[level].append(task)
        return None

    def reprioritize(self, task_id, new_priority):
        if new_priority not in self.task_queue:
            logger.error(f"[TaskQueue] Invalid target priority: {new_priority}")
            return False
        for level in ["high", "normal", "low"]:
            for task in list(self.task_queue[level]):
                if task.get("id") == task_id:
                    self.task_queue[level].remove(task)
                    task["priority"] = new_priority
                    self.task_queue[new_priority].append(task)
                    self.task_meta[task_id]["priority"] = new_priority
                    self.task_status[task_id] = "reprioritized"
                    logger.info(f"[TaskQueue] Task {task_id} moved to {new_priority}")
                    self._save_snapshot()
                    return True
        logger.warning(f"[TaskQueue] Task ID {task_id} not found in any queue.")
        return False

    def promote_old_tasks(self):
        now = datetime.utcnow()
        threshold = timedelta(seconds=ESCALATION_THRESHOLD_SEC)
        for level, next_level in [("low", "normal"), ("normal", "high")]:
            to_promote = []
            for task in list(self.task_queue[level]):
                tid = task.get("id")
                if not tid or tid not in self.task_meta:
                    continue
                timestamp = datetime.fromisoformat(self.task_meta[tid]["timestamp"])
                if now - timestamp > threshold:
                    to_promote.append(task)
                    self.task_queue[level].remove(task)
                    self.task_meta[tid]["priority"] = next_level
                    logger.info(f"[ESCALATION] Promoted task {tid} to {next_level}")
            for task in to_promote:
                self.task_queue[next_level].append(task)
        self._save_snapshot()

    def retry(self, task):
        tid = task.get("id")
        if tid:
            self.task_meta[tid]["retries"] += 1
            self.task_status[tid] = "retried"
            priority = self.task_meta[tid].get("priority", "normal")
            self.task_queue[priority].append(task)
            logger.warning(f"[TaskQueue] Retried ({priority}): {tid}")
            self._save_snapshot()

    def update_task_status(self, task_id, status):
        self.task_status[task_id] = status
        logger.debug(f"[TaskQueue] {task_id} => {status}")
        self._save_snapshot()

    def get_all_tasks(self):
        return [
            {
                "id": k,
                "type": self.task_meta[k]["type"],
                "status": self.task_status[k],
                "priority": self.task_meta[k].get("priority", "normal"),
                "retries": self.task_meta[k].get("retries", 0),
                "timestamp": self.task_meta[k].get("timestamp"),
            }
            for k in self.task_status
        ]

    def dump(self):
        return {
            "high": list(self.task_queue["high"]),
            "normal": list(self.task_queue["normal"]),
            "low": list(self.task_queue["low"]),
        }

    def _save_snapshot(self):
        def make_serializable(obj):
            if isinstance(obj, defaultdict):
                obj = dict(obj)
            if isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [make_serializable(i) for i in obj]
            if isinstance(obj, (datetime,)):
                return obj.isoformat()
            return obj

        try:
            snapshot = {
                "queue": {k: list(v) for k, v in self.task_queue.items()},
                "status": make_serializable(self.task_status),
                "meta": make_serializable(dict(self.task_meta)),
            }
            with open(QUEUE_FILE, "w") as f:
                json.dump(snapshot, f, indent=2, default=str)
                logger.debug("[TaskQueue] Snapshot saved.")
        except Exception as e:
            logger.error(f"[TaskQueue] Snapshot save failed: {e}")

    def _load_snapshot(self):
        try:
            with open(QUEUE_FILE, "r") as f:
                data = json.load(f)
                for level in self.task_queue:
                    self.task_queue[level].clear()
                    self.task_queue[level].extend(data.get("queue", {}).get(level, []))
                self.task_status.update(data.get("status", {}))
                self.task_meta = defaultdict(dict, data.get("meta", {}))
            logger.info("[TaskQueue] Queue restored from snapshot.")
        except Exception as e:
            logger.warning(f"[TaskQueue] Failed to load queue snapshot: {e}")

    def is_empty(self):
        """
        Check if all priority queues (high, normal, low) are empty.
        Used by FSM to determine when to halt or pause execution loop.
        """
        empty = all(len(queue) == 0 for queue in self.task_queue.values())
        logger.debug(f"[TaskQueue] is_empty() → {empty}")
        return empty

    def get_next(self):
        """
        Fetches the next available task using internal priority order.
        Equivalent to fetch_task(task_type=None), but callable by FSM directly.
        Marks task as 'running' and returns it.
        """
        task = self.fetch_task()
        if task:
            logger.debug(f"[TaskQueue] get_next() → {task['id']}")
        else:
            logger.debug("[TaskQueue] get_next() → None")
        return task


# --- Legacy function API for FSM compatibility ---
# --- Legacy function API for FSM compatibility ---
"""
Legacy function API for FSM compatibility.

These functions provide a module-level interface to the TaskQueue singleton instance,
allowing legacy code and FSM modules to enqueue, fetch, reprioritize, and manage tasks
without directly instantiating or referencing the TaskQueue class. This ensures backward
compatibility and simplifies integration with existing agent and FSM workflows.

Usage:
    enqueue_task(task_dict)
    fetch_task(task_type=None)
    reprioritize(task_id, new_priority)
    promote_old_tasks()
    retry(task)
    get_all_tasks()
    update_task_status(task_id, status)
    dump()
    get_next()
    is_empty()
"""

# Singleton instance for static functions

_task_queue = TaskQueue()


def enqueue_task(task):
    return _task_queue.enqueue_task(task)


def fetch_task(task_type=None):
    return _task_queue.fetch_task(task_type)


def reprioritize(task_id, new_priority):
    return _task_queue.reprioritize(task_id, new_priority)


def promote_old_tasks():
    return _task_queue.promote_old_tasks()


def retry(task):
    return _task_queue.retry(task)


def get_all_tasks():
    return _task_queue.get_all_tasks()


def update_task_status(task_id, status):
    return _task_queue.update_task_status(task_id, status)


def dump():
    return _task_queue.dump()


def get_next():
    return _task_queue.get_next()


def is_empty():
    return _task_queue.is_empty()


__all__ = [
    "TaskQueue",
    "enqueue_task",
    "fetch_task",
    "get_next",
    "is_empty",
    "reprioritize",
    "promote_old_tasks",
    "retry",
    "get_all_tasks",
    "update_task_status",
    "dump",
]
