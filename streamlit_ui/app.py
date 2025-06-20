import streamlit as st
import requests
from streamlit_extras.colored_header import colored_header

st.set_page_config(
    page_title="OptiSys Product Integrator",
    layout="centered",
    page_icon="🧠"
)

colored_header(
    label="OptiSys Autonomous Integration",
    description="Connect cloud credentials. Deploy enterprise-grade products autonomously.",
    color_name="blue-green-70",
)

API_BASE = "https://optisys-api.up.railway.app/api/integrations/trigger"

product_icons = {
    "SecurePact": "🛡️", "CarbonIQ": "🌿", "StratEx": "📊", "DataLakeIQ": "💾",
    "IntellicoreAGI": "🧠", "ProverbsAPI": "📜", "Nexonomy": "💱", "Enginuty": "⚙️", "HoloUX": "🎛️"
}

product_labels = [f"{icon} {name}" for name, icon in product_icons.items()]
product_map = {label: name for label, name in zip(product_labels, product_icons.keys())}

product_label = st.selectbox("📦 Select a Product to Integrate", product_labels)
product = product_map[product_label]

st.subheader("🔐 Integration Parameters")

with st.form("integration_form"):
    customer_id = st.text_input("🧾 Customer ID", value="demo-customer-001")
    api_key = st.text_input("🔑 API Key", value="xyz-abc-123", type="password")
    region = st.selectbox("🌍 Region", ["us-east-1", "us-west-2", "eu-central-1"])

    st.markdown("### ☁️ Cloud Credentials (Optional)")
    aws_access_key = st.text_input("🔐 AWS Access Key ID", type="password")
    aws_secret_key = st.text_input("🔐 AWS Secret Access Key", type="password")

    submitted = st.form_submit_button("🚀 Trigger Integration")

if submitted:
    payload = {
        "product": product,
        "customer_id": customer_id,
        "api_key": api_key,
        "region": region,
        "cloud_credentials": {
            "aws_access_key_id": aws_access_key,
            "aws_secret_access_key": aws_secret_key
        }
    }

    with st.spinner(f"Launching {product} integration..."):
        try:
            response = requests.post(API_BASE, json=payload)
            response.raise_for_status()
            result = response.json()
            st.success("✅ Integration Complete")
            st.markdown(f"📊 [View Dashboard]({result.get('dashboard_url')})")
        except Exception as e:
            st.error(f"❌ Integration failed: {e}")
