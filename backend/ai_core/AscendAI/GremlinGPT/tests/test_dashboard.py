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

# tests/test_dashboard.py

import requests


def test_backend_api():
    res = requests.get("http://localhost:5050/")
    assert res.status_code == 200
    assert "GremlinGPT" in res.text or "Backend" in res.text


def test_chat_handler():
    res = requests.post(
        "http://localhost:5050/api/chat", json={"text": "scan penny stocks"}
    )
    assert res.status_code == 200
    assert "response" in res.json()
