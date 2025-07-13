#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import json
from datetime import datetime
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("scraper")

WATERMARK = "source:GremlinGPT"
ORIGIN = "tws_scraper"

HEADERS = {
    "User-Agent": "GremlinGPT/5.0 (+https://gremlingpt.ai/bot)",
    "Accept": "text/html,python,javascript,java,markdown,jupyter,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


MODULE = "tws_scraper"
DEFAULT_SIMULATION = {
    "symbol": "SIMTWS",
    "price": 0.87,
    "volume": 1000000,
    "ema": 0.83,
    "vwap": 0.84,
    "timestamp": datetime.utcnow().isoformat(),
}


def locate_tws_files():
    """
    Scan for known TWS output, export, or log files dynamically.
    """
    try:
        home = Path.home()
        candidates = []

        search_patterns = [
            "**/tws*/logs/*.json",
            "**/tws*/data/*.csv",
            "**/IBKR*/export/*.json",
            "**/InteractiveBrokers*/output/*.log",
        ]

        for pattern in search_patterns:
            candidates += list(home.glob(pattern))

        # System-wide paths
        candidates += list(Path("/var/log").glob("**/ib*.log"))
        candidates += list(Path("/tmp").glob("tws*.json"))

        return [c for c in candidates if c.exists()]
    except Exception as e:
        logger.warning(f"[{MODULE}] File scan failed: {e}")
        return []


def try_parse_file(file_path):
    try:
        with open(file_path, "r") as f:
            raw = f.read()

            if file_path.suffix == ".json":
                data = json.loads(raw)
                return parse_tws_json(data)

            elif file_path.suffix == ".csv":
                lines = raw.splitlines()
                if len(lines) > 1:
                    values = lines[1].split(",")
                    return [
                        {
                            "symbol": values[0],
                            "price": float(values[1]),
                            "volume": int(values[2]),
                            "ema": float(values[3]),
                            "vwap": float(values[4]),
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ]
    except Exception as e:
        logger.warning(f"[{MODULE}] Could not parse {file_path}: {e}")
    return []


def parse_tws_json(data):
    try:
        if isinstance(data, dict):
            return [
                {
                    "symbol": data.get("symbol", "TWS"),
                    "price": data.get("price", 1.0),
                    "volume": data.get("volume", 100000),
                    "ema": data.get("ema", 1.0),
                    "vwap": data.get("vwap", 1.0),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ]
        elif isinstance(data, list) and data:
            return [parse_tws_json(data[0])[0]]
    except Exception as e:
        logger.warning(f"[{MODULE}] JSON parsing error: {e}")
    return []


def safe_scrape_tws():
    try:
        files = locate_tws_files()
        logger.debug(f"[{MODULE}] Found {len(files)} candidate files.")

        for file in files:
            result = try_parse_file(file)
            if result:
                logger.success(f"[{MODULE}] Parsed TWS data from: {file}")
                return result

        logger.info(f"[{MODULE}] No valid files found — using fallback simulation.")
        return [DEFAULT_SIMULATION]

    except Exception as e:
        logger.error(f"[{MODULE}] Scrape failed: {e}")
        return [DEFAULT_SIMULATION]


# CLI test mode
if __name__ == "__main__":
    print(safe_scrape_tws())
