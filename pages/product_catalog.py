import streamlit as st

st.set_page_config(page_title="OptiSys Stack Integrations", layout="wide")
st.title("📦 Discover Available Stack Integrations")

st.markdown("""
OptiSys dynamically recommends integrations based on a customer's tech stack.
Product catalog browsing has been deprecated in favor of **autonomous stack-driven integration**.
""")

# Placeholder logic for now
example_stack = [
    {"name": "SecurePact", "type": "Compliance", "autonomous": True},
    {"name": "StratEx", "type": "Analytics", "autonomous": False},
    {"name": "CarbonIQ", "type": "Performance Optimization", "autonomous": True}
]

st.markdown("### 🧠 Available Integrations")
for item in example_stack:
    icon = "🤖" if item["autonomous"] else "🛠️"
    st.markdown(f"- {icon} **{item['name']}** — _{item['type']}_")

st.info("To launch an integration, visit the Integration Trigger Panel in the sidebar.")
