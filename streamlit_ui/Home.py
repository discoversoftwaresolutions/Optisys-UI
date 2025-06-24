import streamlit as st
from utils import load_client_profile

client_id = st.query_params.get("client_id", "demo")
load_client_profile(client_id)

st.set_page_config(page_title=f"{st.session_state.brand['name']} Console")
st.image(st.session_state.brand["logo_url"], width=160)

st.sidebar.markdown(f"**Client**: `{client_id}`")
st.sidebar.markdown(f"[Support]({st.session_state.brand['support_email']})")
