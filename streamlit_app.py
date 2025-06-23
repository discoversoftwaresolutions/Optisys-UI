import streamlit as st
from datetime import datetime

st.set_page_config(page_title="OptiSys Console", layout="wide")
st.title("🎯 OptiSys Launch Console")

st.markdown("Welcome back. Here's everything that matters right now—summarized and actionable.")

# ----- INSTANT ACTIONS -----
st.subheader("⚡ Quick Commands")
st.button("🔄 Run Stack Integration")
st.button("🚀 Trigger SecurePact Now")
st.button("🧠 Generate Stack-Based Recommendations")

# ----- CURRENT SESSION CONTEXT -----
st.subheader("🛠️ Latest Session")
col1, col2 = st.columns(2)
col1.code("Session ID: SecurePact_demo001")
col2.metric("Last Status", "✅ Completed")

# ----- RECENT EVENT FEED -----
st.subheader("📜 Recent Activity")
st.markdown("""
- ✅ Integration `SecurePact_demo001` completed at `10:42 AM`
- ⚙️ Stack scan ran for merchant `CarbonIQ_demo01` at `10:25 AM`
- ❌ StratEx trial integration failed at `9:58 AM`
""")

# ----- SYSTEM STATUS PULSE -----
st.subheader("🔋 System Pulse")
col3, col4, col5 = st.columns(3)
col3.success("API: Online")
col4.success("WebSocket: Live")
col5.success("Database: ✅ Connected")

# ----- INSIGHT OF THE MOMENT -----
st.markdown("### 🧠 Stack Tip of the Day")
st.info("Most Shopify+ stores improved conversion by adding HoloUX within 2 mins of checkout. Want to try it?")
