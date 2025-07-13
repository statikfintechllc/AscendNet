#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from flask import jsonify
from memory.vector_store.embedder import get_all_embeddings
from backend.globals import MEM
from memory.log_history import log_event
import logging

logger = logging.getLogger("GremlinGPT.TaskQueue")
from datetime import datetime, UTC


def graph():
    """
    Returns memory graph data as JSON.
    Includes vector metadata and telemetry for frontend graph rendering.
    """
    try:
        limit = MEM["search"].get("default_top_k", 10)
        threshold = MEM["search"].get("similarity_threshold", 0.75)
        dimension = MEM.get("embedding_dim", 384)

        records = get_all_embeddings(limit=limit)

        response = {
            "count": len(records),
            "results": records,
            "meta": {
                "limit": limit,
                "embedding_dim": dimension,
                "similarity_threshold": threshold,
                "timestamp": datetime.now(UTC).isoformat(),
                "source": "memory_api.graph",
                "watermark": "source:GremlinGPT",
            },
        }

        log_event("memory_api", "graph_fetch", {"count": len(records)}, status="success")
        logger.info(f"[MEMORY_API] Served {len(records)} vector nodes.")

        return jsonify(response)

    except (KeyError, TypeError) as e:
        logger.error(f"[MEMORY_API] Graph load failure: {e}")
        log_event("memory_api", "graph_error", {"error": str(e)}, status="failure")
        return jsonify({"error": "Failed to load memory graph", "details": str(e)}), 500
    except Exception as e:
        logger.error(f"[MEMORY_API] Unexpected error: {e}")
        log_event("memory_api", "graph_error", {"error": str(e)}, status="failure")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
