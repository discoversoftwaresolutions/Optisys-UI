import streamlit as st
import asyncio
import websockets

st.set_page_config(page_title="Real-Time Integration Logs")
st.title("📡 Real-Time Integration Logs")

# Session ID input
session_id = st.text_input("Session ID", value="SecurePact_demo001")

# Initialize log state
if "logs" not in st.session_state:
    st.session_state.logs = []

# Async log handler
async def log_listener(ws_url: str):
    try:
        async with websockets.connect(ws_url) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.logs.append(msg)
                await asyncio.sleep(0.2)
    except Exception as e:
        st.error(f"❌ WebSocket error: {e}")

# Connection trigger
if st.button("🛰️ Connect"):
    ws_url = f"wss://optisys-agent-production.up.railway.app/ws/{session_id}"
    st.session_state.logs.clear()  # Clear previous logs
    asyncio.run(log_listener(ws_url))

# Log output UI
st.text_area("📋 Log Stream", "\n".join(st.session_state.logs), height=400)
