import streamlit as st

st.set_page_config(page_title="OptiSys Suite", layout="wide")
st.title("🔧 OptiSys Autonomous Integration Dashboard")

st.markdown("Welcome to the **OptiSys Integration Suite**. Use the sidebar to access:")
st.markdown("- 🧠 Integration Trigger Panel")
st.markdown("- 📡 Live Integration Logs")
st.markdown("- ⚙️ Product Configuration")

with open(os.path.join(base_path, "app.py"), "w") as f:
    f.write(app_py)

# Write log_view.py in pages/
log_view_py = '''\
import asyncio
import streamlit as st
import websockets
import os

st.set_page_config(page_title="📡 Integration Logs", layout="centered")
st.title("📡 Real-Time Integration Logs")

WS_URL = os.getenv("WS_URL", "wss://optisys-agent-production.up.railway.app/ws/progress")

if "log_lines" not in st.session_state:
    st.session_state.log_lines = []

def start_ws_client():
    asyncio.run(log_handler())

async def log_handler():
    async with websockets.connect(WS_URL) as ws:
        while True:
            msg = await ws.recv()
            st.session_state.log_lines.append(msg)
            st.experimental_rerun()

if st.button("🛰️ Connect to WebSocket"):
    start_ws_client()

st.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines[-100:]), height=400)
