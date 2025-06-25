import os
import streamlit as st
import requests

st.set_page_config(page_title="OptiSys Integration", page_icon="🔗")
st.title("🔗 OptiSys Full Integration")

API_BASE = os.getenv("API_BASE", "https://optisys-agent-production.up.railway.app/api/integrations/trigger")

# Store user's debug toggle + selected provider
if "show_secrets" not in st.session_state:
    st.session_state.show_secrets = False

products = [
    "SecurePact", "CarbonIQ", "StratEx", "DataLakeIQ",
    "IntellicoreAGI", "ProverbsAPI", "Nexonomy", "Enginuty", "HoloUX"
]

product = st.selectbox("Select a Product", products)

# Select provider OUTSIDE form so it triggers a re-render
cloud_provider = st.selectbox("Cloud Provider", ["AWS", "GCP", "Azure", "Oracle"])
provider = cloud_provider.lower()
st.session_state["cloud_provider"] = provider

st.checkbox("🔍 Show sensitive fields for debugging", key="show_secrets")

with st.form("integration_form"):
    customer_id = st.text_input("Customer ID", value="demo-customer-001")
    api_key = st.text_input("API Key", value="xyz-abc-123")
    region = st.selectbox("Region", ["us-east-1", "us-west-2", "eu-central-1"])

    cloud_credentials = {}

    if cloud_provider == "AWS":
        cloud_credentials = {
            "access_key": st.text_input("AWS Access Key"),
            "secret_key": st.text_input("AWS Secret Key", type=None if st.session_state.show_secrets else "password"),
            "session_token": st.text_input("Session Token", value="", type=None if st.session_state.show_secrets else "password", help="Optional")
        }

    elif cloud_provider == "GCP":
        cloud_credentials = {
            "gcp_service_account_json": st.text_area("GCP Service Account JSON", help="Paste entire service account JSON")
        }

    elif cloud_provider == "Azure":
        cloud_credentials = {
            "tenant_id": st.text_input("Azure Tenant ID"),
            "client_id": st.text_input("Azure Client ID"),
            "client_secret": st.text_input("Azure Client Secret", type=None if st.session_state.show_secrets else "password"),
            "subscription_id": st.text_input("Azure Subscription ID")
        }

    elif cloud_provider == "Oracle":
        if st.session_state.show_secrets:
            private_key = st.text_area("Private Key PEM")
        else:
            private_key = st.text_input("Private Key PEM", type="password")

        cloud_credentials = {
            "tenancy_ocid": st.text_input("Oracle Tenancy OCID"),
            "user_ocid": st.text_input("Oracle User OCID"),
            "fingerprint": st.text_input("API Key Fingerprint"),
            "private_key": private_key,
            "region": st.text_input("Oracle Region", value="us-ashburn-1")
        }

    st.caption("🔒 Credentials are used only for this integration session and are never stored.")
    submitted = st.form_submit_button("🚀 Run OptiSys Integration")

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

session_id = f"{product}_{customer_id}"

st.components.v1.html(f"""
    <script>
    const ws = new WebSocket("wss://optisys-agent-production.up.railway.app/ws/progress?product={product}&customer_id={customer_id}");
    ws.onmessage = function(event) {{
        const logBox = document.getElementById("log");
        logBox.innerHTML += "<div>" + event.data + "</div>";
        logBox.scrollTop = logBox.scrollHeight;
    }};
    </script>
    <div id="log" style="background:#111;color:#0f0;padding:1em;height:300px;overflow:auto;font-family:monospace;"></div>
""", height=320)
