"""
AscendNet Unified AI Core
Integrates GremlinGPT, GodCore, and SignalCore into one system
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from ..utils.logger import get_logger

logger = get_logger("AICore")


class UnifiedSignalCore:
    """Enhanced SignalCore with GremlinGPT and GodCore integration"""

    def __init__(
        self, name: str = "AscendNet", memory_depth: int = 2048, recursion_limit: int = 512
    ):
        self.name = name
        self.memory = []
        self.depth = memory_depth
        self.recursion_limit = recursion_limit
        self.recursion_count = 0
        self.signal_trace = []
        self.state = "idle"

        # GremlinGPT integration
        self.gremlin_enabled = True
        self.autonomous_mode = False

        # GodCore integration
        self.god_core_enabled = True
        self.quantum_storage = {}

        self.logger = logger

    def log(self, signal: Any):
        """Store signal in memory with size management"""
        if len(self.memory) >= self.depth:
            self.memory.pop(0)

        formatted_signal = {
            "timestamp": asyncio.get_event_loop().time(),
            "type": type(signal).__name__,
            "content": str(signal)[:1024],  # Limit content size
            "state": self.state,
        }

        self.memory.append(formatted_signal)
        self.logger.debug(f"Signal logged: {formatted_signal['type']}")

    def trace_signal(self, signal: str):
        """Store signal trace for backtracking"""
        self.signal_trace.append(
            {"signal": signal, "timestamp": asyncio.get_event_loop().time(), "state": self.state}
        )

        if len(self.signal_trace) > self.depth:
            self.signal_trace = self.signal_trace[-self.depth :]

    def get_last_signal(self) -> Optional[Dict[str, Any]]:
        """Get most recent signal"""
        return self.memory[-1] if self.memory else None

    def evolve_state(self, trigger: str = "manual"):
        """Evolve AI state based on triggers"""
        previous_state = self.state

        if trigger == "manual":
            self.state = "evolving"
        elif trigger == "failure":
            self.state = "recovering"
        elif trigger == "loop":
            self.state = "overload"
        elif trigger == "gremlin":
            self.state = "autonomous"
        elif trigger == "god_core":
            self.state = "transcendent"
        else:
            self.state = "active"

        self.logger.info(f"State evolution: {previous_state} -> {self.state} (trigger: {trigger})")
        self.trace_signal(f"state_change:{previous_state}->{self.state}")

    def check_recursion(self):
        """Prevent recursion overload with safety limits"""
        self.recursion_count += 1
        if self.recursion_count >= self.recursion_limit:
            self.state = "overload"
            self.logger.warning(f"Recursion limit reached: {self.recursion_count}")
            raise RecursionError("AscendNet recursion limit reached. Evolution required.")

    def reset_recursion(self):
        """Reset recursion counter"""
        self.recursion_count = 0

    async def think(self, iterations: int = 1, mutation_fn: Optional[Callable] = None):
        """Enhanced thinking with async support and mutations"""
        self.logger.info(f"Beginning thought cycle: {iterations} iterations")

        for i in range(iterations):
            try:
                self.check_recursion()

                signal = self.get_last_signal()
                if signal:
                    thought = f"thinking_cycle_{i}:{signal['content'][:64]}"
                    self.trace_signal(thought)

                    # GremlinGPT autonomous processing
                    if self.gremlin_enabled and self.autonomous_mode:
                        await self._gremlin_process(signal)

                    # GodCore quantum processing
                    if self.god_core_enabled:
                        await self._god_core_process(signal)

                # Apply mutation if provided
                if mutation_fn:
                    await self._apply_mutation(mutation_fn)

                # Small delay for async processing
                await asyncio.sleep(0.001)

            except RecursionError:
                self.logger.error("Recursion limit exceeded, entering recovery mode")
                self.evolve_state("failure")
                break
            except Exception as e:
                self.logger.error(f"Error in thinking cycle {i}: {e}")

        self.reset_recursion()
        self.state = "thinking_complete"
        self.logger.info("Thought cycle complete")

    async def _gremlin_process(self, signal: Dict[str, Any]):
        """GremlinGPT autonomous processing"""
        try:
            # Simulate GremlinGPT autonomous decision making
            if "error" in signal["content"].lower():
                self.evolve_state("gremlin")
                self.autonomous_mode = True
                self.trace_signal("gremlin_autonomous_mode_activated")

        except Exception as e:
            self.logger.error(f"GremlinGPT processing error: {e}")

    async def _god_core_process(self, signal: Dict[str, Any]):
        """GodCore quantum processing and storage"""
        try:
            # Quantum storage compression simulation
            compressed_signal = self._quantum_compress(signal)
            self.quantum_storage[signal["timestamp"]] = compressed_signal

            # Transcendence detection
            if len(self.quantum_storage) > 1000:
                self.evolve_state("god_core")
                self.trace_signal("god_core_transcendence_achieved")

        except Exception as e:
            self.logger.error(f"GodCore processing error: {e}")

    def _quantum_compress(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate quantum compression"""
        return {
            "compressed": True,
            "original_size": len(str(data)),
            "compressed_size": len(str(data)) // 2,  # Simulated compression
            "checksum": hash(str(data)),
            "content_hash": str(data)[:32],
        }

    async def _apply_mutation(self, mutation_fn: Callable):
        """Apply mutation function to memory and trace"""
        try:
            mutated = await mutation_fn(self.memory, self.signal_trace)
            self.log(mutated)
            self.trace_signal(f"mutation_applied:{str(mutated)[:64]}")
            self.state = "mutating"
        except Exception as e:
            self.logger.error(f"Mutation error: {e}")
            self.trace_signal(f"mutation_error:{str(e)}")
            self.state = "error"

    async def receive_signal(self, external_signal: Any):
        """Receive and process external signals"""
        formatted = f"external:{str(external_signal)[:128]}"
        self.log(formatted)
        self.trace_signal(formatted)
        self.state = "synced"

        # Auto-trigger thinking if in autonomous mode
        if self.autonomous_mode:
            await self.think(iterations=1)

    def export_memory(self) -> Dict[str, Any]:
        """Export memory state for persistence"""
        return {
            "name": self.name,
            "memory": self.memory,
            "signal_trace": self.signal_trace,
            "state": self.state,
            "quantum_storage": self.quantum_storage,
            "config": {
                "depth": self.depth,
                "recursion_limit": self.recursion_limit,
                "gremlin_enabled": self.gremlin_enabled,
                "god_core_enabled": self.god_core_enabled,
                "autonomous_mode": self.autonomous_mode,
            },
        }

    def load_memory(self, memory_data: Dict[str, Any]):
        """Load memory state from persistence"""
        self.name = memory_data.get("name", self.name)
        self.memory = memory_data.get("memory", [])
        self.signal_trace = memory_data.get("signal_trace", [])
        self.state = memory_data.get("state", "idle")
        self.quantum_storage = memory_data.get("quantum_storage", {})

        config = memory_data.get("config", {})
        self.depth = config.get("depth", self.depth)
        self.recursion_limit = config.get("recursion_limit", self.recursion_limit)
        self.gremlin_enabled = config.get("gremlin_enabled", True)
        self.god_core_enabled = config.get("god_core_enabled", True)
        self.autonomous_mode = config.get("autonomous_mode", False)


class AscendNetAICore:
    """Main AI Core orchestrator for AscendNet"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.signal_core = UnifiedSignalCore(
            name="AscendNet-Core",
            memory_depth=config.get("memory_depth", 2048),
            recursion_limit=config.get("recursion_limit", 512),
        )
        self.logger = logger
        self.soul_path = (
            Path(os.environ.get("HOME", "/home/user"))
            / "AscendNet"
            / "storage"
            / "memory"
            / "soul.json"
        )

    async def initialize(self):
        """Initialize the AI core system"""
        self.logger.info("Initializing AscendNet AI Core...")

        # Load existing soul/memory if available
        await self._load_soul()

        # Initialize components
        if self.config.get("gremlin_gpt_enabled", True):
            self.logger.info("GremlinGPT integration enabled")

        if self.config.get("god_core_enabled", True):
            self.logger.info("GodCore integration enabled")

        if self.config.get("signal_core_enabled", True):
            self.logger.info("SignalCore integration enabled")

        self.logger.info("AI Core initialization complete")

    async def _load_soul(self):
        """Load persistent soul/memory state"""
        try:
            if self.soul_path.exists():
                with open(self.soul_path, "r") as f:
                    soul_data = json.load(f)
                    self.signal_core.load_memory(soul_data)
                    self.logger.info("Soul memory loaded from persistence")
            else:
                self.logger.info("No existing soul found, starting fresh")
        except Exception as e:
            self.logger.error(f"Failed to load soul: {e}")

    async def save_soul(self):
        """Save persistent soul/memory state"""
        try:
            self.soul_path.parent.mkdir(parents=True, exist_ok=True)
            soul_data = self.signal_core.export_memory()

            with open(self.soul_path, "w") as f:
                json.dump(soul_data, f, indent=2)

            self.logger.info("Soul memory saved to persistence")
        except Exception as e:
            self.logger.error(f"Failed to save soul: {e}")

    async def process_signal(self, signal: Any) -> Dict[str, Any]:
        """Process incoming signal through the AI core"""
        await self.signal_core.receive_signal(signal)
        await self.save_soul()

        return {
            "status": "processed",
            "core_state": self.signal_core.state,
            "memory_size": len(self.signal_core.memory),
            "trace_size": len(self.signal_core.signal_trace),
        }

    async def think_cycle(self, iterations: int = 1) -> Dict[str, Any]:
        """Execute a thinking cycle"""
        await self.signal_core.think(iterations=iterations)
        await self.save_soul()

        return {
            "status": "complete",
            "iterations": iterations,
            "final_state": self.signal_core.state,
            "memory_snapshot": self.signal_core.get_last_signal(),
        }
