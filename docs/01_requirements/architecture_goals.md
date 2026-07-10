# 🏙️ Technical Specifications: SmartCity Platform

## **Intelligent system for monitoring and analyzing urban infrastructure**

---

## 1. General information

- **Project Name:** SmartCity
- **Development Goal:** To create a high-load web platform for aggregating, processing, analyzing, and visualizing telemetry data received in real time from a distributed network of IoT sensors (traffic intensity, meteorological indicators, environmental atmospheric monitoring).

### 👥 Use cases and role model

#### **Role: Guest (Unauthorized User)**

- **Free Access:** View an interactive world map with geotagged active IoT modules and the ability to filter by measured parameter types.
- **Standby Mode:** If no sensor is selected, an information widget is displayed with the total number of functioning devices in the system and the local time of the current time zone.
- **Data Details:** Selecting a specific sensor opens a panel with a brief regional summary and a dynamic graph of historical indicators.
- **Forecasting:** Initiate a request to build predictive analytics by clicking the dedicated button.

#### **Role: Administrator**

- **Authentication:** Secure login via a dedicated authorization form.
- **Entity Management:** Access to the administrative panel with a table interface for CRUD operations on monitoring point metadata and sensor configurations.

### 🎯 Key System Tasks

- **Data Injection:** Receiving and processing high-intensity telemetry streams from IoT devices in real time.
- **Storage:** Accumulating, structuring, and archiving historical data in an analytical warehouse.
- **Access Interfaces:** Providing low-latency REST API and WebSocket connections for client applications.
- **Analytics:** Visualizing the current state of the infrastructure and generating predictive models on demand.
- **Reliability:** Provides horizontal scalability, end-to-end logging, test coverage, and continuous component monitoring.

---

## 2. System Architecture

The platform is a distributed microservice architecture consisting of five key layers.

### 🖥️ 2.1. Frontend Layer

- **Stack:** `NuxtJS 3` (TypeScript), `Bootstrap UI`(responsive layout).
- **Security:** `JWT-based` authorization; Access tokens stored in application memory, Refresh tokens stored in secure HttpOnly cookies.
- **Transport:** Persistent `WebSocket` connection for reactive dashboard updates.
- **Interfaces:** Interactive map, analytical charts, predictive screens, and an isolated administration module.

### ⚙️ 2.2. Backend Layer (System Core)

- **Core Stack:** `FastAPI` (Python 3.14), `Pydantic` (strict data contract validation).
- **Data Layer:** `SQLAlchemy ORM`, `TimescaleDB` DBMS (relational metadata and aggregate storage).
- **Caching and Brokers:** `Redis` (fast cache, distributed sessions), `Apache Kafka` (fault-tolerant incoming IoT event bus).
- **Integrations:** `gRPC` client for communication with the analytics module, WebSocket server for broadcasting metrics to the frontend.
- **Infrastructure:** `Docker` for containerization, `GatewayAPI/Nginx` as a reverse proxy and request router.

### 📟 2.3. IoT Sensor Simulation Module

- **Implementation:** A standalone lightweight Python microservice (`python-kafka`).
- **Event Format:** A JSON message containing `sensor_id`, `data_type` (traffic, temperature, air_quality), `value` (float), and `timestamp`.
- **Rate:** Discrete sending of packets to the corresponding `Kafka` topics at intervals of 1–3 seconds.

### 🧠 2.4. Analytics Module

- **Implementation:** Isolated high-performance gRPC service.
- **Functionality:** Processing incoming data vectors from the Backend core, using ML models to calculate trends (temperature changes, pollution index dynamics), and returning prediction matrices.

### 🚀 2.5. DevOps and Infrastructure

- **Orchestration:** Deployment and lifecycle management of containers in a Kubernetes cluster.
- **CI/CD:** Automated pipelines based on `GitHub Actions`.
- **Observability:** `Prometheus` (metrics collection), `Grafana` + `Loki` (visualization, log analytics, centralized alerting).
- **Balancing:** `GatewayAPI` for distributing incoming traffic.

---

## 📊 3. System Requirements

### 3.1. Functional Requirements

| Role | Capabilities |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| **Guest** | View shared dashboards and the interactive map (without authorization). |
| **Administrator** | User management, configuration and CRUD sensors, viewing system logs. |

### ⚡ 3.2. Non-functional Requirements

- **Performance:** Support for incoming data flows of up to **10,000 messages per second** from Apache Kafka.
- **Scalability:** Horizontal scaling of microservices (stateless components) in Kubernetes.
- **Reliability:** System availability (uptime) of at least **99.5%**.
- **Security:** Use of JWT, HTTPS, and end-to-end protection against XSS and CSRF vulnerabilities.
- **CI/CD:** Fully automated build, testing, and deployment processes.

---

## 🧪 4. Testing Strategy

### 🎨 4.1. Frontend Testing

- **Unit Tests:** `Jest` + `Vue Test Utils` (testing isolated component logic).
- **E2E Tests:** `Cypress` (validation of end-to-end user flows).
- **UI Regression:** `Storybook` + `Chromatic` (visual inspection of UI changes).
- **Accessibility:** `axe-core` (checking interface accessibility).
- **Static Analysis:** `ESLint` + `Prettier`.

### 💾 4.2. Backend Testing

- **Unit Tests:** `Pytest` (checking API and business logic correctness).
- **Integration tests**: `Docker Compose` + `Pytest` (emulating FastAPI ↔ DB ↔ Kafka).
- **Load testing**: `Locust` (measuring system performance limits).
- **API testing**: `Postman` / `Newman` for REST endpoint verification.
- **Security**: `OWASP ZAP` automated and manual scanning tools.
- **Static analysis**: Type checking with `ruff`.

### ⚙️ 4.3. Infrastructure Testing (DevOps)

- Validation of build steps and tests in the GitHub Actions pipeline when committing changes to the `main` branch.
- Conducting automated smoke tests of containers immediately after deployment to a Kubernetes cluster.
- Continuous monitoring of service availability and metrics via `Prometheus`.

---

## 📂 5. Documentation Management

- **Location:** All design artifacts are consolidated in the `docs/` directory in the repository root.
- **Standardization:** Architecture modeling is performed using the **C4 Pattern** methodology and the `mermaid` syntax.
- **Synchronization:** Automatic integration of local Markdown files with the project's GitHub Wiki is configured.
- **Description Depth:** Documentation describes the current state of the system and each C4 layer. Use-case, ER, and sequence diagrams serve as Layer 4 (Code).
- **Entry Point:** The `README.md` file in the repository root contains a brief description of the architecture, instructions for launching, and a link to the project's Kanban board.
