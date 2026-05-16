"""
Test script to verify the wealth management pipeline produces correct output.
"""

from graph import run_wealth_analysis

def test_client(client_id):
    print(f"\n{'='*60}")
    print(f"TESTING CLIENT {client_id}")
    print(f"{'='*60}")

    result = run_wealth_analysis(client_id)

    # Check status
    print(f"\nStatus: {result.get('status')}")

    # Check client profile
    profile = result.get('client_profile', {})
    print(f"Client: {profile.get('name')}, Age: {profile.get('age')}, Income: ₹{profile.get('annual_income_lakhs')}L")

    # Check asset summary
    asset_summary = result.get('asset_summary', {})
    print(f"Portfolio Value: ₹{asset_summary.get('total_value', 0):,.0f}")
    print(f"Total Invested: ₹{asset_summary.get('total_invested', 0):,.0f}")
    print(f"Unrealized P&L: ₹{asset_summary.get('total_unrealized_pnl', 0):,.0f}")

    # Check tax analysis
    tax = result.get('tax_analysis', {})
    print(f"\nTax Analysis:")
    print(f"  80C Used: ₹{tax.get('sec_80c_used', 0):,.0f} / ₹150,000")
    print(f"  80C Remaining: ₹{tax.get('sec_80c_remaining', 0):,.0f}")
    print(f"  NPS Used: ₹{tax.get('nps_used', 0):,.0f} / ₹50,000")
    print(f"  NPS Remaining: ₹{tax.get('nps_remaining', 0):,.0f}")
    print(f"  Equity Gains: ₹{tax.get('equity_gains', 0):,.0f}")
    print(f"  Equity Losses: ₹{tax.get('equity_losses', 0):,.0f}")
    print(f"  Taxable LTCG: ₹{tax.get('taxable_ltcg', 0):,.0f}")
    print(f"  LTCG Tax: ₹{tax.get('ltcg_tax', 0):,.0f}")
    print(f"  Tax Flags: {len(tax.get('flags', []))}")

    # Check report
    report = result.get('report', {})
    print(f"\nReport:")
    print(f"  Client Name: {report.get('client_name')}")
    print(f"  Portfolio Value: ₹{report.get('portfolio_value', 0):,.0f}")
    print(f"  Tax Savings Potential: ₹{report.get('tax_savings_potential', 0):,.0f}")
    print(f"  Executive Summary Length: {len(report.get('executive_summary', ''))} chars")
    print(f"  Recommendations: {len(report.get('recommendations', []))}")

    # Check recommendations for f-string issues
    print(f"\nRecommendations Detail:")
    for i, rec in enumerate(report.get('recommendations', [])):
        print(f"\n  {i+1}. [{rec['priority'].upper()}] {rec['title']}")
        print(f"     Category: {rec['category']}")
        print(f"     Description: {rec['description']}")
        print(f"     Actions:")
        for action in rec.get('action_items', []):
            # Check for unformatted f-string patterns
            if "{" in action and "}" in action:
                print(f"       ⚠️  RAW F-STRING: {action}")
            else:
                print(f"       ✓ {action}")

    # Check for errors
    errors = result.get('errors', [])
    if errors:
        print(f"\n⚠️  ERRORS: {errors}")
    else:
        print(f"\n✓ No errors")

    # Validate no raw f-strings in descriptions
    print(f"\nValidation:")
    for rec in report.get('recommendations', []):
        desc = rec['description']
        if "{" in desc and "}" in desc and "₹" not in desc:
            print(f"  ⚠️  Potential raw f-string in description: {desc}")
        else:
            print(f"  ✓ Description formatted correctly: {desc[:60]}...")

    return result

if __name__ == "__main__":
    for cid in [1, 2, 3]:
        test_client(cid)

    print(f"\n{'='*60}")
    print("ALL TESTS COMPLETE")
    print(f"{'='*60}")
