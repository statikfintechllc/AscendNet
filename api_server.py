#!/usr/bin/env python3
"""
AscendNet Unified API Server
Main entry point for the FastAPI application
"""

import os
import sys
import uvicorn
import logging
from fastapi import FastAPI, HTTPException, Request  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from contextlib import asynccontextmanager
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AscendNet")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager"""
    logger.info("🚀 AscendNet API Server starting...")
    yield
    logger.info("💤 AscendNet API Server shutting down...")

# Create FastAPI application
app = FastAPI(
    title="AscendNet Unified API",
    description="Unified API for AscendNet AI-powered decentralized system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 AscendNet Unified API Server",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-07-12",
        "services": {
            "api": "operational",
            "ai_core": "operational",
            "statik_server": "operational"
        }
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
