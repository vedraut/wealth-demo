"""
Data Retrieval Agent - Fetches client portfolio data from SQLite DB.
"""

import sqlite3
from typing import Any
from models.state import WealthManagementState, AgentThought
from datetime import datetime


def data_retrieval_agent(state: WealthManagementState) -> WealthManagementState:
    """
    Fetch client profile and portfolio holdings from database.
    Updates state with client_profile, portfolio, and asset_summary.
    """
    client_id = state["client_id"]
    thoughts = state.get("agent_thoughts", [])

    def add_thought(step: str, thought: str):
        thoughts.append(AgentThought(
            agent="DataRetrievalAgent",
            step=step,
            thought=thought,
            timestamp=datetime.now().isoformat()
        ))

    add_thought("init", f"Starting data retrieval for client_id={client_id}")

    try:
        from database.seed_data import get_connection
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch client profile
        cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Client {client_id} not found")

        client_profile = dict(row)
        add_thought("profile", f"Found client: {client_profile['name']}, Age: {client_profile['age']}, Income: ₹{client_profile['annual_income_lakhs']}L")

        # Fetch holdings
        cursor.execute("SELECT * FROM holdings WHERE client_id = ?", (client_id,))
        holdings = [dict(r) for r in cursor.fetchall()]
        add_thought("holdings", f"Retrieved {len(holdings)} holdings across multiple asset classes")

        # Asset summary
        cursor.execute("""
            SELECT asset_type, SUM(current_value) as value, SUM(unrealized_pnl) as pnl
            FROM holdings WHERE client_id = ? GROUP BY asset_type
        """, (client_id,))
        asset_summary = [dict(r) for r in cursor.fetchall()]

        total_value = sum(h["current_value"] for h in holdings)
        total_invested = sum(h["invested_amount"] for h in holdings)
        total_pnl = total_value - total_invested

        add_thought("summary", f"Total portfolio: ₹{total_value:,.0f} | Invested: ₹{total_invested:,.0f} | P&L: ₹{total_pnl:,.0f}")

        # Fetch tax deductions
        cursor.execute("SELECT * FROM tax_deductions WHERE client_id = ? AND financial_year = '2025-26'", (client_id,))
        deductions = [dict(r) for r in cursor.fetchall()]
        add_thought("deductions", f"Found {len(deductions)} tax deductions for FY 2025-26")

        conn.close()

        return {
            **state,
            "client_profile": client_profile,
            "portfolio": holdings,
            "asset_summary": {
                "total_value": total_value,
                "total_invested": total_invested,
                "total_unrealized_pnl": total_pnl,
                "breakdown": asset_summary,
                "deductions": deductions,
            },
            "agent_thoughts": thoughts,
            "status": "data_fetched",
        }

    except Exception as e:
        errors = state.get("errors", [])
        errors.append(f"DataRetrievalAgent: {str(e)}")
        add_thought("error", f"Error: {str(e)}")
        return {
            **state,
            "errors": errors,
            "agent_thoughts": thoughts,
            "status": "error",
        }
