# ws_client.py
import streamlit as st
import websockets
import asyncio

WS_URL = "wss://optisys-agent-production.up.railway.app/ws/progress"

async def log_handler():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ WebSocket error: {e}")
