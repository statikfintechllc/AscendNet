# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# trading_core/rules_engine.py

from datetime import datetime
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("trading_core")
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark

WATERMARK = "source:GremlinGPT"
ORIGIN = "rules_engine"


def apply_signal_rules(stock: dict):
    """
    Evaluates trading conditions on a stock and returns actionable signals.
    Args:
        stock (dict): {
            "symbol": str,
            "price": float,
            "ema": float,
            "vwap": float,
            "volume": int,
            "rsi": float,
            ...
        }
    Returns:
        dict | None
    """
    try:
        symbol = stock.get("symbol", "UNKNOWN")
        price = stock.get("price", 0)
        ema = stock.get("ema", 0)
        vwap = stock.get("vwap", 0)
        volume = stock.get("volume", 0)
        rsi = stock.get("rsi", 50)

        signals = []

        # === Core Signal Rules ===
        if price > ema and price > vwap:
            signals.append("Breakout")

        if volume > 150000:
            signals.append("Volume Spike")

        if rsi < 30:
            signals.append("Oversold")

        if rsi > 70:
            signals.append("Overbought")

        if price < ema and rsi < 40:
            signals.append("Pullback")

        if not signals:
            return None

        summary = f"{symbol}: {', '.join(signals)} @ ${price} (EMA: {ema}, VWAP: {vwap}, RSI: {rsi}, VOL: {volume})"
        vector = embed_text(summary)

        package_embedding(
            text=summary,
            vector=vector,
            meta={
                "symbol": symbol,
                "price": price,
                "ema": ema,
                "vwap": vwap,
                "rsi": rsi,
                "volume": volume,
                "signals": signals,
                "timestamp": datetime.utcnow().isoformat(),
                "origin": ORIGIN,
                "watermark": WATERMARK,
            },
        )

        logger.success(f"[RULES] Signal generated → {summary}")
        inject_watermark(origin=ORIGIN)

        return {"symbol": symbol, "signal": signals}

    except Exception as e:
        logger.error(f"[RULES] Signal rule error: {e}")
        return None
