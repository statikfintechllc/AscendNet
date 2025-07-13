#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# Bulletproofed: Never fails on no task, pipeline errors, or module import issues.

import asyncio
import time
from datetime import datetime

try:
    from scraper.playwright_handler import get_dom_html
    from scraper.page_simulator import store_scrape_to_memory
    from backend.globals import CFG, logger
    from agent_core.task_queue import fetch_task
    from memory.log_history import log_event
except Exception as import_err:
    # If any import fails, log and enter idle loop
    import sys

    print(f"[SCRAPER_LOOP] Import error: {import_err}")

    async def run_scraper():
        while True:
            print(f"[SCRAPER_LOOP] Import error persists: {import_err}")
            await asyncio.sleep(30)

    if __name__ == "__main__":
        asyncio.run(run_scraper())
    sys.exit(0)

MODULE = "scraper_loop"


async def run_scraper():
    logger.info(f"[{MODULE.upper()}] Autonomous loop engaged.")
    interval = CFG.get("scraper", {}).get("scrape_interval_sec", 10)
    if not isinstance(interval, (int, float)) or interval <= 0:
        interval = 10

    while True:
        try:
            loop_start = time.time()
            tick_time = datetime.utcnow().isoformat()
            log_event(MODULE, "tick_start", {"timestamp": tick_time})

            try:
                task = fetch_task("scrape")
            except Exception as task_fetch_err:
                logger.error(
                    f"[{MODULE.upper()}] Error fetching task: {task_fetch_err}"
                )
                log_event(
                    MODULE,
                    "task_fetch_error",
                    {"error": str(task_fetch_err)},
                    status="fail",
                )
                task = None

            if task:
                logger.info(f"[{MODULE.upper()}] Acquired task: {task}")
                try:
                    dom = await get_dom_html(task["target"])
                    store_scrape_to_memory(task["target"], dom)
                    logger.success(
                        f"[{MODULE.upper()}] Stored scrape snapshot from {task['target']}"
                    )
                    log_event(
                        MODULE,
                        "task_complete",
                        {"target": task["target"]},
                        status="success",
                    )
                except Exception as e:
                    logger.error(f"[{MODULE.upper()}] Scrape failed: {e}")
                    log_event(MODULE, "task_error", {"error": str(e)}, status="fail")
            else:
                logger.debug(f"[{MODULE.upper()}] No pending scrape task.")

            elapsed = time.time() - loop_start
            logger.debug(f"[{MODULE.upper()}] Cycle completed in {elapsed:.2f} sec.")
            await asyncio.sleep(interval)
        except Exception as loop_err:
            logger.error(f"[{MODULE.upper()}] Unhandled loop error: {loop_err}")
            log_event(MODULE, "loop_error", {"error": str(loop_err)}, status="fail")
            await asyncio.sleep(10)  # Wait before retrying loop


if __name__ == "__main__":
    try:
        asyncio.run(run_scraper())
    except KeyboardInterrupt:
        print("[SCRAPER_LOOP] KeyboardInterrupt: Exiting cleanly.")
    except Exception as main_err:
        print(f"[SCRAPER_LOOP] Top-level error: {main_err}")
