# 🔄 Sequence Diagram: On-Demand Ingestion & Live Telemetry Stream

This workflow specifies the dual-path data pipeline (Cold/Hot Path separation) enforcing high-throughput ingestion (10,000 rps) alongside dynamic client web socket subscriptions.

```mermaid
sequenceDiagram
    autonumber
    actor Guest as 👥 Guest User
    participant Front as 🖥️ Frontend (NuxtJS)
    participant Gateway as 🌐 API Gateway
    participant FastAPI as "⚙️ Core Backend (FastAPI)"
    participant Redis as 🚀 Cache & Pub/Sub (Redis)
    participant Ingestor as 🔄 Ingestion Worker
    participant Timescale as 💾 Time-Series (TimescaleDB)

    %% === PHASE 1: CLIENT INITIALIZES SUBSCRIPTION ===
    Note over Guest, Redis: Phase 1: Client Open Viewport & Subscribe Request
    Guest->>Front: Clicks on a sensor pin (device_id: "sensor_99")
    
    par Dual Client Actions
        Front->>Gateway: GET /api/v1/devices/sensor_99/history (24h chart data)
        Gateway->>FastAPI: Forward REST query
        FastAPI->>Timescale: Read aggregated historical blocks
        Timescale-->>FastAPI: Return 24h data matrix
        FastAPI-->>Front: JSON Payload (Render static background chart)
    and
        Front->>Gateway: WS Control Signal: { "action": "subscribe", "device_id": "sensor_99" }
        Gateway->>FastAPI: Route frame to WebSocket Manager
    end

    FastAPI->>FastAPI: Map Client Socket to room:sensor_99
    FastAPI->>Redis: Centralized Registry Update: HINCRBY smartcity:active_sensors "sensor_99" 1
    Note over Redis: "sensor_99" marked as ACTIVE stream

    %% === PHASE 2: INGESTION PIPELINE & DUAL-PATH ROUTING ===
    Note over Ingestor, Timescale: Phase 2: Streaming, Bulk Insertion & Hot-Path Filtering
    
    loop Stream Processing from Apache Kafka (Every 1-3 seconds)
        Ingestor->>Ingestor: Fetch message batch from Kafka topic (e.g., 500 records)
        
        %% COLD PATH
        Note over Ingestor, Timescale: [Cold Path] Persistent Logging
        Ingestor->>Timescale: Execute Bulk Insert (SQL Multi-row INSERT) into hypertables
        Timescale-->>Ingestor: Transaction Commit OK
        
        %% HOT PATH WITH FILTERING
        Note over Ingestor, Redis: [Hot Path] Low-Latency Live Multiplexing
        loop For each message in batch
            Ingestor->>Redis: Guard Check: HEXISTS active      
            alt Sensor has ACTIVE viewers (HEXISTS = 1)
                Ingestor->>Redis: PUBLISH channel "telemetry:sensor_99" [JSON payload]
            else NO active viewers (HEXISTS = 0) 
                Ingestor->>Ingestor: Drop message
            end
        end
    end

    %% === PHASE 3: LIVE BROADCAST TO BROWSER ===
    Note over Redis, Guest: Phase 3: Non-blocking Background Relay to UI
    Redis-->>FastAPI: Async Trigger: Pattern match intercepted on "telemetry:*"
    FastAPI->>FastAPI: Redis Pub/Sub Relay extracts data payload
    FastAPI->>FastAPI: WebSocket Manager locates active clients in room:sensor_99
    FastAPI->>Gateway: Push downstream payload via active WS channel
    Gateway->>Front: Send live JSON ticker frame
    Front->>Front: Append new point to active UI chart element
    Front-->>Guest: Chart smoothly ticks in real-time
```
