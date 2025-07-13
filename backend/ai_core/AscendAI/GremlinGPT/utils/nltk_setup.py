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
    Only uses the project's data/nltk_data directory.

    Returns:
        str: The absolute path to the base NLTK data directory used.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "nltk_data"))

    # Ensure the directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Clear default NLTK data paths and set only our project directory
    nltk.data.path.clear()
    nltk.data.path.append(base_dir)

    # Set NLTK_DATA environment variable to prevent downloads to $HOME
    os.environ["NLTK_DATA"] = base_dir

    # Download required NLTK resources
    required_resources = [("tokenizers/punkt", "punkt"), ("tokenizers/punkt_tab", "punkt_tab")]

    for resource_path, resource_name in required_resources:
        try:
            nltk.data.find(resource_path)
            print(f"[NLTK] Found {resource_name} in {base_dir}")
        except LookupError:
            print(f"[NLTK] Downloading {resource_name} to {base_dir}")
            try:
                nltk.download(resource_name, download_dir=base_dir, quiet=True)
            except Exception as e:
                print(f"[NLTK] Failed to download {resource_name}: {e}")
        except Exception as e:
            print(f"[NLTK] Error checking {resource_name}: {e}")

    return base_dir
