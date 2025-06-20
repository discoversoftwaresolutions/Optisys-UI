import os
import streamlit as st
import asyncio
import websockets
from dotenv import load_dotenv

load_dotenv()

# WebSocket URL from environment or default
WS_URL = os.getenv("WS_URL", "wss://optisys-agent-production.up.railway.app/ws/progress")

def render_logs_tab():
    st.title("📡 Real-Time Integration Logs")

    if "log_lines" not in st.session_state:
        st.session_state.log_lines = []

    if st.button("🛰️ Connect to WebSocket"):
        st.session_state["connect_logs"] = True

    if st.session_state.get("connect_logs", False):
        st.info("Connecting to WebSocket...")
        asyncio.run(log_handler())

    log_output = st.empty()
    log_output.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines), height=400)

async def log_handler():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                await asyncio.sleep(0.1)
    except Exception as e:
        st.error(f"WebSocket Error: {str(e)}")
