import os
import asyncio
import streamlit as st
import websockets

st.set_page_config(page_title="OptiSys Suite", layout="wide")
st.title("🔧 OptiSys Autonomous Integration Dashboard")

st.markdown("Welcome to the **OptiSys Integration Suite**. Use the sidebar to access:")
st.markdown("- 🧠 Integration Trigger Panel")
st.markdown("- 📡 Live Integration Logs")
st.markdown("- ⚙️ Product Configuration")

st.markdown("---")
st.set_page_config(page_title="📡 Integration Logs", layout="centered")
st.title("📡 Real-Time Integration Logs")

WS_URL = os.getenv("WS_URL", "wss://optisys-agent-production.up.railway.app/ws/progress")

if "log_lines" not in st.session_state:
    st.session_state.log_lines = []

async def log_handler():
    async with websockets.connect(WS_URL) as ws:
        while True:
            msg = await ws.recv()
            st.session_state.log_lines.append(msg)
            st.experimental_rerun()

def start_ws_client():
    asyncio.run(log_handler())

if st.button("🛰️ Connect to WebSocket"):
    start_ws_client()

st.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines[-100:]), height=400)
import streamlit as st
import asyncio
import websockets

WS_URL = "wss://optisys-agent-production.up.railway.app/ws/progress"

async def log_handler():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                st.experimental_rerun()
    except websockets.exceptions.InvalidStatus as e:
        st.error(f"⚠️ WebSocket error: Invalid status - {e}")
    except Exception as e:
        st.error(f"❌ WebSocket error: {e}")
