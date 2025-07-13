"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.StatikMemoryRouter = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const express_1 = require("express");
class StatikMemoryRouter {
    constructor() {
        this.memoryPath = path.join(os.homedir(), "AscendNet", "storage", "memory");
        this.router = (0, express_1.Router)();
        this.setupRoutes();
    }
    setupRoutes() {
        // Unified memory API
        this.router.get("/api/statik/memory", (req, res) => {
            const memoryState = this.loadUnifiedMemory();
            res.json(memoryState);
        });
        // GremlinGPT FSM state
        this.router.get("/api/statik/gremlin", (req, res) => {
            const gremlinState = this.loadGremlinState();
            res.json(gremlinState);
        });
        // GodCore execution context
        this.router.get("/api/statik/godcore", (req, res) => {
            const godCoreState = this.loadGodCoreState();
            res.json(godCoreState);
        });
        // Mobile-Mirror dashboard
        this.router.get("/api/statik/mobile", (req, res) => {
            const mobileState = this.loadMobileState();
            res.json(mobileState);
        });
        // Live memory feed (SSE)
        this.router.get("/api/statik/memory/live", (req, res) => {
            res.writeHead(200, {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            });
            // Send memory updates every 2 seconds
            const interval = setInterval(() => {
                const memory = this.loadUnifiedMemory();
                res.write(`data: ${JSON.stringify(memory)}\n\n`);
            }, 2000);
            req.on("close", () => clearInterval(interval));
        });
    }
    loadUnifiedMemory() {
        return {
            gremlinGPT: this.loadGremlinState(),
            godCore: this.loadGodCoreState(),
            mobileMirror: this.loadMobileState(),
            signalCore: this.loadSignalCoreState()
        };
    }
    loadGremlinState() {
        const soulPath = path.join(this.memoryPath, "soul.json");
        if (fs.existsSync(soulPath)) {
            try {
                const soulData = JSON.parse(fs.readFileSync(soulPath, "utf8"));
                return {
                    fsm_state: soulData.state || "idle",
                    memory_entries: soulData.memory || [],
                    signal_trace: soulData.signal_trace || [],
                    autonomous_mode: soulData.autonomous_mode || false
                };
            }
            catch (error) {
                console.warn("Error loading soul.json:", error);
            }
        }
        return {
            fsm_state: "idle",
            memory_entries: [],
            signal_trace: [],
            autonomous_mode: false
        };
    }
    loadGodCoreState() {
        const godCorePath = path.join(os.homedir(), "AscendNet", "GodCore");
        // Check if GodCore directory exists and load state
        if (fs.existsSync(godCorePath)) {
            return {
                shell_state: "ready",
                execution_context: { status: "online" },
                quantum_storage: [],
                model_status: [
                    { name: "Mistral-13B", status: "online", load: Math.floor(Math.random() * 50 + 20) },
                    { name: "Monday.AI", status: "online", load: Math.floor(Math.random() * 30 + 10) },
                    { name: "GPT-4", status: "offline", load: 0 }
                ]
            };
        }
        return {
            shell_state: "offline",
            execution_context: {},
            quantum_storage: [],
            model_status: []
        };
    }
    loadMobileState() {
        const mobilePath = path.join(os.homedir(), "AscendNet", "Mobile-Mirror");
        // Check if Mobile-Mirror directory exists
        if (fs.existsSync(mobilePath)) {
            return {
                dashboard_state: { active: true },
                tunnel_status: "connected",
                pwa_ready: true,
                connected_devices: [
                    { name: "iPhone 15 Pro", ip: "100.64.0.3", status: "online" },
                    { name: "Samsung Galaxy S24", ip: "100.64.0.4", status: "online" }
                ]
            };
        }
        return {
            dashboard_state: { active: false },
            tunnel_status: "disconnected",
            pwa_ready: false,
            connected_devices: []
        };
    }
    loadSignalCoreState() {
        return {
            state: "active",
            memory_depth: 2048,
            recursion_count: Math.floor(Math.random() * 100),
            soul_integrity: 94.7
        };
    }
    getRouter() {
        return this.router;
    }
}
exports.StatikMemoryRouter = StatikMemoryRouter;
//# sourceMappingURL=memory-router.js.map