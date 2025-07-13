# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
#!/usr/bin/env python3

import os
import time
import sys
import shutil
import pyautogui
import pyperclip
import pytesseract
import subprocess
import platform
from PIL import ImageGrab, Image
from datetime import datetime, timedelta
from pathlib import Path
import json
import argparse
from typing import Optional

try:
    from backend.globals import logger
    from memory.vector_store.embedder import (
        embed_text as _embed_text,
        package_embedding as _package_embedding,
        inject_watermark as _inject_watermark,
    )
    from memory.log_history import log_event as original_log_event

    def log_event(message: Optional[str] = None, **kwargs) -> None:
        """Wrapper for log_event with flexible parameters."""
        if message and not kwargs:
            # Simple string message
            original_log_event("info", "general", {"message": message})
        elif kwargs:
            # Pass through with original parameters
            original_log_event(**kwargs)
        else:
            pass

    # Create properly typed wrapper functions
    def embed_text(x: str) -> list[float]:
        """Convert text to embedding vector."""
        result = _embed_text(x)
        if hasattr(result, "tolist"):
            return result.tolist()  # Convert numpy array to list
        elif isinstance(result, list):
            return result
        else:
            return [0.0] * 768  # Default embedding size

    def package_embedding(**x) -> None:
        """Package embedding data."""
        if len(x) >= 3:
            args = list(x.values())
            _package_embedding(args[0], args[1], args[2])

    def inject_watermark(**x) -> None:
        """Inject watermark into data."""
        origin = x.get("origin", "unknown")
        _inject_watermark(origin)

except ImportError:
    # Minimal fallback implementations
    class _MiniLogger:
        def info(self, *a, **k):
            print("[INFO]", *a, **k, file=sys.stderr)

        def success(self, *a, **k):
            print("[SUCCESS]", *a, **k, file=sys.stderr)

        def warning(self, *a, **k):
            print("[WARNING]", *a, **k, file=sys.stderr)

        def error(self, *a, **k):
            print("[ERROR]", *a, **k, file=sys.stderr)

    logger = _MiniLogger()

    def embed_text(x: str) -> list[float]:
        """Fallback embedding function."""
        return [0.0] * 768  # Return default embedding

    def package_embedding(**x) -> None:
        """Fallback package embedding function."""
        pass

    def inject_watermark(**x) -> None:
        """Fallback watermark function."""
        pass

    def log_event(message: Optional[str] = None, **kwargs) -> None:
        """Fallback log event function."""
        if message:
            logger.info(f"Event: {message}")
        elif kwargs:
            logger.info(f"Event: {kwargs}")
        else:
            pass


# ---- GREMLIN FLAVOR: Watermark, structure, memory
WATERMARK = "source:GremlinGPT"
ORIGIN = "ask_monday_handler"

SCREENSHOT_DIR = Path(os.path.expanduser("data/logs/screenshots"))
MEMORY_DIR = Path(os.path.expanduser("data/logs/chat_responses"))
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

SESSION_WINDOWS = {}


def log(msg, *a):
    logger.info(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}", *a)


# ---- WINDOW MANAGEMENT ----


def list_gremlingpt_windows():
    try:
        out = subprocess.check_output(["wmctrl", "-lx"]).decode()
        windows = {
            line.split()[0]: line for line in out.strip().splitlines() if "chatgpt" in line.lower()
        }
        log(f"Gremlin detected windows: {windows}")
        return windows
    except Exception as e:
        logger.warning(f"wmctrl failed: {e}")
        return {}


def focus_window(window_id):
    try:
        log(f"Focusing window {window_id}")
        subprocess.run(["wmctrl", "-ia", window_id])
        time.sleep(0.7)
    except Exception as e:
        logger.warning(f"Focus window failed: {e}")


def launch_gremlingpt(session_id):
    log(f"Launching ChatGPT window for Gremlin session: {session_id}")
    before = set(list_gremlingpt_windows().keys())
    system = platform.system()

    # Try native/CLI launch
    try:
        if system == "Linux":
            # Try desktop shortcut first (like GodCore), fallback to gdk-launch or command
            desktop_path = os.path.expanduser("~/.local/share/applications/chatgpt.desktop")
            gtk_launch_exists = (
                subprocess.call(
                    ["which", "gtk-launch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                == 0
            )
            if gtk_launch_exists and os.path.exists(desktop_path):
                subprocess.Popen(["gtk-launch", "chatgpt"])
            elif shutil.which("gdk-launch"):
                subprocess.Popen(["gdk-launch", "chatgpt"])
            elif shutil.which("chatgpt"):
                subprocess.Popen(["chatgpt"])
            else:
                subprocess.Popen(["xdg-open", desktop_path])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "ChatGPT"])
        elif system == "Windows":
            subprocess.Popen(["start", "", "ChatGPT"], shell=True)
        else:
            raise RuntimeError("Unsupported OS for Gremlin launch.")
        time.sleep(5)
        pyautogui.click()
    except Exception as e:
        logger.error(f"[ASK] Failed to launch ChatGPT for Gremlin: {e}")
        raise

    # Wait for new window (12s timeout)
    max_wait = 12
    for i in range(max_wait):
        time.sleep(1.5)
        after = list_gremlingpt_windows()
        new_windows = set(after.keys()) - before
        if new_windows:
            win_id = list(new_windows)[0]
            log(f"Found new ChatGPT window: {win_id}")
            SESSION_WINDOWS[session_id] = win_id
            focus_window(win_id)
            return win_id
    log("Failed to detect new ChatGPT window.")
    raise RuntimeError("Failed to launch new ChatGPT window")


def ensure_window_for_session(session_id):
    if session_id in SESSION_WINDOWS and SESSION_WINDOWS[session_id]:
        focus_window(SESSION_WINDOWS[session_id])
        return SESSION_WINDOWS[session_id]
    else:
        return launch_gremlingpt(session_id)


# ---- CHAT INTERACTION ----


def paste_and_enter(text):
    try:
        pyperclip.copy(text)
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        log("Gremlin sent prompt via clipboard and enter.")
    except Exception as e:
        logger.error(f"paste_and_enter failed: {e}")
        raise


def scroll_and_capture(n_scrolls=3, base_delay=10):
    """Scrolls & captures the ChatGPT response."""
    images = []
    time.sleep(base_delay)
    for i in range(n_scrolls):
        screenshot = ImageGrab.grab()
        path = (
            SCREENSHOT_DIR / f"gremlin_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
        )
        screenshot.save(path)
        images.append(path)
        pyautogui.scroll(-500)
        time.sleep(1.5)
    return images


def ocr_images(image_paths):
    blocks = []
    for p in image_paths:
        try:
            img = Image.open(p)
            text = pytesseract.image_to_string(img)
            blocks.append(text.strip())
        except Exception as e:
            logger.warning(f"[ASK] OCR failed for {p}: {e}")
            blocks.append("[OCR ERROR]")
    return "\n---\n".join(blocks)


def save_to_memory(prompt, response):
    timestamp = datetime.utcnow().isoformat()
    vector = embed_text(response)
    summary = f"GremlinGPT ChatGPT response to: {prompt[:100]}"
    package_embedding(
        text=summary,
        vector=vector,
        meta={
            "origin": ORIGIN,
            "timestamp": timestamp,
            "prompt": prompt,
            "response_len": len(response),
            "watermark": WATERMARK,
        },
    )
    inject_watermark(origin=ORIGIN)
    log_event(
        event_type="ask", task_type="gremlin_query", details={"prompt": prompt}, status="external"
    )
    filename = MEMORY_DIR / f"chat_response_{timestamp.replace(':','').replace('-','')}.md"
    with open(filename, "w") as f:
        f.write(f"# Prompt:\n{prompt}\n\n# Response:\n{response}\n")
    logger.success(f"[ASK] GremlinGPT result embedded and saved: {filename}")


def ask_monday(prompt, session_id="default"):
    logger.info(f"[ASK] Asking ChatGPT (Gremlin session): {prompt}")
    ensure_window_for_session(session_id)
    paste_and_enter(prompt)
    images = scroll_and_capture()
    response = ocr_images(images)
    save_to_memory(prompt, response)
    return {"prompt": prompt, "response": response}


# For streaming FastAPI (optional)
def ask_monday_stream(prompt, session_id="default", interrupt_checker=None):
    logger.info(f"[ASK/STREAM] Gremlin streaming: {prompt}")
    try:
        win_id = ensure_window_for_session(session_id)
        paste_and_enter(prompt)
    except Exception as e:
        yield json.dumps({"model": "chatgpt", "delta": f"[WINDOW ERROR: {e}]"})
        yield "[END_OF_RESPONSE]"
        return

    last_text = ""
    start_time = datetime.utcnow()
    max_duration = timedelta(minutes=3.5)
    while True:
        now = datetime.utcnow()
        if now - start_time > max_duration:
            logger.warning("Max duration reached, ending stream.")
            break
        if interrupt_checker and interrupt_checker():
            logger.info("Streaming interrupted by backend.")
            break
        time.sleep(2.5 if last_text == "" else 1.5)
        try:
            screenshot = ImageGrab.grab()
            text = pytesseract.image_to_string(screenshot)
            logger.info(f"OCR: {len(text or '')} chars (delta: {text != last_text})")
            if text and text.strip() and text != last_text:
                last_text = text
                yield json.dumps({"model": "chatgpt", "delta": text.strip()}) + "\n"
            pyautogui.scroll(-500)
        except Exception as e:
            logger.warning(f"OCR failed: {e}")
            yield json.dumps({"model": "chatgpt", "delta": f"[OCR ERROR: {e}]"})
            break
    yield "[END_OF_RESPONSE]"


# FSM/Gremlin agent interface
def handle(task):
    prompt = task.get("target") or task.get("text") or "What is your task?"
    session_id = task.get("session_id", "default")
    return ask_monday(prompt, session_id=session_id)


# Optional: FastAPI server for streaming (toggle with --serve)
def serve_api(port=8080, host="0.0.0.0"):
    from fastapi import FastAPI, Request  # type: ignore
    from fastapi.middleware.cors import CORSMiddleware  # type: ignore
    from fastapi.responses import StreamingResponse  # type: ignore
    import uvicorn  # type: ignore

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
        return {"message": "GremlinGPT handler is live. POST to /v1/chat/completions"}

    @app.post("/v1/chat/completions")
    async def chat_completions(request: Request):
        try:
            body = await request.json()
            prompt = body.get("target") or body.get("text") or ""
            session_id = body.get("session_id", None) or "default"

            async def streamer():
                for chunk in ask_monday_stream(prompt, session_id=session_id):
                    yield f"data: {chunk}\n\n"

            return StreamingResponse(streamer(), media_type="text/event-stream")
        except Exception as e:
            logger.warning(f"chat_completions error: {e}")

            async def errstream():
                yield f"data: [ERROR: {str(e)}]\n\n"

            return StreamingResponse(errstream(), media_type="text/event-stream")

    logger.success(f"🚀 GremlinGPT handler API ready on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


# Standalone or API mode
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="Prompt to send")
    parser.add_argument("--serve", action="store_true", help="Run FastAPI server")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()

    if args.serve:
        serve_api(port=args.port, host=args.host)
    elif args.prompt:
        print(json.dumps(ask_monday(args.prompt)))
    else:
        # Demo run
        prompt = "Explain the core differences between GremlinGPT and GodCore (be brutally honest)."
        print(json.dumps(ask_monday(prompt)))
