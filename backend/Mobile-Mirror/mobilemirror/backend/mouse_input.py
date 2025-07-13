#!/usr/bin/env python3
# mouse_input.py — Simulate mouse move/click from phone using xdotool

import subprocess
from logger import log_event

def move_mouse(x=None, y=None, click=False):
    try:
        if x is not None and y is not None:
            subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
            log_event(f"Mouse moved to ({x}, {y})")

        if click:
            subprocess.run(["xdotool", "click", "1"], check=True)
            log_event(f"Mouse click at ({x}, {y})")

        return {
            "status": "mouse action sent",
            "x": x,
            "y": y,
            "click": click
        }

    except subprocess.CalledProcessError as e:
        log_event(f"[ERR] move_mouse subprocess error: {e}")
        return {"error": str(e)}
    except Exception as e:
        log_event(f"[ERR] move_mouse general error: {e}")
        return {"error": str(e)}