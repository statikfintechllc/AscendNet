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

# GremlinGPT v1.0.3 – Full Structure Tree (2025)

*This tree reflects the current, fully-wired, state-of-the-art GremlinGPT system, including all analytics, dashboard, trading, and self-healing logic.*

```text
GremlinGPT/
│
├── __init__.py
├── install.sh
├── reboot_recover.sh
│
├── agents/
│   └── planner_agent.py
│
├── agent_core/
│   ├── agent_profiles.py
│   ├── agent_profiles.yaml
│   ├── error_log.py
│   ├── fsm.py
│   ├── heuristics.py
│   └── task_queue.py
│
├── backend/
│   ├── __init__.py
│   ├── api/
│   │   ├── api_endpoints.py
│   │   ├── chat_handler.py
│   │   ├── memory_api.py
│   │   ├── planner.py
│   │   └── scraping_api.py
│   ├── globals.py
│   ├── interface/
│   │   └── commands.py
│   ├── router.py
│   ├── scheduler.py
│   ├── server.py
│   ├── state_manager.py
│   └── utils/
│       └── git_ops.py
│
├── conda_envs/
│   ├── create_envs.sh
│   ├── gremlin-dashboard.yml
│   ├── gremlin-dashboard_requirements.txt
│   ├── gremlin-memory.yml
│   ├── gremlin-memory_requirements.txt
│   ├── gremlin-nlp.yml
│   ├── gremlin-nlp_requirements.txt
│   ├── gremlin-orchestrator.yml
│   ├── gremlin-orchestrator_requirements.txt
│   ├── gremlin-scraper.yml
│   └── gremlin-scraper_requirements.txt
│
├── config/
│   ├── config.toml
│   └── memory.json
│
├── core/
│   ├── kernel.py
│   ├── loop.py
│   └── snapshot.py
│
├── data/
│   ├── embeddings/
│   ├── logs/
│   │   ├── .gitkeep
│   │   ├── backend.out
│   │   ├── bootstrap.log
│   │   ├── dash_cli.log
│   │   ├── frontend.out
│   │   ├── fsm.out
│   │   ├── install.log
│   │   ├── memory.out
│   │   ├── ngrok.out
│   │   ├── nlp.out
│   │   ├── runtime.log
│   │   ├── scraper.out
│   │   └── trainer.out
│   ├── nlp_training_sets/
│   ├── prompts/
│   └── raw_scrapes/
│
├── demos/
│   ├── Backend_Successfull_Test_1.png
│   ├── Environment.png
│   ├── IMG_7267.png
│   ├── IMG_C6A6CCEB-DCB1-4166-B349-A7431E0D5657.jpeg
│   ├── NLP_Prebuilt_Temp_Install.png
│   └── Stop_Backend_Environment_Stays_Active.png
│
├── dev-experiment/
│   ├── broken_scrapers/
│   │   ├── README.md
│   │   ├── discord_leaks_scraper.py
│   │   ├── legacy_twitter_collector.py
│   │   └── unstable_playwright_agent.py
│   ├── memory_hacking/
│   │   ├── README.md
│   │   ├── inject_custom_embeddings.py
│   │   ├── memory_probe_tool.py
│   │   └── override_reward_trace.py
│   ├── new_agents/
│   │   ├── README.md
│   │   ├── loop_extensions/
│   │   │   ├── dynamic_interval_mutator.py
│   │   │   └── fsm_tick_debugger.py
│   │   ├── planning/
│   │   │   ├── scratchpad_agent.py
│   │   │   └── speculative_planner.py
│   │   └── self_reflection/
│   │       ├── anomaly_analyzer.py
│   │       └── hallucination_guard.py
│   └── your_mutations_here.md
│
├── docs/
│   ├── GREMLINGPT-v1.0.3_PATCH_PLAN.md
│   ├── GREMLINGPT_AUTONOMY_REPORT.md
│   ├── README.md
│   ├── REVIEWER'S_GUIDE.md
│   ├── WHY_GREMLINGPT.md
│   ├── automated_shell.md
│   ├── fsm_architecture.md
│   ├── full_structure_tree.md
│   ├── gremlin.service.md
│   ├── memory_pipeline.md
│   ├── ngrok_integration.md
│   ├── self_training.md
│   ├── system_call_graph.md
│   ├── system_overview.md
│   └── trading_signals.md
│
├── executors/
│   ├── python_executor.py
│   ├── shell_executor.py
│   └── tool_executor.py
│
├── frontend/
│   ├── Icon_Logo/
│   ├── app.js
│   ├── components/
│   │   ├── ChatInterface.js
│   │   ├── MemoryGraph.js
│   │   ├── RewardFeedView.js
│   │   ├── TaskTreeView.js
│   │   └── TradingPanel.js
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   └── theme.css
│
├── memory/
│   ├── local_index/
│   ├── log_history.py
│   └── vector_store/
│       ├── chroma/
│       ├── embedder.py
│       └── faiss/
│
├── nlp_engine/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── chat_session.py
│   ├── diff_engine.py
│   ├── mini_attention.py
│   ├── nlp_check.py
│   ├── parser.py
│   ├── pos_tagger.py
│   ├── semantic_score.py
│   ├── tokenizer.py
│   └── transformer_core.py
│
├── run/
│   ├── checkpoints/
│   ├── cli.py
│   ├── module_tracer.py
│   ├── ngrok_launcher.py
│   ├── nohup.out
│   ├── reboot_recover.sh
│   ├── start_all.sh
│   └── stop_all.sh
│
├── scraper/
│   ├── ask_monday_handler.py
│   ├── dom_navigator.py
│   ├── page_simulator.py
│   ├── persistance/
│   ├── playwright_handler.py
│   ├── profiles/
│   ├── scraper_loop.py
│   ├── source_router.py
│   ├── stt_scraper.py
│   ├── tws_scraper.py
│   └── web_knowledge_scraper.py
│
├── self_mutation_watcher/
│   ├── mutation_daemon.py
│   └── watcher.py
│
├── self_training/
│   ├── feedback_loop.py
│   ├── generate_dataset.py
│   ├── mutation_engine.py
│   └── trainer.py
│
├── systemd/
│   ├── gremlin.service
│   └── gremlin_auto_boot.sh
│
├── tests/
│   ├── test_dashboard.py
│   ├── test_memory.py
│   ├── test_nlp.py
│   └── test_scraper.py
│
├── tools/
│   └── reward_model.py
│
├── trading_core/
│   ├── portfolio_tracker.py
│   ├── rules_engine.py
│   ├── signal_generator.py
│   ├── stock_scraper.py
│   └── tax_estimator.py
│
├── utils/
│   ├── dash_cli.sh
│   └── nltk_setup.py
│
└── README.md
```
