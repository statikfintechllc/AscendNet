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
import platform
from datetime import datetime
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("scraper")

MODULE = "stt_scraper"
DEFAULT_FALLBACK = {
    "symbol": "STTLIVE",
    "price": 1.23,
    "volume": 1500000,
    "ema": 1.18,
    "vwap": 1.21,
    "timestamp": datetime.utcnow().isoformat(),
}


def locate_stt_paths():
    guesses = []
    system = platform.system()
    logger.debug(f"[{MODULE}] OS detected: {system}")

    try:
        home = Path.home()
        if system == "Windows":
            guesses += list(home.glob("**/AppData/Local/StocksToTrade*/logs/*.json"))
        else:
            guesses += list(home.glob("**/StocksToTrade*/logs/*.json"))

        guesses += list(home.glob("**/StocksToTrade*/data/*.csv"))
        guesses += list(Path("/tmp").glob("**/stt*.json"))
        guesses += list(Path("/var/log").glob("**/stt*.log"))

    except Exception as e:
        logger.warning(f"[{MODULE}] Path scan failed: {e}")

    return [p for p in guesses if p.exists()]


def try_parse_file(file_path):
    try:
        with open(file_path, "r") as f:
            raw = f.read()

            if file_path.suffix == ".json":
                data = json.loads(raw)
                return parse_stt_data(data)

            elif file_path.suffix == ".csv":
                lines = raw.splitlines()
                if not lines or len(lines) < 2:
                    return []
                latest = lines[1].split(",")
                return [
                    {
                        "symbol": latest[0],
                        "price": float(latest[1]),
                        "volume": int(latest[2]),
                        "ema": float(latest[3]),
                        "vwap": float(latest[4]),
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                ]
    except Exception as e:
        logger.warning(f"[{MODULE}] Failed to parse {file_path}: {e}")
    return []


def parse_stt_data(data):
    try:
        if isinstance(data, dict):
            return [
                {
                    "symbol": data.get("symbol", "STT"),
                    "price": data.get("price", 1.0),
                    "volume": data.get("volume", 100000),
                    "ema": data.get("ema", 1.0),
                    "vwap": data.get("vwap", 1.0),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ]
        elif isinstance(data, list) and data:
            return [parse_stt_data(data[0])[0]]
    except Exception as e:
        logger.warning(f"[{MODULE}] Error parsing data blob: {e}")
    return []


def safe_scrape_stt():
    try:
        candidates = locate_stt_paths()
        logger.debug(f"[{MODULE}] Candidate files: {len(candidates)}")

        for file in candidates:
            result = try_parse_file(file)
            if result:
                logger.success(f"[{MODULE}] Scraped STT data from: {file}")
                return result

        logger.warning(f"[{MODULE}] No usable STT data found. Returning fallback.")
        return [DEFAULT_FALLBACK]

    except Exception as e:
        logger.error(f"[{MODULE}] STT scrape failed: {e}")
        return [DEFAULT_FALLBACK]


if __name__ == "__main__":
    print(safe_scrape_stt())
