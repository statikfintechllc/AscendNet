#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: kernel.py

from datetime import datetime
from pathlib import Path
from memory.vector_store.embedder import embed_text, package_embedding
from self_training.feedback_loop import inject_feedback
from nlp_engine.diff_engine import diff_texts
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("core")
from backend.globals import CFG
import shutil
import uuid
import subprocess

KERNEL_TAG = "kernel_writer"
SOURCE_ROOT = Path("GremlinGPT")
ROLLBACK_DIR = Path(CFG["paths"].get("checkpoints_dir", "run/checkpoints/")) / "snapshots"
ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[KERNEL] Failed to read {path}: {e}")
        return None


def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        logger.success(f"[KERNEL] Overwrote: {path}")
        return True
    except Exception as e:
        logger.error(f"[KERNEL] Failed to write {path}: {e}")
        return False


def backup_snapshot(path):
    try:
        filename = Path(path).name
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        snapshot_path = ROLLBACK_DIR / f"{filename}.{timestamp}.bak"
        shutil.copy(path, snapshot_path)
        logger.info(f"[KERNEL] Snapshot: {snapshot_path}")
        return snapshot_path
    except Exception as e:
        logger.warning(f"[KERNEL] Snapshot backup failed: {e}")
        return None


def test_patch_syntax(code):
    try:
        compile(code, "<string>", "exec")
        return True
    except SyntaxError as e:
        logger.error(f"[KERNEL] Patch syntax invalid: {e}")
        return False


def run_patch_test(temp_code):
    try:
        result = subprocess.run(
            ["python3", "-c", temp_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True,
        )
        if result.returncode != 0:
            logger.warning(f"[KERNEL] Patch test failed: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        logger.warning(f"[KERNEL] Exception during patch test: {e}")
        return False


def apply_patch(file_path, new_code, reason="mutation", safe_mode=True):
    original = read_file(file_path)
    if original is None or original == new_code:
        logger.info(f"[KERNEL] No change or failed read for: {file_path}")
        return False

    patch_testing_enabled = CFG["system"].get("enable_patch_test", True)

    if safe_mode and patch_testing_enabled:
        if not test_patch_syntax(new_code):
            return False
        if not run_patch_test(new_code):
            return False

    backup_snapshot(file_path)

    diff = diff_texts(original, new_code)
    diff_text = "\n".join(diff["diff_lines"])
    vector = embed_text(diff_text)
    patch_id = str(uuid.uuid4())

    package_embedding(
        text=diff_text,
        vector=vector,
        meta={
            "origin": KERNEL_TAG,
            "file": file_path,
            "type": "code_patch",
            "reason": reason,
            "patch_id": patch_id,
            "semantic_score": diff.get("semantic_score", 0),
            "embedding_delta": diff.get("embedding_delta", 0),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

    logger.debug(
        f"[KERNEL] Watermark embedded: {{'patch_id': '{patch_id}', 'file': '{file_path}'}}"
    )

    success = write_file(file_path, new_code)
    if success:
        inject_feedback()
        logger.success(f"[KERNEL] Patch applied: {patch_id}")
    else:
        logger.error(f"[KERNEL] Patch failed for: {file_path}")
    return success


def patch_from_text(target_file, injected_code, reason="human"):
    path = SOURCE_ROOT / target_file
    return apply_patch(str(path), injected_code, reason)


def patch_from_file(target_file, patch_file):
    try:
        with open(patch_file, "r") as f:
            new_code = f.read()
        return patch_from_text(target_file, new_code, reason=f"patch:{patch_file}")
    except Exception as e:
        logger.error(f"[KERNEL] Failed patch from file: {e}")
        return False


if __name__ == "__main__":
    test_file = "agent_core/tool_executor.py"
    test_patch = """
def execute_tool(task):
    return f"Mocked execution of {task}"
"""
    patch_from_text(test_file, test_patch.strip(), reason="example_patch")
