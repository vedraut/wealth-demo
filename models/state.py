"""
Shared state model for the Wealth Management LangGraph.

All agents read from and write to this typed state dictionary.
"""

from typing import TypedDict, NotRequired, Optional
from typing import Any


class TaxFlag(TypedDict):
    """A tax-related flag or recommendation."""
    severity: str  # info, warning, critical
    section: str  # e.g., 80C, STCG, LTCG
    message: str
    potential_savings: Optional[float]


class AdvisoryRecommendation(TypedDict):
    """A single advisory recommendation."""
    category: str  # tax, rebalancing, risk, goal
    priority: str  # high, medium, low
    title: str
    description: str
    action_items: list[str]


class AgentThought(TypedDict):
    """Track an agent's reasoning step."""
    agent: str
    step: str
    thought: str
    timestamp: str


class WealthManagementState(TypedDict):
    """
    Shared state across all agents in the wealth management graph.

    Fields:
        client_id: Selected client to analyze
        client_profile: Basic client info from DB
        portfolio: Full portfolio holdings
        tax_analysis: Computed tax liability and flags
        report: Final synthesized advisory report
        errors: Any errors encountered during execution
        agent_thoughts: Streaming thoughts from agents for UI display
        status: Current graph execution status
    """
    client_id: int
    client_profile: NotRequired[dict[str, Any]]
    portfolio: NotRequired[list[dict[str, Any]]]
    asset_summary: NotRequired[dict[str, Any]]
    tax_analysis: NotRequired[dict[str, Any]]
    report: NotRequired[dict[str, Any]]
    errors: NotRequired[list[str]]
    agent_thoughts: NotRequired[list[AgentThought]]
    status: NotRequired[str]  # initialized, data_fetched, tax_analyzed, completed, error
