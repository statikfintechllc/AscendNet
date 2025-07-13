# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.


import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
import uuid

from nlp_engine.diff_engine import diff_texts
from memory.vector_store.embedder import embed_text, package_embedding
from backend.globals import logger

SNAPSHOT_ROOT = Path("run/checkpoints/snapshots/")
SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def build_tree(directory):
    tree = {}
    for root, _, files in os.walk(directory):
        for f in files:
            full_path = Path(root) / f
            rel_path = str(full_path.relative_to(directory))
            try:
                tree[rel_path] = sha256_file(full_path)
            except Exception as e:
                logger.warning(f"[SNAPSHOT] Could not hash {rel_path}: {e}")
    return tree


def snapshot_file(file_path, label="manual", return_meta=False):
    file = Path(file_path)
    if not file.exists():
        logger.error(f"[SNAPSHOT] {file} does not exist.")
        return None

    content = file.read_text()
    hash_val = hashlib.sha256(content.encode()).hexdigest()
    time_stamp = datetime.utcnow().isoformat()
    lineage_id = str(uuid.uuid4())
    snap_name = f"{file.stem}_{label}_{time_stamp}.snap"
    snap_path = SNAPSHOT_ROOT / snap_name

    snapshot_data = {
        "path": str(file),
        "hash": hash_val,
        "timestamp": time_stamp,
        "label": label,
        "lineage_id": lineage_id,
        "code": content,
    }

    try:
        with open(snap_path, "w") as f:
            json.dump(snapshot_data, f, indent=2)

        logger.success(f"[SNAPSHOT] Saved snapshot: {snap_name}")

        # Also embed the snapshot into vector memory
        vector = embed_text(content)
        meta = {
            "origin": "snapshot_system",
            "file": str(file),
            "type": "code_snapshot",
            "label": label,
            "lineage_id": lineage_id,
            "timestamp": time_stamp,
        }
        package_embedding(text=content, vector=vector, meta=meta)

        return (snap_path, meta) if return_meta else snap_path
    except Exception as e:
        logger.error(f"[SNAPSHOT] Save failed: {e}")
        return None


def rollback(file_path, snapshot_file):
    try:
        with open(snapshot_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"[SNAPSHOT] Failed to read snapshot: {e}")
        return False

    old_code = data["code"]
    lineage_id = data.get("lineage_id", str(uuid.uuid4()))
    current_code = Path(file_path).read_text()

    if old_code == current_code:
        logger.info("[SNAPSHOT] File already matches snapshot.")
        return True

    diff = diff_texts(current_code, old_code)
    diff_text = "\n".join(diff["diff_lines"])
    vector = embed_text(diff_text)

    package_embedding(
        text=diff_text,
        vector=vector,
        meta={
            "origin": "snapshot_system",
            "file": file_path,
            "type": "rollback",
            "semantic_score": diff["semantic_score"],
            "embedding_delta": diff["embedding_delta"],
            "lineage_id": lineage_id,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

    Path(file_path).write_text(old_code)
    logger.warning(f"[SNAPSHOT] Rolled back: {file_path} → {snapshot_file}")
    return True


def verify_snapshot(file_path, snapshot_path):
    try:
        with open(snapshot_path, "r") as f:
            data = json.load(f)
        expected_hash = data["hash"]
        current = Path(file_path).read_text()
        current_hash = hashlib.sha256(current.encode()).hexdigest()
        return current_hash == expected_hash
    except Exception as e:
        logger.error(f"[SNAPSHOT] Verification failed: {e}")
        return False


# CLI usage
if __name__ == "__main__":
    src = "agent_core/tool_executor.py"
    result = snapshot_file(src, label="test", return_meta=True)
    if result and isinstance(result, tuple):
        snap, meta = result
        if snap and not verify_snapshot(src, snap):
            rollback(src, snap)
    else:
        logger.error("[SNAPSHOT] Snapshot creation failed; skipping verification/rollback.")
