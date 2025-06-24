import streamlit as st
from optisys_console import render

# --- Global Page Setup ---
st.set_page_config(page_title="OptiSys Console", layout="wide")

# --- Client ID Injection ---
client_id = st.query_params.get("client_id", "demo-client")

# --- Optional Branding (skip or customize as needed) ---
st.title("🎯 OptiSys Launch Console")
st.caption(f"Tenant: `{client_id}`")

# --- Launch Console ---
try:
    render(client_id)
except Exception as e:
    st.error(f"❌ Failed to render dashboard: {e}")
