import os
import asyncio
import streamlit as st
import websockets

from utils.ws_client import log_handler  # Presuming this exists, or else remove

# ✅ Page config and heading
st.set_page_config(page_title="OptiSys Suite", layout="wide")
st.title("🔧 OptiSys Autonomous Integration Dashboard")

# ✅ Overview
st.markdown("Welcome to the **OptiSys Integration Suite**. Use the sidebar to access:")
st.markdown("- 🧠 Integration Trigger Panel")
st.markdown("- 📡 Live Integration Logs")
st.markdown("- ⚙️ Product Configuration")
st.markdown("---")

# ✅ Log Stream Section
st.subheader("📡 Real-Time Integration Logs")

WS_URL = os.getenv("WS_URL", "wss://optisys-agent-production.up.railway.app/ws/progress")

if "log_lines" not in st.session_state:
    st.session_state.log_lines = []

async def start_log_listener():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                await asyncio.sleep(0.1)
                st.experimental_rerun()
    except websockets.exceptions.InvalidStatus as e:
        st.error(f"⚠️ WebSocket error: Invalid status - {e}")
    except Exception as e:
        st.error(f"❌ WebSocket error: {e}")

if st.button("🛰️ Connect to WebSocket"):
    asyncio.run(start_log_listener())

st.text_area("📋 Log Stream", "\n".join(st.session_state.log_lines[-100:]), height=400)

# ✅ Optional: Integration Insights (shown after a successful integration run)
# Note: 'result' must already be defined in the session or imported for this to work
if "result" in st.session_state:
    result = st.session_state["result"]
    
    st.markdown("### 🔍 Integration Insights")
    st.json({
        "recommended_sdk": result.get("analysis", {}).get("recommended_sdk"),
        "deployment_target": result.get("analysis", {}).get("deployment_target"),
        "license_ok": result.get("compliance", {}).get("license_ok"),
        "regression_detected": result.get("performance", {}).get("regression_detected")
    })
