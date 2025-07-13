#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import logging
from datetime import datetime, timezone
from backend.globals import CFG
from pathlib import Path
import json
import uuid
from typing import Union

log_dir = (CFG.get("paths") or {}).get("logs_dir")  # Fixed to match config.toml
if not log_dir or not isinstance(log_dir, str):
    raise RuntimeError("Missing or invalid 'logs_dir' in CFG['paths']")
ERROR_LOG_FILE = Path(log_dir) / "task_errors.jsonl"

# Configure logger for error logging
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)


class JsonlFormatter(logging.Formatter):
    def format(self, record):
        return record.getMessage()


if not error_logger.handlers:
    # Ensure log directory exists
    ERROR_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Custom formatter expects pre-serialized JSON strings as log messages.
    fh = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
    fh.setFormatter(JsonlFormatter())
    error_logger.addHandler(fh)


def log_error(task: dict, error: Union[Exception, str], source: str = "unknown"):
    """
    Logs structured, agent-aligned error with traceability for GremlinFSM.
    Supports console output and persistent JSONL storage.
    If logging to file fails, the error record is appended directly to the log file as a fallback.

    Args:
        task (dict): Task dictionary, expected to contain at least a "type" key (str) and any other relevant payload data.
        error (Exception or str): The error encountered.
        source (str): The agent or module source of the error.

    Example task structure:
        {
            "type": "task_type_name",
            "payload": {...},  # Additional task-specific fields
            ...
        }
    """

    trace_id = str(uuid.uuid4())
    task_type = task.get("type", "unknown")

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": source,
        "task_type": task_type,
        "task_payload": task,
        "error": str(error),
        "severity": "error",
        "trace_id": trace_id,
    }

    # Log to terminal
    print(f"[ERROR_LOG] [{trace_id}] {task_type} failed — {error}")

    # Persist to file using logging
    try:
        error_logger.error(json.dumps(record))
    except Exception as e:
        print(f"[ERROR_LOG] Failed to persist log: {e}")
        # Fallback: use logger's handler directly if available
        for handler in error_logger.handlers:
            try:
                handler.emit(
                    logging.LogRecord(
                        name="error_logger",
                        level=logging.ERROR,
                        pathname=__file__,
                        lineno=0,
                        msg=json.dumps(record),
                        args=(),
                        exc_info=None,
                    )
                )
                break
            except Exception:
                continue
        else:
            # As a last resort, open the file once and keep it open for the session (not recommended for multi-process)
            try:
                with open(ERROR_LOG_FILE, "a", encoding="utf-8") as fallback_file:
                    fallback_file.write(json.dumps(record) + "\n")
            except Exception as file_error:
                print(f"[ERROR_LOG] Fallback file write failed: {file_error}")
