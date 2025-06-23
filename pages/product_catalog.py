import streamlit as st

st.set_page_config(page_title="OptiSys Stack Integrations", layout="wide")
st.title("📦 Discover Available Stack Integrations")

st.markdown("""
OptiSys recommends post-purchase integrations based on your customer's stack.
Browse integrations or paste a tech stack description to receive custom suggestions.
""")

# Example integration data
example_stack = [
    {
        "name": "SecurePact",
        "type": "Compliance",
        "autonomous": True,
        "description": "Capture and forward webhook events securely."
    },
    {
        "name": "StratEx",
        "type": "Analytics",
        "autonomous": False,
        "description": "Perform post-purchase data enrichment and cohort analysis."
    },
    {
        "name": "CarbonIQ",
        "type": "Performance Optimization",
        "autonomous": True,
        "description": "Track and optimize your stack’s sustainability footprint."
    }
]

# Sidebar filters
autonomous_only = st.sidebar.checkbox("🤖 Show Autonomous Only")

# Dynamic Stack Suggestions (optional future hook)
stack_input = st.text_area("💡 Paste Customer Stack Description")
if st.button("Suggest Integrations"):
    st.warning("Integration suggestion logic coming soon...")
    # Later: hook this to `suggest_integrations(...)` API

# Integration browser
st.markdown("### 🔍 Available Integrations")

for item in example_stack:
    if autonomous_only and not item["autonomous"]:
        continue

    with st.expander(f"{item['name']} — {item['type']}"):
        st.markdown(item["description"])
        icon = "✅ Autonomous" if item["autonomous"] else "🧰 Manual Configuration Required"
        st.write(f"**Mode**: {icon}")
        st.button(f"🚀 Trigger {item['name']}", key=item["name"])

st.info("To launch a stack-based integration, paste a stack description or select an item above.")
