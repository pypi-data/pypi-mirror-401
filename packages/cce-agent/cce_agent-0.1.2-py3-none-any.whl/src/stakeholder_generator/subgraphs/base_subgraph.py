"""
Base Stakeholder Subgraph Implementation

Provides the foundation for creating LangGraph subgraphs for each stakeholder domain.
Each subgraph is a compiled LangGraph graph that can be invoked independently
with proper state management and handoffs via Command(goto=...).
"""

import logging
import time
from typing import Annotated, Any

from langchain_core.messages import AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command
from typing_extensions import TypedDict

from src.prompts.manager import PromptManager

from ..schemas import StakeholderAnalysis
from ..stakeholder_agents import StakeholderAgent, StakeholderContext, StakeholderType


class StakeholderSubgraphState(TypedDict):
    """State schema for individual stakeholder subgraphs"""

    messages: Annotated[list[BaseMessage], add_messages]

    # Input from supervisor
    integration_challenge: str
    stakeholder_charter: str | None
    context: StakeholderContext | None

    # Stakeholder processing
    stakeholder_type: str
    analysis_result: StakeholderAnalysis | None
    processing_status: str  # "pending", "analyzing", "completed", "error"
    error_message: str | None

    # Metadata
    session_id: str
    start_time: float | None
    end_time: float | None


def create_stakeholder_subgraph(
    stakeholder_type: StakeholderType, llm: ChatOpenAI | None = None, checkpointer: Any | None = None
) -> StateGraph:
    """
    Create a LangGraph subgraph for a specific stakeholder domain.

    This replaces the previous node-based approach with a true subgraph
    that can be compiled and invoked independently.

    Args:
        stakeholder_type: The type of stakeholder (AIDER, LangGraph, etc.)
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph ready for supervisor integration
    """
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

    if checkpointer is None:
        checkpointer = MemorySaver()

    # Initialize stakeholder agent
    stakeholder_agent = StakeholderAgent(stakeholder_type, llm=llm)
    prompt_manager = PromptManager()
    logger = logging.getLogger(f"stakeholder_subgraph.{stakeholder_type.value}")

    # Define subgraph nodes
    def initialize_stakeholder(state: StakeholderSubgraphState) -> StakeholderSubgraphState:
        """Initialize the stakeholder analysis process"""
        logger.info(f"Initializing {stakeholder_type.value} stakeholder analysis")

        return {
            **state,
            "processing_status": "analyzing",
            "start_time": time.time(),
            "stakeholder_type": stakeholder_type.value,
        }

    def analyze_requirements(state: StakeholderSubgraphState) -> StakeholderSubgraphState:
        """Perform the core stakeholder analysis"""
        logger.info(f"Running analysis for {stakeholder_type.value} stakeholder")

        try:
            # Create context for analysis
            context = state.get("context") or StakeholderContext(
                integration_challenge=state["integration_challenge"],
                charter=state.get("stakeholder_charter", ""),
                previous_contributions=state.get("previous_contributions", {}),
                messages=state.get("messages", []),
            )

            # Run stakeholder analysis
            analysis_result = stakeholder_agent.analyze(context)

            logger.info(f"Analysis completed for {stakeholder_type.value}")

            return {
                **state,
                "analysis_result": analysis_result,
                "processing_status": "completed",
                "end_time": time.time(),
            }

        except Exception as e:
            logger.error(f"Error in {stakeholder_type.value} analysis: {e}")
            return {**state, "processing_status": "error", "error_message": str(e), "end_time": time.time()}

    def finalize_analysis(state: StakeholderSubgraphState) -> StakeholderSubgraphState:
        """Finalize the analysis and prepare for handoff back to supervisor"""
        logger.info(f"Finalizing {stakeholder_type.value} stakeholder analysis")

        # Add completion message to state
        if state["processing_status"] == "completed" and state.get("analysis_result"):
            completion_msg = AIMessage(
                content=f"{stakeholder_type.value} stakeholder analysis completed successfully",
                additional_kwargs={
                    "stakeholder_type": stakeholder_type.value,
                    "analysis_result": state["analysis_result"].model_dump() if state["analysis_result"] else None,
                    "processing_time": (state.get("end_time", 0) - state.get("start_time", 0)),
                },
            )

            return {**state, "messages": state.get("messages", []) + [completion_msg]}
        else:
            error_msg = AIMessage(
                content=f"{stakeholder_type.value} stakeholder analysis failed: {state.get('error_message', 'Unknown error')}",
                additional_kwargs={"stakeholder_type": stakeholder_type.value, "error": state.get("error_message")},
            )

            return {**state, "messages": state.get("messages", []) + [error_msg]}

    # Build the subgraph
    subgraph = StateGraph(StakeholderSubgraphState)

    # Add nodes
    subgraph.add_node("initialize", initialize_stakeholder)
    subgraph.add_node("analyze", analyze_requirements)
    subgraph.add_node("finalize", finalize_analysis)

    # Add edges
    subgraph.add_edge(START, "initialize")
    subgraph.add_edge("initialize", "analyze")
    subgraph.add_edge("analyze", "finalize")
    subgraph.add_edge("finalize", END)

    # Compile with checkpointer
    compiled_subgraph = subgraph.compile(checkpointer=checkpointer)

    logger.info(f"Compiled {stakeholder_type.value} subgraph successfully")

    return compiled_subgraph


def create_stakeholder_handoff_command(stakeholder_type: StakeholderType, state: dict[str, Any]) -> Command:
    """
    Create a Command(goto=...) for handoff to a stakeholder subgraph.

    This enables the supervisor to properly hand off control to individual
    stakeholder subgraphs using LangGraph's Command pattern.

    Args:
        stakeholder_type: The stakeholder to hand off to
        state: Current supervisor state

    Returns:
        Command object for LangGraph handoff
    """
    subgraph_name = f"{stakeholder_type.value}_subgraph"

    # Prepare state for subgraph
    subgraph_state = {
        "integration_challenge": state.get("integration_challenge", ""),
        "stakeholder_charter": state.get("stakeholder_charter"),
        "session_id": state.get("session_id", ""),
        "processing_status": "pending",
        "stakeholder_type": stakeholder_type.value,
        "messages": [],
    }

    return Command(goto=subgraph_name, update=subgraph_state)
