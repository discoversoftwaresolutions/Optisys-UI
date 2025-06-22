import os
import streamlit as st
import requests

st.title("🔗 OptiSys Full Integration")

API_BASE = os.getenv("API_BASE", "https://optisys-agent-production.up.railway.app/api/trigger/full")

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

    submitted = st.form_submit_button("🚀 Run OptiSys Integration")

if submitted:
    # Describe the customer's stack for reasoning
    stack_description = (
        f"The customer has purchased {product} and is operating in {region} on {cloud_provider}. "
        f"Integration should connect this service into their post-purchase flow using available credentials."
    )

    st.markdown("🧪 **Payload Preview**")
    st.json({
        "stack_description": stack_description
    })

    with st.spinner("🤖 OptiSys is reasoning, integrating, and validating..."):
        try:
            response = requests.post(API_BASE, json={"stack_description": stack_description})
            response.raise_for_status()
            result = response.json().get("result", {})
            st.success("✅ Integration Complete!")
            st.json(result)
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Integration failed with status {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"💥 Unexpected error: {e}")
