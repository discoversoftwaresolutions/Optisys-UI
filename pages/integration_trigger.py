import os
import streamlit as st
import requests

st.set_page_config(page_title="OptiSys Integration", page_icon="🔗")
st.title("🔗 OptiSys Full Integration")

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

    cloud_provider = st.selectbox("Cloud Provider", ["AWS", "GCP", "Azure", "Oracle"])
    provider = cloud_provider.lower()

    show_secrets = st.checkbox("🔍 Show sensitive fields for debugging")

    cloud_credentials = {}
    required_fields_filled = True

    if cloud_provider == "AWS":
        access_key = st.text_input("AWS Access Key")
        secret_key = st.text_input("AWS Secret Key", type=None if show_secrets else "password")
        session_token = st.text_input("Session Token", value="", help="Optional", type=None if show_secrets else "password")

        cloud_credentials = {
            "access_key": access_key,
            "secret_key": secret_key,
            "session_token": session_token
        }

        required_fields_filled = all([access_key, secret_key])

    elif cloud_provider == "GCP":
        gcp_json = st.text_area("GCP Service Account JSON", help="Paste the entire service account JSON key")
        cloud_credentials = {"gcp_service_account_json": gcp_json}
        required_fields_filled = bool(gcp_json.strip())

    elif cloud_provider == "Azure":
        tenant_id = st.text_input("Azure Tenant ID")
        client_id = st.text_input("Azure Client ID")
        client_secret = st.text_input("Azure Client Secret", type=None if show_secrets else "password")
        subscription_id = st.text_input("Azure Subscription ID")

        cloud_credentials = {
            "tenant_id": tenant_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "subscription_id": subscription_id
        }

        required_fields_filled = all([tenant_id, client_id, client_secret, subscription_id])

    elif cloud_provider == "Oracle":
        tenancy_ocid = st.text_input("Oracle Tenancy OCID")
        user_ocid = st.text_input("Oracle User OCID")
        fingerprint = st.text_input("API Key Fingerprint")
        private_key = st.text_area("Private Key PEM", type=None if show_secrets else "password")
        oracle_region = st.text_input("Oracle Region", value="us-ashburn-1")

        cloud_credentials = {
            "tenancy_ocid": tenancy_ocid,
            "user_ocid": user_ocid,
            "fingerprint": fingerprint,
            "private_key": private_key,
            "region": oracle_region
        }

        required_fields_filled = all([tenancy_ocid, user_ocid, fingerprint, private_key, oracle_region])

    st.caption("🔒 Credentials are used only for this integration session and are never stored.")

    form_ready = all([product, customer_id, api_key, region, provider, required_fields_filled])
    submitted = st.form_submit_button("🚀 Run OptiSys Integration", disabled=not form_ready)

if submitted:
    payload = {
        "product": product,
        "customer_id": customer_id,
        "api_key": api_key,
        "region": region,
        "provider": provider,
        "cloud_credentials": cloud_credentials
    }

    st.markdown("🧪 **Payload Preview**")
    st.json(payload)

    with st.spinner("🤖 OptiSys is reasoning, integrating, and validating..."):
        try:
            response = requests.post(API_BASE, json=payload)
            response.raise_for_status()
            result = response.json()
            st.success("✅ Integration Complete!")
            st.json(result)
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Integration failed with status {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"💥 Unexpected error: {e}")
