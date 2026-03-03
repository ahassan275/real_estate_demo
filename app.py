import streamlit as st

st.set_page_config(
    page_title="Demo Apps",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Demo Applications")

st.markdown("""
## Available Dashboards

### 🏠 Real Estate Market Insights
Explore Ontario real estate market data with interactive visualizations and analysis.

**Features:**
- Market trends and price analysis
- Geographic visualizations
- Property type comparisons
- Time series analysis

---

### 🎯 Ontario Public Sector Lead Generation
Filter and analyze privacy, compliance, legal, and security professionals from Ontario's public service salary disclosure data.

**Features:**
- 9,082 qualified leads from 377,881 public servants
- Priority scoring and categorization
- Interactive filtering and search
- Export capabilities

**Target Roles:** Privacy Officers, Compliance, Legal Counsel, CISO, Risk Management, Governance

---

## Quick Start
👈 **Select a dashboard from the sidebar to get started**
""")

st.sidebar.success("Select a dashboard above")
