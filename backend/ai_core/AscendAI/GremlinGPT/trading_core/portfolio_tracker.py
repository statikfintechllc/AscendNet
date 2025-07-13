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

# trading_core/portfolio_tracker.py

import json
from pathlib import Path
from datetime import datetime
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("trading_core")
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
import shutil
import math
from agent_core.task_queue import enqueue_task  # FSM/task queue hook
from self_training.feedback_loop import tag_event  # Feedback/tagging

# === File Paths ===
PORTFOLIO_FILE = Path("data/portfolio.json")
HISTORY_FILE = Path("data/trade_history.jsonl")

# === Metadata ===
WATERMARK = "source:GremlinGPT"
ORIGIN = "portfolio_tracker"

PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)


# === Load/Save Helpers ===
def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_portfolio():
    return load_json(PORTFOLIO_FILE)


def save_portfolio(data):
    save_json(PORTFOLIO_FILE, data)
    inject_watermark(origin=ORIGIN)
    logger.info("[PORTFOLIO] Portfolio saved.")


# === Trade Logging ===
def log_trade(symbol, action, shares, price):
    event = {
        "symbol": symbol,
        "action": action,
        "shares": shares,
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "origin": ORIGIN,
        "watermark": WATERMARK,
    }

    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    logger.info(f"[PORTFOLIO] Trade logged: {event}")

    summary = f"{action.upper()} {shares} {symbol} @ ${price:.2f}"
    vector = embed_text(summary)

    package_embedding(
        text=summary,
        vector=vector,
        meta=event,
    )

    inject_watermark(origin=f"{ORIGIN}::trade")


# === Update Position ===
def update_position(symbol, price, shares, action="buy"):
    portfolio = load_portfolio()
    existing = portfolio.get(symbol, {"shares": 0, "price": 0.0})

    if action == "buy":
        total_shares = existing["shares"] + shares
        avg_price = (
            (existing["shares"] * existing["price"] + shares * price) / total_shares
            if total_shares > 0
            else price
        )
    elif action == "sell":
        total_shares = max(0, existing["shares"] - shares)
        avg_price = existing["price"] if total_shares > 0 else 0.0
    else:
        total_shares = shares
        avg_price = price

    portfolio[symbol] = {
        "price": round(avg_price, 2),
        "shares": total_shares,
        "last_updated": datetime.utcnow().isoformat(),
    }

    save_portfolio(portfolio)
    log_trade(symbol, action, shares, price)


# === Position Utilities ===
def get_position(symbol):
    return load_portfolio().get(symbol, {"price": 0.0, "shares": 0})


def calculate_unrealized(symbol, current_price):
    position = get_position(symbol)
    return round((current_price - position["price"]) * position["shares"], 2)


def get_portfolio_summary(current_prices: dict):
    portfolio = load_portfolio()
    summary = {}
    total_value = 0.0
    total_cost = 0.0

    for symbol, data in portfolio.items():
        current_price = current_prices.get(symbol, data["price"])
        shares = data["shares"]
        entry_price = data["price"]
        cost = shares * entry_price
        value = shares * current_price
        pnl = value - cost

        summary[symbol] = {
            "shares": shares,
            "entry_price": entry_price,
            "current_price": current_price,
            "value": round(value, 2),
            "pnl": round(pnl, 2),
            "last_updated": data.get("last_updated"),
        }

        total_value += value
        total_cost += cost

    summary["total"] = {
        "value": round(total_value, 2),
        "cost_basis": round(total_cost, 2),
        "unrealized_gain": round(total_value - total_cost, 2),
    }

    logger.info(f"[PORTFOLIO] Summary generated. Total value: ${summary['total']['value']:.2f}")
    return summary


# === Backup & Recovery ===
BACKUP_FILE = Path("data/portfolio_backup.json")


def backup_portfolio():
    shutil.copy(PORTFOLIO_FILE, BACKUP_FILE)
    logger.info("[PORTFOLIO] Backup created.")


def restore_portfolio():
    if BACKUP_FILE.exists():
        shutil.copy(BACKUP_FILE, PORTFOLIO_FILE)
        logger.info("[PORTFOLIO] Portfolio restored from backup.")
    else:
        logger.warning("[PORTFOLIO] No backup found.")


# === Audit Trail ===
def audit_portfolio():
    portfolio = load_portfolio()
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = [json.loads(line) for line in f]
    audit = {"portfolio": portfolio, "history": history, "timestamp": datetime.utcnow().isoformat()}
    logger.info(f"[PORTFOLIO] Audit: {audit}")
    return audit


# === Advanced Trade Types ===
def place_order(
    symbol, action, shares, price, order_type="market", limit_price=None, stop_price=None
):
    if order_type == "market":
        update_position(symbol, price, shares, action)
    elif order_type == "limit":
        if (action == "buy" and price <= limit_price) or (
            action == "sell" and price >= limit_price
        ):
            update_position(symbol, price, shares, action)
        else:
            logger.info(f"[PORTFOLIO] Limit order not filled: {symbol} {action} @ {limit_price}")
    elif order_type == "stop":
        if (action == "buy" and price >= stop_price) or (action == "sell" and price <= stop_price):
            update_position(symbol, price, shares, action)
        else:
            logger.info(f"[PORTFOLIO] Stop order not triggered: {symbol} {action} @ {stop_price}")
    else:
        logger.warning(f"[PORTFOLIO] Unknown order type: {order_type}")
    tag_event(
        "trade",
        {
            "symbol": symbol,
            "action": action,
            "shares": shares,
            "price": price,
            "order_type": order_type,
        },
    )
    enqueue_task(
        {
            "type": "trade_event",
            "symbol": symbol,
            "action": action,
            "shares": shares,
            "price": price,
            "order_type": order_type,
        }
    )


# === Portfolio Analytics ===
def calculate_risk_metrics(current_prices: dict):
    portfolio = load_portfolio()
    total_value = sum(
        current_prices.get(sym, d["price"]) * d["shares"] for sym, d in portfolio.items()
    )
    exposures = {
        sym: (current_prices.get(sym, d["price"]) * d["shares"]) / total_value if total_value else 0
        for sym, d in portfolio.items()
    }
    diversification = 1 - sum(v**2 for v in exposures.values())  # Herfindahl index
    returns = []
    for sym, d in portfolio.items():
        entry = d["price"]
        curr = current_prices.get(sym, entry)
        if entry > 0:
            returns.append((curr - entry) / entry)
    mean_return = sum(returns) / len(returns) if returns else 0
    stddev = (
        math.sqrt(sum((r - mean_return) ** 2 for r in returns) / len(returns)) if returns else 0
    )
    sharpe = mean_return / stddev if stddev else 0
    metrics = {
        "exposures": exposures,
        "diversification": diversification,
        "sharpe_ratio": round(sharpe, 3),
        "mean_return": round(mean_return, 4),
        "stddev": round(stddev, 4),
    }
    logger.info(f"[PORTFOLIO] Risk metrics: {metrics}")
    return metrics


# === CLI/API Interface ===
def cli_interface():
    import argparse

    parser = argparse.ArgumentParser(description="GremlinGPT Portfolio Tracker CLI")
    parser.add_argument(
        "action", choices=["buy", "sell", "audit", "backup", "restore", "summary", "risk"]
    )
    parser.add_argument("--symbol", type=str)
    parser.add_argument("--shares", type=int, default=0)
    parser.add_argument("--price", type=float, default=0.0)
    parser.add_argument("--order_type", type=str, default="market")
    parser.add_argument("--limit_price", type=float)
    parser.add_argument("--stop_price", type=float)
    parser.add_argument("--current_prices", type=str, help="JSON string of current prices")
    args = parser.parse_args()

    if args.action in ["buy", "sell"]:
        place_order(
            args.symbol,
            args.action,
            args.shares,
            args.price,
            order_type=args.order_type,
            limit_price=args.limit_price,
            stop_price=args.stop_price,
        )
    elif args.action == "audit":
        print(json.dumps(audit_portfolio(), indent=2))
    elif args.action == "backup":
        backup_portfolio()
    elif args.action == "restore":
        restore_portfolio()
    elif args.action == "summary":
        prices = json.loads(args.current_prices) if args.current_prices else {}
        print(json.dumps(get_portfolio_summary(prices), indent=2))
    elif args.action == "risk":
        prices = json.loads(args.current_prices) if args.current_prices else {}
        print(json.dumps(calculate_risk_metrics(prices), indent=2))


if __name__ == "__main__":
    cli_interface()
