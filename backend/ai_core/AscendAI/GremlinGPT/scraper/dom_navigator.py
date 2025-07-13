# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from bs4 import BeautifulSoup
from loguru import logger
from collections import Counter

WATERMARK = "source:GremlinGPT"
ORIGIN = "dom_navigator"


def extract_dom_structure(html):
    """
    Extracts structured DOM metadata, links, semantic blocks, and top text from HTML.
    Enriches memory and NLP context for semantic tagging and search.
    """
    soup = BeautifulSoup(html, "lxml")
    body = soup.body

    if not body:
        logger.warning("[DOM NAVIGATOR] No <body> tag found in HTML.")
        return {
            "links": [],
            "text": "",
            "tags": {},
            "nodes": [],
            "watermark": WATERMARK,
        }

    # Extract anchor href links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Count tag types (structure profiling)
    tag_counts = Counter(tag.name for tag in soup.find_all())

    # Extract key semantic sections
    semantic_tags = ["header", "nav", "main", "section", "article", "footer"]
    nodes = []
    for tag in semantic_tags:
        for elem in soup.find_all(tag):
            content = elem.get_text(strip=True)
            if len(content) > 20:
                nodes.append(
                    {
                        "type": tag,
                        "text": content[:500],
                        "length": len(content),
                    }
                )

    # Full-body plaintext with safety limits
    full_text = soup.get_text(separator="\n", strip=True)

    result = {
        "links": links,
        "text": full_text[:2000],
        "tags": dict(tag_counts),
        "nodes": nodes,
        "watermark": WATERMARK,
    }

    logger.info(
        f"[DOM NAVIGATOR] Parsed HTML → {len(links)} links, "
        f"{len(nodes)} semantic nodes, {len(full_text)} chars of text."
    )

    return result


# CLI Debug
if __name__ == "__main__":
    try:
        with open("example_page.html", "r") as f:
            html = f.read()
        summary = extract_dom_structure(html)
        print(summary)
    except Exception as e:
        logger.error(f"[DOM NAVIGATOR] Debug run failed: {e}")
