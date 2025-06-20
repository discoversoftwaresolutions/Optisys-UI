import asyncio
import streamlit as st
import websockets

WS_URL = "wss://optisys-api.up.railway.app/ws/progress"

def render_logs_tab():
    st.title("📡 Real-Time Integration Logs")

    if "log_lines" not in st.session_state:
        st.session_state.log_lines = []

    st.button("🛰️ Connect to WebSocket", on_click=start_ws_client)

    log_output = st.empty()
    log_output.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines), height=400)

async def log_handler():
    async with websockets.connect(WS_URL) as ws:
        while True:
            msg = await ws.recv()
            st.session_state.log_lines.append(msg)
            await asyncio.sleep(0.1)

def start_ws_client():
    asyncio.run(log_handler())
