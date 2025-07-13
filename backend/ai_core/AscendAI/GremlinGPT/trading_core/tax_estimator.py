#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("trading_core")
from datetime import datetime

DEFAULT_TAX_RATE = 0.15  # Can be made dynamic via config or input


def estimate_tax(position, tax_rate=None, log=True, persist=False):
    """
    Estimate tax for a single position.
    :param position: dict with 'symbol', 'price', 'shares', optional 'side', 'open_date', etc.
    :param tax_rate: override tax rate (float 0..1), else use DEFAULT_TAX_RATE.
    :param log: if True, log the estimate.
    :param persist: if True, store result for audit/training.
    :return: dict {symbol, shares, price, value, tax, tax_rate, meta}
    """
    try:
        shares = float(position.get("shares", 0))
        price = float(position.get("price", 0))
        symbol = position.get("symbol", "UNKNOWN")
        side = position.get("side", "long")
        open_date = position.get("open_date")
        close_date = position.get("close_date")
        meta = {
            k: v
            for k, v in position.items()
            if k not in {"symbol", "price", "shares", "side", "open_date", "close_date"}
        }

        total_value = shares * price
        rate = float(tax_rate) if tax_rate is not None else DEFAULT_TAX_RATE
        tax = round(total_value * rate, 2)

        result = {
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "value": round(total_value, 2),
            "tax": tax,
            "tax_rate": rate,
            "side": side,
            "open_date": open_date,
            "close_date": close_date,
            "meta": meta,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if log:
            logger.info(
                f"[TAX_ESTIMATE] {symbol}: value=${total_value:.2f}, tax=${tax:.2f} at {rate*100:.1f}%"
            )

        if persist:
            _persist_tax_estimate(result)

        return result

    except Exception as e:
        logger.error(f"[TAX_ESTIMATE] Error for {position}: {e}")
        return {"error": str(e), "position": position}


def estimate_batch(positions, tax_rate=None, log=True, persist=False):
    """
    Estimate taxes for a batch of positions.
    :param positions: list of position dicts
    :return: list of estimate results
    """
    return [estimate_tax(pos, tax_rate=tax_rate, log=log, persist=persist) for pos in positions]


def _persist_tax_estimate(result):
    """
    Persist a single tax estimate to memory/log for audit/self-training.
    """
    try:
        from memory.vector_store.embedder import package_embedding, embed_text

        text = f"TAX {result['symbol']} {result['shares']} @ {result['price']} = Tax ${result['tax']} ({result['tax_rate']*100:.1f}%)"
        vector = embed_text(text)
        package_embedding(text=text, vector=vector, meta=result)
        logger.debug(f"[TAX_ESTIMATE] Persisted embedding for {result['symbol']}")
    except Exception as e:
        logger.warning(f"[TAX_ESTIMATE] Persist failed: {e}")
