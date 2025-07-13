# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from scraper.dom_navigator import extract_dom_structure
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from loguru import logger
from datetime import datetime

WATERMARK = "source:GremlinGPT"
ORIGIN = "page_simulator"


def store_scrape_to_memory(url, html):
    """
    Extracts DOM metadata from scraped HTML and stores a vectorized summary in memory.
    """
    try:
        structure = extract_dom_structure(html)
        summary_text = f"[{url}]\n{structure.get('text', '')}"
        vector = embed_text(summary_text)

        package_embedding(
            text=summary_text,
            vector=vector,
            meta={
                "origin": ORIGIN,
                "type": "scrape_snapshot",
                "url": url,
                "timestamp": datetime.utcnow().isoformat(),
                "watermark": WATERMARK,
            },
        )

        inject_watermark(origin=ORIGIN)
        logger.info(f"[{ORIGIN.upper()}] Stored scrape vector for: {url}")

    except Exception as e:
        logger.error(f"[{ORIGIN.upper()}] Failed to store scrape for {url}: {e}")
