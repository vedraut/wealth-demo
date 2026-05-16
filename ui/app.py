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
    page_icon="assets/favicon.ico" if os.path.exists("assets/favicon.ico") else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DESIGN SYSTEM - Finance Professional Theme
# Based on UI/UX Pro Max: Trust & Authority + Minimalism & Swiss Style
# =============================================================================
FINANCE_COLORS = {
    "primary": "#1E3A5F",        # Deep navy - trust, authority
    "primary_light": "#2A4A73",  # Lighter navy for hover
    "secondary": "#2563EB",      # Royal blue - action, links
    "accent": "#059669",         # Emerald green - profit, positive
    "accent_light": "#10B981",   # Light green
    "warning": "#D97706",        # Amber - caution
    "danger": "#DC2626",         # Red - loss, critical
    "danger_light": "#EF4444",
    "background": "#F8FAFC",     # Cool white - clean
    "surface": "#FFFFFF",        # Pure white - cards
    "surface_alt": "#F1F5F9",    # Slight gray - alternating
    "text_primary": "#0F172A",   # Near black - headings
    "text_secondary": "#475569", # Slate - body text
    "text_muted": "#94A3B8",     # Light slate - labels
    "border": "#E2E8F0",         # Light border
    "border_strong": "#CBD5E1",  # Stronger border
    "gold": "#B45309",           # Premium gold accent
    "gold_light": "#D97706",
}

# =============================================================================
# CUSTOM CSS - Professional Finance Styling
# =============================================================================
def inject_custom_css():
    css = f"""
    <style>
        /* Import professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: {FINANCE_COLORS["background"]};
        }}
        
        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {FINANCE_COLORS["surface"]};
            border-right: 1px solid {FINANCE_COLORS["border"]};
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {FINANCE_COLORS["text_secondary"]};
        }}
        
        /* Header area */
        .app-header {{
            background: linear-gradient(135deg, {FINANCE_COLORS["primary"]} 0%, {FINANCE_COLORS["primary_light"]} 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        
        .app-header h1 {{
            color: #FFFFFF;
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.025em;
        }}
        
        .app-header p {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.875rem;
            margin: 0.25rem 0 0 0;
            font-weight: 400;
        }}
        
        /* KPI Cards */
        .kpi-card {{
            background-color: {FINANCE_COLORS["surface"]};
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }}
        
        .kpi-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transform: translateY(-1px);
        }}
        
        .kpi-label {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {FINANCE_COLORS["text_muted"]};
            margin-bottom: 0.5rem;
        }}
        
        .kpi-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {FINANCE_COLORS["text_primary"]};
            letter-spacing: -0.02em;
        }}
        
        .kpi-delta {{
            font-size: 0.8125rem;
            font-weight: 600;
            margin-top: 0.25rem;
        }}
        
        .kpi-delta.positive {{
            color: {FINANCE_COLORS["accent"]};
        }}
        
        .kpi-delta.negative {{
            color: {FINANCE_COLORS["danger"]};
        }}
        
        /* Section Cards */
        .section-card {{
            background-color: {FINANCE_COLORS["surface"]};
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        
        .section-header {{
            font-size: 1.125rem;
            font-weight: 700;
            color: {FINANCE_COLORS["text_primary"]};
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid {FINANCE_COLORS["border"]};
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* Agent Timeline */
        .agent-timeline {{
            position: relative;
            padding-left: 2rem;
        }}
        
        .agent-timeline::before {{
            content: '';
            position: absolute;
            left: 0.5rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, {FINANCE_COLORS["secondary"]} 0%, {FINANCE_COLORS["accent"]} 100%);
            border-radius: 1px;
        }}
        
        .agent-step {{
            position: relative;
            margin-bottom: 1.25rem;
            padding: 1rem;
            background-color: {FINANCE_COLORS["surface"]};
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 10px;
            border-left: 3px solid {FINANCE_COLORS["secondary"]};
        }}
        
        .agent-step::before {{
            content: '';
            position: absolute;
            left: -1.75rem;
            top: 1.25rem;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: {FINANCE_COLORS["secondary"]};
            border: 2px solid {FINANCE_COLORS["surface"]};
            box-shadow: 0 0 0 2px {FINANCE_COLORS["secondary"]};
        }}
        
        .agent-step.completed::before {{
            background-color: {FINANCE_COLORS["accent"]};
            box-shadow: 0 0 0 2px {FINANCE_COLORS["accent"]};
        }}
        
        .agent-step.completed {{
            border-left-color: {FINANCE_COLORS["accent"]};
        }}
        
        .agent-name {{
            font-size: 0.8125rem;
            font-weight: 700;
            color: {FINANCE_COLORS["secondary"]};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }}
        
        .agent-step-name {{
            font-size: 0.875rem;
            font-weight: 600;
            color: {FINANCE_COLORS["text_primary"]};
            margin-bottom: 0.25rem;
        }}
        
        .agent-thought {{
            font-size: 0.8125rem;
            color: {FINANCE_COLORS["text_secondary"]};
            line-height: 1.5;
        }}
        
        /* Tax Flags */
        .tax-flag {{
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            border-left: 4px solid;
            background-color: {FINANCE_COLORS["surface"]};
        }}
        
        .tax-flag.warning {{
            border-left-color: {FINANCE_COLORS["warning"]};
            background-color: #FFFBEB;
        }}
        
        .tax-flag.info {{
            border-left-color: {FINANCE_COLORS["secondary"]};
            background-color: #EFF6FF;
        }}
        
        .tax-flag.critical {{
            border-left-color: {FINANCE_COLORS["danger"]};
            background-color: #FEF2F2;
        }}
        
        .tax-flag-header {{
            font-size: 0.8125rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .tax-flag-section {{
            color: {FINANCE_COLORS["text_primary"]};
        }}
        
        .tax-flag-severity {{
            font-size: 0.6875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.125rem 0.5rem;
            border-radius: 4px;
            font-weight: 700;
        }}
        
        .tax-flag-severity.warning {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        
        .tax-flag-severity.info {{
            background-color: #DBEAFE;
            color: #1E40AF;
        }}
        
        .tax-flag-severity.critical {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
        
        .tax-flag-message {{
            font-size: 0.8125rem;
            color: {FINANCE_COLORS["text_secondary"]};
            margin-bottom: 0.25rem;
        }}
        
        .tax-flag-savings {{
            font-size: 0.75rem;
            font-weight: 600;
            color: {FINANCE_COLORS["accent"]};
        }}
        
        /* Recommendations */
        .recommendation-card {{
            padding: 1.25rem;
            border-radius: 10px;
            margin-bottom: 0.75rem;
            border: 1px solid {FINANCE_COLORS["border"]};
            background-color: {FINANCE_COLORS["surface"]};
            transition: box-shadow 0.2s ease;
        }}
        
        .recommendation-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        
        .recommendation-card.high {{
            border-left: 4px solid {FINANCE_COLORS["danger"]};
        }}
        
        .recommendation-card.medium {{
            border-left: 4px solid {FINANCE_COLORS["warning"]};
        }}
        
        .recommendation-card.low {{
            border-left: 4px solid {FINANCE_COLORS["accent"]};
        }}
        
        .rec-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }}
        
        .rec-title {{
            font-size: 0.9375rem;
            font-weight: 700;
            color: {FINANCE_COLORS["text_primary"]};
        }}
        
        .rec-priority {{
            font-size: 0.6875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.25rem 0.625rem;
            border-radius: 4px;
            font-weight: 700;
        }}
        
        .rec-priority.high {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
        
        .rec-priority.medium {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        
        .rec-priority.low {{
            background-color: #D1FAE5;
            color: #065F46;
        }}
        
        .rec-category {{
            font-size: 0.75rem;
            font-weight: 600;
            color: {FINANCE_COLORS["text_muted"]};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .rec-description {{
            font-size: 0.8125rem;
            color: {FINANCE_COLORS["text_secondary"]};
            line-height: 1.6;
            margin-bottom: 0.75rem;
        }}
        
        .rec-actions {{
            font-size: 0.8125rem;
            color: {FINANCE_COLORS["text_primary"]};
        }}
        
        .rec-actions ul {{
            margin: 0.25rem 0 0 0;
            padding-left: 1.25rem;
        }}
        
        .rec-actions li {{
            margin-bottom: 0.25rem;
            color: {FINANCE_COLORS["text_secondary"]};
        }}
        
        /* Executive Summary */
        .exec-summary {{
            background: linear-gradient(135deg, {FINANCE_COLORS["surface"]} 0%, {FINANCE_COLORS["surface_alt"]} 100%);
            border: 1px solid {FINANCE_COLORS["border"]};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .exec-summary h3 {{
            font-size: 1rem;
            font-weight: 700;
            color: {FINANCE_COLORS["primary"]};
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {FINANCE_COLORS["border"]};
        }}
        
        .exec-summary p {{
            font-size: 0.875rem;
            color: {FINANCE_COLORS["text_secondary"]};
            line-height: 1.7;
            margin-bottom: 0.75rem;
        }}
        
        /* Progress bars */
        .progress-container {{
            background-color: {FINANCE_COLORS["surface_alt"]};
            border-radius: 6px;
            height: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        
        .progress-bar {{
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s ease;
        }}
        
        /* Holdings table styling */
        .holdings-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .holdings-table th {{
            text-align: left;
            padding: 0.75rem;
            font-size: 0.6875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {FINANCE_COLORS["text_muted"]};
            border-bottom: 2px solid {FINANCE_COLORS["border"]};
        }}
        
        .holdings-table td {{
            padding: 0.75rem;
            font-size: 0.8125rem;
            border-bottom: 1px solid {FINANCE_COLORS["border"]};
        }}
        
        .holdings-table tr:hover td {{
            background-color: {FINANCE_COLORS["surface_alt"]};
        }}
        
        /* Status badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.625rem;
            border-radius: 4px;
            font-size: 0.6875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .badge-success {{
            background-color: #D1FAE5;
            color: #065F46;
        }}
        
        .badge-warning {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        
        .badge-info {{
            background-color: #DBEAFE;
            color: #1E40AF;
        }}
        
        /* Client profile sidebar */
        .client-profile {{
            padding: 1rem;
            background-color: {FINANCE_COLORS["surface_alt"]};
            border-radius: 10px;
            margin-top: 1rem;
        }}
        
        .client-profile-item {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid {FINANCE_COLORS["border"]};
            font-size: 0.8125rem;
        }}
        
        .client-profile-item:last-child {{
            border-bottom: none;
        }}
        
        .client-profile-label {{
            color: {FINANCE_COLORS["text_muted"]};
            font-weight: 500;
        }}
        
        .client-profile-value {{
            color: {FINANCE_COLORS["text_primary"]};
            font-weight: 600;
        }}
        
        /* Button styling override */
        .stButton > button {{
            background: linear-gradient(135deg, {FINANCE_COLORS["primary"]} 0%, {FINANCE_COLORS["secondary"]} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.9375rem;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Divider */
        .section-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, {FINANCE_COLORS["border"]} 50%, transparent 100%);
            margin: 1.5rem 0;
        }}
        
        /* Empty state */
        .empty-state {{
            text-align: center;
            padding: 3rem 2rem;
            color: {FINANCE_COLORS["text_muted"]};
        }}
        
        .empty-state-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: {FINANCE_COLORS["text_primary"]} !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: {FINANCE_COLORS["text_muted"]} !important;
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: 0.8125rem !important;
            font-weight: 600 !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# =============================================================================
# DATABASE FUNCTIONS
# =============================================================================
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


# =============================================================================
# UI COMPONENTS
# =============================================================================
def render_header():
    """Render the professional app header."""
    st.markdown("""
    <div class="app-header">
        <h1>LaraCorp Wealth AI</h1>
        <p>Intelligent Portfolio & Tax Advisory System</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(clients):
    """Render the sidebar with client selection and profile."""
    st.sidebar.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <h2 style="font-size: 1.125rem; font-weight: 700; color: #0F172A; margin: 0;">
            Client Portal
        </h2>
        <p style="font-size: 0.75rem; color: #94A3B8; margin: 0.25rem 0 0 0;">
            Select a client to analyze
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    client_names = {
        c["client_id"]: f"{c['name']} — {c['occupation']}"
        for c in clients
    }
    
    selected_client_id = st.sidebar.selectbox(
        "Select Client",
        options=list(client_names.keys()),
        format_func=lambda x: client_names[x],
        label_visibility="collapsed"
    )
    
    selected_client = next(c for c in clients if c["client_id"] == selected_client_id)
    
    # Client profile card
    st.sidebar.markdown(f"""
    <div class="client-profile">
        <div style="font-size: 1rem; font-weight: 700; color: #1E3A5F; margin-bottom: 0.75rem;">
            {selected_client['name']}
        </div>
        <div class="client-profile-item">
            <span class="client-profile-label">Age</span>
            <span class="client-profile-value">{selected_client['age']} years</span>
        </div>
        <div class="client-profile-item">
            <span class="client-profile-label">Occupation</span>
            <span class="client-profile-value">{selected_client['occupation']}</span>
        </div>
        <div class="client-profile-item">
            <span class="client-profile-label">Annual Income</span>
            <span class="client-profile-value">&#8377;{selected_client['annual_income_lakhs']:,.1f}L</span>
        </div>
        <div class="client-profile-item">
            <span class="client-profile-label">Tax Regime</span>
            <span class="client-profile-value">{selected_client['tax_regime'].upper()}</span>
        </div>
        <div class="client-profile-item">
            <span class="client-profile-label">City</span>
            <span class="client-profile-value">{selected_client['city']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return selected_client_id


def render_kpi_cards(asset_summary, tax_analysis):
    """Render KPI metric cards at the top of the dashboard."""
    total_value = asset_summary.get("total_value", 0)
    total_invested = asset_summary.get("total_invested", 0)
    total_pnl = asset_summary.get("total_unrealized_pnl", 0)
    
    tax_savings = sum(
        f.get("potential_savings", 0)
        for f in tax_analysis.get("flags", [])
    )
    
    pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    pnl_class = "positive" if total_pnl >= 0 else "negative"
    pnl_sign = "+" if total_pnl >= 0 else ""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Portfolio Value</div>
            <div class="kpi-value">&#8377;{total_value:,.0f}</div>
            <div class="kpi-delta {pnl_class}">{pnl_sign}{pnl_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Invested</div>
            <div class="kpi-value">&#8377;{total_invested:,.0f}</div>
            <div class="kpi-delta" style="color: #94A3B8;">Cost basis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pnl_display = f"&#8377;{abs(total_pnl):,.0f}"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Unrealized P&L</div>
            <div class="kpi-value" style="color: {'#059669' if total_pnl >= 0 else '#DC2626'};">
                {pnl_sign}{pnl_display}
            </div>
            <div class="kpi-delta {pnl_class}">{pnl_sign}{pnl_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Tax Savings Potential</div>
            <div class="kpi-value" style="color: #059669;">&#8377;{tax_savings:,.0f}</div>
            <div class="kpi-delta positive">Annual opportunity</div>
        </div>
        """, unsafe_allow_html=True)


def render_agent_timeline(thoughts):
    """Render agent execution as a professional timeline."""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            Agent Execution Timeline
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="agent-timeline">', unsafe_allow_html=True)
    
    for i, thought in enumerate(thoughts):
        agent_name = thought["agent"]
        step = thought["step"]
        content = thought["thought"]
        
        # Map agent names to cleaner display names
        agent_display = {
            "DataRetrievalAgent": "Data Retrieval",
            "TaxAgent": "Tax Analysis",
            "AdvisoryAgent": "Advisory Report",
        }.get(agent_name, agent_name)
        
        is_completed = i < len(thoughts) - 1 or step in ["summary", "flags", "recommendations", "llm"]
        completed_class = "completed" if is_completed else ""
        
        st.markdown(f"""
        <div class="agent-step {completed_class}">
            <div class="agent-name">{agent_display}</div>
            <div class="agent-step-name">{step.replace('_', ' ').title()}</div>
            <div class="agent-thought">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_portfolio_section(asset_summary, portfolio):
    """Render portfolio breakdown with charts and holdings table."""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            Portfolio Analysis
        </div>
    """, unsafe_allow_html=True)
    
    breakdown = asset_summary.get("breakdown", [])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Asset allocation pie chart
        if breakdown:
            df_breakdown = pd.DataFrame(breakdown)
            df_breakdown = df_breakdown.sort_values("value", ascending=False)
            
            fig = px.pie(
                df_breakdown,
                values="value",
                names="asset_type",
                title="Asset Allocation",
                color_discrete_sequence=[
                    "#1E3A5F", "#2563EB", "#059669", "#D97706",
                    "#7C3AED", "#DC2626", "#0891B2", "#65A30D"
                ],
                hole=0.55,
            )
            fig.update_layout(
                font=dict(family="Inter, sans-serif", size=12),
                title_font=dict(size=14, color="#0F172A"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11)
                ),
                margin=dict(t=40, b=60, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate="%{label}<br>₹%{value:,.0f}<br>%{percent}<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with col2:
        # Asset class summary cards
        if breakdown:
            for item in sorted(breakdown, key=lambda x: x["value"], reverse=True):
                asset_type = item["asset_type"].replace("_", " ").title()
                value = item["value"]
                pnl = item.get("pnl", 0)
                pnl_pct = (pnl / value * 100) if value > 0 else 0
                pnl_color = "#059669" if pnl >= 0 else "#DC2626"
                pnl_sign = "+" if pnl >= 0 else ""
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 0.625rem 0; border-bottom: 1px solid #E2E8F0;">
                    <div>
                        <div style="font-size: 0.8125rem; font-weight: 600; color: #0F172A;">
                            {asset_type}
                        </div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">
                            {pnl_sign}{pnl_pct:.1f}%
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.875rem; font-weight: 700; color: #0F172A;">
                            &#8377;{value:,.0f}
                        </div>
                        <div style="font-size: 0.75rem; color: {pnl_color}; font-weight: 600;">
                            {pnl_sign}&#8377;{abs(pnl):,.0f}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Holdings table
    if portfolio:
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.875rem; font-weight: 700; color: #0F172A; margin-bottom: 0.75rem;'>Holdings Detail</div>", unsafe_allow_html=True)
        
        holdings_df = pd.DataFrame(portfolio)
        holdings_df["asset_type"] = holdings_df["asset_type"].str.replace("_", " ").str.title()
        holdings_df["pnl_pct"] = (holdings_df["unrealized_pnl"] / holdings_df["invested_amount"] * 100).round(1)
        
        # Format for display
        display_df = holdings_df[[
            "asset_type", "instrument_name", "units", "avg_buy_price",
            "current_price", "current_value", "unrealized_pnl", "pnl_pct"
        ]].copy()
        
        display_df.columns = [
            "Asset Type", "Instrument", "Units", "Buy Price",
            "Current", "Value", "P&L", "P&L %"
        ]
        
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
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_tax_section(tax_analysis):
    """Render tax analysis with progress bars and flags."""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            Tax Analysis (FY 2025-26)
        </div>
    """, unsafe_allow_html=True)
    
    # Tax metrics
    sec_80c_used = tax_analysis.get("sec_80c_used", 0)
    sec_80c_limit = 150000
    sec_80c_pct = min(100, (sec_80c_used / sec_80c_limit * 100)) if sec_80c_limit > 0 else 0
    
    nps_used = tax_analysis.get("nps_used", 0)
    nps_limit = 50000
    nps_pct = min(100, (nps_used / nps_limit * 100)) if nps_limit > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Section 80C Used",
            f"₹{sec_80c_used:,.0f}",
            f"₹{sec_80c_limit - sec_80c_used:,.0f} remaining"
        )
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {sec_80c_pct}%; background: linear-gradient(90deg, #059669, #10B981);"></div>
        </div>
        <div style="font-size: 0.6875rem; color: #94A3B8; margin-top: 0.25rem; text-align: right;">
            {sec_80c_pct:.0f}% utilized
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "80CCD(1B) NPS",
            f"₹{nps_used:,.0f}",
            f"₹{nps_limit - nps_used:,.0f} remaining"
        )
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {nps_pct}%; background: linear-gradient(90deg, #2563EB, #3B82F6);"></div>
        </div>
        <div style="font-size: 0.6875rem; color: #94A3B8; margin-top: 0.25rem; text-align: right;">
            {nps_pct:.0f}% utilized
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        taxable_ltcg = tax_analysis.get("taxable_ltcg", 0)
        ltcg_tax = tax_analysis.get("ltcg_tax", 0)
        st.metric(
            "Taxable LTCG",
            f"₹{taxable_ltcg:,.0f}",
            f"Tax: ₹{ltcg_tax:,.0f}" if ltcg_tax > 0 else "Within exemption"
        )
    
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Tax flags
    flags = tax_analysis.get("flags", [])
    if flags:
        st.markdown("<div style='font-size: 0.875rem; font-weight: 700; color: #0F172A; margin-bottom: 0.75rem;'>Tax Flags & Opportunities</div>", unsafe_allow_html=True)
        
        for flag in flags:
            severity = flag["severity"]
            section = flag["section"]
            message = flag["message"]
            savings = flag.get("potential_savings", 0)
            
            st.markdown(f"""
            <div class="tax-flag {severity}">
                <div class="tax-flag-header">
                    <span class="tax-flag-section">{section}</span>
                    <span class="tax-flag-severity {severity}">{severity}</span>
                </div>
                <div class="tax-flag-message">{message}</div>
                <div class="tax-flag-savings">Potential Savings: &#8377;{savings:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # LLM Insights
    if tax_analysis.get("llm_insights"):
        with st.expander("🤖 AI Tax Insights"):
            st.markdown(tax_analysis["llm_insights"])
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_report_section(report):
    """Render advisory report with executive summary and recommendations."""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            Advisory Report
        </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary
    if report.get("executive_summary"):
        st.subheader("📋 Executive Summary")
        st.markdown(report["executive_summary"])
        st.divider()
    
    # Recommendations
    recommendations = report.get("recommendations", [])
    if recommendations:
        st.subheader("🎯 Recommendations")
        
        for rec in recommendations:
            priority = rec["priority"]
            category = rec["category"]
            title = rec["title"]
            description = rec["description"]
            actions = rec.get("action_items", [])
            
            # Priority emoji
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
            
            with st.container():
                st.markdown(f"**{priority_emoji} {title}** ({category.upper()})")
                st.markdown(description)
                
                if actions:
                    st.markdown("**Action Items:**")
                    for action in actions:
                        st.markdown(f"- {action}")
                
                st.divider()
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_empty_state():
    """Render the initial empty state before analysis."""
    st.markdown("""
    <div class="section-card">
        <div class="empty-state">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;">&#9670;</div>
            <div style="font-size: 1.125rem; font-weight: 600; color: #0F172A; margin-bottom: 0.5rem;">
                Ready to Analyze
            </div>
            <div style="font-size: 0.875rem; color: #94A3B8; max-width: 400px; margin: 0 auto;">
                Select a client from the sidebar and click "Generate Wealth Report" 
                to run the multi-agent analysis pipeline.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


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
    
    # Sidebar toggle button in main content (in case sidebar is closed)
    sidebar_col1, sidebar_col2 = st.columns([1, 4])
    with sidebar_col1:
        if st.button("☰ Client Menu", type="secondary", use_container_width=True):
            # This will open the sidebar
            st.session_state.sidebar_open = True
            st.rerun()
    
    # Sidebar
    clients = get_clients()
    selected_client_id = render_sidebar(clients)
    
    # Main action button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button(
            "Generate Wealth Report",
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
        
        # Advisory Report
        report = result.get("report", {})
        if report:
            render_report_section(report)
        
        # Footer timestamp
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0; color: #94A3B8; font-size: 0.75rem;">
            Report generated on {datetime.now().strftime("%B %d, %Y at %H:%M")} 
            | LaraCorp Wealth AI v1.0
        </div>
        """, unsafe_allow_html=True)
    
    else:
        render_empty_state()


if __name__ == "__main__":
    main()
