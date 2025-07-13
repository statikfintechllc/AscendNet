# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import spacy
import ast
from datetime import datetime
from nlp_engine.tokenizer import tokenize
from nlp_engine.pos_tagger import get_pos_tags
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from backend.globals import logger

WATERMARK = "source:GremlinGPT"
ORIGIN = "nlp_parser"

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# === Financial Ontology Dictionary ===
FIN_KEYWORDS = {
    "indicators": ["RSI", "MACD", "EMA", "Bollinger Bands", "VWAP"],
    "actions": ["buy", "sell", "short", "exit", "hold"],
    "assets": ["stock", "ETF", "option", "equity"],
    "tickers": ["AAPL", "TSLA", "NVDA", "SPY", "QQQ"],
    "terms": ["support", "resistance", "breakout", "volume", "earnings"],
}


def extract_code_entities(code_str):
    """
    Attempt to parse and extract Python AST node types from source code.
    """
    try:
        tree = ast.parse(code_str)
        return [node.__class__.__name__ for node in ast.walk(tree)]
    except Exception as e:
        logger.warning(f"[PARSER] Code parse failed: {e}")
        return []


def detect_financial_terms(text):
    """
    Scan input text for financial signal keywords.
    """
    found = []
    for category, terms in FIN_KEYWORDS.items():
        for term in terms:
            if term.lower() in text.lower():
                found.append((term, category))
    return found


def classify_intent(text, code_entities, financial_hits):
    """
    Classify user input based on structural analysis.
    """
    if code_entities:
        return "code"
    elif financial_hits:
        return "finance"
    else:
        return "general"


def parse_nlp(text):
    """
    Main NLP parsing pipeline. Extracts syntactic, semantic, and domain-specific intelligence.
    Returns structured dictionary with full trace.
    """
    tokens = tokenize(text)
    pos_tags = get_pos_tags(text)

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    dependencies = [(token.text, token.dep_, token.head.text) for token in doc]

    code_entities = []
    if any(kw in text for kw in ["def ", "import ", "lambda", "return", "class "]):
        code_entities = extract_code_entities(text)

    financial_hits = detect_financial_terms(text)
    route = classify_intent(text, code_entities, financial_hits)

    # Log and embed structured trace
    summary = (
        f"Intent: {route} | Tokens: {len(tokens)} | "
        f"Entities: {len(entities)} | Finance Matches: {len(financial_hits)} | "
        f"Code Constructs: {len(code_entities)}"
    )
    vector = embed_text(summary)

    package_embedding(
        text=summary,
        vector=vector,
        meta={
            "origin": ORIGIN,
            "timestamp": datetime.utcnow().isoformat(),
            "route": route,
            "tokens": len(tokens),
            "entities": len(entities),
            "financial_hits": financial_hits,
            "code": bool(code_entities),
            "watermark": WATERMARK,
        },
    )

    inject_watermark(origin=ORIGIN)

    return {
        "route": route,
        "tokens": tokens,
        "pos": pos_tags,
        "entities": entities,
        "dependencies": dependencies,
        "code_entities": code_entities,
        "financial_hits": financial_hits,
    }
