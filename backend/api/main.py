"""
AscendNet Backend API - Main FastAPI Entry Point
Unified system following the architectural blueprint
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging
from pathlib import Path

# Import route modules
from .routes import prompts, compute, users, health
from ..utils.logger import setup_logging
from ..utils.config import load_config
from ..p2p.node import P2PNode
from .dependencies import get_current_user, rate_limit

# Initialize logging
logger = setup_logging()

# Load configuration
config = load_config()

# Initialize FastAPI app
app = FastAPI(
    title="AscendNet API",
    description="Unified AscendNet P2P AI Marketplace Backend",
    version="1.0.0-alpha",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get("cors_origins", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=config.get("allowed_hosts", ["*"])
)

# Global P2P Node instance
p2p_node = None

@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    global p2p_node
    
    logger.info("🚀 Starting AscendNet Backend...")
    
    # Initialize P2P node
    try:
        p2p_node = P2PNode(config=config.get("p2p", {}))
        await p2p_node.start()
        logger.info("✅ P2P Node initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize P2P node: {e}")
    
    logger.info("🎯 AscendNet Backend ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global p2p_node
    
    logger.info("🛑 Shutting down AscendNet Backend...")
    
    if p2p_node:
        await p2p_node.stop()
        logger.info("✅ P2P Node stopped")
    
    logger.info("👋 AscendNet Backend shutdown complete")

# Include route modules
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["health"]
)

app.include_router(
    prompts.router,
    prefix="/api/v1/prompts",
    tags=["prompts"],
    dependencies=[Depends(rate_limit)]
)

app.include_router(
    compute.router,
    prefix="/api/v1/compute",
    tags=["compute"],
    dependencies=[Depends(rate_limit)]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AscendNet API - Unified P2P AI Marketplace",
        "version": "1.0.0-alpha",
        "status": "operational",
        "docs": "/docs"
    }

def main():
    """Main entry point"""
    uvicorn.run(
        "main:app",
        host=config.get("host", "0.0.0.0"),
        port=config.get("port", 8000),
        reload=config.get("debug", False),
        log_level="info"
    )

if __name__ == "__main__":
    main()
