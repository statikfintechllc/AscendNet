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

# FSM Architecture: GremlinGPT v1.0.3

---

## Overview

GremlinGPT uses a **modular Finite State Machine (FSM)** to orchestrate agent operations, task execution, memory embedding, retry/rollback, and self-improving logic.  
The FSM is fully autonomous, offline, and tightly integrated with planner, persistent vector memory, agent feedback, and mutation/recovery.

---

## Key Components

| File                               | Role                                         |
|-------------------------------------|----------------------------------------------|
| `fsm.py`                           | Main FSM loop + scheduling                   |
| `task_queue.py`                    | Persistent task queue with retry/priorities  |
| `tool_executor.py`                 | Executes tools for each task type            |
| `heuristics.py`                    | Evaluates which tasks to run/skip            |
| `error_log.py`                     | Records failure, retries, error tracking     |
| `planner_agent.py`                 | Autonomous planner, enqueues next tasks      |
| `watcher.py`                       | Mutation/retrain watcher for FSM changes     |

---

## FSM States

```text
[IDLE] <-> [RUNNING] <-> [WAITING]
```

- FSM begins in [IDLE], transitions to [RUNNING] if tasks are queued.
- In [RUNNING], executes tasks via heuristic/task logic.
- [WAITING] for I/O, external events, or mutation (rare).
- When task queue depletes, FSM calls planner_agent.enqueue_next() for autonomous re-seeding.

⸻

## Loop Flow

**1. Queue Read**
- Pulls next task: task_queue.get_next()
- If empty, FSM idles.

**2. Heuristic Evaluation**
- Run task through evaluate_task(task)
- Skips if context/conditions not met.

**3. Dispatch**
- Calls execute_tool(task), which may run:
- Scraper (scraper_loop)
- Signal generator (trading_core)
- NLP encoder/transformer
- Self-training feedback
- Raw shell commands

**4. Logging + Retry**
- On failure: logs to error_log.py, retries up to config limit.
 
**5. Memory Update**
- All outputs/results are embedded via package_embedding()
- Embedding metadata includes task type, semantic context, mutation flag, timestamp.
- Persisted to memory/local_index/documents/ and cross-indexed in metadata DB.

⸻

## Task Types

## 🧠 Task Type ↔️ System Handler Map

| **Type**       | **Handled By**                                     |
|----------------|----------------------------------------------------|
| `scrape`       | `get_dom_html()` from `scraper_loop.py`            |
| `signal_scan`  | `generate_signals()` from `trading_core/`          |
| `nlp`          | `transformer_core.encode()`                        |
| `self_train`   | `feedback_loop.inject_feedback()`                  |
| `shell`        | `agent_shell.run_shell_command()`                  |

⸻

## Scheduling

- FSM can be launched:
- Direct CLI (python fsm.py)
- Background schedule (run_schedule(), every 30s)
- Integrated via start_all.sh
- Each FSM pass checks and executes tasks, then idles or re-seeds via planner.
- Designed for 24/7 daemon operation.

⸻

## Autonomy & Resilience

- FSM restart state and queue stored in state_snapshot.json.
- On crash: reboot_recover.sh reloads task queue and memory, resumes loop.
- Each tool call logs results and embeddings persistently for full recovery.

⸻

## Mutability

- FSM behavior monitored by self_mutation_watcher/watcher.py.
- If fsm.py, heuristics.py, or rules_engine.py are changed:
- Code diff is stored in vector memory
- Retrain trigger is set in checkpoints/retrain_trigger.json
- trainer.py loads mutated logs, regenerates/retrains NLP dataset

⸻

## Example Task Cycle

```json
{
  "type": "scrape",
  "target": "https://www.sec.gov/filings"
}
```

- FSM picks up the task → runs scraper → stores DOM HTML → embeds in memory → logs result.

⸻

## Self-Planning Logic

- When task queue is empty, FSM auto-calls planner_agent.enqueue_next()
- Uses reward memory to choose next most effective actions
- Embeds all new plan steps in vector memory, enabling recursive improvement

⸻

## Mutation Awareness

- Any changes to FSM logic (e.g., fsm.py, heuristics) trigger:
- Code diff via watcher.py
- Diff/patch embedded in memory vector store
- Retrain trigger for the feedback loop (retrain_trigger.json)
- Trainer ingests mutated logs and updates NLP/decision models
- FSM continues running with latest, most effective heuristics and logic

⸻

##Conclusion

- GremlinGPT’s FSM core is built for resilience, autonomy, and memory-driven evolution.
- It doesn’t just execute scripts—it learns, adapts, and rewrites itself to improve over time.
- The FSM loop is the recursive intelligence core that powers true autonomous operation.





