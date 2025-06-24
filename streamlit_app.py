import requests
import websocket
import threading
import time
import json
from datetime import datetime

API_URL = "http://localhost:8000"  # Replace with deployed backend
WS_HOST = "ws://localhost:8000"    # Replace for WebSocket if hosted

PRODUCTS = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

st.set_page_config(page_title="OptiSys Console", layout="wide")
st.title("🎯 OptiSys Launch Console")

# --- WebSocket Logging ---
def stream_logs(session_id, ws_url):
    log_container = st.empty()
    logs = []

    def on_message(ws, message):
        logs.append(message)
        log_container.code("\n".join(logs[-10:]))

    def run():
        ws = websocket.WebSocketApp(ws_url, on_message=on_message)
        ws.run_forever()

    threading.Thread(target=run, daemon=True).start()
    time.sleep(1)

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 Live Logs", "📦 Stack Engine", "🧠 AgentBridge",
    "🗂 Upload Products", "📊 System Pulse"
])

# --- Tab 1: Live Log Stream ---
with tab1:
    st.subheader("🖥️ Real-Time Integration Logs")
    product = st.selectbox("Product", PRODUCTS)
    client = st.text_input("Client ID", value="demo-client")
    if st.button("Stream Logs"):
        sid = f"{product}_{client}"
        ws_url = f"{WS_HOST}/ws/progress?product={product}&customer_id={client}"
        stream_logs(sid, ws_url)

# --- Tab 2: Stack-Based Dispatcher ---
with tab2:
    st.subheader("⚙️ Describe Your Stack")
    stack = st.text_area("Stack Description", placeholder="e.g., FastAPI + GCP + PostgreSQL")
    context = st.text_area("Optional JSON Context", value='{}')

    col1, col2 = st.columns(2)
    if col1.button("🔄 Run Integration"):
        try:
            resp = requests.post(f"{API_URL}/stack/auto-integrate", json={
                "description": stack,
                "context": json.loads(context or "{}")
            })
            st.success("✅ Dispatcher triggered")
            st.json(resp.json())
        except Exception as e:
            st.error(f"Error: {e}")

    if col2.button("🎙️ Use Voice Input"):
        audio = st.file_uploader("Upload voice (WAV, MP3)", type=["wav", "mp3", "m4a"])
        if audio:
            resp = requests.post(f"{API_URL}/stack/voice-integrate", files={"file": audio})
            st.success("✅ Transcribed and dispatched")
            st.json(resp.json())

# --- Tab 3: AgentBridge Trigger ---
with tab3:
    st.subheader("🤖 Agent-to-Agent Invocation")
    agent_id = st.text_input("Agent ID", value="store-optimizer-01")
    client_id = st.text_input("Client ID", value="acme-corp")
    intent = st.selectbox("Intent", ["optimize", "auto_integrate"])
    data = st.text_area("Payload (JSON)", value='{"metrics": {"cpu_usage": 85, "memory_usage": 74, "latency": 210}}')

    if st.button("Invoke Agent"):
        try:
            payload = {
                "agent_id": agent_id,
                "client_id": client_id,
                "intent": intent,
                "data": json.loads(data)
            }
            r = requests.post(f"{API_URL}/agent/invoke", json=payload)
            st.success("✅ Agent Invoked")
            st.json(r.json())
        except Exception as e:
            st.error(str(e))

# --- Tab 4: Upload Product Set ---
with tab4:
    st.subheader("📦 Upload Client Products")
    c_id = st.text_input("Client ID for Upload", value="demo-client")
    product_payload = st.text_area("Product JSON", placeholder='[{"name": "BoostX", "category": "add-on"}]')

    if st.button("Upload"):
        try:
            parsed = json.loads(product_payload)
            r = requests.post(f"{API_URL}/client/products/upload", json={
                "client_id": c_id,
                "products": parsed
            })
            st.success(f"✅ Uploaded {len(parsed)} products")
        except Exception as e:
            st.error(f"Upload failed: {e}")

# --- Tab 5: System Pulse / Optimization Preview ---
with tab5:
    st.subheader("📊 Latest Optimization Snapshot")
    cid = st.text_input("Client ID to Diagnose", value="demo-client-opt")
    metrics = st.text_area("Live Metrics (JSON)", value='{"cpu_usage": 88, "memory_usage": 72, "latency": 250}')
    region = st.selectbox("Region", ["us", "eu", "de", "asia"])
    stack = st.text_area("Current Stack (JSON)", value='{"data_types":["PHI"], "hipaa_certified": false, "data_encryption_at_rest": false}')

    if st.button("Run Optimization Agent"):
        try:
            payload = {
                "metrics": json.loads(metrics),
                "client_id": cid,
                "region": region,
                "stack": json.loads(stack)
            }
            r = requests.post(f"{API_URL}/agent/invoke", json={
                "agent_id": "store-optimizer-01",
                "client_id": cid,
                "intent": "optimize",
                "data": payload
            })
            st.success("✅ Optimization Run")
            st.json(r.json())
        except Exception as e:
            st.error(f"Agent run failed: {e}")

tab6 = st.tabs(["🔐 Credentials"])[0]
with tab6:
    st.subheader("🔑 Client Secret Manager")
    target_client = st.text_input("Client ID", value="demo-client")
    if st.button("🔍 Check Secrets"):
        try:
            r = requests.get(f"{API_URL}/client/secrets/check/{target_client}")
            resp = r.json()
            st.success(f"✅ Keys Present: {resp['valid_keys']}")
            if resp["missing"]:
                st.warning(f"❌ Missing: {resp['missing']}")
            else:
                st.success("🟢 All required secrets provided.")
        except Exception as e:
            st.error(f"Secret check failed: {e}")
