#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("backend")

from backend.api import chat_handler, memory_api, scraping_api, planner


def register_routes(app):
    logger.info("[ROUTER] Verifying and backing up API routes...")

    routes = [
        ("/api/chat", chat_handler.chat, ["POST"]),
        ("/api/memory/graph", memory_api.graph, ["GET"]),
        ("/api/scrape", scraping_api.scrape_url, ["POST"]),
        ("/api/agent/tasks", planner.list_tasks, ["GET"]),
        ("/api/trading/signals", planner.get_signals, ["GET"]),
        ("/api/tasks/priority", planner.set_task_priority, ["POST"]),
    ]

    # Build a set of existing route paths for efficient lookup
    existing_paths = {rule.rule for rule in app.url_map.iter_rules()}

    for path, handler, methods in routes:
        # Check if the route already exists (likely via blueprint)
        if path in existing_paths:
            logger.info(f"[ROUTER] Verified: {path} is already registered (likely via blueprint).")
            # Optionally, backup/verify handler identity
            existing_rule = next(
                (rule for rule in app.url_map.iter_rules() if rule.rule == path), None
            )
            if existing_rule and hasattr(existing_rule, "endpoint"):
                logger.debug(f"[ROUTER] Existing endpoint for {path}: {existing_rule.endpoint}")
        else:
            try:
                endpoint_name = f"{handler.__module__}.{handler.__name__}"
                app.add_url_rule(path, view_func=handler, methods=methods, endpoint=endpoint_name)
                app.add_url_rule(path, view_func=handler, methods=methods)
                logger.success(f"[ROUTER] Route registered as backup: {path} -> {handler.__name__}")
            except Exception as e:
                logger.error(f"[ROUTER] Backup registration failed for {path}: {e}")
