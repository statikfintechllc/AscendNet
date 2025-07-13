# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import asyncio
import psutil
import threading
import time
from datetime import datetime
from loguru import logger

from scraper.tws_scraper import safe_scrape_tws
from scraper.stt_scraper import safe_scrape_stt
from scraper.playwright_scraper import safe_scrape_web
from scraper.page_simulator import store_scrape_to_memory
from memory.log_history import log_event

WATERMARK = "source:GremlinGPT"
ORIGIN = "source_router"

MODULE = "source_router"
_last_scraped = []
_async_lock = asyncio.Lock()  # Protect async scraping


def detect_apps():
    try:
        procs = [p.name().lower() for p in psutil.process_iter()]
        return {
            "tws": any("tws" in p for p in procs),
            "stt": any("stockstotrade" in p for p in procs),
        }
    except Exception as e:
        logger.warning(f"[{MODULE}] App detection failed: {e}")
        return {"tws": False, "stt": False}


async def route_scraping_async():
    """Autonomous source router across available platforms."""
    async with _async_lock:
        try:
            tick = datetime.utcnow().isoformat()
            apps = detect_apps()
            logger.info(f"[{MODULE.upper()}] Detected: {apps}")
            log_event(MODULE, "detection", {"apps": apps, "timestamp": tick})

            if apps["tws"]:
                result = safe_scrape_tws()
                source = "TWS"
            elif apps["stt"]:
                result = safe_scrape_stt()
                source = "STT"
            else:
                result = await safe_scrape_web()
                source = "WEB"

            for item in result:
                content = (
                    f"[{item.get('symbol', 'N/A')}] Price: {item.get('price')} "
                    f"Volume: {item.get('volume')}"
                )
                store_scrape_to_memory(source, content)

            logger.success(f"[{MODULE.upper()}] Scraped from: {source}")
            return result

        except Exception as e:
            logger.warning(f"[{MODULE}] Routing failed: {e}")
            return []


def periodic_refresh(interval_sec=5):
    global _last_scraped
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            logger.debug(f"[{MODULE}] Refresh triggered.")
            result = loop.run_until_complete(route_scraping_async())
            _last_scraped = result
        except Exception as e:
            logger.error(f"[{MODULE}] Refresh error: {e}")
        time.sleep(interval_sec)


def get_live_snapshot():
    return _last_scraped


def start_scraper_loop():
    logger.info(f"[{MODULE}] Launching async scrape monitor.")
    t = threading.Thread(target=periodic_refresh, daemon=True)
    t.start()
