import streamlit as st
import requests

st.title("📦 Discover Product Catalog")

PRODUCTS_API = "https://optisys-agent-production.up.railway.app/api/products/"

try:
    response = requests.get(PRODUCTS_API)
    response.raise_for_status()
    products = response.json().get("products", [])
    for product in products:
        st.subheader(product.get("name", "Unnamed"))
        st.markdown(f"📄 Docs: {product.get('docs_url', 'N/A')}")
        st.json(product)
except Exception as e:
    st.error(f"Could not fetch product catalog: {e}")
