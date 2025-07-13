# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import time
import threading
import requests
from datetime import datetime
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("self_mutation_watcher")
from pathlib import Path
import json
import uuid
import shutil
import os

from self_mutation_watcher.watcher import (
    scan_and_diff,
    generate_diff,
    WATCH_PATHS,
    load_snapshot,
)
from agents.planner_agent import enqueue_next
from memory.vector_store.embedder import embed_text, package_embedding
from nlp_engine.semantic_score import semantic_similarity
from backend.utils.git_ops import archive_json_log
from agent_core.task_queue import enqueue_task
from backend import globals as G
from backend.utils.git_ops import auto_commit

SCAN_INTERVAL_MIN = 5
NOTIFY_DASHBOARD = True
DASHBOARD_ENDPOINT = "http://localhost:5050/api/mutation/ping"
DATASET_OUT = Path("data/nlp_training_sets/live_mutations.jsonl")
DATASET_OUT.parent.mkdir(parents=True, exist_ok=True)


def notify_dashboard(message):
    try:
        if NOTIFY_DASHBOARD:
            requests.post(DASHBOARD_ENDPOINT, json={"message": message})
            logger.debug("[WATCHER] Dashboard notified.")
    except Exception as e:
        logger.warning(f"[WATCHER] Dashboard notification failed: {e}")


def rollback_file(path, backup_code, lineage_id, score):
    try:
        Path(path).write_text(backup_code)
        logger.warning(f"[WATCHER] Rolled back {path} due to unsafe semantic delta.")

        diff = generate_diff(backup_code, backup_code)
        vector = embed_text(diff)

        package_embedding(
            text=diff,
            vector=vector,
            meta={
                "origin": "rollback",
                "file": path,
                "type": "rollback_snapshot",
                "semantic_score": round(score, 4),
                "lineage_id": lineage_id,
                "timestamp": datetime.utcnow().isoformat(),
                "watermark": "source:GremlinGPT",
            },
        )

    except Exception as e:
        logger.error(f"[WATCHER] Rollback failed for {path}: {e}")


def log_to_dataset(original, mutated, score, file_path, lineage_id):
    entry = {
        "input": original,
        "output": mutated,
        "file": file_path,
        "semantic_score": round(score, 4),
        "lineage_id": lineage_id,
        "timestamp": datetime.utcnow().isoformat(),
        "watermark": "source:GremlinGPT",
    }
    try:
        with open(DATASET_OUT, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"[WATCHER] Failed to log mutation to dataset: {e}")


def archive_dataset(output_path):
    if not os.path.exists(output_path):
        return
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    archive_name = f"docs/dataset_dump_{timestamp}.jsonl"
    try:
        shutil.copyfile(output_path, archive_name)
        logger.info(f"[WATCHER] Dataset backup created → {archive_name}")
        return archive_name
    except Exception as e:
        logger.error(f"[WATCHER] Dataset backup failed: {e}")
        return None


def mutation_loop():
    logger.info("[WATCHER] Mutation Daemon Started.")
    while True:
        try:
            scan_and_diff()
        except Exception as e:
            logger.error(f"[WATCHER] scan_and_diff() failed: {e}")
        try:
            analyze_mutation_diff()
        except Exception as e:
            logger.error(f"[WATCHER] analyze_mutation_diff() failed: {e}")
        try:
            notify_dashboard("Self-mutation scan complete.")
        except Exception as e:
            logger.error(f"[WATCHER] notify_dashboard() failed: {e}")
        try:
            enqueue_next()
            logger.info(
                f"[WATCHER] Planner task injected post-mutation at {datetime.utcnow().isoformat()}"
            )
        except Exception as e:
            logger.error(f"[WATCHER] enqueue_next() failed: {e}")

        try:
            if DATASET_OUT.exists():
                backup = archive_json_log(str(DATASET_OUT), prefix="dataset_dump")
                auto_commit(backup)
                if G.CFG.get("git", {}).get("auto_push", False):
                    auto_push()
        except Exception as e:
            logger.error(f"[WATCHER] Dataset backup or git push failed: {e}")
        time.sleep(SCAN_INTERVAL_MIN * 60)


def auto_push():
    try:
        branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
        result = os.system(f"git push origin {branch}")
        if result == 0:
            logger.info(f"[WATCHER] Git pushed to origin/{branch}.")
        else:
            logger.warning(f"[WATCHER] Git push failed with exit code: {result}")
    except Exception as e:
        logger.warning(f"[WATCHER] Git push error: {e}")


def analyze_mutation_diff():
    for path in WATCH_PATHS:
        try:
            with open(path, "r") as f:
                current = f.read()
            previous = load_snapshot(path)

            if current != previous:
                diff = generate_diff(previous, current)
                score = semantic_similarity(previous, current)
                lineage_id = str(uuid.uuid4())

                logger.info(f"[WATCHER] Semantic similarity for {path}: {round(score, 4)}")

                vector = embed_text(diff)
                package_embedding(
                    text=diff,
                    vector=vector,
                    meta={
                        "origin": "mutation_daemon",
                        "type": "code_diff",
                        "file": path,
                        "semantic_score": round(score, 4),
                        "lineage_id": lineage_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "watermark": "source:GremlinGPT",
                    },
                )

                log_to_dataset(previous, current, score, path, lineage_id)

                if score < 0.6:
                    enqueue_task(
                        {
                            "type": "self_train",
                            "meta": {
                                "reason": f"semantic_delta::{path}",
                                "lineage_id": lineage_id,
                                "triggered_by": "mutation_daemon",
                            },
                        }
                    )
                    logger.warning(
                        f"[WATCHER] mutation_event=significant | "
                        f"action=self_train | file={path} | score={round(score, 4)}"
                    )

                if score < 0.4:
                    rollback_file(path, previous, lineage_id, score)

        except Exception as e:
            logger.error(f"[WATCHER] Semantic diff scoring failed for {path}: {e}")


def run_daemon():
    try:
        t = threading.Thread(target=mutation_loop, daemon=True)
        t.start()
        logger.info("[WATCHER] Mutation Daemon thread started.")
    except Exception as e:
        logger.error(f"[WATCHER] Failed to start mutation daemon thread: {e}")
