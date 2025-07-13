#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: FSM Core & Module Integrity Directive

import time
import schedule  # type: ignore
import json
import os
from pathlib import Path
from rich.console import Console
from datetime import datetime, timezone

from agent_core.task_queue import TaskQueue, reprioritize, promote_old_tasks
from executors.tool_executor import execute_tool
from agent_core.heuristics import evaluate_task
from agent_core.error_log import log_error
from agents.planner_agent import enqueue_next
from backend.globals import CFG  # import only used symbol
from backend.utils.git_ops import archive_json_log, auto_commit
from memory.vector_store.embedder import inject_watermark
from memory.log_history import log_event
from self_mutation_watcher.watcher import scan_and_diff
from self_mutation_watcher.mutation_daemon import run_daemon
from agent_core.agent_profiles import resolve_agent_role
from self_training.generate_dataset import generate_datasets
from core.kernel import apply_patch  # 🧠 Kernel hook for patchable execution
from utils.nltk_setup import setup_nltk_data

# import nltk  # Removed unused import
import os

NLTK_DATA_DIR = setup_nltk_data()

# NLTK_DATA_DIR = os.path.abspath(
#    os.path.join(os.path.dirname(__file__), "../data/nltk_data")
# )
# os.makedirs(NLTK_DATA_DIR, exist_ok=True)
# nltk.data.path.clear()
# nltk.data.path.append(NLTK_DATA_DIR)

FSM_STATE = "IDLE"
console = Console()
task_queue = TaskQueue()
tick_delay = CFG.get("loop", {}).get("fsm_tick_delay", 0.5)
DATASET_PATH = "data/nlp_training_sets/auto_generated.jsonl"
LOG_CRASH_PATH = "data/logs/fsm_crash.log"


def auto_push():
    try:
        branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
        push_cmd = f"git push origin {branch}"
        result = os.system(push_cmd)
        if result == 0:
            console.log(f"[FSM] Git pushed to origin/{branch}.")
        else:
            console.log(f"[FSM] Git push failed with exit code: {result}")
    except Exception as e:
        console.log(f"[FSM] Git push error: {e}")


def fsm_loop():
    global FSM_STATE
    FSM_STATE = "RUNNING"
    tick_time = datetime.now(timezone.utc).isoformat()
    console.log(f"[FSM] Tick start @ {tick_time}")
    log_event("fsm", "tick_start", {"timestamp": tick_time})

    try:
        promote_old_tasks()
    except Exception as e:
        console.log(f"[FSM] Priority escalation failed: {e}")

    # --- Start bulletproof anti-fail loop ---
    idle_tick = False
    try:
        if task_queue.is_empty():
            idle_tick = True
            FSM_STATE = "IDLE"
            console.log("[FSM] No tasks in queue. Idling this tick.")
            log_event("fsm", "queue_idle", {"timestamp": tick_time}, status="idle")
        while not task_queue.is_empty():
            task = task_queue.get_next()
            if not task:
                FSM_STATE = "IDLE"
                break

            # Dynamic agent role assignment per task
            role = resolve_agent_role(task["type"])
            task["assigned_role"] = role
            console.log(f"[FSM] Task {task['type']} assigned to role: {role}")

            log_event("fsm", "task_start", {"task": task}, status="begin")

            try:
                if task["type"] == "patch_kernel":
                    file = task.get("target_file")
                    code = task.get("code")
                    reason = task.get("meta", {}).get("reason", "planner")
                    result = apply_patch(file, code, reason)
                    console.log(f"[FSM] Kernel patch applied to {file}: {result}")
                    log_event("fsm", "patch_kernel", {"task": task, "result": result})

                elif task["type"] == "code_patch":
                    file_path = task.get("file")
                    code = task.get("code")
                    if file_path and code:
                        success = apply_patch(file_path, code, reason="fsm_patch")
                        result = {"patched": success}
                    else:
                        raise ValueError("Missing 'file' or 'code' in patch task.")
                    console.log(f"[FSM] Code patch result: {result}")
                    log_event("fsm", "code_patch", {"task": task, "result": result})

                elif evaluate_task(task):
                    result = execute_tool(task)
                    console.log(f"[FSM] {task['type']} => {result}")
                    log_event("fsm", "task_exec", {"task": task, "result": result})

                else:
                    console.log(f"[FSM] Skipped: {task}")
                    log_event("fsm", "task_skipped", {"task": task}, status="skip")
                    continue

            except Exception as e:
                log_error(task, e)
                task_queue.retry(task)
                log_event("fsm", "task_error", {"task": task, "error": str(e)}, status="fail")
                tid = task.get("id")
                retries = task_queue.task_meta.get(tid, {}).get("retries", 0)
                if retries >= 2:
                    reprioritize(tid, "high")
                    console.log(f"[FSM] Reprioritized failing task {tid} to HIGH")

            # Self-mutation check
            try:
                scan_and_diff()
            except Exception as e:
                console.log(f"[FSM] Diff scan error: {e}")
                log_event("fsm", "diff_error", {"error": str(e)}, status="warn")

            time.sleep(tick_delay)

        if task_queue.is_empty():
            FSM_STATE = "IDLE"
            console.log("[FSM] Queue empty — invoking planner to enqueue new task.")
            try:
                enqueue_next()
            except Exception as e:
                console.log(f"[FSM] Planner enqueue failed: {e}")

            try:
                inject_watermark(origin="fsm_loop")
                console.log("[FSM] Memory watermark injected.")
            except Exception as e:
                console.log(f"[FSM] Watermark injection failed: {e}")

            try:
                generate_datasets(root_dir=".", output_file=DATASET_PATH)
                console.log("[FSM] Training dataset updated.")
                archive_path = archive_json_log(DATASET_PATH, prefix="dataset_dump")
                if archive_path:
                    auto_commit(archive_path, message="[autocommit] Dataset updated by FSM loop")

                if CFG.get("git", {}).get("auto_push", False):
                    auto_push()
            except Exception as e:
                console.log(f"[FSM] Dataset generation failed: {e}")
                with open(LOG_CRASH_PATH, "a") as logf:
                    logf.write(
                        f"{datetime.now(timezone.utc).isoformat()} :: Dataset Error: {str(e)}\n"
                    )
        else:
            FSM_STATE = "RUNNING"

    except Exception as main_fsm_ex:
        FSM_STATE = "ERROR"
        console.log(f"[FSM] General FSM loop error: {main_fsm_ex}")
        log_event("fsm", "loop_error", {"error": str(main_fsm_ex)}, status="fail")
        # Do not exit, just idle and retry on next tick

    FSM_STATE = "IDLE" if task_queue.is_empty() else "RUNNING"
    if idle_tick:
        console.log("[FSM] Idle: No tasks processed this tick.")
    else:
        console.log("[FSM] Queue cleared or work done.")
    log_event("fsm", "loop_complete", {}, status="idle" if idle_tick else "complete")


def run_schedule():
    try:
        run_daemon()
    except Exception as e:
        console.log(f"[FSM] Daemon launch failed: {e}")
        log_event("fsm", "daemon_error", {"error": str(e)}, status="fail")
    schedule.every(30).seconds.do(fsm_loop)
    console.log("[FSM] Scheduler engaged.")
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            console.log(f"[FSM] Scheduler error: {e}")
            log_event("fsm", "schedule_error", {"error": str(e)}, status="fail")
        time.sleep(1)


if __name__ == "__main__":
    # Optionally: try/catch bulk enqueue to avoid crash if sample tasks are malformed
    try:
        task_queue.enqueue_task({"type": "scrape"})
        task_queue.enqueue_task({"type": "signal_scan"})
        task_queue.enqueue_task({"type": "nlp", "text": "What is support and resistance?"})
        task_queue.enqueue_task(
            {
                "type": "code_patch",
                "file": "agent_core/tool_executor.py",
                "code": "def execute_tool(task):\n    return f'Patched exec of {task}'",
            }
        )
    except Exception as e:
        console.log(f"[FSM] Startup task enqueue failed: {e}")
        log_event("fsm", "startup_enqueue_error", {"error": str(e)}, status="fail")
    run_schedule()


# --- Dashboard & API Control Hooks ---


def get_fsm_status():
    """Return the current FSM state and task queue."""
    queue_length = sum(len(task_queue.task_queue[level]) for level in ["high", "normal", "low"])
    return {
        "state": FSM_STATE,
        "queue_length": queue_length,
        "queue": task_queue.dump(),
    }


def step_fsm():
    """Advance FSM by a single task (without full loop)."""
    global FSM_STATE
    FSM_STATE = "RUNNING"
    if task_queue.is_empty():
        FSM_STATE = "IDLE"
        return {"result": "queue_empty"}
    task = task_queue.get_next()
    if not task:
        FSM_STATE = "IDLE"
        return {"result": "no_task"}
    try:
        role = resolve_agent_role(task["type"])
        task["assigned_role"] = role
        if task["type"] == "patch_kernel":
            file = task.get("target_file")
            code = task.get("code")
            reason = task.get("meta", {}).get("reason", "planner")
            result = apply_patch(file, code, reason)
        elif task["type"] == "code_patch":
            file_path = task.get("file")
            code = task.get("code")
            if file_path and code:
                result = apply_patch(file_path, code, reason="fsm_patch")
            else:
                raise ValueError("Missing 'file' or 'code' in patch task.")
        elif evaluate_task(task):
            result = execute_tool(task)
        else:
            result = "skipped"
        FSM_STATE = "IDLE" if task_queue.is_empty() else "RUNNING"
        return {"result": result, "task": task}
    except Exception as e:
        log_error(task, e)
        FSM_STATE = "ERROR"
        return {"error": str(e), "task": task}


def reset_fsm():
    """Reset FSM state and clear the task queue."""
    global FSM_STATE, task_queue
    FSM_STATE = "IDLE"
    task_queue = TaskQueue()
    return {"reset": True}


def inject_task(task):
    """Inject a new task into the FSM's task queue."""
    try:
        task_queue.enqueue_task(task)
        return {"injected": True, "task": task}
    except Exception as e:
        return {"injected": False, "error": str(e)}
