import streamlit as st
import requests
import websocket
import threading
import time
from datetime import datetime

API_URL = "http://localhost:8000"  # Replace with your deployed FastAPI backend
PRODUCTS = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy",
    "Enginuty", "HoloUX"
]

st.set_page_config(page_title="OptiSys Console", layout="wide")
st.title("🎯 OptiSys Launch Console")

if "status_msg" not in st.session_state:
    st.session_state.status_msg = None

# --- WebSocket log client ---
def stream_logs(session_id, ws_url):
    log_container = st.empty()
    logs = []

    def on_message(ws, message):
        logs.append(message)
        log_container.code("\n".join(logs[-10:]))

    def on_error(ws, error):
        log_container.error(f"WebSocket error: {error}")

    def on_close(ws, code, msg):
        log_container.warning("🔌 Connection closed")

    def run():
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()

    thread = threading.Thread(target=run)
    thread.start()
    time.sleep(1)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📡 Live Logs", "📦 Stack Engine", "⚙️ System Pulse"])

# --- Tab 1: Live Logs ---
with tab1:
    st.subheader("🖥️ Integration Log Stream")
    selected_product = st.selectbox("Choose Product", PRODUCTS, key="product_select")
    customer_id = st.text_input("Customer ID", value="demo-customer-001", key="cid_input")

    if st.button("🎥 Stream Logs", key="stream_btn"):
        session_id = f"{selected_product}_{customer_id}"
        ws_url = f"ws://localhost:8000/ws/progress?product={selected_product}&customer_id={customer_id}"
        stream_logs(session_id, ws_url)

# --- Tab 2: Stack Management ---
with tab2:
    st.subheader("⚙️ Stack-Based Integration")
    stack_input = st.text_area("Describe Your Stack", height=150, placeholder="e.g., FastAPI backend, PostgreSQL, deployed to AWS")

    colA, colB = st.columns(2)
    if colA.button("🔄 Run Integration"):
        if stack_input.strip():
            with st.spinner("Triggering OptiSys backend..."):
                try:
                    payload = {"description": stack_input.strip()}
                    response = requests.post(f"{API_URL}/stack/describe", json=payload, timeout=10)
                    if response.ok:
                        data = response.json()
                        st.success(data.get("message", "✅ Integration triggered"))
                        st.json(data.get("details", {}))
                        st.session_state.status_msg = f"✅ {datetime.now().strftime('%I:%M %p')} - Triggered"
                    else:
                        st.error(f"🚨 Server error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Stack description cannot be empty.")

    if colB.button("🧠 Show Stack Suggestions"):
        try:
            suggestions = requests.get(f"{API_URL}/stack/suggestions", timeout=10).json()
            for item in suggestions.get("recommendations", []):
                st.markdown(f"• **{item['product']}** → _{item['reason']}_")
        except Exception as e:
            st.error(f"Could not retrieve suggestions: {e}")

# --- Tab 3: System Status ---
with tab3:
    st.subheader("🔋 System Pulse")

    col1, col2, col3 = st.columns(3)
    try:
        ping = requests.get(f"{API_URL}/health", timeout=5)
        if ping.ok:
            col1.success("API: Online")
            col2.success("WebSocket: Active")
            col3.success("DB: Connected")
        else:
            col1.error("API Down")
    except Exception:
        col1.error("🚨 Backend Offline")

    st.info("Most Shopify+ stores boosted conversions by enabling HoloUX checkout. Want to enable it with one click?")
