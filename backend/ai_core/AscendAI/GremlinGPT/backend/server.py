#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

# CRITICAL: Eventlet monkey patching MUST happen before any other imports
try:
    import eventlet

    eventlet.monkey_patch()
except ImportError:
    pass  # eventlet is optional

# Set up NLTK data path before any imports
import os
import sys

# Configure NLTK to use project directory
GREMLIN_HOME = os.path.abspath(os.path.dirname(__file__) + "/..")
NLTK_DATA_PATH = os.path.join(GREMLIN_HOME, "data", "nltk_data")
os.environ["NLTK_DATA"] = NLTK_DATA_PATH

# Set up Python path and imports
sys.path.insert(0, GREMLIN_HOME)

from flask import Flask, send_from_directory
from flask_socketio import SocketIO  # type: ignore
from backend.api.api_endpoints import api_blueprint
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("backend")
from backend.globals import CFG
import eventlet  # type: ignore
import traceback

# Initialize NLTK data setup
try:
    from utils.nltk_setup import setup_nltk_data

    setup_nltk_data()
    logger.info(f"[SERVER] NLTK configured to use: {NLTK_DATA_PATH}")
except Exception as e:
    logger.warning(f"[SERVER] NLTK setup failed: {e}")

eventlet.monkey_patch()

# App and SocketIO Initialization
app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.config["SECRET_KEY"] = CFG.get("backend", {}).get("secret_key", "gremlin_secret")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Route Registration (optional, comment out if causing issues)
try:
    from backend.router import register_routes

    register_routes(app)
    logger.info("[SERVER] Additional routes registered")
except Exception as e:
    logger.warning(f"[SERVER] Could not register additional routes: {e}")
    # Continue without additional routes - API endpoints are already registered

# Log directory is already set up by globals.py, no need to duplicate logger setup


# Broadcast function for system status
def broadcast_status(msg):
    try:
        socketio.emit("system_broadcast", {"status": msg})
        logger.info(f"[BROADCAST] {msg}")
    except Exception as e:
        logger.error(f"[BROADCAST] Broadcast failed: {e}")


# Base API Checkpoint
@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("../frontend", filename)


def run_server_forever():
    host = CFG.get("backend", {}).get("host", "0.0.0.0")
    port = CFG.get("backend", {}).get("port", 8080)

    # Main bulletproof loop
    while True:
        try:
            logger.info(f"[BACKEND] Starting GremlinGPT backend on {host}:{port}")
            broadcast_status(f"GremlinGPT backend server online at {host}:{port}")
            socketio.run(app, host=host, port=port)
        except KeyboardInterrupt:
            logger.warning("[BACKEND] KeyboardInterrupt received. Shutting down server.")
            broadcast_status("GremlinGPT backend server received shutdown signal.")
            break
        except Exception as e:
            err_info = f"[BACKEND] Server error: {e}\n{traceback.format_exc()}"
            logger.error(err_info)
            broadcast_status(f"GremlinGPT backend server encountered error and is restarting: {e}")
            # Wait before restart to avoid busy-loop
            import time

            time.sleep(5)
        else:
            # If server exits cleanly, break loop
            broadcast_status("GremlinGPT backend server exited cleanly.")
            break


if __name__ == "__main__":
    run_server_forever()
