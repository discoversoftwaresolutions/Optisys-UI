import os
import streamlit as st
import asyncio
import websockets
from dotenv import load_dotenv

load_dotenv()

def render_logs_tab():
    st.title("📡 Live Integration Logs")

    # Session ID input
    session_id = st.text_input("Session ID", value="SecurePact_demo001")

    if "log_lines" not in st.session_state:
        st.session_state.log_lines = []

    # Button to start log stream
    if st.button("🛰️ Connect to Logs"):
        st.session_state["connect_logs"] = True
        st.session_state.log_lines.clear()  # Reset previous logs

    # Trigger WebSocket connection
    if st.session_state.get("connect_logs", False):
        st.info(f"Connecting to session: `{session_id}`...")
        ws_url = f"wss://optisys-agent-production.up.railway.app/ws/{session_id}"
        try:
            asyncio.run(log_handler(ws_url))
        except Exception as e:
            st.error(f"❌ WebSocket connection error: {str(e)}")

    st.markdown("### 📋 Log Output")
    st.text_area("Log Stream", "\n".join(st.session_state.log_lines), height=500)

async def log_handler(ws_url: str):
    try:
        async with websockets.connect(ws_url) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                await asyncio.sleep(0.1)
    except Exception as e:
        st.error(f"❌ WebSocket error: {str(e)}")
