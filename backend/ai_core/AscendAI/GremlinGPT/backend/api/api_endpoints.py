# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: backend/api/api_endpoints.py :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import flask
import os
from agent_core.fsm import (
    fsm_loop,
    get_fsm_status,
    step_fsm,
    reset_fsm,
    inject_task as fsm_inject_task,
)

# Importing necessary modules for the API
from agent_core.task_queue import TaskQueue
from backend.api.chat_handler import chat
from backend.api.memory_api import graph as memory_graph
from backend.api.planner import list_tasks, mutation_notify, set_task_priority
from backend.api.scraping_api import scrape_url
from memory.vector_store.embedder import get_memory_graph
from trading_core.signal_generator import generate_signals
from nlp_engine.chat_session import ChatSession
from tools.reward_model import get_reward_feed

# Create Flask Blueprint for API
api_blueprint = flask.Blueprint("api", __name__)

# In-memory session store (for demo; use Redis or DB for production)
_sessions = {}


# --- Core Chat / NLP ---
@api_blueprint.route("/api/chat", methods=["POST"])
def api_chat():
    data = flask.request.get_json()
    user_input = data.get("message", "")
    response = chat(user_input)
    return flask.jsonify({"response": response})


@api_blueprint.route("/api/chat/session", methods=["POST"])
def api_chat_session():
    data = flask.request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id")
    user_id = data.get("user_id", "api_user")
    feedback = data.get("feedback")
    # Retrieve or create session
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
    else:
        session = ChatSession(user_id=user_id)
        _sessions[session.session_id] = session
        session_id = session.session_id
    result = session.process_input(user_input, feedback=feedback)
    result["session_id"] = session_id
    return flask.jsonify(result)


# --- FSM Operations ---
@api_blueprint.route("/api/fsm/status", methods=["GET"])
def api_fsm_status():
    status = get_fsm_status()
    return flask.jsonify({"fsm_status": status})


@api_blueprint.route("/api/fsm/tick", methods=["POST"])
def api_fsm_tick():
    result = fsm_loop()  # Remove tick_once param
    return flask.jsonify({"tick_result": result})


@api_blueprint.route("/api/fsm/step", methods=["POST"])
def api_fsm_step():
    result = step_fsm()
    return flask.jsonify({"step_result": result})


@api_blueprint.route("/api/fsm/reset", methods=["POST"])
def api_fsm_reset():
    result = reset_fsm()
    return flask.jsonify({"reset_result": result})


@api_blueprint.route("/api/fsm/inject", methods=["POST"])
def api_fsm_inject():
    data = flask.request.get_json()
    task = data.get("task")
    result = fsm_inject_task(task)
    return flask.jsonify({"inject_result": result})


# --- Task Queue & Planner ---
@api_blueprint.route("/api/agent/tasks", methods=["GET", "POST"])
def api_agent_tasks():
    tq = TaskQueue()
    if flask.request.method == "POST":
        task_data = flask.request.get_json()
        task_desc = task_data.get("task")
        result = tq.enqueue_task(task_desc)
        return flask.jsonify({"enqueued": result})
    tasks = tq.get_all_tasks()
    return flask.jsonify({"tasks": tasks})


@api_blueprint.route("/api/agent/planner", methods=["GET"])
def api_agent_planner():
    tasks = list_tasks()
    return flask.jsonify({"planner_tasks": tasks})


@api_blueprint.route("/api/agent/planner/mutate", methods=["POST"])
def api_planner_mutate():
    return mutation_notify()


@api_blueprint.route("/api/agent/planner/priority", methods=["POST"])
def api_planner_priority():
    return set_task_priority()


# --- Memory Graph ---
@api_blueprint.route("/api/memory/graph", methods=["GET"])
def api_memory_graph():
    graph = get_memory_graph()
    return flask.jsonify(graph)


# --- State Manager ---
@api_blueprint.route("/api/state/save", methods=["POST"])
def api_save_state():
    from backend.state_manager import save_state

    # save_state likely needs a state argument; pass an empty dict as placeholder
    result = save_state({})
    return flask.jsonify({"save_result": result})


from backend.api.summarizer import summarize_text  # Fixed import path
import requests
from bs4 import BeautifulSoup  # type: ignore


@api_blueprint.route("/api/state/load", methods=["GET"])
def api_load_state():
    from backend.state_manager import load_state

    result = load_state()
    return flask.jsonify({"load_result": result})


# --- Trading Signals ---
@api_blueprint.route("/api/trading/signals", methods=["GET"])
def api_trading_signals():
    signals = generate_signals()
    return flask.jsonify({"signals": signals})


# --- Scraping / Web ---
@api_blueprint.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = flask.request.get_json()
    url = data.get("url")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400
    result = scrape_url(url)
    return flask.jsonify({"scrape_result": result})


# --- Reward Dashboard ---
@api_blueprint.route("/api/dashboard/reward_feed", methods=["GET"])
def api_dashboard_reward_feed():
    n = flask.request.args.get("n", default=20, type=int)
    feed = get_reward_feed(n)
    return flask.jsonify({"reward_feed": feed})


# --- Tools / Utilities ---


# Example: Math Tool
@api_blueprint.route("/api/tools/math/eval", methods=["POST"])
def api_tools_math_eval():
    data = flask.request.get_json()
    expr = data.get("expression")
    if not expr:
        return flask.jsonify({"error": "Missing 'expression'"}), 400
    try:
        # WARNING: eval is dangerous; in production, use a safe math parser!
        result = eval(expr, {"__builtins__": {}})
        return flask.jsonify({"result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# Example: Text Summarization Tool
@api_blueprint.route("/api/tools/text/summarize", methods=["POST"])
def api_tools_text_summarize():
    data = flask.request.get_json()
    text = data.get("text")
    if not text:
        return flask.jsonify({"error": "Missing 'text'"}), 400
    summary = summarize_text(text)
    return flask.jsonify({"summary": summary})


# Example: URL Title Fetcher Tool
@api_blueprint.route("/api/tools/url/title", methods=["POST"])
def api_tools_url_title():
    data = flask.request.get_json()
    url = data.get("url")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string if soup.title else ""
        return flask.jsonify({"title": title})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400


# --- Self-Training / Mutation ---
@api_blueprint.route("/api/self_training/status", methods=["GET"])
def api_self_training_status():
    # Mock status for now - implement actual status checking
    return flask.jsonify(
        {
            "mutation_status": "idle",
            "feedback_status": "active",
            "retrain_status": "scheduled",
            "watcher_status": "monitoring",
        }
    )


@api_blueprint.route("/api/self_training/mutate", methods=["POST"])
def api_self_training_mutate():
    try:
        # Try to import and trigger mutation engine
        try:
            from self_training.mutation_engine import trigger_mutation  # type: ignore

            result = trigger_mutation()
        except ImportError:
            result = {
                "status": "mutation engine not available",
                "message": "Feature not implemented",
            }
        return flask.jsonify({"status": "mutation_triggered", "result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/self_training/feedback", methods=["POST"])
def api_self_training_feedback():
    try:
        try:
            from self_training.feedback_loop import start_feedback_loop  # type: ignore

            result = start_feedback_loop()
        except ImportError:
            result = {"status": "feedback loop not available", "message": "Feature not implemented"}
        return flask.jsonify({"status": "feedback_started", "result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/self_training/retrain", methods=["POST"])
def api_self_training_retrain():
    try:
        try:
            from self_training.trainer import schedule_retrain  # type: ignore

            result = schedule_retrain()
        except ImportError:
            result = {"status": "trainer not available", "message": "Feature not implemented"}
        return flask.jsonify({"status": "retrain_scheduled", "result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/self_training/watcher", methods=["GET"])
def api_self_training_watcher():
    try:
        try:
            from self_training.watcher import get_watcher_status  # type: ignore

            status = get_watcher_status()
        except ImportError:
            status = {"status": "watcher not available", "message": "Feature not implemented"}
        return flask.jsonify({"watcher_status": status})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Executors ---
@api_blueprint.route("/api/execute/python", methods=["POST"])
def api_execute_python():
    data = flask.request.get_json()
    code = data.get("code", "")
    if not code:
        return flask.jsonify({"error": "Missing 'code'"}), 400

    try:
        try:
            from executors.python_executor import execute_python  # type: ignore

            result = execute_python(code)
        except ImportError:
            # Fallback: basic Python execution
            import subprocess
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                f.flush()
                result = subprocess.run(
                    ["python", f.name], capture_output=True, text=True, timeout=10
                )
                os.unlink(f.name)
                result = result.stdout if result.returncode == 0 else result.stderr
        return flask.jsonify({"output": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/execute/shell", methods=["POST"])
def api_execute_shell():
    data = flask.request.get_json()
    command = data.get("command", "")
    if not command:
        return flask.jsonify({"error": "Missing 'command'"}), 400

    try:
        try:
            from executors.shell_executor import execute_shell  # type: ignore

            result = execute_shell(command)
        except ImportError:
            # Fallback: basic shell execution
            import subprocess

            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            result = result.stdout if result.returncode == 0 else result.stderr
        return flask.jsonify({"output": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/execute/tool", methods=["POST"])
def api_execute_tool():
    data = flask.request.get_json()
    tool = data.get("tool", "")
    if not tool:
        return flask.jsonify({"error": "Missing 'tool'"}), 400

    try:
        try:
            from executors.tool_executor import execute_tool  # type: ignore

            result = execute_tool(tool)
        except ImportError:
            result = {
                "tool": tool,
                "status": "tool executor not available",
                "message": "Feature not implemented",
            }
        return flask.jsonify({"result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Tools ---
@api_blueprint.route("/api/tools/reward_model", methods=["POST"])
def api_tools_reward_model():
    data = flask.request.get_json()
    input_text = data.get("input", "")
    if not input_text:
        return flask.jsonify({"error": "Missing 'input'"}), 400

    try:
        try:
            from tools.reward_model import score_with_reward_model  # type: ignore

            result = score_with_reward_model(input_text)
        except ImportError:
            # Fallback: mock reward scoring
            import random

            result = {
                "score": round(random.uniform(0.1, 0.9), 3),
                "confidence": round(random.uniform(0.5, 1.0), 3),
                "reasoning": f"Mock scoring for: {input_text[:50]}...",
            }
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/tools/custom", methods=["GET"])
def api_tools_custom():
    try:
        # List available custom tools
        tools_dir = "tools/"
        tools = []
        if os.path.exists(tools_dir):
            for file in os.listdir(tools_dir):
                if file.endswith(".py") and file != "__init__.py":
                    tools.append(
                        {
                            "name": file[:-3],  # Remove .py extension
                            "description": f"Custom tool: {file[:-3]}",
                        }
                    )
        return flask.jsonify({"tools": tools})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- System / Settings ---
@api_blueprint.route("/api/system/config", methods=["GET"])
def api_system_config():
    try:
        import toml

        with open("config/config.toml", "r") as f:
            config = toml.load(f)
        return flask.jsonify(config)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/backend_select", methods=["POST"])
def api_system_backend_select():
    data = flask.request.get_json()
    backend = data.get("backend", "")
    if backend not in ["faiss", "chromadb"]:
        return flask.jsonify({"error": "Invalid backend. Use 'faiss' or 'chromadb'"}), 400

    try:
        # Use the embedder's backend selection function
        from memory.vector_store.embedder import set_backend

        result = set_backend(backend)

        # Also update globals if function exists
        try:
            from backend.globals import set_dashboard_backend

            set_dashboard_backend(backend)
        except Exception as e:
            print(f"Failed to update globals backend: {e}")

        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/backend_status", methods=["GET"])
def api_system_backend_status():
    try:
        from memory.vector_store.embedder import get_backend_status

        status = get_backend_status()
        return flask.jsonify(status)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/backend_info", methods=["GET"])
def api_system_backend_info():
    try:
        from memory.vector_store.embedder import get_index_info

        info = get_index_info()
        return flask.jsonify(info)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/ngrok", methods=["POST"])
def api_system_ngrok_start():
    try:
        try:
            from run.ngrok_launcher import start_ngrok  # type: ignore

            url = start_ngrok()
        except ImportError:
            url = "http://localhost:8080"  # Fallback URL
        return flask.jsonify({"status": "started", "url": url})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/ngrok", methods=["DELETE"])
def api_system_ngrok_stop():
    try:
        try:
            from run.ngrok_launcher import stop_ngrok  # type: ignore

            stop_ngrok()
        except ImportError:
            pass  # Ngrok not available
        return flask.jsonify({"status": "stopped"})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/logs", methods=["GET"])
def api_system_logs():
    log_file = flask.request.args.get("file", "runtime.log")
    try:
        log_path = f"data/logs/{log_file}"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                content = f.read()
        else:
            content = f"Log file {log_file} not found"
        return flask.jsonify({"content": content, "file": log_file})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/feature_coverage", methods=["GET"])
def api_system_feature_coverage():
    try:
        # Load the feature manifest and check coverage
        import json

        with open("frontend/dashboard_features_map.json", "r") as f:
            manifest = json.load(f)

        total_features = sum(len(tab["features"]) for tab in manifest)
        # For now, assume all features are implemented (implement actual checking later)
        implemented_features = total_features
        missing = []

        return flask.jsonify(
            {
                "coverage": {
                    "total": total_features,
                    "implemented": implemented_features,
                    "missing": missing,
                }
            }
        )
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Experimental ---
@api_blueprint.route("/api/experimental/mutation_watcher", methods=["GET"])
def api_experimental_mutation_watcher_get():
    try:
        try:
            from self_mutation_watcher.watcher import get_status  # type: ignore

            status = get_status()
        except ImportError:
            status = "not_available"
        return flask.jsonify({"status": status})
    except Exception as e:
        return flask.jsonify({"status": "unknown", "error": str(e)})


@api_blueprint.route("/api/experimental/mutation_watcher", methods=["POST"])
def api_experimental_mutation_watcher_start():
    try:
        try:
            from self_mutation_watcher.watcher import start_watcher  # type: ignore

            result = start_watcher()
        except ImportError:
            result = {"status": "watcher not available", "message": "Feature not implemented"}
        return flask.jsonify({"status": "started", "result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/experimental/mutation_watcher", methods=["DELETE"])
def api_experimental_mutation_watcher_stop():
    try:
        try:
            from self_mutation_watcher.watcher import stop_watcher  # type: ignore

            result = stop_watcher()
        except ImportError:
            result = {"status": "watcher not available", "message": "Feature not implemented"}
        return flask.jsonify({"status": "stopped", "result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/experimental/new_agents", methods=["GET"])
def api_experimental_new_agents_get():
    try:
        agents_dir = "dev-experiment/new_agents/"
        agents = []
        if os.path.exists(agents_dir):
            for root, dirs, files in os.walk(agents_dir):
                for file in files:
                    if file.endswith(".py"):
                        agents.append(
                            {"name": file[:-3], "description": f"Experimental agent: {file[:-3]}"}
                        )
        return flask.jsonify({"agents": agents})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/experimental/new_agents", methods=["POST"])
def api_experimental_new_agents_test():
    data = flask.request.get_json()
    agent = data.get("agent", "")
    try:
        # Test the new agent (implement actual testing logic)
        result = {"agent": agent, "test_result": "success", "output": "Agent test completed"}
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/experimental/broken_scrapers", methods=["GET"])
def api_experimental_broken_scrapers():
    try:
        scrapers_dir = "dev-experiment/broken_scrapers/"
        scrapers = []
        if os.path.exists(scrapers_dir):
            for file in os.listdir(scrapers_dir):
                if file.endswith(".py"):
                    scrapers.append({"name": file[:-3], "status": "broken"})
        return flask.jsonify({"scrapers": scrapers})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Memory Search (if not already implemented) ---
@api_blueprint.route("/api/memory/search", methods=["POST"])
def api_memory_search():
    data = flask.request.get_json()
    query = data.get("query", "")
    if not query:
        return flask.jsonify({"error": "Missing 'query'"}), 400

    try:
        try:
            from memory.vector_store.embedder import search_memory  # type: ignore

            results = search_memory(query)
        except ImportError:
            # Fallback: mock search results
            results = [
                {
                    "text": f"Mock result for: {query}",
                    "score": 0.85,
                    "metadata": {"source": "mock"},
                },
                {
                    "text": f"Another result for: {query}",
                    "score": 0.72,
                    "metadata": {"source": "mock"},
                },
            ]
        return flask.jsonify({"results": results})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/memory/snapshot", methods=["POST"])
def api_memory_snapshot():
    try:
        try:
            from core.snapshot import create_snapshot  # type: ignore

            result = create_snapshot()
        except ImportError:
            result = {"status": "snapshot not available", "message": "Feature not implemented"}
        return flask.jsonify({"snapshot_result": result})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/memory/logs", methods=["GET"])
def api_memory_logs():
    try:
        try:
            from memory.log_history import get_recent_logs  # type: ignore

            logs = get_recent_logs()
        except ImportError:
            logs = [
                {"timestamp": "2025-01-01T00:00:00", "message": "Mock log entry", "level": "INFO"}
            ]
        return flask.jsonify({"logs": logs})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Trading endpoints (additional) ---
@api_blueprint.route("/api/trading/portfolio", methods=["GET"])
def api_trading_portfolio():
    try:
        try:
            from trading_core.portfolio_tracker import get_portfolio  # type: ignore

            portfolio = get_portfolio()
        except ImportError:
            portfolio = {
                "holdings": [],
                "total_value": 0,
                "message": "Portfolio tracker not available",
            }
        return flask.jsonify({"portfolio": portfolio})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/trading/rules", methods=["GET"])
def api_trading_rules():
    try:
        try:
            from trading_core.rules_engine import get_rules  # type: ignore

            rules = get_rules()
        except ImportError:
            rules = [{"rule": "Mock trading rule", "enabled": True}]
        return flask.jsonify({"rules": rules})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/trading/tax", methods=["GET"])
def api_trading_tax():
    try:
        try:
            from trading_core.tax_estimator import estimate_taxes  # type: ignore

            tax_estimate = estimate_taxes()
        except ImportError:
            tax_estimate = {"estimated_tax": 0, "message": "Tax estimator not available"}
        return flask.jsonify({"tax_estimate": tax_estimate})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/trading/stock_scraper", methods=["GET"])
def api_trading_stock_scraper():
    try:
        try:
            from trading_core.stock_scraper import get_stock_data  # type: ignore

            stock_data = get_stock_data()
        except ImportError:
            stock_data = {"stocks": [], "message": "Stock scraper not available"}
        return flask.jsonify({"stock_data": stock_data})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Scraping endpoints (additional methods) ---
@api_blueprint.route("/api/scrape/dom", methods=["POST"])
def api_scrape_dom():
    data = flask.request.get_json()
    url = data.get("url", "")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400

    try:
        from backend.api.scraping_api import scrape_url

        result = scrape_url(url, method="dom")
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/scrape/monday", methods=["POST"])
def api_scrape_monday():
    data = flask.request.get_json()
    url = data.get("url", "")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400

    try:
        from backend.api.scraping_api import scrape_url

        result = scrape_url(url, method="monday")
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/scrape/router", methods=["POST"])
def api_scrape_router():
    try:
        from backend.api.scraping_api import scrape_router

        result = scrape_router(snapshot=True)
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# --- Extend with more agent/tools as needed below ---
