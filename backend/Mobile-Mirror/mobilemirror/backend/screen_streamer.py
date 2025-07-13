#!/usr/bin/env python3
# screen_streamer.py — TouchCore screen broadcast daemon starter

import subprocess
from pathlib import Path
from logger import log_event

APPDIR = str(Path.home() / ".local/share/applications")
LOGDIR = f"{APPDIR}/system/services"
STREAM_PORT = "5901"  # Standard VNC port

def start_stream():
    log_event("Starting screen streamer...")

    try:
        subprocess.Popen([
            "x11vnc",
            "-display", ":0",
            "-rfbport", STREAM_PORT,
            "-forever",
            "-nopw",
            "-shared",
            "-bg",
            "-o", f"{LOGDIR}/x11vnc.log"
        ])
        log_event(f"x11vnc started on port {STREAM_PORT}")
        return {"status": "screen stream started", "port": STREAM_PORT}

    except FileNotFoundError:
        msg = "x11vnc not found. Please install it via: sudo apt install x11vnc"
        log_event(f"[ERR] {msg}")
        return {"error": msg}

    except Exception as e:
        log_event(f"[ERR] screen_streamer: {e}")
        return {"error": str(e)}