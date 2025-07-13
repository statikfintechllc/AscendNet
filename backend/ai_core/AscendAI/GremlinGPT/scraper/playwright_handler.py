#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from playwright.async_api import async_playwright, TimeoutError
from backend.globals import CFG, logger
from datetime import datetime

ORIGIN = "playwright_handler"


async def get_dom_html(url):
    profile_path = CFG["scraper"].get("browser_profile", "/tmp/browser_profile")
    timestamp = datetime.utcnow().isoformat()

    try:
        logger.info(f"[{ORIGIN.upper()}] [{timestamp}] Launching browser for: {url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                profile_path, headless=True
            )
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            content = await page.content()
            await browser.close()

            logger.success(f"[{ORIGIN.upper()}] [{timestamp}] DOM fetched for: {url}")
            return content

    except TimeoutError:
        logger.error(f"[{ORIGIN.upper()}] [{timestamp}] Timeout loading page: {url}")
        return "<html><body><h1>Timeout Error</h1></body></html>"

    except Exception as e:
        logger.error(
            f"[{ORIGIN.upper()}] [{timestamp}] Browser session failed for {url}: {e}"
        )
        return f"<html><body><h1>Error: {e}</h1></body></html>"
