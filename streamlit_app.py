
import streamlit as st
import requests
import os
import asyncio
import websockets

st.set_page_config(page_title="OptiSys Product Integrator", layout="centered")
st.title("🧠 OptiSys Autonomous Integrator")

API_BASE = os.getenv("API_BASE", "https://optisys-agent-production.up.railway.app")
TRIGGER_ENDPOINT = f"{API_BASE}/api/integrations/trigger"
WS_URL = f"wss://optisys-agent-production.up.railway.app/ws/progress"

products = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

tabs = st.tabs(["🚀 Integrate Product", "📡 Live Logs"])

with tabs[0]:
    product = st.selectbox("Select a Product to Integrate", products)

    with st.form("integration_form"):
        st.subheader("🔐 User Info & API Keys")
        customer_id = st.text_input("Customer ID", value="demo-customer-001")
        api_key = st.text_input("API Key", value="xyz-abc-123")
        region = st.selectbox("Region", ["us-east-1", "us-west-2", "eu-central-1"])

        with st.expander("☁️ Cloud Credentials (Optional)"):
            st.markdown("These will be encrypted at runtime and never stored.")
            aws_access_key = st.text_input("AWS Access Key ID", type="password")
            aws_secret_key = st.text_input("AWS Secret Access Key", type="password")
            gcp_service_account_json = st.text_area("GCP Service Account JSON", height=100)

        submitted = st.form_submit_button("🔄 Trigger Integration")

    if submitted:
        cloud_credentials = {
            "aws": {
                "access_key": aws_access_key,
                "secret_key": aws_secret_key,
            },
            "gcp": {
                "service_account_json": gcp_service_account_json,
            }
        }

        payload = {
            "product": product,
            "customer_id": customer_id,
            "api_key": api_key,
            "region": region,
            "cloud_credentials": cloud_credentials,
        }

        with st.spinner(f"Integrating {product}..."):
            try:
                res = requests.post(TRIGGER_ENDPOINT, json=payload)
                res.raise_for_status()
                result = res.json()
                st.success(f"{product} integration complete!")
                if result.get("dashboard_url"):
                    st.markdown(f"📊 [View Dashboard]({result.get('dashboard_url')})")
            except Exception as e:
                st.error(f"Integration failed: {e}")

with tabs[1]:
    st.subheader("📡 Real-Time Integration Logs")

    if "log_lines" not in st.session_state:
        st.session_state.log_lines = []

    if st.button("🛰️ Connect to WebSocket"):
        asyncio.run(log_handler())

    log_output = st.empty()
    log_output.text_area("📋 Log Stream", "\\n".join(st.session_state.log_lines), height=400)

async def log_handler():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                st.session_state.log_lines.append(msg)
                await asyncio.sleep(0.1)
    except Exception as e:
        st.session_state.log_lines.append(f"[Error] WebSocket connection failed: {e}")
