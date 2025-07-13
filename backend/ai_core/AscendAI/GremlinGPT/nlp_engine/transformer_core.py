#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
from backend.globals import CFG, logger

# ─────────────────────────────────────────────
# Config Load
MODEL_NAME = CFG["nlp"].get("transformer_model", "bert-base-uncased")
EMBEDDING_DIM = CFG["nlp"].get("embedding_dim", 384)
DEVICE = CFG["nlp"].get("device", "auto")

if DEVICE == "auto":
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ─────────────────────────────────────────────
# Model Bootstrap
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    logger.success(f"[TRANSFORMER] Loaded model: {MODEL_NAME} on {DEVICE}")
except Exception as e:
    logger.error(f"[TRANSFORMER] Failed to load model '{MODEL_NAME}': {e}")
    tokenizer = None
    model = None


# ─────────────────────────────────────────────
def encode(text):
    """
    Encodes input text using the configured transformer model.
    Returns a float32 numpy vector.
    """
    if not tokenizer or not model:
        logger.warning("[TRANSFORMER] Model not initialized. Returning zeros.")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )
        # Move inputs to same device as model
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)

        vector = outputs.last_hidden_state.mean(dim=1).squeeze()
        return vector.cpu().numpy().astype(np.float32)

    except Exception as e:
        logger.error(f"[TRANSFORMER] Encoding failed: {e}")
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    sample = "What is resistance level in trading?"
    vec = encode(sample)
    print(f"Vector ({len(vec)}): {vec[:10]} ...")
