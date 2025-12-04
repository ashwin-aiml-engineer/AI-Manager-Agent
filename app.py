import streamlit as st

# Page Config
st.set_page_config(
    page_title="AI Manager Agent",
    page_icon="🤖",
    layout="wide"
)

# Title and Intro
st.title("🤖 AI Business Manager (Local HQ)")
st.markdown("---")

# Dashboard Stats (Mockup for now)
col1, col2, col3 = st.columns(3)

with col1:
    st.info("⚖️ **Legal Module**\n\nReady to draft contracts and answer queries.")

with col2:
    st.success("📊 **Data Module**\n\nReady to analyze sales CSVs and generate charts.")

with col3:
    st.warning("🔒 **System Status**\n\nRunning 100% Offline via Ollama.")

st.markdown("---")
st.subheader("👈 Select a Module from the Sidebar to begin.")

# Instructions
st.markdown("""
### Quick Start Guide:
1. **Legal Agent:** Upload a PDF (Contract/Petition) and ask questions.
2. **Data Analyst:** Upload a CSV (Sales/Expenses) and ask for charts.
""")