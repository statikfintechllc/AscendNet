#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: utils/nltk_setup.py :: Module Integrity Directive
# Self-improving NLTK setup for GremlinGPT.
# This script is a component of the GremlinGPT system, under Alpha expansion.

import os
import nltk


def setup_nltk_data():
    """
    Ensures that the required NLTK data (such as 'punkt') is available by checking
    specified directories and downloading missing resources if necessary.

    Returns:
        str: The absolute path to the base NLTK data directory used.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "nltk_data"))
    fallback_dirs = ["/usr/local/share/nltk_data", base_dir]

    for path in fallback_dirs:
        if path not in nltk.data.path:
            nltk.data.path.append(path)

    try:
        nltk.data.find("tokenizers/punkt")
        nltk.download("punkt")
        nltk.download("punkt", download_dir=base_dir)
    except LookupError:
        nltk.download("punkt", download_dir=base_dir)
    except Exception as e:
        print(f"NLTK setup error: {e}")

    return base_dir
