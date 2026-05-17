"""
Tax Analysis Agent - Analyzes portfolio against Indian Income Tax Act 2025.
"""

from models.state import WealthManagementState, AgentThought, TaxFlag
from agents.llm_client import get_llm_client
from datetime import datetime


def tax_analysis_agent(state: WealthManagementState) -> WealthManagementState:
    """
    Analyze portfolio for tax implications under Indian Income Tax Act 2025.
    Identifies tax-saving opportunities, flags compliance issues, calculates liabilities.
    """
    thoughts = state.get("agent_thoughts", [])
    asset_summary = state.get("asset_summary", {})
    client_profile = state.get("client_profile", {})

    def add_thought(step: str, thought: str):
        thoughts.append(AgentThought(
            agent="TaxAgent",
            step=step,
            thought=thought,
            timestamp=datetime.now().isoformat()
        ))

    add_thought("init", "Starting tax analysis under Income Tax Act 2025")

    try:
        income = client_profile.get("annual_income_lakhs", 0) * 100000
        regime = client_profile.get("tax_regime", "old")
        total_value = asset_summary.get("total_value", 0)
        deductions = asset_summary.get("deductions", [])
        holdings = state.get("portfolio", [])

        # Calculate Section 80C utilization
        sec_80c_used = sum(d["amount"] for d in deductions if d["section"] == "80C")
        sec_80c_limit = 150000
        sec_80c_remaining = max(0, sec_80c_limit - sec_80c_used)

        # Calculate NPS 80CCD(1B) utilization
        nps_80ccd = sum(d["amount"] for d in deductions if d["section"] == "80CCD(1B)")
        nps_limit = 50000
        nps_remaining = max(0, nps_limit - nps_80ccd)

        # Calculate capital gains
        equity_holdings = [h for h in holdings if h["asset_type"] == "equity"]
        debt_holdings = [h for h in holdings if h["asset_type"] == "debt"]

        # LTCG on equity (>1 year, >₹1.25L exempt)
        equity_gains = sum(h["unrealized_pnl"] for h in equity_holdings if h["unrealized_pnl"] > 0)
        equity_losses = sum(h["unrealized_pnl"] for h in equity_holdings if h["unrealized_pnl"] < 0)
        ltcg_exemption = 125000  # FY 2025-26
        taxable_ltcg = max(0, equity_gains - ltcg_exemption)
        ltcg_tax = taxable_ltcg * 0.125  # 12.5% beyond ₹1.25L

        # STCG on equity (<1 year)
        # Simplified: assume all equity is long-term for demo
        stcg_tax = 0

        # Debt taxation (indexation benefits removed in new regime for some)
        debt_gains = sum(h["unrealized_pnl"] for h in debt_holdings if h["unrealized_pnl"] > 0)

        # Tax flags
        flags = []

        if sec_80c_remaining > 0:
            flags.append(TaxFlag(
                severity="warning",
                section="80C",
                message=f"Section 80C underutilized. ₹{sec_80c_remaining:,.0f} remaining of ₹{sec_80c_limit:,.0f} limit",
                potential_savings=sec_80c_remaining * 0.30  # Approx at 30% slab
            ))

        if nps_remaining > 0:
            flags.append(TaxFlag(
                severity="info",
                section="80CCD(1B)",
                message=f"Additional NPS contribution possible: ₹{nps_remaining:,.0f}",
                potential_savings=nps_remaining * 0.30
            ))

        if taxable_ltcg > 0:
            flags.append(TaxFlag(
                severity="warning",
                section="LTCG",
                message=f"Taxable LTCG: ₹{taxable_ltcg:,.0f} (beyond ₹1.25L exemption). Tax: ₹{ltcg_tax:,.0f}",
                potential_savings=equity_losses * 0.125 if equity_losses < 0 else 0
            ))

        # Check for tax-loss harvesting opportunity
        if equity_losses < 0:
            flags.append(TaxFlag(
                severity="info",
                section="Tax Loss Harvesting",
                message=f"Unrealized equity losses: ₹{abs(equity_losses):,.0f}. Consider harvesting to offset gains.",
                potential_savings=abs(equity_losses) * 0.125
            ))

        # Health insurance check
        health_insurance = sum(d["amount"] for d in deductions if d["section"] == "80D")
        if health_insurance < 25000:
            flags.append(TaxFlag(
                severity="info",
                section="80D",
                message="Health insurance coverage appears low. Consider increasing for better protection and tax benefits.",
                potential_savings=25000 * 0.30
            ))

        add_thought("80C", f"80C utilization: ₹{sec_80c_used:,.0f} / ₹{sec_80c_limit:,.0f}")
        add_thought("LTCG", f"Equity LTCG: ₹{equity_gains:,.0f} | Taxable: ₹{taxable_ltcg:,.0f} | Tax: ₹{ltcg_tax:,.0f}")
        add_thought("flags", f"Generated {len(flags)} tax flags/recommendations")

        # Use LLM for nuanced analysis
        llm = get_llm_client()
        tax_prompt = f"""
You are an Indian tax expert. Analyze this client's tax situation:

Client: {client_profile.get('name')}, Age: {client_profile.get('age')}
Annual Income: ₹{income:,.0f}
Tax Regime: {regime}
Portfolio Value: ₹{total_value:,.0f}

Current Deductions:
{chr(10).join([f"- {d['section']}: ₹{d['amount']:,.0f} ({d['description']})" for d in deductions])}

Tax Flags Identified:
{chr(10).join([f"- [{f['severity']}] {f['section']}: {f['message']}" for f in flags])}

Provide 3-4 specific, actionable tax optimization strategies for FY 2025-26.
Keep it concise and practical.
"""

        llm_insights = llm.generate(
            tax_prompt, 
            system="You are a senior tax advisor specializing in Indian Income Tax Act 2025. Provide concise, actionable advice.",
            client_id=state.get('client_id'),
            response_type='tax',
            use_cache=True
        )
        add_thought("llm", "Generated AI-powered tax insights")

        return {
            **state,
            "tax_analysis": {
                "income": income,
                "regime": regime,
                "sec_80c_used": sec_80c_used,
                "sec_80c_remaining": sec_80c_remaining,
                "nps_used": nps_80ccd,
                "nps_remaining": nps_remaining,
                "equity_gains": equity_gains,
                "equity_losses": equity_losses,
                "taxable_ltcg": taxable_ltcg,
                "ltcg_tax": ltcg_tax,
                "flags": flags,
                "llm_insights": llm_insights,
            },
            "agent_thoughts": thoughts,
            "status": "tax_analyzed",
        }

    except Exception as e:
        errors = state.get("errors", [])
        errors.append(f"TaxAgent: {str(e)}")
        add_thought("error", f"Error: {str(e)}")
        return {
            **state,
            "errors": errors,
            "agent_thoughts": thoughts,
            "status": "error",
        }
