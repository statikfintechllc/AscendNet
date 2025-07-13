# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.


from scraper.dom_navigator import extract_dom_structure
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from memory.log_history import log_event

WATERMARK = "source:GremlinGPT"
ORIGIN = "web_knowledge_scraper"

HEADERS = {
    "User-Agent": "GremlinGPT/5.0 (+https://gremlingpt.ai/bot)",
    "Accept": "text/html,python,javascript,java,markdown,jupyter,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            if response.status == 200:
                return await response.text()
            logger.warning(f"[{ORIGIN}] Non-200 for {url}: {response.status}")
    except Exception as e:
        logger.error(f"[{ORIGIN}] Failed to fetch {url}: {e}")
    return ""


async def scrape_web_knowledge(urls):
    results = []
    timestamp = datetime.utcnow().isoformat()

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [fetch_html(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    for url, html in zip(urls, pages):
        if not html:
            continue

        structure = extract_dom_structure(html)

        if not structure.get("text"):
            soup = BeautifulSoup(html, "lxml")
            fallback_text = soup.get_text(separator="\n", strip=True)[:1500]
            structure["text"] = fallback_text
            logger.warning(f"[{ORIGIN}] Fallback parsing used for {url}")

        domain = urlparse(url).netloc.replace("www.", "")
        summary = f"[{url}]\n{structure['text']}"
        vector = embed_text(summary)

        metadata = {
            "origin": ORIGIN,
            "timestamp": timestamp,
            "url": url,
            "domain": domain,
            "tags": structure.get("tags", {}),
            "length": len(summary),
            "watermark": WATERMARK,
        }

        package_embedding(text=summary, vector=vector, meta=metadata)
        inject_watermark(origin=ORIGIN)
        log_event("scraper", "knowledge_fetch", {"url": url, "summary_len": len(summary)})

        results.append(
            {
                "url": url,
                "summary": summary,
                "nodes": structure.get("nodes", []),
                "links": structure.get("links", []),
            }
        )

        logger.success(f"[{ORIGIN}] Embedded: {url}")

    return results


def run_search_and_scrape(urls):
    try:
        os.makedirs("run/logs", exist_ok=True)
        results = asyncio.run(scrape_web_knowledge(urls))

        with open("run/logs/sample_scrape.json", "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"[{ORIGIN}] Scrape batch complete.")
        return results
    except Exception as e:
        logger.error(f"[{ORIGIN}] Execution error: {e}")
        return []


if __name__ == "__main__":
    test_urls = [
        "https://finance.yahoo.com/",
        "https://www.investing.com/news/stock-market-news",
    ]
    run_search_and_scrape(test_urls)
