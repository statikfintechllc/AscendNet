#!/usr/bin/env python3
# terminal_bridge.py — Handles pty ↔ WebSocket shell for TouchCore

import asyncio
import os
import pty
from fastapi import WebSocket, WebSocketDisconnect
from logger import log_event

SHELL = os.environ.get("SHELL", "/bin/bash")

async def handle_terminal(websocket: WebSocket):
    try:
        await websocket.accept()
        log_event("WebSocket shell connection accepted.")

        pid, fd = pty.fork()
        if pid == 0:
            os.execvp(SHELL, [SHELL])  # Child process: shell
        else:
            async def read_from_shell():
                try:
                    while True:
                        data = os.read(fd, 1024)
                        await websocket.send_text(data.decode(errors="ignore"))
                except Exception as e:
                    log_event(f"[WS Shell Read Error] {e}")
                    await websocket.close()

            async def write_to_shell():
                try:
                    while True:
                        data = await websocket.receive_text()
                        os.write(fd, data.encode())
                except WebSocketDisconnect:
                    log_event("WebSocket shell disconnected cleanly.")
                except Exception as e:
                    log_event(f"[WS Shell Write Error] {e}")
                    await websocket.close()

            await asyncio.gather(read_from_shell(), write_to_shell())

    except Exception as e:
        log_event(f"[WS Terminal Error] {e}")
        try:
            await websocket.close()
        except:
            pass