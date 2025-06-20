import streamlit as st
import asyncio
import websockets

WS_URL = "wss://optisys-agent-production.up.railway.app/ws/progress"

st.title("📡 Real-Time Integration Logs")

if "logs" not in st.session_state:
    st.session_state.logs = []

def start_log_listener():
    async def log_listener():
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.logs.append(msg)
                await asyncio.sleep(0.2)

    asyncio.run(log_listener())

if st.button("🛰️ Connect"):
    start_log_listener()

st.text_area("📋 Logs", "\n".join(st.session_state.logs), height=400)
