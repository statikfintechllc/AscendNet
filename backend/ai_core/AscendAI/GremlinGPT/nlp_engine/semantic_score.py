#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: nlp_engine/semantic_score.py :: Module Integrity Directive
# Self-improving semantic similarity engine for GremlinGPT.
# This script is a component of the GremlinGPT system, under Alpha expansion.

import re
import numpy as np
import langdetect
import torch
from backend.globals import logger
from backend.globals import CFG
from sentence_transformers import SentenceTransformer, util
from utils.nltk_setup import setup_nltk_data
import nltk
from nltk.tokenize import word_tokenize
from memory.log_history import log_event

try:
    from self_training.feedback_loop import inject_feedback
except ImportError:
    inject_feedback = None

NLTK_DATA_DIR = setup_nltk_data()

WATERMARK = "source:GremlinGPT"
ORIGIN = "semantic_score"

# Ensure punkt is available
# NLTK_PATHS = ["/usr/local/share/nltk_data", ".data/nltk_data"]
# for path in NLTK_PATHS:
#    nltk.data.path.append(path)

# try:
#    nltk.data.find("tokenizers/punkt")
# except LookupError:
# Try downloading to a writable directory
#    for path in NLTK_PATHS:
#        try:
#            nltk.download("punkt", download_dir=path)
#            break
#        except Exception as e:
#            pass  # Optionally log or print the failure


MODEL = CFG["nlp"].get("tokenizer_model", "bert-base-uncased")


ENGINE_NAME = "semantic_score"

# ---- DYNAMIC, SMART LOGIC FOR SEMANTIC SIMILARITY ----

# Multilingual support: map language code -> model
MODEL_MAP = {
    "en": "all-MiniLM-L6-v2",
    "de": "distiluse-base-multilingual-cased",  # German example
    "fr": "distiluse-base-multilingual-cased",  # French example
    # Add more language-model pairs as needed
}
DEFAULT_MODEL = "all-MiniLM-L6-v2"
MULTILINGUAL_MODEL = "distiluse-base-multilingual-cased"


_model_cache = {}


def _get_lang(text):
    try:
        return langdetect.detect(text)
    except Exception:
        return "en"


def _get_model(lang_code):
    """
    Loads or reuses a transformer for the requested language.
    Defaults to multilingual for non-English.
    """
    model_name = MODEL_MAP.get(lang_code, None)
    if not model_name:
        # Use multilingual for any non-english language
        model_name = MULTILINGUAL_MODEL
    if model_name not in _model_cache:
        try:
            logger.info(f"[{ENGINE_NAME}] Loading model: {model_name}")
            from backend.globals import CFG

            device = CFG.get("nlp", {}).get("device", "auto")
            if device == "auto":
                import torch

                device = "cuda" if torch.cuda.is_available() else "cpu"
            _model_cache[model_name] = SentenceTransformer(model_name, device=device)
        except Exception as e:
            logger.error(f"[{ENGINE_NAME}] Model {model_name} load failed: {e}")
            _model_cache[model_name] = None
    return _model_cache[model_name]


def clean_text(text: str) -> str:
    """
    Strips non-ASCII chars, compresses whitespace, removes control codes.
    """
    try:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\x00-\x7F]+", "", text)
        return text.strip()
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Text cleaning failed: {e}")
        return text


def split_sentences(text: str):
    try:
        return re.split(r"(?<=[.!?])\s+", text)
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Sentence split failed: {e}")
        return [text]


def tokenize(text: str):
    try:
        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)
        logger.debug(f"[{ENGINE_NAME}] Tokenized {len(tokens)} tokens.")
        return tokens
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Tokenization failed: {e}")
        return []


def semantic_similarity(a: str, b: str, dynamic_language=True, sentence_level=False) -> float:
    """
    Computes semantic similarity between two texts:
        - Detects language automatically if dynamic_language is True.
        - Falls back to multilingual model for non-English.
        - Optionally computes similarity by sentence and averages.
    """
    try:
        text_a, text_b = clean_text(a), clean_text(b)
        if dynamic_language:
            lang_a = _get_lang(text_a)
            lang_b = _get_lang(text_b)
            lang = lang_a if lang_a == lang_b else "en"
        else:
            lang = "en"
        model = _get_model(lang)
        if not model:
            logger.error(f"[{ENGINE_NAME}] No valid model loaded for lang={lang}; returning 0.0")
            return 0.0

        # Sentence-level similarity (average all combinations)
        if sentence_level:
            sents_a = split_sentences(text_a)
            sents_b = split_sentences(text_b)
            embs_a = model.encode(sents_a, convert_to_tensor=True)
            embs_b = model.encode(sents_b, convert_to_tensor=True)
            sims = util.cos_sim(embs_a, embs_b)
            # Return the mean of all max pairwise similarities
            max_per_a = np.max(sims.cpu().numpy(), axis=1)
            max_per_b = np.max(sims.cpu().numpy(), axis=0)
            sim_avg = (np.mean(max_per_a) + np.mean(max_per_b)) / 2.0
            sim_clamped = float(np.clip(sim_avg, 0.0, 1.0))
            logger.debug(f"[{ENGINE_NAME}] Sentence-level similarity: {sim_clamped:.4f}")
            return sim_clamped

        # Whole-text similarity
        emb_a = model.encode(text_a, convert_to_tensor=True)
        emb_b = model.encode(text_b, convert_to_tensor=True)
        sim = util.cos_sim(emb_a, emb_b).item()
        sim_clamped = max(0.0, min(1.0, float(sim)))
        logger.debug(f"[{ENGINE_NAME}] Semantic similarity: {sim_clamped:.4f} (lang: {lang})")
        return sim_clamped

    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Semantic similarity computation failed: {e}")
        return 0.0


def reasoned_similarity(
    a: str,
    b: str,
    dynamic_language=True,
    sentence_level=False,
    feedback=None,
    web_augment=False,
) -> dict:
    """
    Computes semantic similarity and returns a reasoned explanation, logs the event, and optionally injects feedback.
    """
    result = {
        "score": None,
        "explanation": None,
        "web": None,
        "tokens_a": [],
        "tokens_b": [],
        "lang": None,
        "sentence_level": sentence_level,
    }
    try:
        text_a, text_b = clean_text(a), clean_text(b)
        tokens_a, tokens_b = tokenize(text_a), tokenize(text_b)
        result["tokens_a"] = tokens_a
        result["tokens_b"] = tokens_b
        if dynamic_language:
            lang_a = _get_lang(text_a)
            lang_b = _get_lang(text_b)
            lang = lang_a if lang_a == lang_b else "en"
        else:
            lang = "en"
        result["lang"] = lang
        model = _get_model(lang)
        if not model:
            result["score"] = 0.0
            result["explanation"] = f"No valid model loaded for lang={lang}."
            return result
        if sentence_level:
            sents_a = split_sentences(text_a)
            sents_b = split_sentences(text_b)
            embs_a = model.encode(sents_a, convert_to_tensor=True)
            embs_b = model.encode(sents_b, convert_to_tensor=True)
            sims = util.cos_sim(embs_a, embs_b)
            max_per_a = np.max(sims.cpu().numpy(), axis=1)
            max_per_b = np.max(sims.cpu().numpy(), axis=0)
            sim_avg = (np.mean(max_per_a) + np.mean(max_per_b)) / 2.0
            sim_clamped = float(np.clip(sim_avg, 0.0, 1.0))
            result["score"] = sim_clamped
            result["explanation"] = f"Sentence-level similarity: {sim_clamped:.4f} (lang: {lang})"
        else:
            emb_a = model.encode(text_a, convert_to_tensor=True)
            emb_b = model.encode(text_b, convert_to_tensor=True)
            sim = util.cos_sim(emb_a, emb_b).item()
            sim_clamped = max(0.0, min(1.0, float(sim)))
            result["score"] = sim_clamped
            result["explanation"] = f"Whole-text similarity: {sim_clamped:.4f} (lang: {lang})"
        # Optionally augment with web search
        if web_augment:
            try:
                from scraper.web_knowledge_scraper import run_search_and_scrape

                result["web"] = run_search_and_scrape(a + " " + b)
            except Exception:
                result["web"] = None
        # Log event for learning
        log_event(
            "nlp_engine",
            "reasoned_similarity",
            {
                "a": a,
                "b": b,
                "score": result["score"],
                "lang": lang,
                "tokens_a": tokens_a,
                "tokens_b": tokens_b,
                "explanation": result["explanation"],
            },
        )
        # Inject feedback if provided
        if feedback and inject_feedback:
            inject_feedback()
    except Exception as e:
        result["score"] = 0.0
        result["explanation"] = f"Reasoned similarity computation failed: {e}"
    return result


# Utility: find best match from a list
def most_similar(text, candidates, threshold=0.75, **kwargs):
    """
    Returns the (candidate, score) with the highest semantic similarity to 'text'.
    """
    if not candidates:
        return None, 0.0
    scores = [semantic_similarity(text, c, **kwargs) for c in candidates]
    best_idx = int(np.argmax(scores))
    best_score = float(scores[best_idx])
    if best_score >= threshold:
        return candidates[best_idx], best_score
    return None, best_score


__all__ = [
    "semantic_similarity",
    "most_similar",
    "clean_text",
    "split_sentences",
    "tokenize",
    "reasoned_similarity",
]
