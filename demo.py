"""
Terminal demo script for Wealth Management & Tax Advisory.
Run this for a command-line demonstration of the multi-agent system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import run_wealth_analysis
from database.seed_data import create_database, get_connection


def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_agent_thought(thought: dict):
    agent_icons = {
        "DataRetrievalAgent": "📊",
        "TaxAgent": "🧮",
        "AdvisoryAgent": "📋",
    }
    icon = agent_icons.get(thought["agent"], "🤖")
    print(f"\n  {icon} {thought['agent']} — {thought['step']}")
    print(f"     → {thought['thought']}")


def run_terminal_demo(client_id: int = 1):
    """Run a full terminal-based demo."""

    print_header("WEALTH MANAGEMENT & TAX ADVISORY DEMO")
    print("  Multi-Agent System with LangGraph + Ollama/Kimi")
    print("  Indian Income Tax Act 2025")

    # Ensure DB exists
    db_path = os.path.join(os.path.dirname(__file__), "database", "wealth_demo.db")
    if not os.path.exists(db_path):
        print("\n📦 Initializing database...")
        create_database()

    # Get client info
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
    client = dict(cursor.fetchone())
    conn.close()

    print(f"\n👤 Client: {client['name']}")
    print(f"   Age: {client['age']} | Income: ₹{client['annual_income_lakhs']}L | Regime: {client['tax_regime'].upper()}")

    print("\n🚀 Starting AI Analysis...")
    print("-" * 60)

    # Run analysis
    result = run_wealth_analysis(client_id)

    # Display agent thoughts
    print_header("AGENT EXECUTION LOG")
    for thought in result.get("agent_thoughts", []):
        print_agent_thought(thought)

    # Portfolio Summary
    print_header("PORTFOLIO SUMMARY")
    asset_summary = result.get("asset_summary", {})
    print(f"  Total Value:     ₹{asset_summary.get('total_value', 0):>15,.0f}")
    print(f"  Total Invested:  ₹{asset_summary.get('total_invested', 0):>15,.0f}")
    print(f"  Unrealized P&L:  ₹{asset_summary.get('total_unrealized_pnl', 0):>15,.0f}")

    print("\n  Asset Breakdown:")
    for item in asset_summary.get("breakdown", []):
        print(f"    • {item['asset_type']:15s}: ₹{item['value']:>12,.0f} (P&L: ₹{item.get('pnl', 0):>10,.0f})")

    # Tax Analysis
    print_header("TAX ANALYSIS (FY 2025-26)")
    tax = result.get("tax_analysis", {})
    print(f"  Tax Regime:      {tax.get('regime', 'old').upper()}")
    print(f"  80C Used:        ₹{tax.get('sec_80c_used', 0):>15,.0f} / ₹150,000")
    print(f"  80C Remaining:   ₹{tax.get('sec_80c_remaining', 0):>15,.0f}")
    print(f"  NPS (80CCD 1B):  ₹{tax.get('nps_used', 0):>15,.0f} / ₹50,000")
    print(f"  Taxable LTCG:    ₹{tax.get('taxable_ltcg', 0):>15,.0f}")
    print(f"  LTCG Tax (12.5%): ₹{tax.get('ltcg_tax', 0):>14,.0f}")

    print("\n  Tax Flags:")
    for flag in tax.get("flags", []):
        icon = "⚠️" if flag["severity"] == "warning" else "ℹ️"
        print(f"    {icon} [{flag['severity'].upper()}] {flag['section']}")
        print(f"       {flag['message']}")
        if flag.get('potential_savings'):
            print(f"       Potential Savings: ₹{flag['potential_savings']:,.0f}")

    # LLM Insights
    if tax.get("llm_insights"):
        print_header("🤖 AI TAX INSIGHTS")
        print(tax["llm_insights"])

    # Advisory Report
    print_header("ADVISORY REPORT")
    report = result.get("report", {})
    if report.get("executive_summary"):
        print(report["executive_summary"])

    print("\n  🎯 Key Recommendations:")
    for i, rec in enumerate(report.get("recommendations", []), 1):
        priority_icon = "🔴" if rec["priority"] == "high" else "🟡"
        print(f"\n    {priority_icon} {i}. [{rec['priority'].upper()}] {rec['title']} ({rec['category']})")
        print(f"       {rec['description']}")
        print(f"       Action Items:")
        for item in rec["action_items"]:
            print(f"         • {item}")

    # Errors
    errors = result.get("errors", [])
    if errors:
        print_header("⚠️ ERRORS")
        for error in errors:
            print(f"  ❌ {error}")

    print_header("DEMO COMPLETE")
    print("  Thank you for using AI Wealth Management!")
    print(f"{'='*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wealth Management Demo")
    parser.add_argument("--client", type=int, default=1, help="Client ID (1-3)")
    parser.add_argument("--list", action="store_true", help="List available clients")
    args = parser.parse_args()

    if args.list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT client_id, name, occupation, annual_income_lakhs FROM clients")
        print("\nAvailable Clients:")
        for row in cursor.fetchall():
            print(f"  {row['client_id']}. {row['name']} ({row['occupation']}, ₹{row['annual_income_lakhs']}L)")
        conn.close()
        return

    run_terminal_demo(args.client)


if __name__ == "__main__":
    main()
