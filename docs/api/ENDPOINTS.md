# AscendNet API Documentation

## 📡 Statik-Server API Reference

This document covers all API endpoints available in the Statik-Server unified system.

## 🔗 Base URLs

- **Primary API:** `http://localhost:8080/api/statik/`
- **Dashboard:** `http://localhost:8080/statik-dashboard`
- **Mesh VPN:** `http://localhost:8081/`

## 🧠 Memory Management API

### Get Unified Memory State

**Endpoint:** `GET /api/statik/memory`

**Description:** Returns the current memory state of all AI modules.

**Response:**
```json
{
  "gremlinGPT": {
    "fsm_state": "active",
    "memory_entries": [...],
    "signal_trace": [...],
    "autonomous_mode": false
  },
  "godCore": {
    "shell_state": "ready",
    "execution_context": {...},
    "quantum_storage": [...],
    "model_status": [...]
  },
  "mobileMirror": {
    "dashboard_state": {...},
    "tunnel_status": "connected",
    "pwa_ready": true,
    "connected_devices": [...]
  },
  "signalCore": {
    "state": "active",
    "memory_depth": 2048,
    "recursion_count": 45,
    "soul_integrity": 94.7
  }
}
```

### Live Memory Feed (SSE)

**Endpoint:** `GET /api/statik/memory/live`

**Description:** Server-Sent Events stream for real-time memory updates.

**Headers:**
```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

**Example Usage:**
```javascript
const eventSource = new EventSource('/api/statik/memory/live');
eventSource.onmessage = function(event) {
  const memoryState = JSON.parse(event.data);
  updateDashboard(memoryState);
};
```

### Clear Memory

**Endpoint:** `POST /api/statik/memory/clear`

**Description:** Clears all memory states and resets to defaults.

**Response:**
```json
{
  "success": true,
  "message": "Memory cleared successfully"
}
```

### Export Memory

**Endpoint:** `GET /api/statik/memory/export`

**Description:** Downloads complete memory state as JSON file.

**Response:** File download with filename pattern: `statik-memory-{timestamp}.json`

## 🧬 GremlinGPT API

### Get GremlinGPT State

**Endpoint:** `GET /api/statik/gremlin`

**Description:** Returns current FSM state and configuration.

**Response:**
```json
{
  "fsm_state": "thinking",
  "memory_entries": [
    {
      "timestamp": "2025-07-12T10:30:00Z",
      "content": "Processing autonomous decision tree...",
      "type": "cognitive"
    }
  ],
  "signal_trace": [
    {
      "state": "idle",
      "transition": "external_input",
      "timestamp": "2025-07-12T10:29:55Z"
    }
  ],
  "autonomous_mode": false
}
```

### Chat with GremlinGPT

**Endpoint:** `POST /api/statik/gremlin/chat`

**Request Body:**
```json
{
  "message": "Hello GremlinGPT, what's your current state?"
}
```

**Response:**
```json
{
  "response": "Processing autonomous decision tree...",
  "fsm_state": "active",
  "timestamp": "2025-07-12T10:30:00Z"
}
```

### Toggle Autonomous Mode

**Endpoint:** `POST /api/statik/gremlin/autonomous`

**Request Body:**
```json
{
  "autonomous": true
}
```

**Response:**
```json
{
  "success": true,
  "autonomous": true,
  "message": "Autonomous mode enabled"
}
```

### Reset FSM State

**Endpoint:** `POST /api/statik/gremlin/reset`

**Description:** Resets FSM to idle state and clears signal trace.

**Response:**
```json
{
  "success": true,
  "state": "idle",
  "message": "FSM reset to idle state"
}
```

### Step FSM Forward

**Endpoint:** `POST /api/statik/gremlin/step`

**Description:** Manually advances FSM to next state.

**Response:**
```json
{
  "success": true,
  "state": "thinking",
  "previous_state": "idle"
}
```

### Pause FSM

**Endpoint:** `POST /api/statik/gremlin/pause`

**Description:** Pauses FSM execution.

**Response:**
```json
{
  "success": true,
  "message": "FSM paused"
}
```

## ⚡ GodCore API

### Get GodCore State

**Endpoint:** `GET /api/statik/godcore`

**Description:** Returns multi-model routing status and available models.

**Response:**
```json
{
  "shell_state": "ready",
  "execution_context": {
    "status": "online",
    "active_models": 3
  },
  "quantum_storage": [],
  "model_status": [
    {
      "name": "Mistral-13B",
      "status": "online",
      "load": 35,
      "response_time": 120
    },
    {
      "name": "Monday.AI",
      "status": "online", 
      "load": 15,
      "response_time": 80
    },
    {
      "name": "GPT-4",
      "status": "offline",
      "load": 0,
      "response_time": null
    }
  ]
}
```

### Chat with GodCore

**Endpoint:** `POST /api/statik/godcore/chat`

**Request Body:**
```json
{
  "message": "Route this query optimally",
  "model": "auto"
}
```

**Model Options:** `"auto"`, `"mistral"`, `"gpt-4"`, `"claude"`, `"monday"`

**Response:**
```json
{
  "response": "[MISTRAL] Quantum processing complete. Response optimized for your query.",
  "model": "mistral",
  "routing_decision": "selected_for_optimization",
  "timestamp": "2025-07-12T10:30:00Z"
}
```

### Refresh Models

**Endpoint:** `POST /api/statik/godcore/models/refresh`

**Description:** Refreshes model status and availability.

**Response:**
```json
{
  "success": true,
  "models_refreshed": 3,
  "message": "Model status updated"
}
```

### Optimize Routing

**Endpoint:** `POST /api/statik/godcore/routing/optimize`

**Description:** Triggers routing algorithm optimization.

**Response:**
```json
{
  "success": true,
  "optimization_complete": true,
  "routing_efficiency": 94.2
}
```

## 📱 Mobile-Mirror API

### Get Mobile-Mirror State

**Endpoint:** `GET /api/statik/mobile`

**Description:** Returns TouchCore dashboard status and connected devices.

**Response:**
```json
{
  "dashboard_state": {
    "active": true,
    "tabs": 4,
    "active_sessions": 2
  },
  "tunnel_status": "connected",
  "pwa_ready": true,
  "connected_devices": [
    {
      "name": "iPhone 15 Pro",
      "ip": "100.64.0.3",
      "status": "online",
      "last_seen": "2025-07-12T10:29:00Z"
    },
    {
      "name": "Samsung Galaxy S24",
      "ip": "100.64.0.4", 
      "status": "online",
      "last_seen": "2025-07-12T10:28:00Z"
    }
  ]
}
```

### Start Mobile Tunnel

**Endpoint:** `POST /api/statik/mobile/tunnel/start`

**Description:** Initiates tunnel for mobile device connection.

**Response:**
```json
{
  "success": true,
  "tunnel_id": "tunnel-abc123",
  "connection_url": "http://100.64.0.1:8080",
  "expires_at": "2025-07-12T18:30:00Z"
}
```

## 🌐 System API

### Get System Status

**Endpoint:** `GET /api/statik/status`

**Description:** Returns overall system health and service status.

**Response:**
```json
{
  "status": "healthy",
  "uptime": 3600,
  "memory": {
    "rss": 134217728,
    "heapTotal": 67108864,
    "heapUsed": 45088768,
    "external": 1024
  },
  "cpu": {
    "user": 1000000,
    "system": 500000
  },
  "services": {
    "statik-server": "running",
    "headscale": "running", 
    "gremlin-gpt": "running",
    "god-core": "running",
    "mobile-mirror": "running"
  }
}
```

### Restart System

**Endpoint:** `POST /api/statik/system/restart`

**Description:** Initiates system restart (requires admin privileges).

**Response:**
```json
{
  "success": true,
  "message": "System restart initiated",
  "restart_time": "2025-07-12T10:31:00Z"
}
```

### Update System

**Endpoint:** `POST /api/statik/system/update`

**Description:** Triggers system update process.

**Response:**
```json
{
  "success": true,
  "message": "Update process initiated",
  "update_id": "update-xyz789"
}
```

### Restart Service

**Endpoint:** `POST /api/statik/system/services/{service}/restart`

**Path Parameters:**
- `service`: Service name (`statik-server`, `headscale`, `gremlin-gpt`, `god-core`)

**Response:**
```json
{
  "success": true,
  "service": "gremlin-gpt",
  "message": "gremlin-gpt restart initiated"
}
```

## 🌐 Mesh VPN API

### Get Mesh Status

**Endpoint:** `GET /api/statik/mesh/status`

**Description:** Returns mesh network status and statistics.

**Response:**
```json
{
  "connectedNodes": 5,
  "meshIP": "100.64.0.1",
  "status": "connected",
  "bytesIn": 15728640,
  "bytesOut": 8388608,
  "latency": 25,
  "nodes": [
    {
      "name": "iPhone-Pro",
      "ip": "100.64.0.3",
      "status": "online",
      "latency": 12
    },
    {
      "name": "MacBook-Air",
      "ip": "100.64.0.4",
      "status": "online", 
      "latency": 8
    }
  ]
}
```

### Generate Preauth Key

**Endpoint:** `POST /api/statik/mesh/keys/generate`

**Description:** Generates new preauth key for device onboarding.

**Response:**
```json
{
  "success": true,
  "key": "nodekey-1720785000-abc123def456",
  "expires": "never",
  "reusable": true
}
```

## 🔒 Authentication

### API Key Authentication

For programmatic access, include your GitHub token in the Authorization header:

```bash
curl -H "Authorization: Bearer $(cat ~/.statik/keys/github-token)" \
     http://localhost:8080/api/statik/memory
```

### Session Authentication

Web dashboard uses session-based authentication. Users are redirected to login if not authenticated.

## 📊 Response Formats

### Success Response

```json
{
  "success": true,
  "data": {...},
  "timestamp": "2025-07-12T10:30:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request parameters",
    "details": "Field 'model' is required"
  },
  "timestamp": "2025-07-12T10:30:00Z"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

## 🔧 Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Default limit:** 100 requests per minute per IP
- **Burst limit:** 10 requests per second
- **Headers included in response:**
  - `X-RateLimit-Limit`: Requests per minute
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## 📡 WebSocket API

### Real-time Updates

Connect to WebSocket for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/statik');

ws.onmessage = function(event) {
  const update = JSON.parse(event.data);
  console.log('Real-time update:', update);
};

// Subscribe to specific modules
ws.send(JSON.stringify({
  action: 'subscribe',
  modules: ['gremlinGPT', 'godCore']
}));
```

### WebSocket Message Types

**Subscription:**
```json
{
  "action": "subscribe",
  "modules": ["gremlinGPT", "godCore", "mobileMirror"]
}
```

**Update Message:**
```json
{
  "type": "update",
  "module": "gremlinGPT",
  "data": {
    "fsm_state": "thinking",
    "timestamp": "2025-07-12T10:30:00Z"
  }
}
```

## 🧪 Testing API Endpoints

### Using cURL

```bash
# Get memory state
curl http://localhost:8080/api/statik/memory

# Chat with GremlinGPT
curl -X POST http://localhost:8080/api/statik/gremlin/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello GremlinGPT"}'

# Get system status
curl http://localhost:8080/api/statik/status

# Generate mesh key
curl -X POST http://localhost:8080/api/statik/mesh/keys/generate
```

### Using JavaScript

```javascript
// Fetch memory state
const response = await fetch('/api/statik/memory');
const memory = await response.json();

// Chat with GodCore
const chatResponse = await fetch('/api/statik/godcore/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Process this query',
    model: 'auto'
  })
});
const result = await chatResponse.json();
```

### Using Python

```python
import requests

# Get memory state
response = requests.get('http://localhost:8080/api/statik/memory')
memory = response.json()

# Chat with GremlinGPT
chat_response = requests.post(
    'http://localhost:8080/api/statik/gremlin/chat',
    json={'message': 'Hello from Python'}
)
result = chat_response.json()
```

## 📚 SDK Examples

### JavaScript Dashboard Integration

```javascript
class StatikAPI {
  constructor(baseURL = 'http://localhost:8080') {
    this.baseURL = baseURL;
  }

  async getMemory() {
    const response = await fetch(`${this.baseURL}/api/statik/memory`);
    return response.json();
  }

  async chatWithGremlin(message) {
    const response = await fetch(`${this.baseURL}/api/statik/gremlin/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    return response.json();
  }

  startLiveFeed(callback) {
    const eventSource = new EventSource(`${this.baseURL}/api/statik/memory/live`);
    eventSource.onmessage = (event) => {
      callback(JSON.parse(event.data));
    };
    return eventSource;
  }
}

// Usage
const api = new StatikAPI();
const liveFeed = api.startLiveFeed((memory) => {
  console.log('Memory update:', memory);
});
```

---

📡 **Complete API reference for the AscendNet Statik-Server system.** For more examples and advanced usage, see the [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) and [dashboard implementation](../statik-server/src/browser/pages/).
