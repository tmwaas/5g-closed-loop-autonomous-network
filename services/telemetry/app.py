import time
import random
import json
import os
import threading
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

# --- 1. IMPORT PROMETHEUS CLIENT ---
from prometheus_client import generate_latest, Gauge, Counter, REGISTRY

# --- 2. PROMETHEUS METRIC DEFINITIONS ---
GNB_PRB_UTILIZATION = Gauge('gnb_prb_utilization', 'Persentase PRB Utilization per gNodeB', ['gnodeb_id'])
GNB_CALL_DROP_RATE = Gauge('gnb_call_drop_rate', 'Persentase Call Drop Rate per gNodeB', ['gnodeb_id'])

CLOSED_LOOP_REMEDIATIONS = Counter('closed_loop_remediations_total', 'Total successful automated remediations executed by the agent', ['gnodeb_id', 'action'])

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=generate_telemetry_loop, daemon=True).start()
    yield

app = FastAPI(
    title="AI-Driven OSS Platform",
    version="1.2.0",
    lifespan=lifespan
)

DATA_LAKE_DIR = "./data_lake"
os.makedirs(DATA_LAKE_DIR, exist_ok=True)
RAW_TELEMETRY_FILE = f"{DATA_LAKE_DIR}/telemetry_raw.jsonl"
AUTOMATION_LOG_FILE = f"{DATA_LAKE_DIR}/automation_closed_loop.jsonl"

MOCK_3GPP_RUNBOOKS = {
    "HIGH_PRB_UTILIZATION": "Runbook 3GPP-TS-38.300: Cell congestion detected. Standard resolution: Trigger ANR, optimize antenna tilts via SON, or execute load balancing to adjacent cells.",
    "HIGH_CALL_DROP": "Runbook 3GPP-TS-36.331: RRC Connection failures detected. Standard resolution: Reset the gNodeB transceiver module, or adjust handover hysteresis values."
}

active_incidents = {}

def call_rag_knowledge_base(anomaly_type: str, gnodeb_id: str, metric_value: float) -> str:
    runbook_context = MOCK_3GPP_RUNBOOKS.get(anomaly_type, "No specific runbook found.")
    return f"[RAG AI Insights] Analyzing {gnodeb_id} exhibiting {anomaly_type} ({metric_value}). Cross-referencing {runbook_context}."

def execute_closed_loop_agent(gnb_id: str, anomaly_type: str, metric_value: float):
    # STEP 1: Incident Triggered (Initial Detection)
    print(f"\n[🤖 Agent Orchestrator] [CRITICAL] Incident triggered on {gnb_id}! {anomaly_type} detected at value: {metric_value}")
    time.sleep(1.2) 
    
    # STEP 2: Analyzing (Fetching 3GPP RAG Context)
    print(f"[🔍 Agent Orchestrator] [ANALYZING] Querying RAG Knowledge Base for standard operational compliance...")
    rag_insight = call_rag_knowledge_base(anomaly_type, gnb_id, metric_value)
    time.sleep(1.2)
    
    # STEP 3: Mitigating (Executing Automated Actions)
    if anomaly_type == "HIGH_PRB_UTILIZATION":
        action = "EXECUTE_LOAD_BALANCING"
        target_neighbor = f"gNB_{random.randint(1, 100):03d}"
        print(f"[⚙️ Agent Orchestrator] [MITIGATING] Policy Matched. Shifting 25% traffic footprint to neighbor cell: {target_neighbor}...")
    else:
        action = "RESET_RRC_TRANSCEIVER"
        print(f"[⚙️ Agent Orchestrator] [MITIGATING] Policy Matched. Re-initializing RRC transceiver interface layer on {gnb_id}...")
        
    time.sleep(2.0)
    
    # --- 3. TRIGGER PROMETHEUS COUNTER UPON REMEDIATION COMPLETION ---
    CLOSED_LOOP_REMEDIATIONS.labels(gnodeb_id=gnb_id, action=action).inc()
    
    # STEP 4: Verifying (Post-Remediation Validation)
    print(f"[⏳ Agent Orchestrator] [VERIFYING] Monitoring telemetry pipeline stabilization to ensure KPI recovery...")
    time.sleep(1.2)
    
    agent_log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gnodeb_id": gnb_id,
        "anomaly_type": anomaly_type,
        "trigger_value": metric_value,
        "rca_rag": rag_insight,
        "remediation_action": action,
        "validation": "SUCCESS (KPI Stabilized)",
        "tm_forum_compliance": "Level 4"
    }
    
    with open(AUTOMATION_LOG_FILE, "a") as f:
        f.write(json.dumps(agent_log) + "\n")
        
    active_incidents[gnb_id] = {
        "status": "RESOLVED",
        "action_taken": action,
        "timestamp": agent_log["timestamp"]
    }
    
    # STEP 5: Resolved (Final Resolution)
    print(f"[✅ Agent Orchestrator] Closed-loop automation cycle finished for {gnb_id}. Status: RESOLVED.\n")

def analyze_metrics_stream(payload: dict):
    gnb_id = payload["gnodeb_id"]
    prb = payload["prb_utilization"]
    cdr = payload["call_drop_rate"]
    
    # Prevent duplicate thread buildup if the cell is currently undergoing recovery
    if gnb_id in active_incidents and active_incidents[gnb_id]["status"] == "FIRING":
        return

    if prb > 90.0:
        active_incidents[gnb_id] = {"status": "FIRING", "issue": "HIGH_PRB_UTILIZATION", "val": prb}
        threading.Thread(target=execute_closed_loop_agent, args=(gnb_id, "HIGH_PRB_UTILIZATION", prb)).start()
    elif cdr > 4.0:
        active_incidents[gnb_id] = {"status": "FIRING", "issue": "HIGH_CALL_DROP", "val": cdr}
        threading.Thread(target=execute_closed_loop_agent, args=(gnb_id, "HIGH_CALL_DROP", cdr)).start()

def generate_telemetry_loop():
    gnodeb_ids = [f"gNB_{str(i).zfill(3)}" for i in range(1, 101)]
    print("[📡 Telemetry Simulator] Initiating real-time KPI streaming for 100 gNodeBs...")
    
    while True:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for gnb in gnodeb_ids:
            # Condition the anomaly to occasionally cause cascading impacts (High PRB triggers increased Call Drops)
            has_anomaly = random.random() < 0.02
            
            if has_anomaly:
                # --- RANDOM ANOMALY TYPE DISTRIBUTION ---
                if random.random() < 0.20:
                    # 20% Probability: Pure RRC signaling issue (Normal PRB, high Call Drop)
                    prb_util = random.uniform(45.0, 75.0)
                    call_drop = random.uniform(4.5, 9.8)
                    throughput = random.uniform(50, 120)
                else:
                    # 80% Probability: Network congestion (High PRB above 90)
                    prb_util = random.uniform(91.0, 99.0)
                    call_drop = random.uniform(0.05, 0.35)
                    throughput = random.uniform(5, 25)

                # prb_util = random.uniform(91.0, 99.0)
                # call_drop = random.uniform(4.5, 9.8) # Triggers CDR alert > 4.0%
                # throughput = random.uniform(5, 25)
            else:
                prb_util = random.uniform(45.0, 75.0)
                call_drop = random.uniform(0.05, 0.35)
                throughput = random.uniform(180, 420)
            
            payload = {
                "timestamp": timestamp, 
                "gnodeb_id": gnb,
                "prb_utilization": round(prb_util, 2), 
                "call_drop_rate": round(call_drop, 2), 
                "throughput_mbps": round(throughput, 2)
            }
            
            with open(RAW_TELEMETRY_FILE, "a") as f:
                f.write(json.dumps(payload) + "\n")
                
            # --- 4. UPDATE VALUE TO PROMETHEUS GAUGE ---
            GNB_PRB_UTILIZATION.labels(gnodeb_id=gnb).set(prb_util)
            GNB_CALL_DROP_RATE.labels(gnodeb_id=gnb).set(call_drop)
            
            analyze_metrics_stream(payload)
            
        time.sleep(15)

# --- 5. DEDICATED ENDPOINT FOR PROMETHEUS SERVER SCRAPING ---
@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest(REGISTRY)

@app.get("/metrics/active-incidents")
def get_incidents():
    return {"total_tracked": len(active_incidents), "incidents": active_incidents}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)