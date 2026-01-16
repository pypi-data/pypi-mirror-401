# src/stakeholder_generator/subgraphs/base.py
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from ..stakeholder_agents import StakeholderAgent, StakeholderContext


class SubgraphState(TypedDict):
    """
    Represents the state of a stakeholder subgraph.
    """

    messages: Annotated[list[AnyMessage], add_messages]
    stakeholder_agent: StakeholderAgent
    # Add fields for the context
    integration_challenge: str
    stakeholder_charter: str
    previous_contributions: dict
    output: str | None = None


def create_stakeholder_subgraph() -> StateGraph:
    """
    Creates and compiles a stakeholder subgraph.

    This subgraph takes a stakeholder agent and its context as input,
    runs the analysis, and returns the output.
    """
    builder = StateGraph(SubgraphState)

    def run_analysis(state: SubgraphState):
        """
        Runs the stakeholder analysis.
        """
        stakeholder_agent = state["stakeholder_agent"]
        context = StakeholderContext(
            integration_challenge=state["integration_challenge"],
            charter=state["stakeholder_charter"],
            previous_contributions=state["previous_contributions"],
            messages=state["messages"],
        )
        output = stakeholder_agent.analyze(context)
        return {"output": output}

    builder.add_node("run_analysis", run_analysis)
    builder.add_edge("run_analysis", END)
    builder.set_entry_point("run_analysis")

    return builder.compile()
