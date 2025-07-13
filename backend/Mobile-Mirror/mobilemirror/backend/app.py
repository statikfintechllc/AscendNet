#!/usr/bin/env python3
# app.py — TouchCore backend service for mobile streaming + control

import uvicorn
from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Local module imports
from file_ops import list_files, read_file, write_file
from terminal_bridge import handle_terminal
from mouse_input import move_mouse
from screen_streamer import start_stream
from qr_generator import generate_qr
from logger import log_event
from auth import verify_token

# ─────────── Settings ───────────
APPDIR = str(Path.home() / ".local/share/applications")
LOGDIR = f"{APPDIR}/system/services"
PORT = 8000

# ─────────── FastAPI App ───────────
app = FastAPI(title="TouchCore")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────── API ROUTES ───────────

@app.get("/")
def index():
    return {"status": "TouchCore Online", "ui": "http://localhost:5000"}

@app.get("/files")
def get_files(path: str = ".", request: Request = None):
    token = request.headers.get("Authorization", "")
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    return list_files(path)

@app.post("/read")
async def open_file(req: Request):
    token = req.headers.get("Authorization", "")
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    data = await req.json()
    return read_file(data.get("path", ""))

@app.post("/write")
async def save_file(req: Request):
    token = req.headers.get("Authorization", "")
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    data = await req.json()
    return write_file(data.get("path", ""), data.get("content", ""))

@app.websocket("/terminal")
async def ws_terminal(websocket: WebSocket):
    await handle_terminal(websocket)  # optional: inject token handshake for full protection

@app.post("/mouse")
async def handle_mouse(req: Request):
    token = req.headers.get("Authorization", "")
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    data = await req.json()
    return move_mouse(data.get("x"), data.get("y"), data.get("click", False))

@app.get("/qr")
def qr():
    url = f"https://{get_tailscale_ip()}:5000"
    return generate_qr(url)

@app.get("/log")
def get_log():
    return {"log": log_event("query", inline=True)}

# ─────────── UTIL ───────────

def get_tailscale_ip():
    try:
        from subprocess import check_output
        return check_output(["tailscale", "ip", "--4"]).decode().splitlines()[0]
    except:
        return "localhost"

# ─────────── BOOT ───────────

if __name__ == "__main__":
    log_event("TouchCore backend launched.")
    start_stream()
    uvicorn.run(app, host="0.0.0.0", port=PORT)