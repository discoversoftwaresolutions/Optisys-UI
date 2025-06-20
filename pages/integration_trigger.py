import os
import streamlit as st
import requests

st.title("🔗 Product Integration")

API_BASE = os.getenv("API_BASE", "https://optisys-agent-production.up.railway.app/api/integrations/trigger")

products = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

product = st.selectbox("Select a Product", products)

with st.form("integration_form"):
    customer_id = st.text_input("Customer ID", value="demo-customer-001")
    api_key = st.text_input("API Key", value="xyz-abc-123")
    region = st.selectbox("Region", ["us-east-1", "us-west-2", "eu-central-1"])

    cloud_provider = st.selectbox("Cloud Provider", ["AWS", "GCP"])
    if cloud_provider == "AWS":
        cloud_credentials = {
            "access_key": st.text_input("AWS Access Key"),
            "secret_key": st.text_input("AWS Secret Key"),
            "session_token": st.text_input("Session Token", value="", help="Optional")
        }
    else:
        cloud_credentials = {
            "gcp_service_account_json": st.text_area("GCP Service Account JSON")
        }

    submitted = st.form_submit_button("🚀 Trigger Integration")

if submitted:
    payload = {
        "product": product,
        "customer_id": customer_id,
        "api_key": api_key,
        "region": region,
        "cloud_credentials": cloud_credentials
    }

    with st.spinner("🔄 Integrating..."):
        try:
            response = requests.post(API_BASE, json=payload)
            response.raise_for_status()
            result = response.json()
            st.success("✅ Integration Complete!")
            if 'dashboard_url' in result:
                st.markdown(f"[📊 View Dashboard]({result['dashboard_url']})")
        except Exception as e:
            st.error(f"❌ Integration Failed: {e}")
