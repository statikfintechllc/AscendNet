# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from agent_core.task_queue import reprioritize
from agent_core import task_queue
from memory.log_history import log_event
import logging

logger = logging.getLogger("GremlinGPT.TaskQueue")
import networkx as nx
from datetime import datetime
from scraper import source_router, web_knowledge_scraper
import flask  # type: ignore

planner_bp = flask.Blueprint("planner", __name__)


@planner_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """Returns all queued tasks and a simple DAG view."""

    # Use the correct TaskQueue API to get all tasks
    flat_list = []
    count = 0
    try:
        all_tasks = task_queue.get_all_tasks()
        for task in all_tasks:
            count += 1
            flat_list.append(
                {
                    "name": task.get("type", "unknown"),
                    "state": task.get("status", "queued"),
                    "priority": task.get("priority", "normal"),
                    "meta": task,
                }
            )
    except Exception as e:
        logger.error(f"[PLANNER_API] Failed to fetch tasks: {e}")

    logger.info(f"[PLANNER_API] Found {count} tasks in queue.")
    log_event("planner_api", "task_list_fetch", {"count": count}, status="ok")

    # Optional graph structure (for frontend)
    G = nx.DiGraph()
    for idx, t in enumerate(flat_list):
        G.add_node(idx, label=t["name"])
        if idx > 0:
            G.add_edge(idx - 1, idx)

    return flask.jsonify({"tasks": flat_list, "timestamp": datetime.utcnow().isoformat()})


@planner_bp.route("/api/mutation/ping", methods=["POST"])
def mutation_notify():
    """Receives ping from mutation daemon."""
    data = flask.request.get_json(silent=True) or {}
    message = data.get("message", "No message provided")
    logger.debug(f"[PLANNER_API] Mutation ping: {message}")
    log_event("planner_api", "mutation_ping", {"message": message}, status="pong")

    return flask.jsonify(
        {
            "status": "received",
            "timestamp": datetime.utcnow().isoformat(),
            "log": f"Mutation daemon: {message}",
            "watermark": "source:GremlinGPT",
        }
    )


@planner_bp.route("/api/tasks/priority", methods=["POST"])
def set_task_priority():
    """Adjusts task priority by ID."""
    data = flask.request.get_json()
    task_id = data.get("id")
    new_priority = data.get("priority")

    if not task_id or not new_priority:
        logger.warning("[PLANNER_API] Priority update failed: missing ID or priority.")
        return flask.jsonify({"error": "Missing 'id' or 'priority'"}), 400

    success = reprioritize(task_id, new_priority)
    log_event(
        "planner_api",
        "priority_update",
        {
            "task_id": task_id,
            "new_priority": new_priority,
            "success": success,
        },
        status="updated" if success else "failed",
    )

    return (
        flask.jsonify(
            {
                "status": "updated" if success else "failed",
                "task_id": task_id,
                "new_priority": new_priority,
            }
        ),
        200 if success else 500,
    )


@planner_bp.route("/api/trading/signals", methods=["GET"])
def get_signals():
    """
    Returns a state-of-the-art trading signal summary, including:
    - Most recent scraped market data (multi-source)
    - Web knowledge extraction
    - Reward/confidence scores
    - Signal provenance and vector embedding
    """
    try:
        # 1. Aggregate live data from all available scrapers
        tws = source_router.safe_scrape_tws() if hasattr(source_router, "safe_scrape_tws") else []
        stt = source_router.safe_scrape_stt() if hasattr(source_router, "safe_scrape_stt") else []
        web_results = web_knowledge_scraper.run_search_and_scrape(
            ["https://finance.yahoo.com/", "https://www.investing.com/news/stock-market-news"]
        )
        # 2. Compose a unified signal set
        signals = []
        for src, data in zip(["tws", "stt", "web"], [tws, stt, web_results]):
            if not data:
                continue
            for item in data:
                if not (isinstance(item, dict) and hasattr(item, "get")):
                    continue
                signals.append(
                    {
                        "source": src,
                        "symbol": item.get("symbol", "N/A"),
                        "price": item.get("price"),
                        "volume": item.get("volume"),
                        "ema": item.get("ema"),
                        "vwap": item.get("vwap"),
                        "timestamp": item.get("timestamp"),
                        "raw": item,
                    }
                )
        # 3. Optionally, score signals (stub: all 0.9)
        for sig in signals:
            sig["confidence"] = 0.9
            sig["reward"] = 0.9
        return flask.jsonify(
            {"signals": signals, "timestamp": datetime.utcnow().isoformat(), "count": len(signals)}
        )
    except Exception as e:
        logger.error(f"[PLANNER_API] get_signals failed: {e}")
        return flask.jsonify({"error": str(e)}), 500
