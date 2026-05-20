"""
Streamlit UI - Wealth Management & Tax Advisory Demo
Design system: UI/UX Pro Max — Fintech Dark, professional finance dashboard
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import run_wealth_analysis, run_wealth_analysis_streaming
from database.seed_data import create_database, get_connection
from agents.llm_client import set_global_cache, get_global_cache
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Wealth AI",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DESIGN SYSTEM (UI/UX Pro Max — Fintech Dark)
# Colors: deep navy bg, slate cards, electric blue primary, emerald gains, red losses
# Typography: weight hierarchy — 700 headings, 600 labels, 400 body; tabular nums for data
# Spacing: 8dp rhythm; 12px border-radius cards, 16px elevated cards
# =============================================================================
_C = {
    "bg": "#0A0F1E",
    "card": "#111827",
    "elevated": "#1F2937",
    "border": "#1F2937",
    "border_subtle": "#374151",
    "primary": "#3B82F6",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "text": "#F9FAFB",
    "text_sec": "#9CA3AF",
    "text_muted": "#6B7280",
    "chart": ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444", "#06B6D4", "#EC4899"],
}


def inject_design_system():
    st.markdown(f"""
    <style>
        #MainMenu, footer, header {{visibility: hidden;}}
        /* Hide the sidebar collapse button so the nav stays permanently open */
        [data-testid="stSidebarCollapseButton"] {{display: none !important;}}
        [data-testid="collapsedControl"] {{display: none !important;}}

        .stApp {{ background-color: {_C['bg']} !important; }}

        [data-testid="stSidebar"] {{
            background-color: {_C['card']} !important;
            border-right: 1px solid {_C['border_subtle']} !important;
        }}

        /* Metric cards */
        [data-testid="metric-container"] {{
            background: {_C['card']} !important;
            border: 1px solid {_C['border_subtle']} !important;
            border-radius: 12px !important;
            padding: 20px 24px !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 26px !important;
            font-weight: 700 !important;
            font-variant-numeric: tabular-nums !important;
            color: {_C['text']} !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.7px !important;
            color: {_C['text_muted']} !important;
        }}
        [data-testid="stMetricDelta"] {{ font-size: 13px !important; font-weight: 500 !important; }}

        /* Primary button */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.2px !important;
            padding: 12px 32px !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(59,130,246,0.25) !important;
            transition: box-shadow 0.2s ease, transform 0.15s ease !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 6px 20px rgba(59,130,246,0.45) !important;
            transform: translateY(-1px) !important;
        }}

        /* Dataframe */
        [data-testid="stDataFrame"] {{
            border: 1px solid {_C['border_subtle']} !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background: transparent !important;
            border-bottom: 1px solid {_C['border_subtle']} !important;
            gap: 4px !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            color: {_C['text_muted']} !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            padding: 10px 20px !important;
            border: none !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: {_C['primary']} !important;
            font-weight: 600 !important;
            border-bottom: 2px solid {_C['primary']} !important;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background: {_C['elevated']} !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            font-size: 13px !important;
        }}

        /* Progress bars */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, {_C['primary']}, {_C['success']}) !important;
            border-radius: 4px !important;
        }}
        .stProgress > div > div {{
            background: {_C['border_subtle']} !important;
            border-radius: 4px !important;
        }}

        /* Download button — matches primary button theme */
        [data-testid="stDownloadButton"] > button {{
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            letter-spacing: 0.3px !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(59,130,246,0.25) !important;
            transition: box-shadow 0.2s ease, transform 0.15s ease !important;
            width: 100% !important;
            padding: 10px 20px !important;
        }}
        [data-testid="stDownloadButton"] > button:hover {{
            box-shadow: 0 6px 20px rgba(59,130,246,0.45) !important;
            transform: translateY(-1px) !important;
        }}
        [data-testid="stDownloadButton"] > button:active {{
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
        }}

        /* Alert variants */
        [data-testid="stAlert"][data-baseweb="notification"] {{
            border-radius: 8px !important;
        }}

        /* Divider */
        hr {{ border-color: {_C['border_subtle']} !important; opacity: 0.6 !important; }}

        /* Severity badges */
        .badge-critical {{
            display:inline-block; background:rgba(239,68,68,0.15); color:#FCA5A5;
            border:1px solid rgba(239,68,68,0.3); border-radius:4px;
            padding:2px 8px; font-size:11px; font-weight:600;
            text-transform:uppercase; letter-spacing:0.5px;
        }}
        .badge-warning {{
            display:inline-block; background:rgba(245,158,11,0.15); color:#FCD34D;
            border:1px solid rgba(245,158,11,0.3); border-radius:4px;
            padding:2px 8px; font-size:11px; font-weight:600;
            text-transform:uppercase; letter-spacing:0.5px;
        }}
        .badge-info {{
            display:inline-block; background:rgba(59,130,246,0.15); color:#93C5FD;
            border:1px solid rgba(59,130,246,0.3); border-radius:4px;
            padding:2px 8px; font-size:11px; font-weight:600;
            text-transform:uppercase; letter-spacing:0.5px;
        }}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# DATABASE
# =============================================================================
def init_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "wealth_demo.db")
    if not os.path.exists(db_path):
        create_database()


def get_clients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT client_id, name, occupation, annual_income_lakhs FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return clients


# =============================================================================
# CHART HELPERS
# =============================================================================
_CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=_C["text_sec"], size=12),
    margin=dict(t=44, b=16, l=0, r=0),
)


def _donut_chart(breakdown):
    labels = [b["asset_type"].replace("_", " ").title() for b in breakdown]
    values = [b["value"] for b in breakdown]
    total = sum(values)

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=_C["chart"][:len(labels)], line=dict(color=_C["bg"], width=2)),
        textinfo="percent",
        textfont=dict(size=11, color="white"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(
        **_CHART_BASE,
        title=dict(text="Asset Allocation", font=dict(size=14, color=_C["text"]), x=0.5, xanchor="center"),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05,
                    font=dict(size=11, color=_C["text_sec"])),
        annotations=[dict(
            text=f"₹{total/1e5:.1f}L<br><span style='font-size:10px;color:{_C['text_sec']}'>Portfolio</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=15, color=_C["text"]),
        )],
        height=320,
    )
    return fig


def _pnl_bar_chart(breakdown):
    items = sorted(breakdown, key=lambda x: x.get("pnl", 0), reverse=True)
    labels = [b["asset_type"].replace("_", " ").title() for b in items]
    pnls = [b.get("pnl", 0) for b in items]
    bar_colors = [_C["success"] if p >= 0 else _C["danger"] for p in pnls]

    fig = go.Figure(go.Bar(
        x=labels, y=pnls,
        marker=dict(color=bar_colors, line=dict(width=0), opacity=0.9),
        text=[f"₹{p:,.0f}" for p in pnls],
        textposition="outside",
        textfont=dict(size=10, color=_C["text_sec"]),
        hovertemplate="<b>%{x}</b><br>P&L: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **_CHART_BASE,
        title=dict(text="P&L by Asset Class", font=dict(size=14, color=_C["text"]), x=0.5, xanchor="center"),
        yaxis=dict(showgrid=True, gridcolor=_C["border"], zeroline=True,
                   zerolinecolor=_C["border_subtle"], tickformat="₹,.0f",
                   tickfont=dict(color=_C["text_muted"])),
        xaxis=dict(showgrid=False, tickfont=dict(color=_C["text_sec"])),
        showlegend=False, height=320,
    )
    return fig


# =============================================================================
# UI SECTIONS
# =============================================================================
def render_header():
    # ── Download Architecture PPTX (top-right) ──
    pptx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workspace", "wealth-ai-memory-architecture.pptx")
    pptx_bytes = None
    if os.path.exists(pptx_path):
        with open(pptx_path, "rb") as f:
            pptx_bytes = f.read()

    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.markdown(f"""
        <div style="padding:8px 0 20px 0; display:flex; align-items:center; gap:14px;">
            <div style="background:linear-gradient(135deg,#3B82F6,#2563EB); width:40px; height:40px;
                        border-radius:10px; display:flex; align-items:center; justify-content:center;
                        font-size:20px; font-weight:800; color:white; flex-shrink:0;">W</div>
            <div>
                <div style="font-size:22px; font-weight:700; color:{_C['text']}; letter-spacing:-0.3px; line-height:1.2;">Wealth AI</div>
                <div style="font-size:12px; color:{_C['text_muted']}; margin-top:2px;">Multi-Agent Wealth Management & Tax Advisory</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:right; padding-top:12px;">
            <div style="font-size:11px; color:{_C['text_muted']};">Income Tax Act 2025</div>
            <div style="font-size:12px; color:{_C['text_sec']}; font-weight:500;">FY 2025-26</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if pptx_bytes:
            st.download_button(
                label="Download Architecture Deck",
                data=pptx_bytes,
                file_name="wealth-ai-memory-architecture.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
                key="header_pptx_download",
            )
    st.markdown(f'<hr style="border:none; border-top:1px solid {_C["border_subtle"]}; margin:0 0 24px 0;">', unsafe_allow_html=True)


def render_sidebar(clients):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:20px 0 12px 0;">
            <div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:{_C['text_muted']};">
                Client Selection
            </div>
        </div>
        """, unsafe_allow_html=True)

        client_map = {c[1]: c[0] for c in clients}
        selected_name = st.radio("Client", options=list(client_map.keys()), label_visibility="collapsed")

        selected_id = client_map[selected_name]
        client = next(c for c in clients if c[0] == selected_id)

        st.markdown(f'<hr style="border:none; border-top:1px solid {_C["border_subtle"]}; margin:16px 0;">', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:{_C['elevated']}; border:1px solid {_C['border_subtle']}; border-radius:12px; padding:16px;">
            <div style="font-size:15px; font-weight:600; color:{_C['text']}; margin-bottom:4px;">{client[1]}</div>
            <div style="font-size:12px; color:{_C['text_sec']}; margin-bottom:14px;">{client[2]}</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:11px; color:{_C['text_muted']}; text-transform:uppercase; letter-spacing:0.5px;">Annual Income</div>
                <div style="font-size:14px; font-weight:700; color:{_C['success']}; font-variant-numeric:tabular-nums;">₹{client[3]}L</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        return selected_id


def render_kpi_cards(asset_summary, tax_analysis):
    total_value = asset_summary.get("total_value", 0)
    total_invested = asset_summary.get("total_invested", 0)
    total_pnl = asset_summary.get("total_unrealized_pnl", 0)
    tax_savings = sum(f.get("potential_savings", 0) for f in tax_analysis.get("flags", []))
    pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Portfolio Value", f"₹{total_value:,.0f}", f"+{pnl_pct:.1f}%")
    with c2:
        st.metric("Total Invested", f"₹{total_invested:,.0f}")
    with c3:
        delta_color = "normal" if total_pnl >= 0 else "inverse"
        sign = "+" if total_pnl >= 0 else ""
        st.metric("Unrealized P&L", f"₹{total_pnl:,.0f}", f"{sign}{pnl_pct:.1f}%", delta_color=delta_color)
    with c4:
        st.metric("Tax Savings Potential", f"₹{tax_savings:,.0f}", "Opportunity")


def render_agent_timeline(thoughts):
    agent_display = {
        "DataRetrievalAgent": "Data Retrieval",
        "TaxAgent": "Tax Analysis",
        "AdvisoryAgent": "Advisory Report",
    }
    with st.expander("Agent Execution Timeline", expanded=False):
        for i, thought in enumerate(thoughts):
            border = f"border-bottom:1px solid {_C['border']};" if i < len(thoughts) - 1 else ""
            display = agent_display.get(thought["agent"], thought["agent"])
            st.markdown(f"""
            <div style="display:flex; gap:14px; padding:10px 0; {border}">
                <div style="width:7px; min-width:7px; height:7px; border-radius:50%;
                            background:{_C['primary']}; margin-top:7px;"></div>
                <div>
                    <div style="font-size:13px; font-weight:600; color:{_C['text']};">
                        {display}
                        <span style="font-weight:400; color:{_C['text_muted']}; font-size:12px;"> — {thought['step']}</span>
                    </div>
                    <div style="font-size:12px; color:{_C['text_sec']}; margin-top:3px; line-height:1.5;">{thought['thought']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_portfolio_tab(asset_summary, portfolio):
    breakdown = asset_summary.get("breakdown", [])

    col1, col2 = st.columns(2)
    with col1:
        if breakdown:
            st.plotly_chart(_donut_chart(breakdown), use_container_width=True, config={"displayModeBar": False})
    with col2:
        if breakdown:
            st.plotly_chart(_pnl_bar_chart(breakdown), use_container_width=True, config={"displayModeBar": False})

    if portfolio:
        st.markdown(f'<div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]}; margin:24px 0 12px 0;">Holdings Detail</div>', unsafe_allow_html=True)

        df = pd.DataFrame(portfolio)
        df["asset_type"] = df["asset_type"].str.replace("_", " ").str.title()
        df["pnl_pct"] = (df["unrealized_pnl"] / df["invested_amount"] * 100).round(1)
        display_df = df[["asset_type", "instrument_name", "units", "avg_buy_price",
                          "current_price", "current_value", "unrealized_pnl", "pnl_pct"]].copy()
        display_df.columns = ["Asset Type", "Instrument", "Units", "Buy Price", "Current", "Value", "P&L", "P&L %"]

        st.dataframe(
            display_df, use_container_width=True, hide_index=True,
            column_config={
                "Buy Price": st.column_config.NumberColumn(format="₹%.2f"),
                "Current": st.column_config.NumberColumn(format="₹%.2f"),
                "Value": st.column_config.NumberColumn(format="₹%,.0f"),
                "P&L": st.column_config.NumberColumn(format="₹%,.0f"),
                "P&L %": st.column_config.NumberColumn(format="%.1f%%"),
            },
        )


def render_tax_tab(tax_analysis):
    c1, c2, c3 = st.columns(3)

    with c1:
        used = tax_analysis.get("sec_80c_used", 0)
        limit = 150000
        st.metric("Section 80C Used", f"₹{used:,.0f}", f"₹{max(0, limit - used):,.0f} remaining")
        st.progress(min(1.0, used / limit))

    with c2:
        used = tax_analysis.get("nps_used", 0)
        limit = 50000
        st.metric("80CCD(1B) NPS", f"₹{used:,.0f}", f"₹{max(0, limit - used):,.0f} remaining")
        st.progress(min(1.0, used / limit))

    with c3:
        ltcg = tax_analysis.get("taxable_ltcg", 0)
        ltcg_tax = tax_analysis.get("ltcg_tax", 0)
        delta = f"Tax: ₹{ltcg_tax:,.0f}" if ltcg_tax > 0 else "Within exemption"
        st.metric("Taxable LTCG", f"₹{ltcg:,.0f}", delta)

    flags = tax_analysis.get("flags", [])
    if flags:
        st.markdown(f'<div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]}; margin:28px 0 12px 0;">Tax Flags & Opportunities</div>', unsafe_allow_html=True)

        badge_map = {
            "critical": '<span class="badge-critical">Critical</span>',
            "warning": '<span class="badge-warning">Warning</span>',
            "info": '<span class="badge-info">Info</span>',
        }

        for flag in flags:
            badge = badge_map.get(flag["severity"], "")
            savings_html = f'<div style="font-size:13px; font-weight:700; color:{_C["success"]}; white-space:nowrap;">Save ₹{flag["potential_savings"]:,.0f}</div>' if flag.get("potential_savings", 0) > 0 else ""
            st.markdown(f"""
            <div style="background:{_C['elevated']}; border:1px solid {_C['border_subtle']};
                        border-radius:10px; padding:14px 16px; margin-bottom:8px;
                        display:flex; align-items:center; justify-content:space-between; gap:16px;">
                <div style="flex:1;">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        {badge}
                        <span style="font-size:13px; font-weight:600; color:{_C['text']};">{flag['section']}</span>
                    </div>
                    <div style="font-size:13px; color:{_C['text_sec']}; line-height:1.5;">{flag['message']}</div>
                </div>
                {savings_html}
            </div>
            """, unsafe_allow_html=True)

    with st.expander("AI Tax Insights"):
        if tax_analysis.get("llm_insights"):
            st.markdown(tax_analysis["llm_insights"])
        else:
            st.info("AI insights not available for this client.")


def render_report_tab(report):
    if report.get("executive_summary"):
        st.markdown(f'<div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]}; margin-bottom:12px;">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{_C['elevated']}; border:1px solid {_C['border_subtle']};
                    border-left:3px solid {_C['primary']}; border-radius:12px;
                    padding:20px 24px; margin-bottom:28px; line-height:1.75;
                    font-size:14px; color:#D1D5DB;">
            {report['executive_summary']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Executive summary not available.")

    recs = report.get("recommendations", [])
    if recs:
        st.markdown(f'<div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]}; margin-bottom:12px;">Recommendations</div>', unsafe_allow_html=True)

        _border = {"high": _C["danger"], "medium": _C["warning"], "low": _C["success"]}
        _badge_bg = {"high": "rgba(239,68,68,0.15)", "medium": "rgba(245,158,11,0.15)", "low": "rgba(16,185,129,0.15)"}
        _badge_fg = {"high": "#FCA5A5", "medium": "#FCD34D", "low": "#6EE7B7"}

        for rec in recs:
            p = rec["priority"]
            border = _border.get(p, _C["primary"])
            bg = _badge_bg.get(p, "rgba(59,130,246,0.15)")
            fg = _badge_fg.get(p, "#93C5FD")

            actions_html = ""
            if rec.get("action_items"):
                items = "".join([f'<li style="color:{_C["text_sec"]}; font-size:13px; margin-bottom:4px;">{a}</li>' for a in rec["action_items"]])
                actions_html = f'<ul style="margin:10px 0 0 0; padding-left:18px;">{items}</ul>'

            st.markdown(f"""
            <div style="background:{_C['elevated']}; border:1px solid {_C['border_subtle']};
                        border-left:3px solid {border}; border-radius:12px;
                        padding:18px 20px; margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px; flex-wrap:wrap;">
                    <span style="background:{bg}; color:{fg}; border-radius:4px; padding:2px 8px;
                                 font-size:11px; font-weight:600; letter-spacing:0.5px; text-transform:uppercase;">{p}</span>
                    <span style="font-size:14px; font-weight:600; color:{_C['text']};">{rec['title']}</span>
                    <span style="font-size:11px; color:{_C['text_muted']}; text-transform:uppercase; letter-spacing:0.5px;">{rec['category']}</span>
                </div>
                <div style="font-size:13px; color:#D1D5DB; line-height:1.65;">{rec['description']}</div>
                {actions_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recommendations available.")


def render_empty_state():
    st.markdown(f"""
    <div style="text-align:center; padding:80px 40px;">
        <div style="width:64px; height:64px; margin:0 auto 20px auto;
                    background:linear-gradient(135deg,rgba(59,130,246,0.2),rgba(37,99,235,0.08));
                    border:1px solid rgba(59,130,246,0.25); border-radius:16px;
                    display:flex; align-items:center; justify-content:center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                 fill="none" stroke="{_C['primary']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
        </div>
        <div style="font-size:18px; font-weight:600; color:{_C['text']}; margin-bottom:8px;">Ready to Analyze</div>
        <div style="font-size:14px; color:{_C['text_muted']}; max-width:340px; margin:0 auto; line-height:1.65;">
            Select a client from the sidebar and click <strong style="color:{_C['text_sec']};">Generate Wealth Report</strong>
            to run the multi-agent analysis pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN
# =============================================================================
def main():
    inject_design_system()
    render_header()
    init_db()

    clients = get_clients()
    selected_client_id = render_sidebar(clients)

    # LLM Mode — permanently locked to Fast Mode (Cached) to conserve tokens
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.toggle(
            "Fast Mode (Cached)",
            value=True,
            disabled=True,
            help="Live AI mode is temporarily disabled to conserve API tokens. Using cached responses for instant results."
        )
        set_global_cache(True)
    with col2:
        analyze_clicked = st.button("Generate Wealth Report", type="primary", use_container_width=True)
    with col3:
        st.markdown(f'<div style="text-align:center; padding-top:8px;"><span style="background:rgba(16,185,129,0.15); color:#6EE7B7; border:1px solid rgba(16,185,129,0.3); border-radius:4px; padding:4px 10px; font-size:11px; font-weight:600; letter-spacing:0.4px;">Cached · Instant</span></div>', unsafe_allow_html=True)

    if analyze_clicked:
        # Create containers for real-time progress
        progress_container = st.container()
        with progress_container:
            mode_badge = "Cached · Instant"
            mode_color = _C["success"]
            mode_rgb = "16,185,129"
            st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;"><div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]};">Agent Execution Pipeline</div><div style="background:rgba({mode_rgb},0.15); color:{mode_color}; border:1px solid rgba({mode_rgb},0.3); border-radius:4px; padding:3px 10px; font-size:10px; font-weight:600; letter-spacing:0.4px;">{mode_badge}</div></div>', unsafe_allow_html=True)

            # Progress bar
            progress_bar = st.progress(0)

            # Agent status containers
            agent_status_cols = st.columns(3)
            agent_statuses = {}
            agent_abbr = {
                "Data Retrieval Agent": "DR",
                "Tax Analysis Agent": "TA",
                "Advisory Agent": "AD",
            }
            agent_color = {
                "Data Retrieval Agent": _C["primary"],
                "Tax Analysis Agent": "#8B5CF6",
                "Advisory Agent": "#06B6D4",
            }
            agent_descriptions = {
                "Data Retrieval Agent": "Fetching portfolio data from database",
                "Tax Analysis Agent": "Analyzing tax implications under IT Act 2025",
                "Advisory Agent": "Generating recommendations & executive summary",
            }

            for i, (agent_key, col) in enumerate(zip(["Data Retrieval Agent", "Tax Analysis Agent", "Advisory Agent"], agent_status_cols)):
                with col:
                    abbr = agent_abbr.get(agent_key, "AI")
                    color = agent_color.get(agent_key, _C["primary"])
                    desc = agent_descriptions.get(agent_key, "")
                    agent_statuses[agent_key] = st.empty()
                    agent_statuses[agent_key].markdown(f"""
                    <div style="background:{_C['card']}; border:1px solid {_C['border_subtle']}; border-radius:12px; padding:16px; text-align:center; opacity:0.45;">
                        <div style="width:36px; height:36px; border-radius:8px; background:rgba(55,65,81,0.6); display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto; font-size:12px; font-weight:700; color:{_C['text_muted']}; letter-spacing:0.5px;">{abbr}</div>
                        <div style="font-size:13px; font-weight:600; color:{_C['text_muted']};">{agent_key}</div>
                        <div style="font-size:11px; color:{_C['text_muted']}; margin-top:4px;">Waiting</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Live log container
            log_container = st.empty()
            log_messages = []

        # Run the streaming analysis
        result = None
        stage_map = {"data_retrieval": 0, "tax_analysis": 1, "advisory": 2}
        completed_stages = set()

        for event in run_wealth_analysis_streaming(selected_client_id):
            stage = event["stage"]
            agent = event["agent"]
            status = event["status"]
            message = event["message"]

            if stage == "complete":
                result = event["state"]
                progress_bar.progress(1.0)
                break

            # Update progress
            stage_idx = stage_map.get(stage, 0)
            progress = (stage_idx + 0.5) / 3.0
            progress_bar.progress(min(1.0, progress))

            # Update agent status card
            if agent in agent_statuses:
                abbr = agent_abbr.get(agent, "AI")
                color = agent_color.get(agent, _C["primary"])
                desc = agent_descriptions.get(agent, "")

                if status in ("data_fetched", "tax_analyzed"):
                    completed_stages.add(stage)
                    agent_statuses[agent].markdown(f"""
                    <div style="background:{_C['card']}; border:1px solid {_C['success']}; border-radius:12px; padding:16px; text-align:center;">
                        <div style="width:36px; height:36px; border-radius:8px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto; font-size:16px; font-weight:700; color:{_C['success']};">&#10003;</div>
                        <div style="font-size:13px; font-weight:600; color:{_C['success']};">{agent}</div>
                        <div style="font-size:11px; color:{_C['text_sec']}; margin-top:4px;">Completed</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif stage in completed_stages:
                    pass
                else:
                    agent_statuses[agent].markdown(f"""
                    <div style="background:{_C['card']}; border:1px solid {color}; border-radius:12px; padding:16px; text-align:center; box-shadow:0 0 20px rgba(59,130,246,0.12);">
                        <div style="width:36px; height:36px; border-radius:8px; background:rgba(59,130,246,0.15); display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto; font-size:12px; font-weight:700; color:{color}; letter-spacing:0.5px;">{abbr}</div>
                        <div style="font-size:13px; font-weight:600; color:{color};">{agent}</div>
                        <div style="font-size:11px; color:{_C['text_sec']}; margin-top:4px;">{desc}</div>
                        <div style="font-size:11px; color:{_C['text_muted']}; margin-top:8px;">{message[:80]}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Update live log
            log_messages.append((agent, message))
            if len(log_messages) > 6:
                log_messages = log_messages[-6:]
            rows = "".join([
                f'<div style="display:flex; gap:10px; padding:5px 0; border-bottom:1px solid {_C["border"]};">'
                f'<span style="font-size:11px; font-weight:600; color:{agent_color.get(a, _C["primary"])}; min-width:110px; flex-shrink:0;">{a[:14]}</span>'
                f'<span style="font-size:11px; color:{_C["text_sec"]};">{m}</span>'
                f'</div>'
                for a, m in log_messages
            ])
            log_container.markdown(
                f'<div style="background:{_C["card"]}; border:1px solid {_C["border_subtle"]}; border-radius:8px; padding:12px 14px; margin-top:12px;">'
                f'<div style="font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:{_C["text_muted"]}; margin-bottom:8px;">Live Log</div>'
                f'{rows}</div>',
                unsafe_allow_html=True,
            )

            # Small delay for visual effect
            import time
            time.sleep(0.1)

        # Mark remaining agents as completed
        for agent_key in ["Data Retrieval Agent", "Tax Analysis Agent", "Advisory Agent"]:
            if agent_key in agent_statuses:
                agent_statuses[agent_key].markdown(f"""
                <div style="background:{_C['card']}; border:1px solid {_C['success']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="width:36px; height:36px; border-radius:8px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto; font-size:16px; font-weight:700; color:{_C['success']};">&#10003;</div>
                    <div style="font-size:13px; font-weight:600; color:{_C['success']};">{agent_key}</div>
                    <div style="font-size:11px; color:{_C['text_sec']}; margin-top:4px;">Completed</div>
                </div>
                """, unsafe_allow_html=True)

        # Clear the progress container after completion
        progress_container.empty()

        if result is None:
            st.error("Analysis failed to complete.")
            return

        for error in result.get("errors", []):
            st.error(f"Analysis Error: {error}")

        asset_summary = result.get("asset_summary", {})
        tax_analysis = result.get("tax_analysis", {})

        st.markdown("<br>", unsafe_allow_html=True)
        render_kpi_cards(asset_summary, tax_analysis)

        thoughts = result.get("agent_thoughts", [])
        if thoughts:
            st.markdown("<br>", unsafe_allow_html=True)
            render_agent_timeline(thoughts)

        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Portfolio Analysis", "Tax Analysis", "Advisory Report"])

        with tab1:
            portfolio = result.get("portfolio", [])
            if portfolio:
                render_portfolio_tab(asset_summary, portfolio)
            else:
                st.info("Portfolio data not available.")

        with tab2:
            if tax_analysis:
                render_tax_tab(tax_analysis)
            else:
                st.warning("Tax analysis data not available.")

        with tab3:
            report = result.get("report", {})
            if report:
                render_report_tab(report)
            else:
                st.warning("Advisory report not available.")

        st.markdown(
            f'<div style="text-align:center; font-size:12px; color:{_C["text_muted"]}; '
            f'margin-top:40px; padding-top:20px; border-top:1px solid {_C["border"]};">'
            f'Report generated {datetime.now().strftime("%B %d, %Y at %H:%M")} · Wealth AI v1.0 · Indian Income Tax Act 2025</div>',
            unsafe_allow_html=True,
        )

    else:
        render_empty_state()




if __name__ == "__main__":
    main()
