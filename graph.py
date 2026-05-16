"""
LangGraph StateGraph wiring for the Wealth Management workflow.

Flow: Data Retrieval → Tax Analysis → Advisory Report
"""

from langgraph.graph import StateGraph, END
from models.state import WealthManagementState
from agents.data_retrieval import data_retrieval_agent
from agents.tax_analysis import tax_analysis_agent
from agents.advisory import advisory_agent


def create_wealth_graph() -> StateGraph:
    """Create and compile the wealth management LangGraph."""

    # Initialize graph with state schema
    workflow = StateGraph(WealthManagementState)

    # Add nodes
    workflow.add_node("data_retrieval", data_retrieval_agent)
    workflow.add_node("tax_analysis", tax_analysis_agent)
    workflow.add_node("advisory", advisory_agent)

    # Define edges
    workflow.set_entry_point("data_retrieval")
    workflow.add_edge("data_retrieval", "tax_analysis")
    workflow.add_edge("tax_analysis", "advisory")
    workflow.add_edge("advisory", END)

    # Compile
    return workflow.compile()


# Singleton instance
_graph = None


def get_graph():
    """Get or create the compiled graph."""
    global _graph
    if _graph is None:
        _graph = create_wealth_graph()
    return _graph


def run_wealth_analysis(client_id: int) -> WealthManagementState:
    """
    Run the full wealth analysis workflow for a client.

    Args:
        client_id: The client ID to analyze

    Returns:
        Final state with report, tax analysis, and agent thoughts
    """
    graph = get_graph()

    initial_state: WealthManagementState = {
        "client_id": client_id,
        "status": "initialized",
    }

    # Run the graph
    final_state = graph.invoke(initial_state)
    return final_state
