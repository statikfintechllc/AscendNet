# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import json
from datetime import datetime
from pathlib import Path
import numpy as np
from backend.globals import logger
from nlp_engine.semantic_score import semantic_similarity
from nlp_engine.diff_engine import diff_texts
from agent_core.fsm import inject_task  # For feedback loop

LOG_HISTORY_DIR = Path("data/logs/")
REWARD_LOG = LOG_HISTORY_DIR / "rewards.jsonl"
REWARD_LOG.parent.mkdir(parents=True, exist_ok=True)


def evaluate_result(task_type, output_text, reference_text=None):
    """
    Assign reward/confidence based on output:
    - Uses semantic similarity and vector norms
    - Heuristic fallbacks for basic scoring
    """

    reward = 0.0
    confidence = 0.0
    reason = ""

    if reference_text:
        similarity = semantic_similarity(output_text, reference_text)
        delta = np.linalg.norm(np.array([similarity]) - np.array([1.0]))
        confidence = max(0.0, 1.0 - delta)
        reward = similarity
        reason = "semantic_match"
    else:
        if "error" in output_text.lower():
            reward = -0.3
            confidence = 0.2
            reason = "error_detected"
        elif len(output_text.strip()) > 40:
            reward = 0.6
            confidence = 0.7
            reason = "length_heuristic"
        else:
            reward = 0.3
            confidence = 0.5
            reason = "basic_pass"

    return {
        "task": task_type,
        "confidence": round(confidence, 4),
        "reward": round(reward, 4),
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "output": output_text[:300],
    }


def evaluate_with_diff(task_type, output_text, reference_text=None, debug=False, feedback_loop=True):
    """
    Evaluate result with diff analysis:
    - Computes reward/confidence as before
    - Adds diff lines, semantic score, embedding delta if reference_text is provided
    - Returns a richer record for logging and analytics
    - Optionally triggers a feedback event for self-training
    """
    base = evaluate_result(task_type, output_text, reference_text)
    diff_info = None
    if reference_text:
        diff_info = diff_texts(reference_text, output_text, debug=debug)
        # Advanced heuristics: penalize large embedding delta or low semantic score
        if diff_info["embedding_delta"] > 2.0:
            base["reward"] -= 0.2
            base["reason"] += "+embedding_penalty"
        if diff_info["semantic_score"] < 0.5:
            base["reward"] -= 0.2
            base["reason"] += "+semantic_penalty"
        base["semantic_score"] = diff_info["semantic_score"]
        base["embedding_delta"] = diff_info["embedding_delta"]
        base["diff_lines"] = diff_info["diff_lines"]
        # Feedback loop: inject feedback for self-training
        if feedback_loop:
            inject_task({
                "type": "reward_feedback",
                "task": task_type,
                "output": output_text,
                "reference": reference_text,
                "reward": base["reward"],
                "semantic_score": diff_info["semantic_score"],
                "embedding_delta": diff_info["embedding_delta"],
                "timestamp": base["timestamp"],
            })
    return base


def log_reward(record):
    try:
        with open(REWARD_LOG, "a") as f:
            f.write(json.dumps(record) + "\n")
        logger.info(f"[REWARD] Logged: {record['task']} [{record['reason']}]" + (f" | Δ={record.get('embedding_delta', None)}" if 'embedding_delta' in record else ""))
    except Exception as e:
        logger.error(f"[REWARD] Failed to log reward: {e}")


def top_rewarded_tasks(n=5):
    records = []
    try:
        with open(REWARD_LOG, "r") as f:
            for line in f:
                rec = json.loads(line.strip())
                records.append(rec)
    except FileNotFoundError:
        return []

    return sorted(records, key=lambda r: r["reward"], reverse=True)[:n]


def get_reward_feed(n=20):
    """
    Returns the latest n reward+diff records for dashboard/feed usage.
    """
    records = []
    try:
        with open(REWARD_LOG, "r") as f:
            for line in f:
                rec = json.loads(line.strip())
                records.append(rec)
    except FileNotFoundError:
        return []
    return records[-n:][::-1]  # Most recent first


if __name__ == "__main__":
    out = "Successfully scraped 5 stock tickers from Webull."
    ref = "Extract a list of tickers from a market page."
    rec = evaluate_with_diff("scrape", out, ref, feedback_loop=True)
    log_reward(rec)
    print(top_rewarded_tasks())
    print("--- Dashboard Feed Example ---")
    for item in get_reward_feed(3):
        print(item)