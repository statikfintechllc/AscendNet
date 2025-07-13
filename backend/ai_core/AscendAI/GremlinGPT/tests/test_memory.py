# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must test:
#   - That everything integrates seamlessly into the architecture defined in the full outline
#   - Operates autonomously and communicate cross-module via defined protocols
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired logic, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# tests/test_memory.py

from memory.vector_store.embedder import embed_text, package_embedding


def test_embedding_store():
    text = "GremlinGPT stores vector embeddings locally."
    vec = embed_text(text)
    assert len(vec) > 0

    embed = package_embedding(text, vec, {"test_case": True})
    assert "embedding" in embed and "meta" in embed
