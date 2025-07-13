# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

"""
GremlinGPT v1.0.3 :: Dataset Generation Heart Module
This module provides the main dataset generation function for self-training, FSM, and trainer.
It is fully integrated with watermarking, tagging, tokenizing, deduplication, memory, feedback, and logging subsystems.
"""

import os
import json
import time
import uuid
import hashlib
import schedule
from datetime import datetime
from pathlib import Path
from agent_core.task_queue import enqueue_task
from self_training.feedback_loop import inject_feedback
from nlp_engine.tokenizer import tokenize
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from memory.log_history import log_event

WATERMARK = "source:GremlinGPT"
KEYWORDS = ["FAIL", "LOW_CONF", "INVALID", "delta", "error", "retry", "timeout", "null"]
ROOT_DIR = os.path.expanduser("data/logs")
OUTPUT_FILE = os.path.expanduser("data/nlp_training_sets/auto_generated.jsonl")
LINEAGE_TAG = str(uuid.uuid4())
CONFIDENCE_THRESHOLD = 0.4  # Reserved for future use


def hash_entry(entry):
    """Hash entry for deduplication."""
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()


def generate_datasets(
    root_dir=ROOT_DIR, output_file=OUTPUT_FILE, min_len=15, max_len=1000, dedup=True
):
    """
    Main entry point for dataset generation. Scans logs, extracts, tags, tokenizes, embeds, deduplicates, and stores entries.
    Args:
        root_dir: Directory to scan for log files.
        output_file: Output path for the generated dataset.
        min_len: Minimum length of a valid entry.
        max_len: Maximum length of a valid entry.
        dedup: Whether to deduplicate entries by hash.
    Returns:
        List of dataset entries.
    """
    entries = []
    hashes = set()
    root = Path(root_dir)
    now = datetime.utcnow().isoformat()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if any(keyword in line.upper() for keyword in KEYWORDS):
                    cleaned = line.strip()
                    if min_len < len(cleaned) < max_len:
                        tokens = tokenize(cleaned)
                        meta = {
                            "watermark": WATERMARK,
                            "length": len(cleaned),
                            "lineage_id": LINEAGE_TAG,
                            "type": path.suffix or "text",
                            "token_count": len(tokens),
                            "source_file": str(path),
                            "line": i + 1,
                            "timestamp": now,
                        }
                        entry = {
                            "input": cleaned,
                            "output": "TBD",
                            "tokens": tokens,
                            "meta": meta,
                        }
                        h = hash_entry(entry) if dedup else None
                        if not dedup or h not in hashes:
                            entries.append(entry)
                            if dedup:
                                hashes.add(h)
        except Exception as e:
            log_event(
                "dataset", "extract_error", {"file": str(path), "error": str(e)}, status="fail"
            )

    # Optionally deduplicate with previous dataset
    if dedup and os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                for line in f:
                    try:
                        prev = json.loads(line)
                        h = hash_entry(prev)
                        hashes.add(h)
                    except Exception:
                        continue
        except Exception as e:
            log_event(
                "dataset", "dedup_error", {"file": output_file, "error": str(e)}, status="fail"
            )

    if entries:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        log_event(
            "dataset", "generated", {"count": len(entries), "output": output_file}, status="success"
        )
        print(f"[DATASET] Extracted {len(entries)} entries → {output_file}")
        # Embed and store in vector memory
        for entry in entries:
            vector = embed_text(entry["input"])
            package_embedding(
                text=entry["input"],
                vector=vector,
                meta={**entry["meta"], "dataset_hash": hash_entry(entry)},
            )
        # Queue self-training with lineage context
        enqueue_task(
            {
                "type": "self_train",
                "meta": {
                    "reason": "auto_generated_dataset",
                    "lineage_id": LINEAGE_TAG,
                    "source": "dataset_scheduler",
                },
            }
        )
        inject_feedback()
        inject_watermark(origin="generate_datasets")
        print("[DATASET] Self-train task injected.")
    else:
        print("[DATASET] No matching entries found.")
        log_event("dataset", "empty", {"root": root_dir}, status="warn")
    return entries


def schedule_extraction(interval_min=10):
    schedule.every(interval_min).minutes.do(generate_datasets)
    print(f"[SCHEDULER] Training extraction scheduled every {interval_min} min.")
    while True:
        schedule.run_pending()
        time.sleep(30)


def extract_training_data(*args, **kwargs):
    """
    Legacy alias for backward compatibility. Calls generate_datasets.
    """
    return generate_datasets(*args, **kwargs)


if __name__ == "__main__":
    schedule_extraction()
