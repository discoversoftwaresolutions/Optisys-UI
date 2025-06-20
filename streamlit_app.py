# streamlit_app.py

import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from .env for local dev
load_dotenv()

# 🔗 Dynamic API base URL
API_BASE = os.getenv("API_BASE", API_BASE = "https://optisys-api.up.railway.app/api/integrations/trigger"

TRIGGER_ENDPOINT = f"{API_BASE}/integrations/trigger"

st.set_page_config(page_title="OptiSys Product Integrator", layout="centered")
st.title("🧠 OptiSys Autonomous Integrator")

st.markdown("Securely trigger integrations of Discover Software products into your cloud infrastructure.")

# 🧩 Product List
products = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

# 📦 Provider List
cloud_providers = ["aws", "gcp", "azure"]

product = st.selectbox("🔧 Select a Product to Integrate", products)

with st.form("integration_form"):
    customer_id = st.text_input("🧑 Customer ID", value="demo-customer-001")
    api_key = st.text_input("🔐 API Key", value="xyz-abc-123", type="password")
    region = st.selectbox("🌍 Region", ["us-east-1", "us-west-2", "eu-central-1"])
    provider = st.selectbox("☁️ Cloud Provider", cloud_providers)
    submitted = st.form_submit_button("🚀 Trigger Integration")

# 🔄 Trigger Integration
if submitted:
    payload = {
        "product": product,
        "customer_id": customer_id,
        "api_key": api_key,
        "region": region,
        "provider": provider
    }

    with st.spinner(f"Integrating {product} with {provider.upper()}..."):
        try:
            res = requests.post(TRIGGER_ENDPOINT, json=payload)
            res.raise_for_status()
            result = res.json()
            st.success(f"✅ {product} integration complete!")
            st.markdown(f"📊 [View Dashboard]({result.get('dashboard_url')})")
        except Exception as e:
            st.error(f"❌ Integration failed: {e}")
