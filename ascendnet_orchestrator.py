#!/usr/bin/env python3
"""
AscendNet Orchestrator
======================

Main orchestrator that manages and coordinates all AscendNet components.
This is the master control system that ensures all services work together.
"""

import os
import sys
import asyncio
import logging
import signal
import time
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ascendnet-orchestrator")

PROJECT_ROOT = Path(__file__).parent

@dataclass
class ComponentConfig:
    """Configuration for an AscendNet component"""
    name: str
    description: str
    port: int
    startup_script: str
    health_endpoint: str
    dependencies: List[str]
    enabled: bool = True
    process: Optional[subprocess.Popen] = None
    status: str = "stopped"
    last_health_check: Optional[datetime] = None

class AscendNetOrchestrator:
    """Main orchestrator for AscendNet components"""
    
    def __init__(self):
        self.components: Dict[str, ComponentConfig] = {}
        self.running = False
        self.health_check_interval = 30  # seconds
        self.startup_timeout = 60  # seconds
        self.setup_components()
        
    def setup_components(self):
        """Setup component configurations"""
        self.components = {
            "api-server": ComponentConfig(
                name="AscendNet API",
                description="Unified API server and dashboard",
                port=8000,
                startup_script="python api_server.py --host 0.0.0.0 --port 8000",
                health_endpoint="http://localhost:8000/api/health",
                dependencies=[]
            ),
            "statik-server": ComponentConfig(
                name="Statik-Server",
                description="VS Code + Copilot + Mesh VPN",
                port=8080,
                startup_script="cd statik-server && ./startup.sh",
                health_endpoint="http://localhost:8080/healthz",
                dependencies=["api-server"]
            ),
            "gremlin-gpt": ComponentConfig(
                name="GremlinGPT",
                description="Autonomous AI Agent",
                port=8081,
                startup_script="cd backend/ai_core/AscendAI/GremlinGPT && python -m gremlin.main",
                health_endpoint="http://localhost:8081/health",
                dependencies=["api-server"]
            ),
            "godcore": ComponentConfig(
                name="GodCore",
                description="Multi-model AI Router",
                port=8082,
                startup_script="cd godcore && python -m godcore.main",
                health_endpoint="http://localhost:8082/health",
                dependencies=["api-server"]
            ),
            "mobile-mirror": ComponentConfig(
                name="Mobile-Mirror",
                description="Mobile development environment",
                port=8083,
                startup_script="cd backend/Mobile-Mirror && python -m mobilemirror.main",
                health_endpoint="http://localhost:8083/health",
                dependencies=["api-server", "statik-server"]
            ),
            "p2p-network": ComponentConfig(
                name="P2P Network",
                description="Decentralized marketplace",
                port=8084,
                startup_script="cd backend/p2p && python -m p2p.main",
                health_endpoint="http://localhost:8084/health",
                dependencies=["api-server"]
            ),
            "ai-memory": ComponentConfig(
                name="AI Memory",
                description="Neural network memory system",
                port=8085,
                startup_script="cd backend/ai_core && python -m memory.main",
                health_endpoint="http://localhost:8085/health",
                dependencies=["api-server"]
            )
        }
        
        logger.info(f"📋 Configured {len(self.components)} components")
    
    async def start_component(self, component_name: str) -> bool:
        """Start a specific component"""
        if component_name not in self.components:
            logger.error(f"❌ Unknown component: {component_name}")
            return False
        
        component = self.components[component_name]
        
        if component.status == "running":
            logger.info(f"✅ {component.name} already running")
            return True
        
        if not component.enabled:
            logger.info(f"⏸️ {component.name} is disabled, skipping")
            return True
        
        logger.info(f"🚀 Starting {component.name}...")
        
        try:
            # Check dependencies first
            for dep in component.dependencies:
                if dep in self.components and self.components[dep].status != "running":
                    logger.info(f"⏳ Waiting for dependency: {dep}")
                    if not await self.start_component(dep):
                        logger.error(f"❌ Failed to start dependency {dep} for {component.name}")
                        return False
            
            # Start the component
            process = subprocess.Popen(
                component.startup_script,
                shell=True,
                cwd=PROJECT_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            component.process = process
            component.status = "starting"
            
            # Wait for startup with timeout
            startup_time = 0
            while startup_time < self.startup_timeout:
                if await self.health_check_component(component_name):
                    component.status = "running"
                    logger.info(f"✅ {component.name} started successfully on port {component.port}")
                    return True
                
                if process.poll() is not None:
                    # Process has exited
                    stdout, stderr = process.communicate()
                    logger.error(f"❌ {component.name} failed to start")
                    logger.error(f"📤 stdout: {stdout}")
                    logger.error(f"📤 stderr: {stderr}")
                    component.status = "failed"
                    return False
                
                await asyncio.sleep(2)
                startup_time += 2
            
            logger.error(f"⏰ {component.name} startup timeout")
            component.status = "timeout"
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting {component.name}: {e}")
            component.status = "error"
            return False
    
    async def stop_component(self, component_name: str) -> bool:
        """Stop a specific component"""
        if component_name not in self.components:
            logger.error(f"❌ Unknown component: {component_name}")
            return False
        
        component = self.components[component_name]
        
        if component.status != "running":
            logger.info(f"⏹️ {component.name} not running")
            return True
        
        logger.info(f"🛑 Stopping {component.name}...")
        
        try:
            if component.process:
                component.process.terminate()
                try:
                    component.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ Force killing {component.name}")
                    component.process.kill()
                    component.process.wait()
                
                component.process = None
            
            component.status = "stopped"
            logger.info(f"✅ {component.name} stopped")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error stopping {component.name}: {e}")
            return False
    
    async def health_check_component(self, component_name: str) -> bool:
        """Check health of a specific component"""
        if component_name not in self.components:
            return False
        
        component = self.components[component_name]
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(component.health_endpoint, timeout=5) as response:
                    healthy = response.status == 200
                    component.last_health_check = datetime.now()
                    if not healthy and component.status == "running":
                        logger.warning(f"⚠️ {component.name} health check failed")
                    return healthy
        except:
            # If health check fails, assume component is not ready yet
            return False
    
    async def health_check_all(self):
        """Perform health checks on all components"""
        for component_name in self.components:
            if self.components[component_name].status == "running":
                healthy = await self.health_check_component(component_name)
                if not healthy:
                    logger.warning(f"⚠️ {component_name} health check failed")
    
    async def start_all(self) -> bool:
        """Start all enabled components in dependency order"""
        logger.info("🚀 Starting AscendNet Unified System...")
        
        # Determine startup order based on dependencies
        startup_order = self._get_startup_order()
        
        for component_name in startup_order:
            if not await self.start_component(component_name):
                logger.error(f"❌ Failed to start {component_name}, stopping startup")
                return False
        
        logger.info("✅ AscendNet Unified System started successfully!")
        logger.info(f"🎯 Access the dashboard at: http://localhost:8000")
        return True
    
    async def stop_all(self):
        """Stop all components"""
        logger.info("🛑 Stopping AscendNet Unified System...")
        
        # Stop in reverse dependency order
        startup_order = self._get_startup_order()
        for component_name in reversed(startup_order):
            await self.stop_component(component_name)
        
        logger.info("✅ AscendNet Unified System stopped")
    
    def _get_startup_order(self) -> List[str]:
        """Get component startup order based on dependencies"""
        order = []
        visited = set()
        temp_visited = set()
        
        def visit(component_name):
            if component_name in temp_visited:
                raise ValueError(f"Circular dependency detected involving {component_name}")
            if component_name in visited:
                return
            
            temp_visited.add(component_name)
            
            if component_name in self.components:
                for dep in self.components[component_name].dependencies:
                    visit(dep)
            
            temp_visited.remove(component_name)
            visited.add(component_name)
            order.append(component_name)
        
        for component_name in self.components:
            if component_name not in visited:
                visit(component_name)
        
        return order
    
    async def monitor_system(self):
        """Monitor system health and restart failed components"""
        while self.running:
            await self.health_check_all()
            await asyncio.sleep(self.health_check_interval)
    
    async def run(self):
        """Main orchestrator run loop"""
        self.running = True
        
        # Setup signal handlers
        for sig in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(sig, self._signal_handler)
        
        try:
            # Start all components
            if not await self.start_all():
                logger.error("❌ Failed to start AscendNet system")
                return 1
            
            # Start monitoring
            monitor_task = asyncio.create_task(self.monitor_system())
            
            logger.info("🔄 AscendNet Orchestrator running... (Ctrl+C to stop)")
            
            # Wait for shutdown signal
            while self.running:
                await asyncio.sleep(1)
            
            # Cleanup
            monitor_task.cancel()
            await self.stop_all()
            
        except Exception as e:
            logger.error(f"❌ Orchestrator error: {e}")
            return 1
        
        return 0
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum}, initiating shutdown...")
        self.running = False
    
    def status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "system": {
                "running": self.running,
                "timestamp": datetime.now().isoformat()
            },
            "components": {
                name: {
                    "name": comp.name,
                    "description": comp.description,
                    "port": comp.port,
                    "status": comp.status,
                    "enabled": comp.enabled,
                    "last_health_check": comp.last_health_check.isoformat() if comp.last_health_check else None
                }
                for name, comp in self.components.items()
            }
        }

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AscendNet Orchestrator")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--start", metavar="COMPONENT", help="Start specific component")
    parser.add_argument("--stop", metavar="COMPONENT", help="Stop specific component")
    parser.add_argument("--restart", metavar="COMPONENT", help="Restart specific component")
    
    args = parser.parse_args()
    
    orchestrator = AscendNetOrchestrator()
    
    if args.status:
        status = orchestrator.status()
        print(json.dumps(status, indent=2))
        return 0
    
    if args.start:
        success = await orchestrator.start_component(args.start)
        return 0 if success else 1
    
    if args.stop:
        success = await orchestrator.stop_component(args.stop)
        return 0 if success else 1
    
    if args.restart:
        await orchestrator.stop_component(args.restart)
        success = await orchestrator.start_component(args.restart)
        return 0 if success else 1
    
    # Default: run the full orchestrator
    return await orchestrator.run()

if __name__ == "__main__":
    try:
        import aiohttp
    except ImportError:
        print("📦 Installing required dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp"], check=True)
    
    sys.exit(asyncio.run(main()))
