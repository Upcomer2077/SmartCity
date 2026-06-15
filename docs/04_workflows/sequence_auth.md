# 🔄 Sequence Diagram: Admin Authentication & JWT Rotation

This workflow details the secure authentication architecture, token storage guardrails, and silent refresh rotation loops for the Administrator role.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 👨‍💻 Administrator
    participant Front as 🖥️ Frontend (NuxtJS)
    participant Gateway as 🌐 API Gateway
    participant Router as 🚦 API Router (FastAPI)
    participant Auth as 🔒 Auth Service (Jose)
    participant Cache as 🚀 Cache (Redis)

    %% === PHASE 1: LOGIN FLOW ===
    Note over Admin, Cache: Phase 1: Authentication & Token Issuance
    Admin->>Front: Enters credentials (username, password)
    Front->>Gateway: POST /api/v1/auth/login (JSON payload)
    Gateway->>Router: Forward login request
    Router->>Auth: Authenticate (credentials)
    
    Auth->>Cache: Verify if user account is locked/bruteforced
    Cache-->>Auth: Account status OK
    
    Note over Auth: Validates password hashing
    
    Auth->>Auth: Generate Access Token (TTL: 15m)
    Auth->>Auth: Generate Refresh Token (TTL: 7d)
    
    Auth->>Cache: Save Refresh Token state (Token Whitelist)
    Router-->>Gateway: HTTP 200 OK Response
    Note right of Router: Set-Cookie: refresh_token (HttpOnly, Secure, SameSite)<br/>JSON Body: { "access_token": "ey...", "ttl_seconds": 900 }
    Gateway-->>Front: Deliver tokens to client
    Front->>Front: Store Access Token in Application Memory (RAM)
    Front-->>Admin: Render Admin Dashboard view

    %% === PHASE 2: PROTECTED API REQUEST ===
    Note over Admin, Cache: Phase 2: Accessing Protected Operational API
    Admin->>Front: Clicks "Delete IoT Device"
    Front->>Gateway: DELETE /api/v1/devices/{id}<br/>Headers: [Authorization: Bearer <access_token>]
    Gateway->>Router: Forward request with tokens
    Router->>Auth: Intercept & Authorize (access_token)
    Auth->>Auth: Verify cryptographic signature & expiration
    Auth-->>Router: Signature valid (Role: Admin)
    Router->>TimescaleDB: [Internal Call] Execute hard deletion
    Router-->>Front: HTTP 204 No Content
    Front-->>Admin: Refresh tables & show success toast

    %% === PHASE 3: SILENT REFRESH ROTATION ===
    Note over Admin, Cache: Phase 3: Token Expiration & Silent Refresh Loop
    Note left of Front: Access Token expires in RAM
    Front->>Gateway: POST /api/v1/auth/refresh<br/>Cookies: [refresh_token=<token>] (No Authorization header)
    Gateway->>Router: Forward cookie payload
    Router->>Auth: RotateTokens(refresh_token)
    
    Auth->>Cache: Check if refresh_token exists in Whitelist / Blacklist
    Cache-->>Auth: Token valid & active
    
    Auth->>Auth: Generate NEW Access Token (TTL: 15m)
    Auth->>Auth: Generate NEW Refresh Token (Token Rotation Pattern)
    
    Auth->>Cache: Invalidate OLD Refresh Token & Whitelist NEW one
    
    Router-->>Front: HTTP 200 OK Response<br/>Set-Cookie: refresh_token (NEW)<br/>JSON Body: { "access_token": "NEW_ey..." }
    Front->>Front: Overwrite old Access Token in Memory
```
