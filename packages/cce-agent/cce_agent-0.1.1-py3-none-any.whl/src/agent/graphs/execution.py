"""Execution graph builder for the legacy agent."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.agent.state import ExecutionState


def create_execution_graph(agent) -> StateGraph:
    """Create the execution graph that handles iterative work cycles."""
    workflow = StateGraph(ExecutionState)

    # Add nodes for each phase of execution
    workflow.add_node("orient_cycle", agent._orient_for_next_cycle)
    workflow.add_node("execute_react", agent._execute_react_cycle)
    workflow.add_node("reconcile_results", agent._reconcile_cycle_results)
    workflow.add_node("check_status", agent._determine_next_action)

    # Set entry point
    workflow.set_entry_point("orient_cycle")

    # Define linear flow within each cycle
    workflow.add_edge("orient_cycle", "execute_react")
    workflow.add_edge("execute_react", "reconcile_results")
    workflow.add_edge("reconcile_results", "check_status")

    # Conditional routing based on agent_status
    workflow.add_conditional_edges(
        "check_status",
        lambda state: state["agent_status"],
        {
            "running": "orient_cycle",
            "completed": END,
            "failed": END,
        },
    )

    checkpointer = getattr(agent, "memory", None) or getattr(agent, "checkpointer", None)
    return workflow.compile(checkpointer=checkpointer)
