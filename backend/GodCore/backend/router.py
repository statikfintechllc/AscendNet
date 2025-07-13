#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GodCore Open-Use | Commercial Use allowed
# Built under the GodCore Open-Use License v.0.3.0
# © 2025 StatikFintechLLC / GodCore Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GodCore v.0.3.0 :: Module Integrity Directive
# This script is a component of the GodCore system, under Alpha expansion.

import os
import sys
from fastapi import FastAPI, HTTPException, Request  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.responses import StreamingResponse, JSONResponse  # type: ignore
import httpx  # type: ignore
import uvicorn  # type: ignore
import argparse

# Where to find each backend server
MISTRAL_URL = "http://localhost:8000/v1/chat/completions"
MONDAY_URL = "http://localhost:8080/v1/chat/completions"

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
    return {"message": "GodCore Router is live. POST to /v1/chat/completions/[mistral|monday]"}


@app.post("/v1/chat/completions/mistral")
async def proxy_mistral(request: Request):
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                MISTRAL_URL,
                content=await request.body(),
                headers=dict(request.headers),
            ) as backend_resp:
                return StreamingResponse(
                    backend_resp.aiter_raw(),
                    media_type=backend_resp.headers.get("content-type", "text/event-stream"),
                )
    except Exception as e:

        async def errstream():
            yield f"data: [ERROR: {str(e)}]\n\n"

        return StreamingResponse(errstream(), media_type="text/event-stream")


@app.post("/v1/chat/completions/monday")
async def proxy_monday(request: Request):
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            # Monday handler streams responses, so we need to proxy the stream
            async with client.stream(
                "POST",
                MONDAY_URL,
                content=await request.body(),
                headers=dict(request.headers),
            ) as backend_resp:
                return StreamingResponse(
                    backend_resp.aiter_raw(),
                    media_type=backend_resp.headers.get("content-type", "text/event-stream"),
                )
    except Exception as e:
        # On error, return as an SSE message
        async def errstream():
            yield f"data: [ERROR: {str(e)}]\n\n"

        return StreamingResponse(errstream(), media_type="text/event-stream")


@app.post("/v1/chat/completions")
async def proxy_both(request: Request):
    """Legacy/mux endpoint, picks model based on 'model' in body, or defaults to both."""
    body = await request.json()
    model = body.get("model", "").lower()
    # Route to right handler (add your own logic here if needed)
    if model == "monday":
        return await proxy_monday(request)
    elif model.startswith("mistral"):
        return await proxy_mistral(request)
    else:
        # Optionally call both or return error
        return JSONResponse(
            status_code=400,
            content={"error": "Model not recognized. Specify 'monday' or 'mistral'."},
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8088, help="Port to run router on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run router on")
    args = parser.parse_args()
    print(f"🚦 GodCore Router ready on http://{args.host}:{args.port}")
    uvicorn.run("router:app", host=args.host, port=args.port)
