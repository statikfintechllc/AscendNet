import * as fs from "fs"
import * as path from "path"
import { Router } from "express"

export interface MemoryState {
  system?: {
    timestamp: string
    statik_server_version: string
    memory_router_active: boolean
    uptime: number
  }
  gremlinGPT: {
    fsm_state: string
    memory_entries: any[]
    signal_trace: any[]
  }
  godCore: {
    shell_state: string
    execution_context: any
    quantum_storage: any[]
  }
  mobileMirror: {
    dashboard_state: any
    tunnel_status: string
    pwa_ready: boolean
  }
}

export class StatikMemoryRouter {
  private memoryPath = process.env.HOME + "/AscendNet/storage/memory"
  private router = Router()
  
  constructor() {
    this.setupRoutes()
  }
  
  private setupRoutes(): void {
    // Unified memory API
    this.router.get("/api/statik/memory", (req: any, res: any) => {
      const memoryState = this.loadUnifiedMemory()
      res.json(memoryState)
    })
    
    // GremlinGPT FSM state
    this.router.get("/api/statik/gremlin", (req: any, res: any) => {
      const gremlinState = this.loadGremlinState()
      res.json(gremlinState)
    })
    
    // GodCore execution context
    this.router.get("/api/statik/godcore", (req: any, res: any) => {
      const godCoreState = this.loadGodCoreState()
      res.json(godCoreState)
    })
    
    // Mobile-Mirror dashboard
    this.router.get("/api/statik/mobile", (req: any, res: any) => {
      const mobileState = this.loadMobileState()
      res.json(mobileState)
    })
    
    // Live memory feed (SSE)
    this.router.get("/api/statik/memory/live", (req: any, res: any) => {
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
      })
      
      // Send memory updates every 2 seconds
      const interval = setInterval(() => {
        const memory = this.loadUnifiedMemory()
        res.write(`data: ${JSON.stringify(memory)}\n\n`)
      }, 2000)
      
      req.on("close", () => clearInterval(interval))
    })
  }
  
  private loadUnifiedMemory(): MemoryState {
    const timestamp = new Date().toISOString()
    const systemInfo = {
      timestamp,
      statik_server_version: "1.0.0",
      memory_router_active: true,
      uptime: process.uptime()
    }
    
    return {
      system: systemInfo,
      gremlinGPT: this.loadGremlinState(),
      godCore: this.loadGodCoreState(),
      mobileMirror: this.loadMobileState()
    }
  }
  
  private loadGremlinState(): any {
    const soulPath = path.join(this.memoryPath, "soul.json")
    if (fs.existsSync(soulPath)) {
      return JSON.parse(fs.readFileSync(soulPath, "utf8"))
    }
    return { fsm_state: "idle", memory_entries: [], signal_trace: [] }
  }
  
  private loadGodCoreState(): any {
    const godCorePath = process.env.HOME + "/AscendNet/godcore"
    const stateFile = path.join(godCorePath, "godcore_state.json")
    
    try {
      if (fs.existsSync(stateFile)) {
        return JSON.parse(fs.readFileSync(stateFile, "utf8"))
      }
    } catch (error) {
      console.warn("Failed to load GodCore state:", error)
    }
    
    // Default state if file doesn't exist or fails to load
    return { 
      shell_state: "ready", 
      execution_context: {}, 
      quantum_storage: [],
      models_loaded: [],
      routing_active: false
    }
  }
  
  private loadMobileState(): any {
    const mobilePath = process.env.HOME + "/AscendNet/backend/Mobile-Mirror"
    const stateFile = path.join(mobilePath, "mobilemirror", "state", "dashboard.json")
    
    try {
      if (fs.existsSync(stateFile)) {
        return JSON.parse(fs.readFileSync(stateFile, "utf8"))
      }
    } catch (error) {
      console.warn("Failed to load Mobile-Mirror state:", error)
    }
    
    // Default state if file doesn't exist or fails to load
    return { 
      dashboard_state: { active_tabs: 0, connected_devices: [] }, 
      tunnel_status: "connected", 
      pwa_ready: true,
      touchcore_active: false
    }
  }
  
  getRouter(): Router {
    return this.router
  }
}
