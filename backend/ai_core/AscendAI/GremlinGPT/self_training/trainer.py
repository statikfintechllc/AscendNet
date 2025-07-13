#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import time
import json
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.globals import CFG
from self_training.generate_dataset import extract_training_data
from self_training.mutation_engine import mutate_dataset
from memory.vector_store.embedder import package_embedding, embed_text, inject_watermark
from mini_attention import MiniMultiHeadAttention
from datetime import datetime
import numpy as np
import os
import sys

LOG_DIR = CFG["paths"].get("data_dir", "data/") + "logs/"
OUTPUT_PATH = (
    CFG["paths"].get("data_dir", "data/") + "nlp_training_sets/mutated_dataset.json"
)
WATERMARK = "source:GremlinGPT"
TAG = "trainer_module"

attention = MiniMultiHeadAttention(embed_dim=64, num_heads=4)


class LogEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            logger.info("[TRAINER] Log updated. Triggering retraining...")
            trigger_retrain()


def trigger_retrain():
    try:
        # Extract logs and mutate into new dataset
        if not os.path.exists(LOG_DIR) or not os.listdir(LOG_DIR):
            logger.warning(
                f"[TRAINER] No logs found in {LOG_DIR}. Idling, awaiting logs..."
            )
            return

        raw = extract_training_data(LOG_DIR)
        if not raw:
            logger.info(
                f"[TRAINER] No extractable training data found. Idling, awaiting data..."
            )
            return

        mutated = mutate_dataset(raw)

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(mutated, f, indent=2)
        logger.success(f"[TRAINER] Dataset mutation complete → {OUTPUT_PATH}")

        # === Simulate attention training behavior ===
        dummy_input = np.random.rand(8, 64)
        out, weights = attention.forward(dummy_input)

        embed_text_summary = f"Trainer activated attention w/ {attention.num_heads} heads | out shape: {out.shape}"
        vector = embed_text(embed_text_summary)

        package_embedding(
            text=embed_text_summary,
            vector=vector,
            meta={
                "origin": TAG,
                "event": "trainer::attention_trace",
                "timestamp": datetime.utcnow().isoformat(),
                "shape": str(out.shape),
                "watermark": WATERMARK,
            },
        )

        # Inject post-train memory watermark
        inject_watermark(origin="trainer::retrain")
    except Exception as e:
        logger.error(f"[TRAINER] Exception during retrain: {e}")
        # Do not crash—just log and continue to next trigger


def watch_logs():
    """Watch log directory for .log file updates and trigger retrain on modification.
    Robust to empty or missing log folder; will continue watching and not exit on error.
    """
    while True:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            observer = Observer()
            observer.schedule(LogEventHandler(), path=LOG_DIR, recursive=False)
            observer.start()
            logger.info(f"[TRAINER] Watching logs in {LOG_DIR} for changes.")
            while True:
                time.sleep(1)
        except Exception as e:
            logger.error(
                f"[TRAINER] Log watcher encountered error: {e}. Retrying in 5 seconds..."
            )
            time.sleep(5)  # Wait before retrying watcher setup
        finally:
            try:
                observer.stop()
                observer.join()
            except Exception:
                pass  # Observer may not be started yet; ignore


def idle_loop():
    """Bulletproof idle loop for when there are no logs to train on."""
    logger.info("[TRAINER] No logs to train on. Idling and awaiting new logs...")
    while True:
        try:
            if os.path.exists(LOG_DIR) and os.listdir(LOG_DIR):
                logger.info("[TRAINER] Detected new logs. Starting watcher.")
                watch_logs()
                break  # watcher will take over
            time.sleep(10)
        except Exception as e:
            logger.error(f"[TRAINER] Idle loop error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    logger.info("[TRAINER] Launching trainer module.")
    try:
        if os.path.exists(LOG_DIR) and os.listdir(LOG_DIR):
            watch_logs()
        else:
            idle_loop()
    except KeyboardInterrupt:
        logger.warning("[TRAINER] Keyboard interrupt received. Exiting trainer.")
        sys.exit(0)
    except Exception as main_e:
        logger.error(f"[TRAINER] Top-level exception: {main_e}")
        idle_loop()
