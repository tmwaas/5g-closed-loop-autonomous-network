# 5G Closed-Loop Autonomous Network Simulator

[![Architecture: TM Forum AN Level 4 Framework](https://img.shields.io/badge/TM_Forum-Autonomous_Network_Level_4-blue.svg)](https://www.tmforum.org/)
[![Compliance: 3GPP](https://img.shields.io/badge/Compliance-3GPP_TS_38.331-green.svg)](https://www.3gpp.org/)
[![Status: WIP / Foundation Phase](https://img.shields.io/badge/Status-Phase_1:_Telemetry_Foundation-orange.svg)]()

An open-source blueprint and simulator for a **5G Closed-Loop Autonomous Network Remediation** platform. This project demonstrates the architectural evolution toward **zero-touch, self-healing network operations** by combining modern cloud-native observability with upcoming AI-driven multi-agent remediation layers.

> 📢 **Project Status:** Currently in **Phase 1 (Telemetry Foundation)**. The core telemetry ingestion and synthetic network logging pipeline are functional using mocked RAN properties. Cognitive intelligence and closed-loop automation modules (`agents`, `analytics`, `rag`) are actively being mapped under the architectural roadmap.

---

## 🏛️ Target Architecture & Functional Flow

The framework follows an event-driven closed-loop automation pattern (**MAPE-K**: Monitor, Analyze, Plan, Execute, Knowledge). 

```text
  +-----------------------------------------------------------------------+
  |                        5G INFRASTRUCTURE LAYER                        |
  |   [ Simulated gNodeB / RAN ] --(Telemetry Logs)--> [ Data Lake ]      |
  +--------------------------------------------------+--------------------+
                                                     |
                                                     v (Active Stream)
  +--------------------------------------------------+--------------------+
  |              MONITORING & OBSERVABILITY ENGINE (Phase 1)             |
  |             [ Ingestion Pipelines & Telemetry Microservices ]         |
  +--------------------------------------------------+--------------------+
                                                     |
                                                     v [Planned Integration]
  +--------------------------------------------------+--------------------+
  |             [WIP] GENAI-DRIVEN CLOSED-LOOP AUTOMATION LAYER           |
  |                                                                       |
  |    +--------------------+                        +---------------+    |
  |    |  Orchestrator Agent| <====================> | Analyst Agent |    |
  |    +----------+---------+                        +-------+-------+    |
  |               |                                          |            |
  |               v                                          v            |
  |     +------------------+                        +------------------+  |
  |     |  Executor Agent  |                        |  Azure AI Search |  |
  |     +--------+---------+                        +--------+---------+  |
  +--------------|-------------------------------------------|------------+
                 v [Zero-Touch Remediation Action]           v [3GPP RAG Knowledge]
```

1. **Monitor (Active):** Metrics mirroring multi-vendor RAN telemetry properties are generated, processed, and logged via the telemetry microservice layer.

2. **Analyze & Plan (WIP Roadmap):** Anomaly alerts will trigger a Multi-Agent system to cross-reference infrastructure failures against ingested 3GPP TS 38.331 standards.

3. **Execute (WIP Roadmap):** Automated remediation sequences are executed based on compliance knowledge extraction.

---

## 📁 Repository Structure

```text
.
├── 📁 data_lake/             # Storage for simulated telemetry logs & telemetry events
├── 📁 docs/                  # Technical documentation and architecture guidelines
├── 📁 k8s/                   # Cloud-native infrastructure deployment manifests
├── 📁 monitoring/            # Prometheus configuration assets and alerting rules
├── requirements.txt         # Project runtime python package manifest
├── docker-compose.yml       # Local multi-container deployment setup
└── 📁 services/             # Application microservices core sub-system
    ├── 📁 agents/           # [WIP] Multi-Agent logic, prompt flows, and reasoning structures
    ├── 📁 analytics/        # [WIP] Statistical network anomaly identification nodes
    ├── 📁 rag/              # [WIP] Semantic querying layer parsing 3GPP Technical Specifications
    └── 📁 telemetry/        # (Active) Metric streaming and live log ingestion microservice
```

---

## 🛠️ Technology Stack & Roadmap
* **Telemetry & Logging (Active):** Python 3.11+, FastAPI, Docker Compose, Mocked RAN properties log engine.

* **Observability (Active Base):** Prometheus metric configurations & structure rules.

* **Orchestration (Planned):** Kubernetes / Red Hat OpenShift manifests for scale.

* **Cognitive Layer (WIP Roadmap):** Azure AI Search (Vector Search Engine), Multi-Agent Collaboration framework, LangChain ecosystem.

---

## 🚀 Running Phase 1 (Local Setup)
To spin up the core telemetry microservice foundation locally:

```bash
# Clone the repository
git clone https://github.com/tmwaas/5g-closed-loop-autonomous-network.git
cd 5g-closed-loop-autonomous-network

# Spin up core infrastructure and active telemetry services
docker-compose up --build -d

# Verify telemetry node status
docker-compose ps
```

The telemetry service will begin generating synthetic telecom network infrastructure events, preparing data structures within the data_lake directory to hook into the upcoming analytics and AI agent endpoints.