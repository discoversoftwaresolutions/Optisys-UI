import os
import asyncio
import streamlit as st
import websockets

from utils.ws_client import log_handler

# ✅ Page config
st.set_page_config(page_title="OptiSys Suite", layout="wide")
st.title("🔧 OptiSys Autonomous Integration Dashboard")

# ✅ Introduction
st.markdown("Welcome to the **OptiSys Integration Suite**. Use the sidebar to access:")
st.markdown("- 🧠 Integration Trigger Panel")
st.markdown("- 📡 Live Integration Logs")
st.markdown("- ⚙️ Product Configuration")
st.markdown("---")

# ✅ Real-Time Log Viewer
st.title("📡 Real-Time Integration Logs")

WS_URL = os.getenv("WS_URL", "wss://optisys-agent-production.up.railway.app/ws/progress")

if "log_lines" not in st.session_state:
    st.session_state.log_lines = []

async def log_handler():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
