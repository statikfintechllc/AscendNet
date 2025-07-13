#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Utility Module
# This script is a component of the GremlinGPT system, under Alpha expansion.
# Purpose:
#   - Git automation helpers for system-wide autocommit and file archiving
#   - Shared by FSM, Planner, and other modules
#   - Must remain side-effect free unless explicitly invoked
## Auto-Usage:
#   - Automatically archives JSON logs with a timestamp
#   - Automatically stages and commits files to the current Git repository
#   - Designed to be used by other modules without manual intervention

import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.logging_config import get_module_logger

# Initialize module-specific logger
logger = get_module_logger("backend")

DEFAULT_ARCHIVE_DIR = "docs/"


# Archive JSON log files with timestamp
# This function is used to archive JSONL or log files with a timestamp in the docs/ directory.
# It returns the new archive path or an empty string if the operation fails.
# It is designed to be used by other modules without manual intervention.
# The function checks if the source file exists, copies it to the archive directory with a timestamp,
# and logs the operation. If any error occurs, it logs the error and returns an empty string.
# This function is side-effect free unless explicitly invoked.
# It is intended to be used by the FSM, Planner, and other modules that require file archiving functionality.
def archive_json_log(source_path: str, prefix: str = "log") -> str:
    """
    Archive a JSONL or log file with timestamp into docs/ directory.
    Returns the new archive path, or empty string on failure.
    """
    try:
        src = Path(source_path).expanduser().resolve()
        if not src.exists():
            logger.warning(f"[git_ops] Source file not found: {source_path}")
            return ""

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        ext = src.suffix or ".jsonl"
        dest_name = f"{prefix}_{timestamp}{ext}"
        dest_path = Path(DEFAULT_ARCHIVE_DIR).resolve() / dest_name

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest_path)
        logger.info(f"[git_ops] Archived {src} → {dest_path}")
        return str(dest_path)
    except FileNotFoundError:
        logger.error(f"[git_ops] Source file not found: {source_path}")
        return ""
    except PermissionError:
        logger.error(f"[git_ops] Permission denied for {source_path}")
        return ""
    except shutil.SameFileError:
        logger.warning(f"[git_ops] Source and destination are the same: {source_path}")
        return ""
    except OSError as e:
        logger.error(f"[git_ops] OS error during archive: {e}")
        return ""
    except Exception as e:
        logger.error(f"[git_ops] Archive failed: {e}")
        return ""


# Auto-commit changes, staging the specified file and committing with a default message.
# This function is designed to be used by other modules without manual intervention.
# It stages the specified file in the current Git repository and commits it with a default message.
# If the file does not exist, it logs a warning and returns without making any changes.
# The function is side-effect free unless explicitly invoked.
# It is intended to be used by the FSM, Planner, and other modules that require automatic file commits.
# The default commit message can be overridden by passing a custom message.
# If the commit fails, it logs a warning with the error message.
def auto_commit(file_path: str, message: str = "[autocommit] Update via git_ops"):
    """
    Stage and commit a file into the current Git repo.
    """
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            logger.warning(f"[git_ops] File not found: {file_path}")
            return

        os.system(f'git add "{path}"')
        os.system(f'git commit -m "{message}"')
        logger.info(f"[git_ops] Git commit successful for: {path.name}")

    except Exception as e:
        logger.warning(f"[git_ops] Git commit failed: {e}")
