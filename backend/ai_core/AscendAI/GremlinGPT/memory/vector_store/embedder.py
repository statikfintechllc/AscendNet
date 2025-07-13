#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Memory Embedder & Vector Store Core

import os
import shutil
import uuid
import json
import numpy as np # type: ignore
try:
    import faiss
except ImportError:
    try:
        import faiss_cpu as faiss  # type: ignore
    except ImportError as e:
        print(f"[EMBEDDER] faiss import failed: {e}")
        faiss = None
from datetime import datetime, timezone
from loguru import logger # type: ignore

# --- Resilient Imports ---
try:
    import chromadb  # type: ignore
except ImportError as e:
    logger.error(f"[EMBEDDER] chromadb import failed: {e}")
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer # type: ignore
except ImportError as e:
    logger.error(f"[EMBEDDER] sentence_transformers import failed: {e}")
    SentenceTransformer = None

try:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from backend.globals import MEM
    import toml
    CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/config.toml'))
    try:
        config = toml.load(CONFIG_PATH)
        memory_conf = config.get('memory', {})
        dashboard_selected_backend = memory_conf.get('dashboard_selected_backend', 'faiss')
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to load config.toml: {e}")
        dashboard_selected_backend = 'faiss'
except Exception as e:
    logger.error(f"[EMBEDDER] MEM import or type-check failed: {e}")
    MEM = {}

try:
    from nlp_engine.transformer_core import encode
except Exception:
    # fallback to a dummy encoder
    def encode(text):
        _ = text  # Access the parameter to avoid unused variable warning
        return np.zeros(MEM.get("embedding", {}).get("dimension", 384), dtype="float32")

# --- Configuration & Paths ---
storage_conf = MEM.get("storage", {})
if not isinstance(storage_conf, dict):
    logger.error("[EMBEDDER] storage config malformed; resetting to empty dict")
    storage_conf = {}

BASE_VECTOR_PATH = storage_conf.get("vector_store_path", "./memory/vector_store")
FAISS_DIR        = os.path.join(BASE_VECTOR_PATH, "faiss")
CHROMA_DIR       = os.path.join(BASE_VECTOR_PATH, "chroma")
LOCAL_INDEX_ROOT = storage_conf.get("local_index_path", "./memory/local_index")
LOCAL_INDEX_PATH = os.path.join(LOCAL_INDEX_ROOT, "documents")
METADATA_DB_PATH = storage_conf.get("metadata_db", os.path.join(LOCAL_INDEX_ROOT, "memory.json"))

# Use dashboard-selected backend for toggling
USE_FAISS   = dashboard_selected_backend == "faiss"
USE_CHROMA  = dashboard_selected_backend == "chromadb"
EMBED_MODEL = MEM.get("embedding", {}).get("model", "all-MiniLM-L6-v2")
DIMENSION   = MEM.get("embedding", {}).get("dimension", 384)

# --- Ensure directories exist (and log failures) ---
for path in (FAISS_DIR, CHROMA_DIR, LOCAL_INDEX_PATH):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to create directory {path}: {e}")

# --- Chroma Client Setup ---
if chromadb:
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = chroma_client.get_or_create_collection(name="gremlin_memory")
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to initialize Chroma client: {e}")
        collection = None
else:
    collection = None

def add_to_chroma(text, emb_id, vector, meta):
    if not collection:
        logger.warning(f"[CHROMA] Skipping add; collection not available")
        return
    try:
        collection.add(
            documents=[text],
            embeddings=[vector.tolist() if hasattr(vector, "tolist") else list(vector)],
            metadatas=[meta],
            ids=[emb_id]
        )
        logger.info(f"[CHROMA] Added {emb_id}")
    except Exception as e:
        logger.error(f"[CHROMA] Add failed for {emb_id}: {e}")

# --- FAISS Index Setup ---
FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "faiss_index.index")
try:
    if faiss and os.path.exists(FAISS_INDEX_PATH):
        faiss_index = faiss.read_index(FAISS_INDEX_PATH)  # type: ignore
        logger.info(f"[FAISS] Loaded index from {FAISS_INDEX_PATH}")
    elif faiss:
        faiss_index = faiss.IndexFlatL2(DIMENSION)  # type: ignore
        logger.info("[FAISS] Initialized new IndexFlatL2")
    else:
        faiss_index = None
        logger.error("[FAISS] faiss unavailable; index not initialized")
except Exception as e:
    logger.error(f"[FAISS] Failed to load or init index: {e}")
    faiss_index = None

def add_to_faiss(vector, emb_id):
    if not faiss_index:
        logger.warning(f"[FAISS] Skipping add; index not available")
        return
    try:
        vec = np.array(vector, dtype="float32").reshape(1, -1)
        # Diagnostic logging for FAISS index type and available methods
        logger.info(f"[FAISS] Index type: {type(faiss_index)}")
        logger.info(f"[FAISS] Index dir: {dir(faiss_index)}")
        if hasattr(faiss_index, 'add_with_ids') and callable(getattr(faiss_index, 'add_with_ids', None)):
            logger.info(f"[FAISS] Using add_with_ids method.")
            try:
                emb_id_int = int(emb_id) if isinstance(emb_id, int) or (isinstance(emb_id, str) and emb_id.isdigit()) else abs(hash(emb_id)) % (2**63)
            except Exception:
                emb_id_int = abs(hash(str(emb_id))) % (2**63)
            try:
                # Use positional arguments only, as required by FAISS
                faiss_index.add_with_ids(vec, np.array([emb_id_int], dtype="int64"))
            except Exception as e:
                logger.error(f"[FAISS] add_with_ids failed: {e}")
                return
        elif hasattr(faiss_index, 'add') and callable(getattr(faiss_index, 'add', None)):
            logger.info(f"[FAISS] Using add method.")
            try:
                # Use positional arguments only, as required by FAISS
                faiss_index.add(vec)
            except Exception as e:
                logger.error(f"[FAISS] add failed: {e}")
                return
        else:
            logger.error(f"[FAISS] Index object missing valid 'add' or 'add_with_ids' method. Type: {type(faiss_index)}")
            return
        faiss.write_index(faiss_index, FAISS_INDEX_PATH)  # type: ignore
        logger.info(f"[FAISS] Added {emb_id}")
    except Exception as e:
        logger.error(f"[FAISS] Add failed for {emb_id}: {e}")
def get_index_info():
    """Return diagnostic info about FAISS and Chroma index types and available methods."""
    info = {}
    # FAISS
    if 'faiss_index' in globals() and faiss_index:
        info['faiss_type'] = str(type(faiss_index))
        info['faiss_methods'] = dir(faiss_index)
    else:
        info['faiss_type'] = None
        info['faiss_methods'] = []
    # Chroma
    if 'collection' in globals() and collection:
        info['chroma_type'] = str(type(collection))
        info['chroma_methods'] = dir(collection)
    else:
        info['chroma_type'] = None
        info['chroma_methods'] = []
    return info

# --- Model Loading (Resilient) ---
model = None
if SentenceTransformer:
    try:
        model = SentenceTransformer(EMBED_MODEL)
        logger.info(f"[EMBEDDER] Loaded model: {EMBED_MODEL}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Model load failed: {e}")
        model = None
else:
    logger.error("[EMBEDDER] SentenceTransformer unavailable; using fallback")

memory_vectors = {}

# --- Core Embedding Functions ---
def embed_text(text):
    if not model:
        logger.error("[EMBEDDER] No model; returning zero-vector")
        return np.zeros(DIMENSION, dtype="float32")
    try:
        vec = model.encode(text, convert_to_numpy=True)
        logger.debug(f"[EMBEDDER] Embedding norm: {np.linalg.norm(vec):.4f}")
        return vec
    except Exception as e:
        logger.error(f"[EMBEDDER] Embedding failed: {e}")
        return np.zeros(DIMENSION, dtype="float32")

def package_embedding(text, vector, meta):
    emb_id = str(uuid.uuid4())
    if not isinstance(meta, dict):
        logger.warning(f"[EMBEDDER] meta not dict; got {type(meta)}; coercing")
        meta = {"source": str(meta)}
    embedding = {
        "id": emb_id,
        "text": text,
        "embedding": vector.tolist() if hasattr(vector, "tolist") else list(vector),
        "meta": meta,
        "created": datetime.now(timezone.utc).isoformat(),
        "source": meta.get("source", "system"),
        "model": EMBED_MODEL,
        "replaceable": True,
    }
    if USE_FAISS:
        add_to_faiss(vector, emb_id)
    if USE_CHROMA:
        add_to_chroma(text, emb_id, vector, meta)
    memory_vectors[emb_id] = embedding
    try:
        _write_to_disk(embedding)
        logger.info(f"[EMBEDDER] Stored embedding: {emb_id}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Disk write failed for {emb_id}: {e}")
    return embedding

def archive_plan(vector_path="data/nlp_training_sets/auto_generated.jsonl"):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    archive = os.path.join("GremlinGPT", "docs", f"planlog_{stamp}.jsonl")
    try:
        shutil.copyfile(vector_path, archive)
        logger.info(f"[EMBEDDER] Plan archived: {archive}")
        return archive
    except Exception as e:
        logger.error(f"[EMBEDDER] Archive failed: {e}")
        return None

def auto_commit(file_path):
    if not file_path or not os.path.exists(file_path):
        logger.warning(f"[EMBEDDER] auto_commit: invalid path {file_path}")
        return
    try:
        os.system(f"git add {file_path}")
        os.system(f'git commit -m "[autocommit] Updated: {file_path}"')
        logger.info(f"[EMBEDDER] auto_commit succeeded for {file_path}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Git commit failed: {e}")

def get_all_embeddings(limit=50):
    if not memory_vectors:
        _load_from_disk()
    return list(memory_vectors.values())[:limit]

def get_embedding_by_id(emb_id):
    if emb_id not in memory_vectors:
        _load_from_disk()
    return memory_vectors.get(emb_id)

def _write_to_disk(embedding):
    try:
        path = os.path.join(LOCAL_INDEX_PATH, f"{embedding['id']}.json")
        with open(path, "w") as f:
            json.dump(embedding, f, indent=2)
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to write {embedding['id']} to disk: {e}")

def _load_from_disk():
    if not os.path.isdir(LOCAL_INDEX_PATH):
        logger.warning(f"[EMBEDDER] Local index missing: {LOCAL_INDEX_PATH}")
        return
    for fname in os.listdir(LOCAL_INDEX_PATH):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(LOCAL_INDEX_PATH, fname)
        try:
            with open(fpath, "r") as f:
                emb = json.load(f)
            memory_vectors[emb["id"]] = emb
        except Exception as e:
            logger.warning(f"[EMBEDDER] Failed to load {fname}: {e}")

def get_memory_graph():
    if not memory_vectors:
        _load_from_disk()
    nodes, edges = [], []
    for emb in memory_vectors.values():
        nodes.append({
            "id": emb["id"],
            "label": emb["meta"].get("label", emb["text"][:24] + "..."),
            "group": emb["meta"].get("source", "system"),
        })
        if "source_id" in emb["meta"]:
            edges.append({"from": emb["meta"]["source_id"], "to": emb["id"]})
    return {"nodes": nodes, "edges": edges}

def repair_index():
    memory_vectors.clear()
    _load_from_disk()
    logger.info("[EMBEDDER] Index repaired")

def inject_watermark(origin="unknown"):
    text = f"Watermark from {origin} @ {datetime.now(timezone.utc).isoformat()}"
    vector = encode(text)
    meta = {"origin": origin, "timestamp": datetime.now(timezone.utc).isoformat()}
    return package_embedding(text, vector, meta)

# --- Initial Load ---
try:
    _load_from_disk()
    logger.info("[EMBEDDER] Initial disk load complete")
except Exception as e:
    logger.error(f"[EMBEDDER] Initial load failed: {e}")
