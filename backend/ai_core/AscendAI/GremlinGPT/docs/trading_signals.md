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

# Trading Signals — GremlinGPT v1.0.3

---

## Overview

The `trading_core/` subsystem is a modular, fully local engine for **penny stock discovery, signal analysis, and event generation**.  
It operates autonomously, writes all signals to vector memory, and directly integrates with GremlinGPT’s agent loop, planning, and self-training pipelines.

Goal: **Produce precise, explainable, and actionable trading signals (sub-$10/share) — every signal tagged, traceable, and used for AI self-reinforcement.**

---

## Modules

| File                        | Description                                        |
|-----------------------------|----------------------------------------------------|
| `signal_generator.py`       | Generates and embeds trading signals (core logic)  |
| `stock_scraper.py`          | Fetches live/simulated penny stock data            |
| `rules_engine.py`           | Detects EMA/VWAP/volume breakouts                  |
| `portfolio_tracker.py`      | Stores and logs open/closed positions              |
| `tax_estimator.py`          | Calculates U.S. capital gains and tax estimates    |

---

## Pipeline Flow

```plaintext
[stock_scraper.py]
    ↓
[rules_engine.py]
    ↓
[signal_generator.py]
    ↓
[memory/vector_store/embedder.py]
    ↓
[memory/local_index/metadata.db] + [vector_store/faiss/] or [chroma/]
```

---

## Embedding Signals Into Memory

### Process Overview

Each signal is embedded and stored via the following steps:

1. **Vectorization**  
   - Encoded using MiniLM  
   - Modules involved: `semantic_score.py`, `embedder.py`  

2. **Tagging and Persistence**  
   - Passed to `package_embedding()`  
   - Stored with relevant metadata and labels  

3. **Storage Backends**  
   - Default: `memory/vector_store/faiss/`  
   - Optional: ChromaDB backend  

---

### Sample Signal Metadata

```json
{
  "type": "signal",
  "strategy": "EMA_crossover",
  "source": "trading_core",
  "agent_id": "planner001",
  "timestamp": "2025-05-18T13:22:00Z"
}
```

---

### Signal Access Points

- **MemoryGraph**: Visualized in the UI dashboard  
- **`agents/planner_agent.py`**: Used for decision-making logic  
- **`self_training/generate_dataset.py`**: Used in retraining pipelines  

---

## Real-Time Signal Refresh

- **Frontend Component**: `TradingPanel.js`  
- **Polling Endpoint**: `/api/trading/signals`  
- **Frequency**: Every 0.2 seconds (configurable)  
- **Live Update**: Signals automatically refresh and populate dashboard  
- **Color Coding**:  
  - Gold: High-confidence  
  - Silver: Moderate-confidence  

---

---

## FSM / Agent Integration

The FSM enqueues:

```json
{ "type": "signal_scan" }
```

Which triggers:
- `fsm.py` → calls `generate_signals()`
- All resulting signals are:
  - Embedded into memory
  - Logged for audit
- High-confidence signals are passed to `planner_agent.py` for deeper reasoning

---

## NLP Feedback Loop

Failed or misfired signals (e.g., bad prediction, wrong trend) trigger a feedback cascade:

1. Failure logged in: `data/logs/bootstrap.log`  
2. Feedback flagged in: `self_training/feedback_loop.py`  
3. Sample added to: `self_training/generate_dataset.py` output  
4. Model retrained via: `self_training/trainer.py`  

This creates a continuous retraining loop based on performance.

---

## Tax Estimation Logic

When positions are closed in `portfolio_tracker.py`, the `tax_estimator.py` module:

- Distinguishes **long-term vs. short-term** holdings  
- Calculates **cost basis** and **capital gains**  
- Flags **taxable events**  
- Logs structured events to memory for audit

**Example:**

```json
{
  "symbol": "BBIG",
  "action": "SELL",
  "profit": 52.30,
  "term": "short",
  "taxable": true,
  "timestamp": "2025-05-18T13:30:01Z"
}
```

---

## Fault Tolerance

System fallback logic ensures resilience:

- If **live scraping fails** → fallback to Playwright or simulated screener  
- If **external data is unavailable** → fallback to synthetic data from `stock_scraper.py`  
- **FSM** checks scraper health every 5 seconds for auto-recovery

---

## Summary

`trading_core/` is built for:

- **Penny/Momentum Trading** (Stocks <$10)  
- **Offline-first** signal generation  
- **Vector-tagged signals** for traceability  
- **Autonomous feedback loop** for continuous learning  

Every **win** = reinforcement  
Every **loss** = mutation  
Every **signal** = memory

---
