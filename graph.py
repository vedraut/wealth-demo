"""
LangGraph StateGraph wiring for the Wealth Management workflow.

Flow: Data Retrieval → Tax Analysis → Advisory Report
"""

from langgraph.graph import StateGraph, END
from models.state import WealthManagementState
from agents.data_retrieval import data_retrieval_agent
from agents.tax_analysis import tax_analysis_agent
from agents.advisory import advisory_agent
from typing import Generator


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


def run_wealth_analysis_streaming(client_id: int) -> Generator[dict, None, None]:
    """
    Run the full wealth analysis workflow with streaming progress updates.
    Yields progress events so the UI can show real-time agent execution.

    Args:
        client_id: The client ID to analyze

    Yields:
        dict progress events with keys: stage, agent, status, message, state
    """
    from agents.data_retrieval import data_retrieval_agent
    from agents.tax_analysis import tax_analysis_agent
    from agents.advisory import advisory_agent

    initial_state: WealthManagementState = {
        "client_id": client_id,
        "status": "initialized",
    }

    agent_configs = [
        ("data_retrieval", "Data Retrieval Agent", data_retrieval_agent),
        ("tax_analysis", "Tax Analysis Agent", tax_analysis_agent),
        ("advisory", "Advisory Agent", advisory_agent),
    ]

    current_state = initial_state

    for stage_key, agent_name, agent_func in agent_configs:
        # Yield "starting" event
        yield {
            "stage": stage_key,
            "agent": agent_name,
            "status": "running",
            "message": f"Starting {agent_name}...",
            "thought": None,
            "state": current_state,
        }

        # Run the agent
        current_state = agent_func(current_state)

        # Get the latest thought
        thoughts = current_state.get("agent_thoughts", [])
        latest_thought = thoughts[-1] if thoughts else None

        # Yield "completed" event
        yield {
            "stage": stage_key,
            "agent": agent_name,
            "status": current_state.get("status", "completed"),
            "message": latest_thought["thought"] if latest_thought else f"{agent_name} completed",
            "thought": latest_thought,
            "state": current_state,
        }

    # Yield final completion event
    yield {
        "stage": "complete",
        "agent": "System",
        "status": "completed",
        "message": "Analysis complete",
        "thought": None,
        "state": current_state,
    }
