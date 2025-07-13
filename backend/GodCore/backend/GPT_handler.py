#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GodCore Open-Use | Commercial Use allowed
# Built under the GodCore Open-Use License v.0.3.0
# © 2025 StatikFintechLLC / GodCore Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GodCore v.0.3.0 :: Module Integrity Directive
# This script is a component of the GodCore system, under Alpha expansion.

import subprocess
import time
import os
import pyautogui
import pyperclip
import pytesseract
from PIL import ImageGrab
from datetime import datetime, timedelta
import json
import argparse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import sys

SESSION_WINDOWS = {}


# --------- LOGGING ----------
def log(msg, *a):
    print(
        f"[{datetime.now().isoformat(timespec='seconds')}] {msg}", *a, file=sys.stderr
    )


# --------- WINDOW MANAGEMENT ----------
def list_chatgpt_windows():
    try:
        out = subprocess.check_output(["wmctrl", "-lx"]).decode()
        windows = {
            line.split()[0]: line
            for line in out.strip().splitlines()
            if "chatgpt" in line.lower()
        }
        log(f"Detected ChatGPT windows: {windows}")
        return windows
    except Exception as e:
        log(f"wmctrl failed: {e}")
        return {}


def focus_window(window_id):
    try:
        log(f"Focusing window {window_id}")
        subprocess.run(["wmctrl", "-ia", window_id])
        time.sleep(0.7)
    except Exception as e:
        log(f"Focus window failed: {e}")


def launch_chatgpt_for_session(session_id):
    log(f"Launching ChatGPT window for session: {session_id}")
    before = set(list_chatgpt_windows().keys())

    display = os.environ.get("DISPLAY", ":0")
    desktop_path = os.path.expanduser("~/.local/share/applications/chatgpt.desktop")
    gtk_launch_exists = (
        subprocess.call(
            ["which", "gtk-launch"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )

    if not gtk_launch_exists or not os.path.exists(desktop_path):
        log(f"gtk-launch not found or desktop entry missing: {desktop_path}")
        raise RuntimeError("gtk-launch or chatgpt.desktop missing")

    try:
        proc = subprocess.Popen(
            ["gtk-launch", "chatgpt"],
            env={**os.environ, "DISPLAY": display},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        log("Ran gtk-launch chatgpt")
    except Exception as e:
        log(f"gtk-launch failed: {e}")
        # Fallback: xdg-open the desktop file
        try:
            subprocess.Popen(
                ["xdg-open", desktop_path],
                env={**os.environ, "DISPLAY": display},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            log("Fallback: Ran xdg-open on chatgpt.desktop")
        except Exception as e2:
            log(f"xdg-open fallback failed: {e2}")
            raise RuntimeError(f"All launch attempts failed: {e2}")

    # Wait for new window, up to 12 seconds
    max_wait = 12
    for i in range(max_wait):
        time.sleep(1.5)
        after = list_chatgpt_windows()
        new_windows = set(after.keys()) - before
        if new_windows:
            win_id = list(new_windows)[0]
            log(f"Found new ChatGPT window: {win_id}")
            SESSION_WINDOWS[session_id] = win_id
            focus_window(win_id)
            return win_id
        else:
            log(f"No new window yet… ({i+1}/{max_wait})")
    log("Failed to detect new ChatGPT window.")
    raise RuntimeError("Failed to launch new ChatGPT window")


def ensure_window_for_session(session_id):
    if session_id in SESSION_WINDOWS and SESSION_WINDOWS[session_id]:
        focus_window(SESSION_WINDOWS[session_id])
        return SESSION_WINDOWS[session_id]
    else:
        return launch_chatgpt_for_session(session_id)


# --------- CHATGPT INTERACTION ----------
def paste_and_enter(text):
    try:
        pyperclip.copy(text)
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        log("Sent prompt via clipboard and enter.")
    except Exception as e:
        log(f"paste_and_enter failed: {e}")
        raise


def ask_monday_stream(prompt, session_id=None, interrupt_checker=None):
    log(f"[ASK] Asking ChatGPT (session {session_id}): {prompt}")
    try:
        win_id = ensure_window_for_session(session_id or "default")
    except Exception as e:
        yield json.dumps({"model": "chatgpt", "delta": f"[WINDOW ERROR: {e}]"})
        yield "[END_OF_RESPONSE]"
        return

    try:
        paste_and_enter(prompt)
    except Exception as e:
        yield json.dumps({"model": "chatgpt", "delta": f"[PASTE ERROR: {e}]"})
        yield "[END_OF_RESPONSE]"
        return

    last_text = ""
    start_time = datetime.utcnow()
    max_duration = timedelta(minutes=3.5)
    while True:
        now = datetime.utcnow()
        if now - start_time > max_duration:
            log("Max duration reached, ending stream.")
            break
        if interrupt_checker and interrupt_checker():
            log("Streaming interrupted by backend.")
            break
        time.sleep(2.5 if last_text == "" else 1.5)
        try:
            screenshot = ImageGrab.grab()
            text = pytesseract.image_to_string(screenshot)
            log(f"OCR: {len(text or '')} chars (delta: {text != last_text})")
            if text and text.strip() and text != last_text:
                last_text = text
                yield json.dumps({"model": "chatgpt", "delta": text.strip()}) + "\n"
            pyautogui.scroll(-500)
        except Exception as e:
            log(f"OCR failed: {e}")
            yield json.dumps({"model": "chatgpt", "delta": f"[OCR ERROR: {e}]"})
            break
    yield "[END_OF_RESPONSE]"


def ask_monday(prompt, session_id=None):
    log(f"[ASK] (non-stream) ChatGPT (session {session_id}): {prompt}")
    try:
        win_id = ensure_window_for_session(session_id or "default")
        paste_and_enter(prompt)
        time.sleep(10)
        screenshot = ImageGrab.grab()
        text = pytesseract.image_to_string(screenshot)
        response = text.strip() if text else ""
        return {"prompt": prompt, "response": response}
    except Exception as e:
        log(f"ask_monday failed: {e}")
        return {"prompt": prompt, "response": f"[ERROR: {e}]"}


def handle(task):
    prompt = task.get("target") or task.get("text") or "What is your task?"
    session_id = task.get("session_id", None)
    return ask_monday(prompt, session_id=session_id)


# ===== FastAPI Server =====
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ChatGPT handler is live. POST to /v1/chat/completions"}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        prompt = body.get("target") or body.get("text") or ""
        session_id = body.get("session_id", None)

        async def streamer():
            for chunk in ask_monday_stream(prompt, session_id=session_id):
                yield f"data: {chunk}\n\n"

        return StreamingResponse(streamer(), media_type="text/event-stream")
    except Exception as e:
        log(f"chat_completions error: {e}")

        async def errstream():
            yield f"data: [ERROR: {str(e)}]\n\n"

        return StreamingResponse(errstream(), media_type="text/event-stream")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to run server on"
    )
    args = parser.parse_args()

    log(f"🚀 ChatGPT handler API ready on http://{args.host}:{args.port}")
    uvicorn.run("GPT_handler:app", host=args.host, port=args.port)
