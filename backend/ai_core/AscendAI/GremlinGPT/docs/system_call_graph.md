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

# GremlinGPT System Flow v1.0.3

## Full Pipeline Graph — Autonomous + NLP-Aware + Mutation-Safe

## 🧠 Core System Flow

```plaintext
             ┌────────────────────────────┐
             │     generate_dataset.py    │
             └────────────▲───────────────┘
                          │
                    trainer.py
                          ▲
              ┌──────── transformer_core.py ◄────────┐
              │                   ▲                  │
         pos_tagger.py           │             parse_nlp()
              ▲                  │                   ▲
      tokenizer.py ◄─────────────┴─────┐      semantic_score.py
              ▲                        │               ▲
        commands.py ◄──── chat_handler.py ──────► embedder.py ◄────┐
              │                  ▲                 ▲               │
              │                  │         feedback_loop.py        │
              │                  │                 ▲               │
              ▼                  ▼                 │               │
       planner_agent.py ◄────── router.py ◄────────┘               │
              │                  ▲                                 │
              │             server.py                              │
              ▼                                                    │
        task_queue.py ◄───────────── fsm.py ◄──────────────┐       │
              ▲                     │                      │       │
              │                     ▼                      ▼       │
  update_position()         tool_executor.py ───────→ shell_executor.py
              ▲                     │                      ▲       │
  portfolio_tracker.py              │                      │       │
              ▲                     ▼                      │       │
  TradingPanel.js ─────────→ signal_generator.py           │       │
                                  │                        │       │
                                  ▼                        │       │
                         rules_engine.py         log_event + retry │
                                  ▲                                │
                    get_live_penny_stocks()                        │
                                  ▲                                │
                        stock_scraper.py ◄──── scraper_loop.py ◄───┘
                                  ▲                    ▲
                                  │                    │
                     psutil → tws_handler.py     playwright_handler.py
                                  ▲                    ▲
                                  └───── dom_navigator.py ◄──── page_simulator.py

                                          │
                                          ▼
                                  vector_store/memory
```


⸻

GremlinGPT Full Script Call Graph (Fully Extended, v1.0.3)

Core Python Nodes
	•	backend/server.py
	•	backend/router.py
	•	backend/scheduler.py
	•	backend/state_manager.py
	•	backend/api/chat_handler.py
	•	backend/api/memory_api.py
	•	backend/api/scraping_api.py
	•	backend/api/planner.py
	•	backend/interface/commands.py
	•	memory/vector_store/embedder.py
	•	memory/log_history.py
	•	memory/local_index/metadata.db
	•	nlp_engine/tokenizer.py
	•	nlp_engine/transformer_core.py
	•	nlp_engine/semantic_score.py
	•	nlp_engine/pos_tagger.py
	•	nlp_engine/diff_engine.py
	•	nlp_engine/parser.py
	•	nlp_engine/mini_attention.py
	•	agent_core/task_queue.py
	•	agent_core/fsm.py
	•	agent_core/heuristics.py
	•	agent_core/error_log.py
	•	executors/python_executor.py
	•	executors/shell_executor.py
	•	executors/tool_executor.py
	•	scraper/scraper_loop.py
	•	scraper/playwright_handler.py
	•	scraper/dom_navigator.py
	•	scraper/page_simulator.py
	•	trading_core/signal_generator.py
	•	trading_core/stock_scraper.py
	•	trading_core/rules_engine.py
	•	trading_core/portfolio_tracker.py
	•	trading_core/tax_estimator.py
	•	self_mutation_watcher/watcher.py
	•	self_mutation_watcher/diff_engine.py
	•	self_mutation_watcher/mutation_daemon.py
	•	self_training/feedback_loop.py
	•	self_training/generate_dataset.py
	•	self_training/mutation_engine.py
	•	self_training/trainer.py
	•	core/loop.py
	•	core/kernel.py
	•	core/snapshot.py
	•	run/ngrok_launcher.py
	•	run/module_tracer.py

UI/Frontend Nodes
	•	frontend/app.js
	•	frontend/components/ChatInterface.js
	•	frontend/components/MemoryGraph.js
	•	frontend/components/TaskTreeView.js
	•	frontend/components/TradingPanel.js

⸻

Key Connections
	•	server.py → router.py
	•	router.py → chat_handler.py, planner.py, scraping_api.py, memory_api.py
	•	chat_handler.py → commands.py, tokenizer.py, transformer_core.py, embedder.py
	•	planner.py → signal_generator.py, task_queue.py
	•	signal_generator.py → stock_scraper.py, rules_engine.py, embedder.py
	•	memory_api.py → embedder.py
	•	scraping_api.py → task_queue.py
	•	fsm.py → task_queue.py, tool_executor.py, heuristics.py
	•	tool_executor.py → scraper_loop.py, feedback_loop.py, transformer_core.py, signal_generator.py, shell_executor.py
	•	shell_executor.py → subprocess, logger, embedder.py
	•	python_executor.py → subprocess, embedder.py
	•	feedback_loop.py → embedder.py
	•	trainer.py → feedback_loop.py, mutation_engine.py, generate_dataset.py
	•	scraper_loop.py → playwright_handler.py, page_simulator.py, dom_navigator.py, embedder.py
	•	page_simulator.py → dom_navigator.py, embedder.py
	•	app.js → ChatInterface.js, MemoryGraph.js, TaskTreeView.js, TradingPanel.js
	•	TradingPanel.js → planner.py
	•	TaskTreeView.js → fsm.py, embedder.py
	•	MemoryGraph.js → memory_api.py
	•	commands.py → embedder.py, parse_nlp()
	•	parse_nlp() → tokenizer.py, pos_tagger.py, transformer_core.py
	•	portfolio_tracker.py → embedder.py, TradingPanel.js

⸻

Additional System Pathways (Startup/Mutation/Training)
	•	core/loop.py → boots FSM, mutation_daemon, retraining trigger
	•	core/kernel.py → handles patching, safe rollback, embedding code changes
	•	core/snapshot.py → versioned code snapshot, diff, rollback, memory storage
	•	self_training/trainer.py → watchdog loop, dataset generation, model checkpointing
	•	self_mutation_watcher/watcher.py → persistent file monitoring, triggers diff and feedback
	•	run/ngrok_launcher.py → launches ngrok tunnel, outputs QR and live URL
	•	run/module_tracer.py → trace and print live call graph for debugging

⸻

Summary

GremlinGPT’s architecture is built for:
	•	Autonomous Task Execution: Via fsm.py, tool_executor.py, and task_queue.py
	•	Deep Memory: All outputs, failures, diffs, and logic are vectorized and stored for recall/replanning.
	•	Mutation & Self-Improvement: Code/data feedback loops, retraining, safe patching, and snapshot-based rollback.
	•	Production Web UI: Responsive dashboard, live chat, memory/task/trading visualizations — fully offline/remote with ngrok integration.

Every module is tracked, every call is loggable, and every mutation is replayable.
