#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from difflib import unified_diff
import numpy as np
from typing import Dict
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("nlp_engine")

from nlp_engine.semantic_score import semantic_similarity
from nlp_engine.transformer_core import encode

ENGINE_NAME = "diff_engine"


def diff_texts(old: str, new: str, debug: bool = False) -> Dict:
    """
    Computes unified diff, semantic similarity, and embedding delta
    between two strings. Used in mutation safety logic.

    Args:
        old (str): The original text.
        new (str): The new text to compare against the original.
        debug (bool, optional): If True, logs warnings on embedding delta failures. Defaults to False.

    Returns:
        Dict: A dictionary containing diff lines, semantic score, and embedding delta.
    """
    if not old and not new:
        return {
            "diff_lines": [],
            "semantic_score": 1.0,
            "embedding_delta": 0.0,
        }

    lines = list(
        unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile="old",
            tofile="new",
        )
    )
    if old or new:
        sem_score = semantic_similarity(old, new)
        try:
            vec_old = encode(old)
            vec_new = encode(new)
            if vec_old.shape != vec_new.shape:
                if debug:
                    logger.warning(
                        f"[{ENGINE_NAME}] Embedding shapes differ: {vec_old.shape} vs {vec_new.shape}"
                    )
            delta = float(np.linalg.norm(vec_old - vec_new))
        except Exception as e:
            delta = 0.0
            logger.debug(f"[{ENGINE_NAME}] Embedding delta failed: {e}")
            if debug:
                logger.warning(f"[{ENGINE_NAME}] Embedding delta failed: {e}")
    else:
        sem_score = 1.0
        delta = 0.0

    return {
        "diff_lines": lines,
        "semantic_score": round(sem_score, 4),
        "embedding_delta": round(delta, 4),
    }


def diff_files(file_a: str, file_b: str) -> Dict:
    """
    Loads two files and returns structured diff result.
    Handles encoding errors safely.
    """
    try:
        with open(file_a, "r", encoding="utf-8") as f1:
            content_a = f1.read()
        with open(file_b, "r", encoding="utf-8") as f2:
            content_b = f2.read()
        return diff_texts(content_a, content_b)
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Could not diff files: {e}")
        return {
            "diff_lines": [f"# ERROR: Could not diff files: {e}"],
            "semantic_score": 0.0,
            "embedding_delta": 0.0,
        }
