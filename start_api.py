#!/usr/bin/env python3
"""
AscendNet Unified System Launcher
=================================

Quick launcher script that starts the unified AscendNet dashboard.
This provides a simple way to launch the entire platform.
"""

import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ascendnet-launcher")

PROJECT_ROOT = Path(__file__).parent

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        logger.info("✅ FastAPI dependencies found")
        return True
    except ImportError:
        logger.error("❌ FastAPI dependencies missing")
        logger.info("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]", "jinja2"], check=True)
        return True

def start_unified_dashboard():
    """Start the unified AscendNet dashboard"""
    try:
        logger.info("🚀 Starting AscendNet Unified Dashboard...")
        
        # Change to project directory
        os.chdir(PROJECT_ROOT)
        
        # Start the API server
        cmd = [
            sys.executable, 
            "api_server.py",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        logger.info(f"📡 Server starting on http://localhost:8000")
        logger.info("🎯 Access the unified dashboard at: http://localhost:8000")
        logger.info("📊 API documentation at: http://localhost:8000/api/docs")
        
        # Start the server
        process = subprocess.Popen(cmd)
        
        # Wait for interrupt
        try:
            process.wait()
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down AscendNet...")
            process.terminate()
            process.wait()
            logger.info("✅ AscendNet shutdown complete")
            
    except Exception as e:
        logger.error(f"❌ Error starting dashboard: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🔥 AscendNet Unified System Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Dependency check failed")
        return 1
    
    # Start dashboard
    if not start_unified_dashboard():
        logger.error("❌ Failed to start dashboard")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
