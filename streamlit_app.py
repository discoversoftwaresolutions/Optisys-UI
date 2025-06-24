import streamlit as st
import requests
import websocket
import threading
import time
import json

st.set_page_config(page_title="OptiSys Console", layout="wide")
st.title("🎯 OptiSys Launch Console")

API_URL = "https://optisys-agent-production.up.railway.app"
WS_HOST = "wss://optisys-agent-production.up.railway.app"
PRODUCTS = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

# Sample stack descriptions
STACK_TEMPLATES = [
    "",
    "FastAPI + GCP + PostgreSQL",
    "Shopify + AWS + DynamoDB",
    "Streamlit + Azure + CosmosDB",
    "Next.js + Vercel + Firebase"
]

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

def render(client_id):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📡 Live Logs", "📦 Stack Engine", "🧠 AgentBridge",
        "🗂 Upload Products", "📊 System Pulse", "🔐 Credentials", "🧭 Backend Pulse"
    ])

    # Tab 1 – Logs
    with tab1:
        st.subheader("🖥️ Integration Logs")
        product = st.selectbox("Product", PRODUCTS)
        cid = st.text_input("Client ID", value=client_id, key="log_cid")
        if st.button("Stream Logs"):
            sid = f"{product}_{cid}"
            ws_url = f"{WS_HOST}/ws/progress?product={product}&customer_id={cid}"
            stream_logs(sid, ws_url)

    # Tab 2 – Stack Engine
    with tab2:
        st.subheader("⚙️ Describe Your Stack")
        selected = st.selectbox("Or pick a template", STACK_TEMPLATES)
        desc = st.text_area("Stack Description", value=selected or "", placeholder="e.g., FastAPI + GCP + PostgreSQL")
        context = st.text_area("Optional JSON Context", value="{}")
        col1, col2 = st.columns(2)

        if col1.button("🔄 Auto Integrate"):
            if not desc.strip():
                st.warning("⚠️ Please enter a stack description before triggering integration.")
            else:
                try:
                    payload = {
                        "description": desc.strip(),
                        "context": json.loads(context or "{}")
                    }
                    resp = requests.post(f"{API_URL}/stack/auto-integrate", json=payload)
                    st.success("✅ Integration Triggered")
                    st.json(resp.json())
                except Exception as e:
                    st.error(f"Integration failed: {e}")

        if col2.button("🎙️ Use Voice Input"):
            audio = st.file_uploader("Upload voice (WAV/MP3)", type=["wav", "mp3", "m4a"])
            if audio:
                try:
                    resp = requests.post(f"{API_URL}/stack/voice-integrate", files={"file": audio})
                    st.success("✅ Transcribed")
                    st.json(resp.json())
                except Exception as e:
                    st.error(f"Voice integration failed: {e}")

    # Tab 3 – AgentBridge
    with tab3:
        st.subheader("🤖 Agent Invocation")
        agent_id = st.text_input("Agent ID", value="store-optimizer-01")
        client_id_input = st.text_input("Client ID", value=client_id, key="agent_cid")
        intent = st.selectbox("Intent", ["optimize", "auto_integrate"])
        payload = st.text_area("Payload (JSON)", value='{"metrics":{"cpu":85}}')

        if st.button("Invoke Agent"):
            try:
                data = {
                    "agent_id": agent_id,
                    "client_id": client_id_input,
                    "intent": intent,
                    "data": json.loads(payload)
                }
                resp = requests.post(f"{API_URL}/agent/invoke", json=data)
                st.success("✅ Agent Invoked")
                st.json(resp.json())
            except Exception as e:
                st.error(str(e))

    # Tab 4 – Upload Products
    with tab4:
        st.subheader("📦 Upload Client Products")
        uid = st.text_input("Client ID", value=client_id, key="upload_cid")
        if "default_product_payload" not in st.session_state:
            st.session_state.default_product_payload = '[{"name": "BoostX", "category": "add-on"}]'
        json_input = st.text_area("Product JSON", value=st.session_state.default_product_payload)

        if st.button("Upload"):
            if not json_input.strip():
                st.warning("⚠️ Please enter product JSON.")
            else:
                try:
                    parsed = json.loads(json_input)
                    r = requests.post(f"{API_URL}/client/products/upload", json={
                        "client_id": uid,
                        "products": parsed
                    })
                    st.success(f"✅ Uploaded {len(parsed)} product(s)")
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {e}")
                except Exception as e:
                    st.error(f"Upload failed: {e}")

    # Tab 5 – Optimization Snapshot
    with tab5:
        st.subheader("📊 Optimization Snapshot")
        opt_cid = st.text_input("Client ID", value=f"{client_id}-opt", key="pulse_cid")
        metrics = st.text_area("Live Metrics (JSON)", value='{"cpu":88,"memory":72}')
        region = st.selectbox("Region", ["us", "eu", "asia"])
        stack = st.text_area("Current Stack", value='{"hipaa_certified": false}')

        if st.button("Run Optimization"):
            try:
                data = {
                    "metrics": json.loads(metrics),
                    "client_id": opt_cid,
                    "region": region,
                    "stack": json.loads(stack)
                }
                resp = requests.post(f"{API_URL}/agent/invoke", json={
                    "agent_id": "store-optimizer-01",
                    "client_id": opt_cid,
                    "intent": "optimize",
                    "data": data
                })
                st.success("✅ Optimization Triggered")
                st.json(resp.json())
            except Exception as e:
                st.error(f"Agent run failed: {e}")

    # Tab 6 – Secret Check
    with tab6:
        st.subheader("🔐 Secret Validation")
        cid = st.text_input("Client ID", value=client_id, key="secret_cid")
        if st.button("Check Secrets"):
            try:
                r = requests.get(f"{API_URL}/client/secrets/check/{cid}")
                data = r.json()
                if data.get("missing"):
                    st.warning(f"❌ Missing: {data['missing']}")
                else:
                    st.success("✅ All secrets present.")
            except Exception as e:
                st.error(f"Secret check failed: {e}")

    # Tab 7 – Backend Pulse
    with tab7:
        st.subheader("🧭 API Diagnostic")
        try:
            health = requests.get(f"{API_URL}/health").json()
            st.success(f"API Status: {health.get('status', 'unknown')}")
        except Exception as e:
            st.error(f"Health route failed: {e}")

        try:
            client_data = requests.get(f"{API_URL}/client/info/{client_id}").json()
            st.info("Client Info:")
            st.json(client_data)
        except Exception as e:
            st.warning(f"Client info unavailable: {e}")

# Run app
if __name__ == "__main__":
    render("demo-client")
