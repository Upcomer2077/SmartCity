# 🧩 C4 Architecture: Level 3 - Component Diagram (Core Backend)

This diagram details the internal software modules, controllers, and services inside the **Core Backend (FastAPI)** container and maps their interfaces to adjacent system containers.

```mermaid
---
config:
  layout: elk
---
flowchart TB
    %% --- External Containers (C2 Context) ---
    WebUI["🖥️ Web Application\n(NuxtJS 3 / TypeScript)\n\nServes static content \nand renders reactive dashboards."]
    Redis[("🚀 Cache\n(Redis)")]
    Timescale[("💾 Time-Series Storage\n(TimescaleDB / PostGIS)")]
    Analytics["🧠 Analytics Service\n(gRPC / Python)"]
    %% Time-series Worker
    Ingestor["🔄 Ingestion Worker\n(FastAPI / Python)\n\nConsumes micro-batches from Kafka \nand executes bulk insertions."]
       
    %% --- Core Backend Container Boundary ---
    subgraph CoreBackend["⚙️ Core Backend Container (FastAPI)"]
        
        %% Main
        Core["🧩 Core\n(python)\nEntry point. Regulates subservices\nHandles exceptions"]
        
        %% Routing and Contract Validation
        Router["🚦 Router\n(FastAPI)\nValidates incoming data,\nperforms ops execution."]

        %% Cache manager
        CacheManager["💼 Cache manager\nProvides unified\nAPI (CRUD)\nfor Redis-like dbs"]

        %% DB Core module
        DBEngine["⚙️ Database core\n(SQLAlchemy Core)\nGets database connection\nand provides low-level API\nfor query execution"]

        %% Data Access Abstraction
        DBManager["💼 Database manager\n(python/SQLAlchemy)\nProvides high-level API\nfor data manipulation\n(Repository/UoW)"]

        %% Real-time Delivery
        WSManager["🔌 WebSocket Manager\n(FastAPI WebSockets)\n\nHandles persistent client connections,\n connection lifecycles, and pub/sub broadasting."]
        
        %% Authentication & Guardrails
        AuthService["🔒 Auth Service\n(Python / Jose JWT)\n\nImplements password hashing,\naccess/refresh token generation,\nand state verification."]
        
        %% %% Telemetry Background Relay
        PubSubRelay["🔄 Redis Pub/Sub Relay\n(Python Asyncio)\nBackground polling routine\nthat catches incoming metrics from\n Redis and feeds them \nto the WS Manager."]
        
        %% Binary Remote Procedure Call Stub
        gRPCClient["📡 gRPC Analytics Client\n(grpcio)\n\nMaintains optimized persistent TCP channels\n and serializes Protobuf payloads\n for forecasting."]

        %% Logger
        Logger["📜 Logger\n(Winston)\nProvides global logger API"]
    end

   
    %% --- Internal Cross-Component Layer Calls 
    Core -->|Starts| Router
    Core -->|Starts| DBEngine
    Core -->|Starts| gRPCClient
    Core -->|Starts| PubSubRelay
    Core -->|Initializes| Logger

    Router -->|Uses| DBManager
    Router -->|Uses| AuthService
    Router -->|Uses| CacheManager
    Router -->|Uses| WSManager
    Router -->|Triggers forecasts| gRPCClient

    DBManager -->|Uses| DBEngine
    PubSubRelay -->|Sends hot data| WSManager
    
    %% --- External Connections 
    gRPCClient -->|Dispatches async requests| Analytics
    WebUI -->|Routes HTTPS/WS requests| Router
    Ingestor -->|Pushes data| CacheManager
    CacheManager -->|Polling| PubSubRelay
    Ingestor -->|Pushes data| DBManager
    CacheManager -->|CRUD| Redis
    DBEngine -->|CRUD| Timescale
```
