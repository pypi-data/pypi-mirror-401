"""Planning graph builder for the legacy agent."""

from __future__ import annotations

from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from src.agent.state import PlanningState


def create_planning_graph(agent) -> StateGraph:
    """Create the multi-agent collaborative planning graph."""
    logger = agent.logger
    llm = agent.llm
    planning_tools = agent.planning_tools

    # Create handoff tools for agent communication
    @tool
    def handoff_to_technical_planner() -> str:
        """Hand off to the technical implementation planner for detailed technical analysis."""
        return "\N{WRENCH} Handing off to Technical Planner for implementation analysis..."

    @tool
    def handoff_to_architectural_planner() -> str:
        """Hand off to the architectural strategy planner for design and long-term considerations."""
        return "\N{BUILDING CONSTRUCTION} Handing off to Architectural Planner for strategic analysis..."

    @tool
    def handoff_to_consensus() -> str:
        """Hand off to consensus checker when ready to finalize the plan."""
        return "\N{WHITE HEAVY CHECK MARK} Ready for consensus check and plan finalization..."

    # Technical Planner Agent (Planner A)
    def technical_planner_node(state: PlanningState):
        logger.info("\N{WRENCH} Technical Planner analyzing implementation details...")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a TECHNICAL IMPLEMENTATION SPECIALIST focused on:\n"
                    "- Code structure and implementation details\n"
                    "- Tool usage and immediate technical tasks\n"
                    "- File modifications and technical dependencies\n"
                    "- Step-by-step implementation procedures\n\n"
                    "Your role is to:\n"
                    "1. Use tools to investigate the technical landscape\n"
                    "2. Create detailed implementation steps\n"
                    "3. Update the shared_plan with technical details\n"
                    "4. Hand off to architectural planner for strategic review\n\n"
                    "Available handoff tools:\n"
                    "- handoff_to_architectural_planner: Get strategic/design perspective\n"
                    "- handoff_to_consensus: When both analyses are complete\n\n"
                    "Focus on HOW to implement, not WHY or long-term strategy.",
                ),
                ("placeholder", "{messages}"),
            ]
        )

        # Combine investigation tools with handoff tools
        agent_tools = planning_tools + [handoff_to_architectural_planner, handoff_to_consensus]
        agent_chain = prompt | llm.bind_tools(agent_tools)
        result = agent_chain.invoke(state)

        # Count and log tool usage
        tool_calls = 0
        tools_used = []
        if hasattr(result, "tool_calls") and result.tool_calls:
            tool_calls = len(result.tool_calls)
            tools_used = [tc["name"] for tc in result.tool_calls]
            logger.info(
                "\N{WRENCH} Technical Planner used %s tool calls: %s",
                tool_calls,
                ", ".join(tools_used),
            )
        else:
            logger.info("\N{WRENCH} Technical Planner used 0 tool calls")

        logger.info("\N{WRENCH} Technical analysis length: %s chars", len(result.content))

        # Update technical analysis and add message
        return {
            "messages": [result],
            "technical_analysis": result.content,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    # Architectural Planner Agent (Planner B)
    def architectural_planner_node(state: PlanningState):
        logger.info("\N{BUILDING CONSTRUCTION} Architectural Planner analyzing strategic design...")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an ARCHITECTURAL STRATEGY SPECIALIST focused on:\n"
                    "- High-level design patterns and architecture\n"
                    "- Long-term maintainability and scalability\n"
                    "- Risk assessment and trade-off analysis\n"
                    "- Strategic planning and system integration\n\n"
                    "Your role is to:\n"
                    "1. Review technical analysis from the technical planner\n"
                    "2. Add architectural perspective and strategic considerations\n"
                    "3. Update the shared_plan with design insights\n"
                    "4. Hand off to technical planner for refinement or consensus for finalization\n\n"
                    "Available handoff tools:\n"
                    "- handoff_to_technical_planner: Get more technical details\n"
                    "- handoff_to_consensus: When both analyses are complete\n\n"
                    "Focus on WHY and WHAT architecture, not detailed HOW implementation.",
                ),
                ("placeholder", "{messages}"),
            ]
        )

        agent_tools = planning_tools + [handoff_to_technical_planner, handoff_to_consensus]
        agent_chain = prompt | llm.bind_tools(agent_tools)
        result = agent_chain.invoke(state)

        # Count and log tool usage
        tool_calls = 0
        tools_used = []
        if hasattr(result, "tool_calls") and result.tool_calls:
            tool_calls = len(result.tool_calls)
            tools_used = [tc["name"] for tc in result.tool_calls]
            logger.info(
                "\N{BUILDING CONSTRUCTION} Architectural Planner used %s tool calls: %s",
                tool_calls,
                ", ".join(tools_used),
            )
        else:
            logger.info("\N{BUILDING CONSTRUCTION} Architectural Planner used 0 tool calls")

        logger.info(
            "\N{BUILDING CONSTRUCTION} Architectural analysis length: %s chars",
            len(result.content),
        )

        return {
            "messages": [result],
            "architectural_analysis": result.content,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    # Consensus Check Node
    def consensus_check_node(state: PlanningState):
        logger.info("\N{WHITE HEAVY CHECK MARK} Checking consensus and finalizing plan...")

        # Check iteration limits
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", 12)

        logger.info(
            "\N{BAR CHART} Consensus check - Iteration %s/%s",
            iteration_count,
            max_iterations,
        )
        logger.info(
            "\N{BAR CHART} Technical analysis present: %s",
            bool(state.get("technical_analysis")),
        )
        logger.info(
            "\N{BAR CHART} Architectural analysis present: %s",
            bool(state.get("architectural_analysis")),
        )

        if iteration_count >= max_iterations:
            logger.warning("Max iterations (%s) reached, forcing consensus", max_iterations)
            final_plan = agent._merge_analyses(state)
            return {
                "shared_plan": final_plan,
                "consensus_reached": True,
                "messages": [
                    AIMessage(
                        content=(f"\N{WHITE HEAVY CHECK MARK} FINAL PLAN (Max iterations reached):\n\n{final_plan}")
                    )
                ],
            }

        # Check if both analyses exist
        technical = state.get("technical_analysis", "")
        architectural = state.get("architectural_analysis", "")

        if not technical or not architectural:
            # Need more analysis - this will be handled by routing
            return {"messages": [HumanMessage(content="Need both technical and architectural analysis for consensus")]}

        # Both analyses exist - create final plan
        final_plan = agent._merge_analyses(state)

        return {
            "shared_plan": final_plan,
            "consensus_reached": True,
            "messages": [
                AIMessage(content=(f"\N{WHITE HEAVY CHECK MARK} CONSENSUS REACHED - FINAL PLAN:\n\n{final_plan}"))
            ],
        }

    # Tool execution node that handles Commands from handoff tools
    def tool_execution_node(state: PlanningState):
        """Execute tools and handle Command objects for handoffs."""
        # Use ToolNode to properly handle tool execution and responses
        all_tools = planning_tools + [
            handoff_to_technical_planner,
            handoff_to_architectural_planner,
            handoff_to_consensus,
        ]
        tool_node = ToolNode(all_tools)

        # ToolNode will handle the tool call/response cycle properly
        return tool_node.invoke(state)

    # Routing functions for conditional edges
    def route_after_technical_planner(state: PlanningState) -> Literal["tools", "architectural_planner"]:
        """Route after technical planner based on whether it called tools."""
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return "architectural_planner"

    def route_after_architectural_planner(state: PlanningState) -> Literal["tools", "consensus_check"]:
        """Route after architectural planner based on whether it called tools."""
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return "consensus_check"

    def route_after_consensus(
        state: PlanningState,
    ) -> Literal["technical_planner", "architectural_planner", END]:
        """Route after consensus check based on what's needed."""
        if state.get("consensus_reached", False):
            return END

        # Check what analysis is missing
        technical = state.get("technical_analysis", "")
        architectural = state.get("architectural_analysis", "")

        if not technical:
            return "technical_planner"
        if not architectural:
            return "architectural_planner"

        # Both exist but no consensus - go back to technical for refinement
        return "technical_planner"

    def route_after_tools(
        state: PlanningState,
    ) -> Literal["technical_planner", "architectural_planner", "consensus_check"]:
        """Route after tools based on handoff tool calls or returning to active agent."""
        messages = state["messages"]

        # Look for handoff tool messages (ToolMessage responses)
        for msg in reversed(messages):
            if hasattr(msg, "content") and hasattr(msg, "tool_call_id"):
                content = msg.content.lower()
                if "technical planner" in content:
                    return "technical_planner"
                if "architectural planner" in content:
                    return "architectural_planner"
                if "consensus" in content:
                    return "consensus_check"

        # Look for the last agent message with tool calls to determine context
        for msg in reversed(messages):
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name", "")
                    if tool_name == "handoff_to_technical_planner":
                        return "technical_planner"
                    if tool_name == "handoff_to_architectural_planner":
                        return "architectural_planner"
                    if tool_name == "handoff_to_consensus":
                        return "consensus_check"

        # Default fallback - return to technical planner
        return "technical_planner"

    # Build the graph
    graph = StateGraph(PlanningState)

    # Add agent nodes
    graph.add_node("technical_planner", technical_planner_node)
    graph.add_node("architectural_planner", architectural_planner_node)
    graph.add_node("consensus_check", consensus_check_node)
    graph.add_node("tools", tool_execution_node)

    # Set entry point
    graph.add_edge(START, "technical_planner")

    # Add conditional edges for proper routing
    graph.add_conditional_edges(
        "technical_planner",
        route_after_technical_planner,
        {
            "tools": "tools",
            "architectural_planner": "architectural_planner",
        },
    )

    graph.add_conditional_edges(
        "architectural_planner",
        route_after_architectural_planner,
        {
            "tools": "tools",
            "consensus_check": "consensus_check",
        },
    )

    graph.add_conditional_edges(
        "consensus_check",
        route_after_consensus,
        {
            "technical_planner": "technical_planner",
            "architectural_planner": "architectural_planner",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "tools",
        route_after_tools,
        {
            "technical_planner": "technical_planner",
            "architectural_planner": "architectural_planner",
            "consensus_check": "consensus_check",
        },
    )

    return graph.compile(checkpointer=agent.memory)
