#!/usr/bin/env python3
"""
AscendNet Unified API Server
============================

Main FastAPI server that provides the unified dashboard and routes to all AscendNet components.
This is the single entry point for the entire AscendNet platform.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ascendnet-api")

# Get project root
PROJECT_ROOT = Path(__file__).parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
STATIC_DIR = PROJECT_ROOT / "static"

# Create FastAPI app
app = FastAPI(
    title="AscendNet Unified API",
    description="Unified API server for the AscendNet AI development platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory=str(FRONTEND_DIR))

# Component status tracking
component_status = {
    "statik-server": {"status": "online", "port": 8080, "url": "http://localhost:8080"},
    "gremlin": {"status": "online", "port": 8081, "url": "http://localhost:8081"},
    "godcore": {"status": "online", "port": 8082, "url": "http://localhost:8082"},
    "mobile": {"status": "online", "port": 8083, "url": "http://localhost:8083"},
    "p2p": {"status": "online", "port": 8084, "url": "http://localhost:8084"},
    "memory": {"status": "online", "port": 8085, "url": "http://localhost:8085"},
    "admin": {"status": "online", "port": 8086, "url": "http://localhost:8086"}
}

# ============================================================================
# MAIN DASHBOARD ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_main_dashboard(request: Request):
    """Serve the main AscendNet unified dashboard"""
    try:
        dashboard_file = FRONTEND_DIR / "ascendnet-dashboard.html"
        if not dashboard_file.exists():
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        raise HTTPException(status_code=500, detail="Dashboard unavailable")

@app.get("/ascendnet-dashboard.css")
async def serve_dashboard_css():
    """Serve dashboard CSS"""
    css_file = FRONTEND_DIR / "ascendnet-dashboard.css"
    if not css_file.exists():
        raise HTTPException(status_code=404, detail="CSS not found")
    return FileResponse(css_file, media_type="text/css")

@app.get("/ascendnet-dashboard.js")
async def serve_dashboard_js():
    """Serve dashboard JavaScript"""
    js_file = FRONTEND_DIR / "ascendnet-dashboard.js"
    if not js_file.exists():
        raise HTTPException(status_code=404, detail="JavaScript not found")
    return FileResponse(js_file, media_type="application/javascript")

# ============================================================================
# COMPONENT DASHBOARD ROUTES (Proxy/Redirect)
# ============================================================================

@app.get("/statik-dashboard")
async def serve_statik_dashboard():
    """Serve or redirect to Statik-Server dashboard"""
    statik_dashboard = PROJECT_ROOT / "statik-server" / "src" / "browser" / "pages" / "statik-dashboard.html"
    if statik_dashboard.exists():
        with open(statik_dashboard, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    else:
        # Return a placeholder if statik-server dashboard isn't available
        return HTMLResponse(content="""
        <html>
        <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>💻 Statik-Server Dashboard</h1>
            <p>Statik-Server dashboard will load here when available.</p>
            <p>Make sure Statik-Server is running on port 8080.</p>
            <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
        </body>
        </html>
        """)

@app.get("/gremlin-dashboard")
async def serve_gremlin_dashboard():
    """Serve or redirect to GremlinGPT dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>🤖 GremlinGPT Dashboard</h1>
        <p>Autonomous AI Agent interface will load here.</p>
        <p>Make sure GremlinGPT is running on port 8081.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

@app.get("/godcore-dashboard")
async def serve_godcore_dashboard():
    """Serve or redirect to GodCore dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>⚛️ GodCore Dashboard</h1>
        <p>Multi-model AI router interface will load here.</p>
        <p>Make sure GodCore is running on port 8082.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

@app.get("/mobile-dashboard")
async def serve_mobile_dashboard():
    """Serve or redirect to Mobile-Mirror dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>📱 Mobile-Mirror Dashboard</h1>
        <p>Mobile development environment will load here.</p>
        <p>Make sure Mobile-Mirror is running on port 8083.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

@app.get("/p2p-dashboard")
async def serve_p2p_dashboard():
    """Serve or redirect to P2P Network dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>🌐 P2P Network Dashboard</h1>
        <p>Decentralized marketplace interface will load here.</p>
        <p>Make sure P2P Network is running on port 8084.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

@app.get("/memory-dashboard")
async def serve_memory_dashboard():
    """Serve or redirect to AI Memory dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>🧠 AI Memory Dashboard</h1>
        <p>Neural network memory interface will load here.</p>
        <p>Make sure AI Memory service is running on port 8085.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

@app.get("/admin-dashboard")
async def serve_admin_dashboard():
    """Serve or redirect to System Admin dashboard"""
    return HTMLResponse(content="""
    <html>
    <body style="background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>⚙️ System Administration</h1>
        <p>System monitoring and control interface will load here.</p>
        <p>Make sure Admin service is running on port 8086.</p>
        <a href="/" style="color: #ffd700;">← Back to Main Dashboard</a>
    </body>
    </html>
    """)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/status")
async def get_global_status():
    """Get global system status"""
    return {
        "status": "operational",
        "components": component_status,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/status/{component}")
async def get_component_status(component: str):
    """Get status of a specific component"""
    if component not in component_status:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return {
        "component": component,
        "status": component_status[component]["status"],
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/memory/live-feed")
async def get_memory_feed():
    """Get live AI memory feed (mock data for now)"""
    import time
    from datetime import datetime
    
    # Mock memory data - replace with real data from AI components
    mock_data = [
        {
            "timestamp": datetime.now().isoformat(),
            "source": "GremlinGPT",
            "content": "Autonomous processing cycle completed"
        },
        {
            "timestamp": datetime.fromtimestamp(time.time() - 5).isoformat(),
            "source": "GodCore", 
            "content": "Model routing optimized for efficiency"
        },
        {
            "timestamp": datetime.fromtimestamp(time.time() - 10).isoformat(),
            "source": "Statik",
            "content": "User session state synchronized"
        },
        {
            "timestamp": datetime.fromtimestamp(time.time() - 15).isoformat(),
            "source": "GremlinGPT",
            "content": "Memory consolidation in progress"
        }
    ]
    
    return mock_data

@app.post("/api/components/{component}/restart")
async def restart_component(component: str):
    """Restart a specific component"""
    if component not in component_status:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Mock restart - replace with actual restart logic
    logger.info(f"Restarting component: {component}")
    
    return {
        "message": f"Component {component} restart initiated",
        "component": component,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ascendnet-api",
        "version": "1.0.0",
        "timestamp": asyncio.get_event_loop().time()
    }

# ============================================================================
# STATIC FILES & ASSETS
# ============================================================================

# Mount static files directory if it exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 AscendNet Unified API Server starting up...")
    logger.info(f"📁 Frontend directory: {FRONTEND_DIR}")
    logger.info(f"📁 Project root: {PROJECT_ROOT}")
    
    # Check component availability
    for component_name, component_info in component_status.items():
        logger.info(f"📊 {component_name}: {component_info['status']} on port {component_info['port']}")
    
    logger.info("✅ AscendNet Unified API Server ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 AscendNet Unified API Server shutting down...")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the AscendNet API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AscendNet Unified API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting AscendNet Unified API Server on {args.host}:{args.port}")
    
    uvicorn.run(
        "api_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level="info"
    )

if __name__ == "__main__":
    main()
