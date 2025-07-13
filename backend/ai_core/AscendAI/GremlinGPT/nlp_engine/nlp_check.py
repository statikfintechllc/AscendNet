# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import sys
import traceback
from datetime import datetime

NLP_OUT_LOG = "$HOME/data/logs/nlp.out"


def log_nlp_out(message):
    timestamp = datetime.utcnow().isoformat()
    try:
        with open(NLP_OUT_LOG, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"[NLP_CHECK] Could not write to {NLP_OUT_LOG}: {e}", file=sys.stderr)


try:
    from tokenizer import Tokenizer  # Your actual tokenizer
    from transformer_core import TransformerCore  # Your real core model
except ImportError as e:
    err_msg = f"[NLP_CHECK] ImportError: {e}"
    print(err_msg, file=sys.stderr)
    log_nlp_out(err_msg)
    sys.exit(1)


def nlp_internal_check():
    status = "FAILED"
    sys_msg = ""
    try:
        # Simple English test phrase
        test_phrase = "This is a test of the GremlinGPT NLP engine."
        # Instantiate your tokenizer (adjust class name if needed)
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(test_phrase)
        assert isinstance(tokens, list) and len(tokens) > 0, "Tokenization failed"

        # Instantiate your transformer (adjust class name if needed)
        model = TransformerCore()
        result = model.forward(tokens)
        assert result is not None, "Transformer forward failed"

        # Ask the model how it "feels" (system status query)
        try:
            health_query = "How are you feeling? How is your system health?"
            health_tokens = tokenizer.tokenize(health_query)
            health_response = model.forward(health_tokens)
            sys_msg = (
                health_response
                if isinstance(health_response, str)
                else str(health_response)
            )
        except Exception as health_ex:
            sys_msg = f"[NLP_CHECK] Could not get model health: {health_ex}"

        status = "OK"
        print("NLP Internal Check: ✅")
        print(f"[NLP_CHECK] Model says: {sys_msg}")
        log_nlp_out(f"NLP Internal Check: OK | Model: {sys_msg}")

    except Exception as ex:
        err_info = f"[NLP_CHECK] Error: {ex}\n{traceback.format_exc()}"
        print(err_info, file=sys.stderr)
        log_nlp_out(f"NLP Internal Check: FAILED | {ex}")
        sys.exit(1)


if __name__ == "__main__":
    nlp_internal_check()
