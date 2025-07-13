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

# GremlinGPT Autonomous Shell Flow — v1.0.3

GremlinGPT operates a **self-mutating, autonomously routed FSM loop** with embedded vector memory, semantic safety, mutation self-healing, and live planner feedback, beginning from a single kernel call.

---

## Boot Sequence Overview

### **Primary Loop Path**

1. **core/loop.py** starts:
   - `fsm.py`: Main finite state machine loop (task exec, agent role assignment)
   - `mutation_daemon.py`: Self-mutation and rollback watcher
   - Dataset generator (for self-training and log snapshotting)
2. **fsm.py**:
   - Dequeues tasks from persistent memory/task queue
   - Assigns agent roles; executes or escalates based on logic, confidence, or error rate
   - Logs events, embeds memory, manages reward/incentive
3. **tool_executor.py**:
   - Executes agent tools: `nlp`, `signal_scan`, `scrape_live`, `shell`
   - Invokes `shell_executor.py` for raw shell commands when needed
   - Embeds all results via `embedder.py`
   - Logs execution and trace to `log_history.py`
4. **reward_model.py**:
   - Scores execution results and code quality
   - Drives planner incentives via vector similarity/feedback
5. **planner_agent.py**:
   - Reviews recent reward memory and system state
   - Enqueues new tasks autonomously (vector sim, memory triggers)
   - Embeds all planning rationale, injects watermarks for lineage tracking
6. **If file/code is mutated**:
   - `watcher.py` detects file deltas
   - `diff_engine.py` computes AST/semantic diff for patch validation
   - `embedder.py` packages mutation, diff, and watermark into memory
   - `feedback_loop.py` may trigger retraining/rollbacks if needed
7. **If confidence drops**:
   - `mutation_daemon.py` can rollback recent mutations with low semantic integrity
   - `trainer.py` retrains with mutation lineage and feedback logs
8. **Loop cycles forward**, driven by memory, embeddings, reward, and watermark lineage.

---

## Autonomous Mutation Safety

**All code mutations must pass these gates before execution:**

| Check       | Rule                                  |
|-------------|---------------------------------------|
| Syntax      | Verified with `ast.parse()`           |
| Semantic    | Must pass cosine similarity > 0.60    |
| Patch Test  | Executes code with `run_patch_test()` |
| Watermark   | All patches logged with lineage mark  |
| Snapshot    | Rolled back if semantic loss detected |

- Snapshots and versioning stored in:  
  `run/checkpoints/snapshots/`

---

## Mutation Path (Kernel)

**When planner chooses to patch code:**

1. `planner_agent.py` invokes `kernel.py`
2. `kernel.py`:
    - Validates syntax, runs `ast.parse`
    - Backs up the original file via `snapshot.py`
    - Applies mutation and writes new code
    - Computes semantic + vector delta
    - Calls `package_embedding()` to persist patch and lineage
    - Injects watermark for audit
3. Triggers model retraining via `feedback_loop.py` as needed

---

## Scraper Integration (Live + DOM)

- **Sources:**  
  - TWS/STT: via `psutil_check()` for running broker terminals  
  - Browser scraping: `playwright_handler.py`  
  - DOM navigation/mapping: `dom_navigator.py`
- **Storage:**  
  - `store_stock_snapshot()` embeds asset vectors and metadata
  - `signal_generator.py` applies signal/reward logic to scan outputs
- **Refresh:**  
  - Live data refreshed every 5 seconds via scheduler/async

---

## Memory & Watermarking

All vectorized memory, tasks, and code mutations are processed through:

- `embed_text()`: NLP/code/state vectorization
- `package_embedding()`: Memory persist with full metadata
- `inject_watermark()`: Tags all data/mutations with lineage, agent, and timestamp

**Watermarks ensure:**
- Full memory traceability
- Autonomous lineage and mutation validation
- Accountability for every patch, plan, and task

---

## Execution Environment Map

| Component           | Role                               |
|---------------------|------------------------------------|
| gremlin-orchestrator| FSM loop, kernel patcher            |
| gremlin-nlp         | Transformers, scoring, NER          |
| gremlin-memory      | Vector storage, retrieval           |
| gremlin-scraper     | DOM/data ingestion, stock streams   |
| gremlin-dashboard   | Full-stack UI + REST interface      |

---

## Startup Flow

```bash
conda activate gremlin-orchestrator
python3 core/loop.py
```

**To reboot from last state:**

```bash
./reboot_recover.sh
```

⸻

## Core Logs + Datasets

| **Purpose**         | **File / Path**                                  |
|---------------------|--------------------------------------------------|
| Execution Events    | `data/logs/history/gremlin_exec_log.jsonl`       |
| Reward Scores       | `data/logs/rewards.jsonl`                        |
| Mutation Embeds     | `data/nlp_training_sets/live_mutations.jsonl`    |
| Portfolio           | `data/portfolio.json`, `trade_history.jsonl`     |
| Snapshots           | `run/checkpoints/snapshots/`                     |
| Runtime Log         | `run/logs/runtime.log`                           |
