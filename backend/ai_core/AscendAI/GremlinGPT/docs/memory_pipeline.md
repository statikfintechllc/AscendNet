<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/GremlinGPT-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

  <div align="center">
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>
</div>

# Memory Pipeline — GremlinGPT v1.0.3

---

## Purpose

The memory subsystem is GremlinGPT’s **vectorized long-term memory**, storing:

- Web scrapes and DOM content
- Trading signal outputs
- Task plans, priorities, and results
- Code diffs and NLP deltas
- Retrain triggers and mutation feedback

Memory is designed for:
- Fast semantic retrieval
- Continuous learning via vector deltas
- High-granularity tagging and lineage tracking
- **Dynamic backend switching (FAISS ↔ ChromaDB)**
- **Runtime configuration via dashboard/API**

Embeddings are 384-dim float32 vectors (MiniLM-L6-v2) optimized for local FAISS/Chroma indexing.

**Recent Updates:**
- Fixed FAISS method signature compatibility
- Added dynamic backend selection
- Implemented real-time switching via API endpoints

---

## Architecture

The memory stack flows as:

```text
Raw Text
↓
SBERT MiniLM
↓
embed_text()
↓
package_embedding()
↓
➤ Tags + Metadata
↓
➤ Vector Store (FAISS / Chroma)
↓
➤ metadata.db (SQLite) + /documents/
```

---

### Core Layers

- `embed_text()` – encodes all agent and DOM input
- `package_embedding()` – stores vector + metadata, auto-tags
- `inject_watermark()` – marks memory state transitions for traceability
- `faiss/` or `chroma/` – backend vector DB (selected in config)
- `metadata.db` – searchable context, lineage, tags

---

## Configuration

Memory behavior is controlled by:

- `config/config.toml` → `[memory]` (main settings)
- `config/memory_settings.json` → runtime overrides for dev/debug

#### Sample `memory_settings.json`
```json
{
  "vector_backend": "faiss",
  "embedding_dim": 384,
  "auto_index": true,
  "storage": {
    "vector_store_path": "./memory/vector_store/faiss/",
    "metadata_db": "./memory/local_index/metadata.db"
  }
}
```

⸻

Embedding & Tagging

Each memory entry contains:
	•	embedding: 384-dim vector from MiniLM-L6-v2
	•	text: Source text or system summary
	•	meta: Dictionary with semantic keys
	•	tags: Source, purpose, and model lineage

Example:

```json
{
  "id": "abc123",
  "text": "Planned task: scrape SEC filings",
  "embedding": [0.123, 0.991, ...],
  "meta": {
    "agent": "planner_agent",
    "task_type": "scrape",
    "timestamp": "2025-05-18T13:22:01Z"
  },
  "tags": {
    "source": "planner",
    "model": "MiniLM",
    "replaceable": true
  }
}
```

⸻

## Embedder Logic

*Located in memory/vector_store/embedder.py*
- Loads MiniLM-L6-v2 with SentenceTransformer
- Embeds all agent/DOM/task/NLP payloads
- Saves as .json per vector in local_index/documents/
- Updates FAISS index or Chroma collection (per config)

### Main functions:
- embed_text(text)
- package_embedding(text, vector, meta)
- inject_watermark(origin="...")

⸻

## Auto Indexing

*If auto_index = true in config, the following sources are always embedded:*
- DOM content from scraper_loop.py
- Trading signals from signal_generator.py
- Task plans and rationale from planner_agent.py
- Mutations and code diffs from watcher.py
- Shell/NLP command results

⸻

## Semantic Search

*Semantic queries are performed using:*
- Cosine similarity via semantic_score.py
- Configurable threshold (similarity_threshold, default 0.75)
- semantic_boost flag can enhance context window

## Matched results can:

- Trigger new tasks or re-scrapes
- Seed planner logic in planner_agent.py
- Feed self-train loops via generate_dataset.py

⸻

Backends

| Backend | Type | Use Case                          |
|---------|------|-----------------------------------|
| FAISS   | CPU  | Fastest, default, fully local     |
| Chroma  | JSON | Persistent, dev-friendly fallback |

*Selected in [memory] section of config.toml:*
```toml
[memory]
vector_backend = "faiss"
embedding_dim = 384
auto_index = true
```

⸻

## Mutation Awareness

*When FSM, planner, or kernel code is mutated:*
- Code diff is generated via diff_engine.py

*Stored as:*

```json
{
  "type": "code_diff",
  "origin": "self_mutation_watcher",
  "text": "<unified diff>",
  "embedding": [ ... ],
  "meta": {
    "semantic_score": 0.41,
    "lineage_id": "uuid",
    "timestamp": "..."
  }
}
```

- Diffs are used to generate self_train tasks and new datasets (generate_dataset.py).

⸻

## Snapshot & Rollback

- Periodic dumps of vector/metadata state (controlled by snapshot_interval_min in config)
- All memory snapshots stored under run/checkpoints/snapshots/
- Rollback and failover with reboot_recover.sh
- Old backups auto-rotated and versioned

⸻

## Integrated Modules

## 🧩 Module Breakdown

| Module             | Role                                              |
|--------------------|---------------------------------------------------|
| `chat_handler.py`  | Retrieves context from memory for responses       |
| `planner_agent.py` | Picks next task using reward + memory scan        |
| `diff_engine.py`   | Stores semantic/code deltas, triggers training    |
| `feedback_loop.py` | Logs retrain triggers to memory                   |
| `tool_executor.py` | Embeds tool results and signals                   |
| `mutation_daemon.py` | Monitors code for drift, vector deltas         |

⸻

## Logging & Watermarking

*Watermarking:*
- Tags all mutation-aware embeddings and transitions
- Marks FSM or kernel patch events
- Leaves clear source:GremlinGPT lineage metadata

### Example:

```json
{
  "origin": "fsm_loop",
  "timestamp": "2025-05-18T13:26:44Z",
  "watermark": "source:GremlinGPT"
}
```

⸻

## Conclusion

The memory engine enables GremlinGPT to:
- Learn and reason from all past actions
- Replan based on reward/mutation lineage
- React autonomously to environment or self-changes
- Retrain its models directly from mutation logs

> This is not just storage—it’s the core of long-term cognition, replayable reasoning, and evolutionary AI state.
