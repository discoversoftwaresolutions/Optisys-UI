import asyncio
import streamlit as st
import websockets

# Dynamic WebSocket URL base (you can move to .env for config)
WS_URL_BASE = "wss://optisys-agent-production.up.railway.app/ws/progress"

def render_logs_tab():
    st.title("📡 Real-Time Integration Logs")

    product = st.selectbox("Select Product", [
        "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
        "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
    ])
    customer_id = st.text_input("Customer ID", value="demo-customer-001")

    session_id = f"{product}_{customer_id}"
    ws_url = f"{WS_URL_BASE}?product={product}&customer_id={customer_id}"

    if "log_lines" not in st.session_state:
        st.session_state.log_lines = []

    if st.button("🛰️ Connect to Integration Logs"):
        st.session_state.log_lines.clear()
        asyncio.run(start_ws_client(ws_url))

    st.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines), height=400)

async def start_ws_client(ws_url):
    try:
        async with websockets.connect(ws_url) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                await asyncio.sleep(0.1)
    except Exception as e:
        st.session_state.log_lines.append(f"❌ WebSocket error: {str(e)}")
