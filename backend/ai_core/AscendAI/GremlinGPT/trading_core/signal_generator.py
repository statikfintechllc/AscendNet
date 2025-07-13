#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from trading_core.rules_engine import apply_signal_rules
from trading_core.stock_scraper import get_live_penny_stocks
from memory.vector_store.embedder import (
    package_embedding,
    embed_text,
    inject_watermark,
)
from backend.globals import logger
from datetime import datetime

WATERMARK = "source:GremlinGPT"
ORIGIN = "signal_generator"

# --- Main Signal Generator (API-facing) ---


def generate_signals(limit=50, embed=True):
    """
    Generate and return actionable trading signals, persist embeddings, and support dashboard API.
    :param limit: max number of signals to return
    :param embed: if True, store signals as vector embeddings in memory
    :return: list of signal dicts
    """
    try:
        stocks = get_live_penny_stocks()
        signals = []
        n = 0

        for stock in stocks:
            signal = apply_signal_rules(stock)
            if signal:
                n += 1
                result = {**stock, **signal}
                signals.append(result)

                summary = (
                    f"{stock['symbol']} @ ${stock['price']:.2f} | "
                    f"Signal: {', '.join(signal['signal'])}"
                )

                if embed:
                    vector = embed_text(summary)
                    package_embedding(
                        text=summary,
                        vector=vector,
                        meta={
                            "symbol": stock["symbol"],
                            "signal": signal["signal"],
                            "price": stock["price"],
                            "ema": stock.get("ema"),
                            "vwap": stock.get("vwap"),
                            "rsi": stock.get("rsi"),
                            "volume": stock.get("volume"),
                            "timestamp": datetime.utcnow().isoformat(),
                            "origin": ORIGIN,
                            "watermark": WATERMARK,
                        },
                    )
                    inject_watermark(origin=ORIGIN)

                logger.info(f"[SIGNAL] {summary}")

                if n >= limit:
                    break

        logger.info(f"[SIGNAL_GENERATOR] Generated {len(signals)} signals.")
        return signals

    except Exception as e:
        logger.error(f"[SIGNAL_GENERATOR] Error: {e}")
        return []


# --- Optional: For self-healing/mutation, dashboard, or agent tasks ---


def get_signal_history(limit=100):
    """
    Return signal embedding history for dashboard/graph.
    """
    from memory.vector_store.embedder import get_all_embeddings

    signals = []
    for emb in get_all_embeddings(limit):
        if emb["meta"].get("origin") == ORIGIN:
            signals.append(emb)
    return signals


def repair_signal_index():
    """
    Self-repair for embeddings relevant to signals.
    """
    from memory.vector_store.embedder import repair_index

    repair_index()
    logger.info("[SIGNAL_GENERATOR] Signal embedding index repaired.")
