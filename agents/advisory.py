"""
Advisory Agent - Synthesizes portfolio data and tax analysis into a comprehensive report.
"""

from models.state import WealthManagementState, AgentThought, AdvisoryRecommendation
from agents.llm_client import get_llm_client
from datetime import datetime


def advisory_agent(state: WealthManagementState) -> WealthManagementState:
    """
    Synthesize raw portfolio data and tax analysis into a client-facing financial strategy report.
    """
    thoughts = state.get("agent_thoughts", [])
    client_profile = state.get("client_profile", {})
    asset_summary = state.get("asset_summary", {})
    tax_analysis = state.get("tax_analysis", {})

    def add_thought(step: str, thought: str):
        thoughts.append(AgentThought(
            agent="AdvisoryAgent",
            step=step,
            thought=thought,
            timestamp=datetime.now().isoformat()
        ))

    add_thought("init", "Starting advisory report synthesis")

    try:
        # Build structured recommendations
        recommendations = []

        # Tax optimization recommendations
        if tax_analysis.get("sec_80c_remaining", 0) > 0:
            recommendations.append(AdvisoryRecommendation(
                category="tax",
                priority="high",
                title="Maximize Section 80C Benefits",
                description=f"You have ₹{tax_analysis['sec_80c_remaining']:,.0f} remaining under Section 80C. Consider ELSS mutual funds or additional PPF contribution.",
                action_items=[
                    "Invest remaining amount in ELSS before March 31",
                    "Set up SIP for next financial year",
                    "Review existing 80C investments for performance"
                ]
            ))

        if tax_analysis.get("nps_remaining", 0) > 0:
            recommendations.append(AdvisoryRecommendation(
                category="tax",
                priority="medium",
                title="Additional NPS Contribution (80CCD 1B)",
                description=f"Additional ₹{tax_analysis['nps_remaining']:,.0f} can be invested in NPS for exclusive tax benefit beyond 80C.",
                action_items=[
                    "Open NPS Tier-I if not already done",
                    "Invest ₹{tax_analysis['nps_remaining']:,.0f} before March 31",
                    "Consider increasing monthly NPS contribution"
                ]
            ))

        # Tax loss harvesting
        if tax_analysis.get("equity_losses", 0) < 0:
            recommendations.append(AdvisoryRecommendation(
                category="tax",
                priority="high",
                title="Tax Loss Harvesting Opportunity",
                description=f"Unrealized losses of ₹{abs(tax_analysis['equity_losses']):,.0f} can be harvested to offset LTCG of ₹{tax_analysis.get('taxable_ltcg', 0):,.0f}.",
                action_items=[
                    "Review underperforming equity holdings",
                    "Execute loss harvesting before March 31",
                    "Reinvest in similar (not identical) instruments after 30 days"
                ]
            ))

        # Portfolio rebalancing
        breakdown = asset_summary.get("breakdown", [])
        equity_value = sum(b["value"] for b in breakdown if b["asset_type"] == "equity")
        total_value = asset_summary.get("total_value", 1)
        equity_pct = (equity_value / total_value) * 100 if total_value > 0 else 0

        age = client_profile.get("age", 35)
        ideal_equity = max(30, 100 - age)  # Rough rule: 100 - age

        if equity_pct > ideal_equity + 10:
            recommendations.append(AdvisoryRecommendation(
                category="rebalancing",
                priority="medium",
                title="Portfolio Rebalancing Needed",
                description=f"Equity allocation at {equity_pct:.1f}% is above ideal {ideal_equity}% for your age ({age}). Consider shifting to debt.",
                action_items=[
                    f"Reduce equity by ~{equity_pct - ideal_equity:.0f}%",
                    "Invest in debt mutual funds or corporate FDs",
                    "Maintain emergency fund of 6 months expenses"
                ]
            ))
        elif equity_pct < ideal_equity - 10:
            recommendations.append(AdvisoryRecommendation(
                category="rebalancing",
                priority="medium",
                title="Increase Equity Exposure",
                description=f"Equity at {equity_pct:.1f}% is below ideal {ideal_equity}% for your age. Consider increasing for long-term growth.",
                action_items=[
                    f"Increase equity by ~{ideal_equity - equity_pct:.0f}%",
                    "Consider index funds or diversified equity funds",
                    "Use STP from debt to equity over 6 months"
                ]
            ))

        # Goal-based recommendations
        if client_profile.get("annual_income_lakhs", 0) > 100:
            recommendations.append(AdvisoryRecommendation(
                category="goal",
                priority="medium",
                title="Estate Planning Review",
                description="Given your high net worth, consider reviewing estate planning and succession.",
                action_items=[
                    "Review nomination details on all holdings",
                    "Consider creating a will if not done",
                    "Explore trust structures for asset protection"
                ]
            ))

        add_thought("recommendations", f"Generated {len(recommendations)} structured recommendations")

        # Use LLM for final report synthesis
        llm = get_llm_client()

        report_prompt = f"""
Create a professional wealth management report for:

Client: {client_profile.get('name')}
Age: {client_profile.get('age')} | Income: ₹{client_profile.get('annual_income_lakhs')}L/year
Portfolio Value: ₹{asset_summary.get('total_value', 0):,.0f}
Tax Regime: {client_profile.get('tax_regime', 'old')}

Key Findings:
- Total Portfolio: ₹{asset_summary.get('total_value', 0):,.0f}
- Unrealized P&L: ₹{asset_summary.get('total_unrealized_pnl', 0):,.0f}
- 80C Utilization: ₹{tax_analysis.get('sec_80c_used', 0):,.0f} / ₹150,000
- Taxable LTCG: ₹{tax_analysis.get('taxable_ltcg', 0):,.0f}
- Tax Loss Harvesting Potential: ₹{abs(tax_analysis.get('equity_losses', 0)):,.0f}

Write a concise executive summary (3-4 paragraphs) highlighting:
1. Current financial position
2. Key tax optimization opportunities
3. Portfolio rebalancing suggestions
4. Next steps

Tone: Professional, encouraging, actionable.
"""

        executive_summary = llm.generate(
            report_prompt,
            system="You are a senior wealth manager at a top Indian private bank. Write clear, professional reports for HNI clients."
        )
        add_thought("llm", "Generated AI-powered executive summary")

        return {
            **state,
            "report": {
                "executive_summary": executive_summary,
                "recommendations": recommendations,
                "client_name": client_profile.get("name"),
                "report_date": datetime.now().isoformat(),
                "portfolio_value": asset_summary.get("total_value", 0),
                "tax_savings_potential": sum(r.get("potential_savings", 0) for r in tax_analysis.get("flags", [])),
            },
            "agent_thoughts": thoughts,
            "status": "completed",
        }

    except Exception as e:
        errors = state.get("errors", [])
        errors.append(f"AdvisoryAgent: {str(e)}")
        add_thought("error", f"Error: {str(e)}")
        return {
            **state,
            "errors": errors,
            "agent_thoughts": thoughts,
            "status": "error",
        }
