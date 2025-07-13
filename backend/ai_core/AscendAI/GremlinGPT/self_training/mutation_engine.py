# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v1.0.3 :: Module Integrity Directive
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

# self_training/mutation_engine.py

import random
import ast
from datetime import datetime
from nlp_engine.tokenizer import tokenize
from nlp_engine.pos_tagger import get_pos_tags
from nlp_engine.semantic_score import semantic_similarity
from memory.vector_store.embedder import embed_text, package_embedding
from agents.planner_agent import enqueue_next
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("self_training")


def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def mutate_dataset(dataset):
    mutated = []

    for entry in dataset:
        original = entry["log"]
        mutation_type = None
        fix = original
        safe = True
        context_notes = []
        score = 0.0

        tokens = tokenize(original)
        pos_tags = get_pos_tags(original)

        if "scrape" in original:
            fix = original.replace("fail", "retry")
            mutation_type = "scrape_retry"
        elif "scan" in original:
            fix = original.replace("low", "high")
            mutation_type = "signal_boost"
        else:
            suffix = random.choice(
                [
                    " #mutated",
                    f" #patch_{random.randint(100,999)}",
                    f" #delta_{int(datetime.utcnow().timestamp())}",
                ]
            )
            fix = original + suffix
            mutation_type = "suffix_noise"

        # NLP Semantic delta
        score = semantic_similarity(original, fix)
        if score < 0.6:
            context_notes.append("semantic_deviation")
        else:
            context_notes.append("semantic_consistent")

        # Syntax safety check
        if not is_valid_python(fix):
            safe = False
            fix = original
            mutation_type = "invalid_rollback"
            context_notes.append("syntax_failed")
        else:
            context_notes.append("syntax_valid")

        # Embedding for vector memory
        vector = embed_text(fix)
        package_embedding(
            text=fix,
            vector=vector,
            meta={
                "origin": "mutation_engine",
                "type": "code_mutation",
                "label": mutation_type,
                "timestamp": datetime.utcnow().isoformat(),
                "semantic_score": round(score, 4),
                "safe": safe,
            },
        )

        # Route problematic mutations to planner
        if score < 0.5 or not safe:
            logger.warning(f"[MUTATOR] Routed task for planner: score={score}, safe={safe}")
            enqueue_next()

        # Store mutation result
        mutated.append(
            {
                "input": original,
                "mutation": fix,
                "label": "mutated",
                "mutation_type": mutation_type,
                "timestamp": datetime.utcnow().isoformat(),
                "safe": safe,
                "semantic_score": round(score, 4),
                "tokens": tokens,
                "pos_tags": pos_tags,
                "context_flags": context_notes,
            }
        )

    return mutated
