#!/usr/bin/env python3
# logger.py — Append logs to TouchCore service tracker

from datetime import datetime
from pathlib import Path

APPDIR = Path.home() / ".local/share/applications"
LOGFILE = APPDIR / "system/services/touchcore_backend.log"

def log_event(msg: str, inline: bool = False):
    """
    Appends a timestamped log entry.
    If inline=True, returns last 50 lines as plain string.
    """
    try:
        LOGFILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"[{now()}] {msg}\n")
    except Exception as e:
        print(f"[LOG FAIL] {e}")

    if inline:
        try:
            with open(LOGFILE, "r", encoding="utf-8") as f:
                return "".join(f.readlines()[-50:])
        except:
            return "[Log unavailable]"

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")