"""
Streamlit UI for the Wealth Management & Tax Advisory Demo.
"""

import streamlit as st
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import run_wealth_analysis
from database.seed_data import create_database, get_connection
import pandas as pd

# Page config
st.set_page_config(
    page_title="Wealth Management AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .agent-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .tax-flag-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .tax-flag-info {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .recommendation-high {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .recommendation-medium {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


def init_db():
    """Initialize database if needed."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "wealth_demo.db")
    if not os.path.exists(db_path):
        create_database()
    return db_path


def get_clients():
    """Fetch all clients from DB."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT client_id, name, age, occupation, annual_income_lakhs, tax_regime, city FROM clients")
    clients = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return clients


def main():
    st.markdown('<p class="main-header">💰 AI Wealth Management & Tax Advisory</p>', unsafe_allow_html=True)
    st.markdown("*Multi-Agent System powered by LangGraph + Ollama*")

    # Initialize DB
    init_db()

    # Sidebar
    st.sidebar.header("Client Selection")
    clients = get_clients()
    client_names = {c["client_id"]: f"{c['name']} ({c['occupation']}, ₹{c['annual_income_lakhs']}L)" for c in clients}
    selected_client_id = st.sidebar.selectbox(
        "Select Client",
        options=list(client_names.keys()),
        format_func=lambda x: client_names[x]
    )

    selected_client = next(c for c in clients if c["client_id"] == selected_client_id)

    # Client info card
    st.sidebar.markdown("---")
    st.sidebar.subheader("Client Profile")
    st.sidebar.write(f"**Name:** {selected_client['name']}")
    st.sidebar.write(f"**Age:** {selected_client['age']}")
    st.sidebar.write(f"**Occupation:** {selected_client['occupation']}")
    st.sidebar.write(f"**Annual Income:** ₹{selected_client['annual_income_lakhs']} Lakhs")
    st.sidebar.write(f"**Tax Regime:** {selected_client['tax_regime'].upper()}")
    st.sidebar.write(f"**City:** {selected_client['city']}")

    # Main action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Wealth Report", type="primary", use_container_width=True):
            with st.spinner("AI Agents are analyzing your portfolio..."):
                # Run the analysis
                result = run_wealth_analysis(selected_client_id)

                # Display agent thoughts
                st.subheader("🤖 Agent Execution Log")
                thoughts = result.get("agent_thoughts", [])

                for thought in thoughts:
                    agent_icon = {
                        "DataRetrievalAgent": "📊",
                        "TaxAgent": "🧮",
                        "AdvisoryAgent": "📋",
                    }.get(thought["agent"], "🤖")

                    with st.container():
                        st.markdown(f"""
                        <div class="agent-card">
                            <b>{agent_icon} {thought['agent']}</b> — {thought['step']}<br>
                            <small>{thought['thought']}</small>
                        </div>
                        """, unsafe_allow_html=True)

                # Portfolio Summary
                st.markdown("---")
                st.subheader("📊 Portfolio Summary")

                asset_summary = result.get("asset_summary", {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Value", f"₹{asset_summary.get('total_value', 0):,.0f}")
                with col2:
                    st.metric("Invested", f"₹{asset_summary.get('total_invested', 0):,.0f}")
                with col3:
                    st.metric("Unrealized P&L", f"₹{asset_summary.get('total_unrealized_pnl', 0):,.0f}")
                with col4:
                    tax_savings = sum(f.get("potential_savings", 0) for f in result.get("tax_analysis", {}).get("flags", []))
                    st.metric("Tax Savings Potential", f"₹{tax_savings:,.0f}")

                # Asset breakdown chart
                breakdown = asset_summary.get("breakdown", [])
                if breakdown:
                    df = pd.DataFrame(breakdown)
                    st.bar_chart(df.set_index("asset_type")["value"])

                # Tax Analysis
                st.markdown("---")
                st.subheader("🧮 Tax Analysis (FY 2025-26)")

                tax = result.get("tax_analysis", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("80C Used", f"₹{tax.get('sec_80c_used', 0):,.0f}")
                with col2:
                    st.metric("80C Remaining", f"₹{tax.get('sec_80c_remaining', 0):,.0f}")
                with col3:
                    st.metric("Taxable LTCG", f"₹{tax.get('taxable_ltcg', 0):,.0f}")

                # Tax flags
                flags = tax.get("flags", [])
                if flags:
                    st.subheader("⚠️ Tax Flags & Opportunities")
                    for flag in flags:
                        css_class = "tax-flag-warning" if flag["severity"] == "warning" else "tax-flag-info"
                        st.markdown(f"""
                        <div class="{css_class}">
                            <b>[{flag['severity'].upper()}] {flag['section']}</b><br>
                            {flag['message']}<br>
                            <small>Potential Savings: ₹{flag.get('potential_savings', 0):,.0f}</small>
                        </div>
                        """, unsafe_allow_html=True)

                # LLM Insights
                if tax.get("llm_insights"):
                    with st.expander("🤖 AI Tax Insights"):
                        st.write(tax["llm_insights"])

                # Advisory Report
                st.markdown("---")
                st.subheader("📋 Advisory Report")

                report = result.get("report", {})
                if report.get("executive_summary"):
                    st.markdown("### Executive Summary")
                    st.write(report["executive_summary"])

                # Recommendations
                recommendations = report.get("recommendations", [])
                if recommendations:
                    st.markdown("### 🎯 Recommendations")
                    for rec in recommendations:
                        css_class = "recommendation-high" if rec["priority"] == "high" else "recommendation-medium"
                        st.markdown(f"""
                        <div class="{css_class}">
                            <b>[{rec['priority'].upper()}] {rec['title']}</b> ({rec['category']})<br>
                            {rec['description']}<br>
                            <small><b>Action Items:</b></small><br>
                            <small>{'<br>'.join(['• ' + item for item in rec['action_items']])}</small>
                        </div>
                        """, unsafe_allow_html=True)

                # Errors (if any)
                errors = result.get("errors", [])
                if errors:
                    st.error("Errors occurred during analysis:")
                    for error in errors:
                        st.error(error)
        else:
            # Show placeholder
            st.info("👈 Select a client and click 'Generate Wealth Report' to see the AI agents in action!")

        # Show architecture diagram
        st.markdown("---")
        st.subheader("🏗️ System Architecture")
        st.markdown("""
        ```
        ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
        │  📊 Data Agent  │────▶│  🧮 Tax Agent   │────▶│  📋 Advisory    │
        │                 │     │                 │     │     Agent       │
        │  SQLite DB      │     │  Tax Act 2025   │     │  Report Gen     │
        │  Portfolio      │     │  Ollama/Kimi    │     │  Ollama/Kimi    │
        └─────────────────┘     └─────────────────┘     └─────────────────┘
                │                       │                       │
                └───────────────────────┼───────────────────────┘
                                        ▼
                              ┌─────────────────┐
                              │  Shared State   │
                              │  (LangGraph)    │
                              └─────────────────┘
        ```
        """)


if __name__ == "__main__":
    main()
