"""
Streamlit UI for the Wealth Management & Tax Advisory Demo.
Professional Finance Dashboard - UI/UX Pro Max Design System
"""

import streamlit as st
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import run_wealth_analysis
from database.seed_data import create_database, get_connection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="LaraCorp Wealth AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DESIGN SYSTEM - Finance Professional Theme
# Based on UI/UX Pro Max: Trust & Authority + Minimalism
# =============================================================================
FINANCE_COLORS = {
    "primary": "#0F172A",        # Deep navy - trust, authority
    "primary_light": "#1E293B",  # Lighter navy
    "secondary": "#1E3A8A",      # Royal blue - action
    "accent": "#059669",         # Emerald green - profit, positive
    "accent_light": "#10B981",   # Light green
    "warning": "#D97706",        # Amber - caution
    "danger": "#DC2626",         # Red - loss, critical
    "background": "#F8FAFC",     # Cool white - clean
    "surface": "#FFFFFF",        # Pure white - cards
    "text_primary": "#0F172A",   # Near black - headings
    "text_secondary": "#475569", # Slate - body text
    "text_muted": "#64748B",     # Light slate - labels
    "border": "#E2E8F0",         # Light border
}

# =============================================================================
# CUSTOM CSS - Professional Finance Styling
# =============================================================================
def inject_custom_css():
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: {FINANCE_COLORS["background"]};
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Metric Cards */
        div[data-testid="stMetric"] {{
            background-color: {FINANCE_COLORS["surface"]};
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        
        div[data-testid="stMetric"] > div {{
            color: {FINANCE_COLORS["text_muted"]};
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        div[data-testid="stMetric"] p {{
            color: {FINANCE_COLORS["text_primary"]};
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {FINANCE_COLORS["secondary"]};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .stButton > button:hover {{
            background-color: {FINANCE_COLORS["primary"]};
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        /* Expanders */
        div[data-testid="stExpander"] {{
            background-color: {FINANCE_COLORS["surface"]};
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
            margin-bottom: 1rem;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {FINANCE_COLORS["surface"]};
            border-right: 1px solid {FINANCE_COLORS["border"]};
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# =============================================================================
# DATABASE
# =============================================================================
def init_db():
    """Initialize database if needed."""
    if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "wealth_demo.db")):
        create_database()


def get_clients():
    """Get list of clients for sidebar."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT client_id, name, occupation, annual_income_lakhs FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return clients


# =============================================================================
# RENDER FUNCTIONS - Using Streamlit Native Components Only
# =============================================================================
def render_header():
    """Render app header using native Streamlit components."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("💼 LaraCorp Wealth AI")
        st.caption("Multi-Agent Wealth Management & Tax Advisory System")
    with col2:
        # Use native Streamlit components instead of HTML
        st.container()
        st.markdown("""
        <div style="text-align: right;">
            <p style="font-size: 0.75rem; color: #64748B; margin: 0;">
                <span style="font-weight: 600; color: #0F172A;">Indian Income Tax Act 2025</span><br/>
                FY 2025-26
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()


def render_sidebar(clients):
    """Render sidebar with client selection using native components."""
    with st.sidebar:
        st.header("Client Selection")
        st.caption("Select a client to analyze")
        
        client_options = {f"{c[1]} ({c[2]}, ₹{c[3]}L)": c[0] for c in clients}
        selected = st.radio(
            "Choose Client",
            options=list(client_options.keys()),
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Client info card using native components
        selected_id = client_options[selected]
        client = next(c for c in clients if c[0] == selected_id)
        
        with st.container(border=True):
            st.markdown(f"**{client[1]}**")
            st.caption(client[2])
            st.markdown(f"<span style='color: #1E3A8A; font-weight: 700;'>₹{client[3]}L/year</span>", unsafe_allow_html=True)
        
        return selected_id


def render_kpi_cards(asset_summary, tax_analysis):
    """Render KPI metric cards using st.metric."""
    total_value = asset_summary.get("total_value", 0)
    total_invested = asset_summary.get("total_invested", 0)
    total_pnl = asset_summary.get("total_unrealized_pnl", 0)
    tax_savings = sum(f.get("potential_savings", 0) for f in tax_analysis.get("flags", []))
    
    pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio Value", f"₹{total_value:,.0f}", f"{pnl_pct:.1f}%")
    with col2:
        st.metric("Total Invested", f"₹{total_invested:,.0f}")
    with col3:
        delta_color = "normal" if total_pnl >= 0 else "inverse"
        st.metric("Unrealized P&L", f"₹{total_pnl:,.0f}", f"{pnl_pct:.1f}%", delta_color=delta_color)
    with col4:
        st.metric("Tax Savings Potential", f"₹{tax_savings:,.0f}", "Annual opportunity")


def render_agent_timeline(thoughts):
    """Render agent execution timeline using native expander."""
    with st.expander("🔍 Agent Execution Timeline", expanded=False):
        for thought in thoughts:
            agent_name = thought["agent"]
            step = thought["step"]
            content = thought["thought"]
            
            agent_display = {
                "DataRetrievalAgent": "📊 Data Retrieval",
                "TaxAgent": "🧮 Tax Analysis",
                "AdvisoryAgent": "📋 Advisory Report",
            }.get(agent_name, agent_name)
            
            st.markdown(f"**{agent_display}** — *{step}*")
            st.caption(content)
            st.divider()


def render_portfolio_section(asset_summary, portfolio):
    """Render portfolio breakdown with charts using native components."""
    st.subheader("📈 Portfolio Analysis")
    
    breakdown = asset_summary.get("breakdown", [])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if breakdown:
            df_breakdown = pd.DataFrame(breakdown)
            df_breakdown = df_breakdown.sort_values("value", ascending=False)
            
            fig = px.pie(
                df_breakdown,
                values="value",
                names="asset_type",
                title="Asset Allocation",
                color_discrete_sequence=["#0F172A", "#1E3A8A", "#059669", "#D97706", "#7C3AED", "#DC2626", "#0891B2"],
                hole=0.55,
            )
            fig.update_layout(
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=14, color="#0F172A"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=40, b=60, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with col2:
        if breakdown:
            for item in sorted(breakdown, key=lambda x: x["value"], reverse=True):
                asset_type = item["asset_type"].replace("_", " ").title()
                value = item["value"]
                pnl = item.get("pnl", 0)
                pnl_pct = (pnl / value * 100) if value > 0 else 0
                pnl_color = "#059669" if pnl >= 0 else "#DC2626"
                pnl_sign = "+" if pnl >= 0 else ""
                
                # Use native columns instead of HTML
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**{asset_type}**")
                    st.caption(f"{pnl_sign}{pnl_pct:.1f}%")
                with c2:
                    st.markdown(f"<p style='text-align: right; margin: 0;'><strong>₹{value:,.0f}</strong></p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: right; margin: 0; color: {pnl_color}; font-size: 0.75rem; font-weight: 600;'>{pnl_sign}₹{abs(pnl):,.0f}</p>", unsafe_allow_html=True)
                st.divider()
    
    # Holdings table using native st.dataframe
    if portfolio:
        st.markdown("**Holdings Detail**")
        
        holdings_df = pd.DataFrame(portfolio)
        holdings_df["asset_type"] = holdings_df["asset_type"].str.replace("_", " ").str.title()
        holdings_df["pnl_pct"] = (holdings_df["unrealized_pnl"] / holdings_df["invested_amount"] * 100).round(1)
        
        display_df = holdings_df[["asset_type", "instrument_name", "units", "avg_buy_price",
                                   "current_price", "current_value", "unrealized_pnl", "pnl_pct"]].copy()
        display_df.columns = ["Asset Type", "Instrument", "Units", "Buy Price", "Current", "Value", "P&L", "P&L %"]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Buy Price": st.column_config.NumberColumn(format="₹%.2f"),
                "Current": st.column_config.NumberColumn(format="₹%.2f"),
                "Value": st.column_config.NumberColumn(format="₹%,.0f"),
                "P&L": st.column_config.NumberColumn(format="₹%,.0f"),
                "P&L %": st.column_config.NumberColumn(format="%.1f%%"),
            }
        )


def render_tax_section(tax_analysis):
    """Render tax analysis with progress bars and flags using native components."""
    st.subheader("🧮 Tax Analysis (FY 2025-26)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sec_80c_used = tax_analysis.get("sec_80c_used", 0)
        sec_80c_limit = 150000
        remaining_80c = max(0, sec_80c_limit - sec_80c_used)
        st.metric("Section 80C Used", f"₹{sec_80c_used:,.0f}", f"₹{remaining_80c:,.0f} remaining")
        st.progress(min(1.0, sec_80c_used / sec_80c_limit))
    
    with col2:
        nps_used = tax_analysis.get("nps_used", 0)
        nps_limit = 50000
        remaining_nps = max(0, nps_limit - nps_used)
        st.metric("80CCD(1B) NPS", f"₹{nps_used:,.0f}", f"₹{remaining_nps:,.0f} remaining")
        st.progress(min(1.0, nps_used / nps_limit))
    
    with col3:
        taxable_ltcg = tax_analysis.get("taxable_ltcg", 0)
        ltcg_tax = tax_analysis.get("ltcg_tax", 0)
        ltcg_delta = f"Tax: ₹{ltcg_tax:,.0f}" if ltcg_tax > 0 else "Within exemption"
        st.metric("Taxable LTCG", f"₹{taxable_ltcg:,.0f}", ltcg_delta)
    
    # Tax flags using native containers
    flags = tax_analysis.get("flags", [])
    if flags:
        st.markdown("**Tax Flags & Opportunities**")
        
        for flag in flags:
            severity = flag.get("severity", "info")
            section = flag.get("section", "General")
            message = flag.get("message", "")
            savings = flag.get("potential_savings", 0)
            
            emoji = {"warning": "⚠️", "info": "ℹ️", "critical": "🚨"}.get(severity, "•")
            
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{emoji} {section}**")
                    st.caption(message)
                with c2:
                    if savings > 0:
                        st.markdown(f"<p style='text-align: right; color: #059669; font-weight: 600; margin: 0;'>Save ₹{savings:,.0f}</p>", unsafe_allow_html=True)
    else:
        st.info("No tax flags found for this client.")
    
    # LLM Insights using native expander
    llm_insights = tax_analysis.get("llm_insights", "")
    if llm_insights:
        with st.expander("🤖 AI Tax Insights"):
            st.markdown(llm_insights)
    else:
        with st.expander("🤖 AI Tax Insights"):
            st.info("No AI insights available for this analysis.")


def render_report_section(report):
    """Render advisory report with executive summary and recommendations using native components."""
    st.subheader("📋 Advisory Report")
    
    # Executive Summary using native components
    executive_summary = report.get("executive_summary", "")
    if executive_summary:
        with st.container(border=True):
            st.markdown("### 📝 Executive Summary")
            st.markdown(executive_summary)
    else:
        with st.container(border=True):
            st.markdown("### 📝 Executive Summary")
            st.info("No executive summary available.")
    
    st.divider()
    
    # Recommendations using native components
    recommendations = report.get("recommendations", [])
    if recommendations:
        st.markdown("### 🎯 Recommendations")
        
        for i, rec in enumerate(recommendations):
            priority = rec.get("priority", "medium")
            category = rec.get("category", "General")
            title = rec.get("title", "Recommendation")
            description = rec.get("description", "")
            actions = rec.get("action_items", [])
            
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
            priority_color = {"high": "#DC2626", "medium": "#D97706", "low": "#059669"}.get(priority, "#64748B")
            
            with st.container(border=True):
                # Header row
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{priority_emoji} {title}**")
                with c2:
                    st.markdown(f"<p style='text-align: right; margin: 0;'><span style='background-color: {priority_color}20; color: {priority_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;'>{category.upper()}</span></p>", unsafe_allow_html=True)
                
                # Description
                if description:
                    st.markdown(description)
                
                # Action items using native list
                if actions:
                    st.markdown("**Action Items:**")
                    for action in actions:
                        st.markdown(f"- {action}")
                else:
                    st.caption("No specific action items for this recommendation.")
    else:
        st.info("No recommendations available for this client.")


def render_empty_state():
    """Render the initial empty state before analysis."""
    st.info("👆 Select a client from the sidebar and click **Generate Wealth Report** to run the multi-agent analysis pipeline.")


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Render header
    render_header()
    
    # Initialize DB
    init_db()
    
    # Sidebar
    clients = get_clients()
    selected_client_id = render_sidebar(clients)
    
    # Main action button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button(
            "🚀 Generate Wealth Report",
            type="primary",
            use_container_width=True,
        )
    
    if analyze_clicked:
        with st.spinner("Running multi-agent analysis pipeline..."):
            result = run_wealth_analysis(selected_client_id)
        
        # Check for errors
        errors = result.get("errors", [])
        if errors:
            for error in errors:
                st.error(f"Analysis Error: {error}")
        
        # KPI Cards
        asset_summary = result.get("asset_summary", {})
        tax_analysis = result.get("tax_analysis", {})
        render_kpi_cards(asset_summary, tax_analysis)
        
        # Agent Timeline
        thoughts = result.get("agent_thoughts", [])
        if thoughts:
            render_agent_timeline(thoughts)
        
        # Portfolio Section
        portfolio = result.get("portfolio", [])
        if portfolio:
            render_portfolio_section(asset_summary, portfolio)
        
        # Tax Analysis
        if tax_analysis:
            render_tax_section(tax_analysis)
        else:
            st.warning("No tax analysis data available.")
        
        # Advisory Report
        report = result.get("report", {})
        if report:
            render_report_section(report)
        else:
            st.warning("No advisory report available.")
        
        # Footer
        st.caption(f"Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M')} | LaraCorp Wealth AI v1.0")
    
    else:
        render_empty_state()


if __name__ == "__main__":
    main()
