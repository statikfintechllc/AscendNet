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

# Self-Training Architecture — GremlinGPT v1.0.3

---

## Overview

GremlinGPT self-evolves through a **recursive mutation and retraining loop** that monitors code diffs, detects low-confidence or failed outputs, and retrains its NLP engine from its own logs and code feedback. This forms the backbone of autonomous self-improvement.

The goal is a system that:
- Observes and logs its own behavior and code state
- Detects weak, broken, or degraded logic
- Mutates or retrains itself with new data
- Embeds feedback and mutation history into long-term vector memory

---

## Core Modules

| File                           | Purpose                                            |
|--------------------------------|----------------------------------------------------|
| `self_mutation_watcher/watcher.py` | Monitors code/config changes and triggers diffs |
| `self_training/feedback_loop.py`   | Raises retrain flags via retrain_trigger.json   |
| `self_mutation_watcher/mutation_daemon.py` | Alters code/tasks during retrain planning |
| `self_training/generate_dataset.py` | Extracts failure/diff events to JSONL dataset  |
| `self_training/trainer.py`         | Runs retrain loop and updates NLP weights      |
| `self_mutation_watcher/diff_engine.py` | Calculates semantic/code delta and vector shift |
| `agents/planner_agent.py`          | Chooses next task strategies post-retrain      |
| `memory/vector_store/embedder.py`  | Embeds every diff/feedback/signal into memory  |
| `agent_core/tool_executor.py`      | Executes self_train and propagates retrain     |

---

## Training Trigger Logic

Self-training can be triggered by:

1. **Code Mutations**  
   - Detected in monitored logic files:
     - `fsm.py`
     - `rules_engine.py`
     - `heuristics.py`
     - Any file listed in watcher config

2. **Semantic Drift**  
   - Embedding delta or confidence < 0.70

3. **Explicit Task**  
   - Manual queue:
   - 
     ```json
     { "type": "self_train" }
     ```

4. **Feedback Injection**  
   - FSM/task failure
   - Output from `shell_executor.py`
   - Reward model score < threshold

---

## Watcher Loop

The watcher continuously monitors all key files for changes.

#### Key Snippet

```python
if current != previous:
    diff = generate_diff(previous, current)
    vector = embed_text(diff)
    package_embedding(diff, vector, meta={...})
    inject_feedback()
```

- All diffs, confidence drops, or failures are embedded and stored as memory.
- feedback_loop.py then sets a retrain trigger.

⸻

## Feedback Trigger File

*Location:*

run/checkpoints/retrain_trigger.json

**Example contents:**

```json
{
  "trigger": "mutation_watcher",
  "time": "2025-05-18T13:11:00Z",
  "note": "Auto-diff-based training cycle"
}
```

- This is polled by trainer.py.

⸻

## Dataset Generation

**generate_dataset.py pulls from:**
- Log files: data/logs/*.log
- Code diffs (tagged as "type": "code_diff")
- Failed embeddings
- Skipped or low-rewarded tasks

*Sample Output:*

```json
{
  "input": "Task failed to scrape",
  "output": "Rewritten task with URL fix"
}
```

**Output file:**

data/nlp_training_sets/auto_generated.jsonl

⸻

## NLP Retraining

- NLP model based on MiniLM (sentence-transformers)
- Tokenization via local tokenizer
- Executes checkpoint update to transformer core
- Embedded retrain results are tagged:

```json
"replaceable": false
```

**Lineage metadata embedded:**

```json
{
  "source": "GremlinGPT_v4_train",
  "epoch": 2,
  "confidence_gain": 0.13
}
```

⸻

## Reward Model

*tools/reward_model.py scores outcome: (pass/fail/signal strength)*
- Ranks task types and next priority
- Fully pluggable, all scores tracked in memory and logs

⸻

## Mutation Execution

FSM observes diffs through watcher:
	1.	diff_engine.py computes semantic/code delta
	2.	embedder.py packages diff into memory with tags
	3.	feedback_loop.py sets retrain_trigger.json
	4.	trainer.py runs local retraining and checkpoint update

*In progress:*

- kernel.py for safe mutation/rollback
- snapshot.py for versioning/rollback of codebase
- core/loop.py for FSM mutation lifecycle

⸻

## Logging & Auditing

*All mutation and retrain logs are written to:*
- data/logs/bootstrap.log
- data/nlp_training_sets/bootstrap.json
- All embeddings (diffs, feedback, retrain events) are visible in vector memory and dashboard graphs.

⸻

## Summary

GremlinGPT doesn’t just log or retry failures — it learns and rewires itself from every misstep.

This self-training loop is the core of its autonomy. Every code change, signal, or bad scrape becomes a lesson, automatically embedded and replayed for the next round.

> GremlinGPT is not statically coded — it rewrites itself.


