"""
Supervisor Graph - LangGraph Implementation

The supervisor coordinates the multi-stakeholder architecture description process
using LangGraph's StateGraph with proper checkpointing and observability.
"""

import logging
import time
from pathlib import Path
from typing import Annotated, Any, NotRequired

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from src.observability.tracers import get_global_tracer

from .adr import ADRManager
from .decision_tracker import DecisionTracker
from .human_feedback import (
    FeedbackAction,
    HumanFeedback,
    create_final_approval_interrupt,
    create_quality_review_interrupt,
    should_interrupt_for_quality,
)
from .quality import QualityGates
from .schemas import StakeholderAnalysis, SynthesisResult
from .stakeholder_agents import StakeholderType
from .subgraphs import (
    create_aider_integration_subgraph,
    create_context_engineering_subgraph,
    create_developer_experience_subgraph,
    create_langgraph_architecture_subgraph,
    create_production_stability_subgraph,
)
from .synthesis import SynthesisEngine


class SupervisorState(TypedDict):
    """State schema for the supervisor graph"""

    messages: Annotated[list[BaseMessage], add_messages]

    # Core workflow state
    current_phase: str  # "initialization", "stakeholder_analysis", "synthesis", "quality_review", "completion"
    integration_challenge: str
    stakeholder_charter: str | None

    # Stakeholder coordination
    active_stakeholder: str | None
    stakeholder_contributions: dict[str, StakeholderAnalysis]
    completed_stakeholders: list[str]

    # Quality and synthesis
    synthesis_result: SynthesisResult | None
    quality_score: float | None
    implementation_readiness: float | None
    ticket_coverage: float | None
    synthesis_attempts: int = 0
    human_approved: bool = False

    # Decision tracking
    intermediate_decisions: list[dict[str, Any]] = []
    decision_history: list[dict[str, Any]] = []

    # Metadata
    run_id: str
    thread_id: str
    start_time: float
    message_count: int
    max_messages: NotRequired[int]

    # Output paths
    output_directory: str | None
    architecture_document_path: str | None

    # Control flow
    next_action: str
    should_continue: bool


class SupervisorGraph:
    """
    LangGraph-native supervisor for multi-stakeholder architecture generation.

    Coordinates the flow between stakeholder analysis, synthesis, and quality gates
    using proper LangGraph patterns with checkpointing and observability.
    """

    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        max_messages: int = 100,
        checkpointer: BaseCheckpointSaver | None = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.tracer = get_global_tracer()

        # LLM setup
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        # Configuration
        self.max_messages = max_messages
        self.checkpointer = checkpointer or MemorySaver()

        # Initialize components
        self.synthesis_engine = SynthesisEngine(self.llm)
        self.quality_gates = QualityGates(llm=self.llm)
        self.decision_tracker = DecisionTracker()
        self.logger = logging.getLogger(self.__class__.__name__)

        # Create individual stakeholder subgraphs (compiled LangGraph subgraphs)
        self.stakeholder_subgraphs = self._create_stakeholder_subgraphs()

        # Build and compile the main supervisor graph
        self.graph = self._initialize_graph(checkpointer)

        self.logger.info(f"SupervisorGraph initialized with {len(self.stakeholder_subgraphs)} stakeholder subgraphs")

    def _get_initial_prompt(self, integration_challenge: str, stakeholder_charter: str) -> str:
        return f"""
You are the supervisor of a multi-stakeholder group tasked with creating a comprehensive architecture description.
Your goal is to coordinate the stakeholders, synthesize their contributions, and produce a high-quality, actionable architecture document.

Integration Challenge: {integration_challenge}
Charter: {stakeholder_charter}
"""

    def _create_stakeholder_subgraphs(self) -> dict[str, Any]:
        """Create individual LangGraph subgraphs for each stakeholder domain"""
        subgraphs = {}

        # Create AIDER Integration subgraph
        subgraphs["aider_integration"] = create_aider_integration_subgraph(llm=self.llm, checkpointer=self.checkpointer)

        # Create LangGraph Architecture subgraph
        subgraphs["langgraph_architecture"] = create_langgraph_architecture_subgraph(
            llm=self.llm, checkpointer=self.checkpointer
        )

        # Create Context Engineering subgraph
        subgraphs["context_engineering"] = create_context_engineering_subgraph(
            llm=self.llm, checkpointer=self.checkpointer
        )

        # Create Production Stability subgraph
        subgraphs["production_stability"] = create_production_stability_subgraph(
            llm=self.llm, checkpointer=self.checkpointer
        )

        # Create Developer Experience subgraph
        subgraphs["developer_experience"] = create_developer_experience_subgraph(
            llm=self.llm, checkpointer=self.checkpointer
        )

        self.logger.info(f"Created {len(subgraphs)} stakeholder subgraphs")
        return subgraphs

    def _initialize_graph(self, checkpointer: BaseCheckpointSaver | None) -> StateGraph:
        """Build the LangGraph supervisor state machine"""

        # Create the state graph
        workflow = StateGraph(SupervisorState)

        # Add nodes
        workflow.add_node("initialize", self._initialize_session)
        workflow.add_node("coordinate_stakeholders", self._coordinate_stakeholders)
        workflow.add_node("run_stakeholder_analysis", self._run_stakeholder_analysis)
        workflow.add_node("synthesize_contributions", self._synthesize_contributions)
        workflow.add_node("quality_review", self._quality_review)
        workflow.add_node("get_human_approval", self._get_human_approval)
        workflow.add_node("finalize_output", self._finalize_output)

        # Define the flow
        workflow.set_entry_point("initialize")

        # Conditional routing from initialize
        workflow.add_conditional_edges(
            "initialize",
            self._should_continue_after_init,
            {"stakeholder_analysis": "coordinate_stakeholders", "end": END},
        )

        # Stakeholder coordination loop
        workflow.add_conditional_edges(
            "coordinate_stakeholders",
            self._route_stakeholder_work,
            {"run_analysis": "run_stakeholder_analysis", "synthesize": "synthesize_contributions", "end": END},
        )

        # After stakeholder analysis, back to coordination
        workflow.add_edge("run_stakeholder_analysis", "coordinate_stakeholders")

        # Synthesis to quality review
        workflow.add_edge("synthesize_contributions", "quality_review")

        # Quality review routing
        workflow.add_conditional_edges(
            "quality_review",
            self._route_quality_review,
            {"get_human_approval": "get_human_approval", "synthesize": "synthesize_contributions", "end": END},
        )

        # Human approval routing
        workflow.add_conditional_edges(
            "get_human_approval",
            self._route_human_approval,
            {"finalize_output": "finalize_output", "synthesize": "synthesize_contributions", "end": END},
        )

        # Finalize to end
        workflow.add_edge("finalize_output", END)

        # Compile with checkpointer and interrupt points
        return workflow.compile(
            checkpointer=checkpointer,
            interrupt_before=[
                "get_human_approval",  # Human approval before finalization
                "quality_review",  # Optional interrupt for quality review
            ],
        )

    def _initialize_session(self, state: SupervisorState) -> dict[str, Any]:
        """Initialize the stakeholder session"""
        self.logger.info(f"Initializing supervisor session: {state['run_id']}")

        # Set up initial state
        updates = {
            "current_phase": "initialization",
            "message_count": len(state.get("messages", [])),
            "stakeholder_contributions": {},
            "completed_stakeholders": [],
            "should_continue": True,
            "next_action": "stakeholder_analysis",
        }

        # Add initialization message
        init_message = SystemMessage(
            content=f"""Starting multi-stakeholder architecture analysis session.

Integration Challenge: {state.get("integration_challenge", "Not specified")}
Charter: {state.get("stakeholder_charter", "Not specified")}
Available Stakeholder Subgraphs: {list(self.stakeholder_subgraphs.keys())}

Session initialized at {time.strftime("%Y-%m-%d %H:%M:%S")}"""
        )

        updates["messages"] = [init_message]

        return updates

    def _coordinate_stakeholders(self, state: SupervisorState) -> dict[str, Any]:
        """Coordinate which stakeholder should act next"""
        completed = set(state.get("completed_stakeholders", []))
        available = set(self.stakeholder_subgraphs.keys()) - completed

        self.logger.info(f"Coordinating stakeholders. Completed: {len(completed)}, Available: {len(available)}")

        if not available:
            # All stakeholders have contributed
            return {"current_phase": "synthesis", "next_action": "synthesize", "active_stakeholder": None}

        # Select next stakeholder (simple round-robin for now)
        next_stakeholder = list(available)[0]

        return {
            "current_phase": "stakeholder_analysis",
            "active_stakeholder": next_stakeholder,
            "next_action": "run_analysis",
        }

    def _run_stakeholder_analysis(self, state: SupervisorState) -> dict:
        active_stakeholder_name = state.get("active_stakeholder")
        if not active_stakeholder_name:
            # This should ideally not happen if the routing is correct.
            # Adding a graceful exit path.
            return {"next_action": "end", "messages": [("tool", "error: No active stakeholder to run analysis.")]}

        self.logger.info(f"Running analysis for stakeholder: {active_stakeholder_name}")

        active_stakeholder_type = StakeholderType[active_stakeholder_name.upper()]

        # Prepare the state for the subgraph
        subgraph_input_state = {
            "messages": state["messages"],
            "integration_challenge": state.get("integration_challenge", ""),
            "stakeholder_charter": state.get("stakeholder_charter", ""),
            "previous_contributions": state.get("stakeholder_contributions", {}),
        }

        # Retrieve the thread_id from the state for the subgraph invocation
        thread_id = state.get("thread_id")

        # Invoke the subgraph
        # Get the specific subgraph for this stakeholder
        stakeholder_subgraph = self.stakeholder_subgraphs[active_stakeholder_type.value]

        # Subgraphs need their own thread_id management if they are to be stateful.
        # For now, we pass the main thread_id, but a more robust solution
        # might involve creating sub-threads.
        subgraph_output_state = stakeholder_subgraph.invoke(
            subgraph_input_state,
            config={"configurable": {"thread_id": f"{thread_id}_subgraph_{active_stakeholder_name}"}},
        )

        contribution: StakeholderAnalysis = subgraph_output_state.get("analysis_result")

        if not contribution or not isinstance(contribution, StakeholderAnalysis):
            contribution = StakeholderAnalysis(
                perspective="Error", aspects=[], analysis="No valid contribution was provided by the stakeholder agent."
            )

        self.logger.info(f"Contribution from {active_stakeholder_name}: {contribution.perspective}...")

        # Capture stakeholder decisions
        stakeholder_decision = self.decision_tracker.capture_stakeholder_decision(
            stakeholder_type=active_stakeholder_name,
            decision=f"Stakeholder analysis completed: {contribution.perspective}",
            rationale=contribution.analysis[:200] + "..."
            if len(contribution.analysis) > 200
            else contribution.analysis,
            context=f"Analysis for integration challenge: {state.get('integration_challenge', '')[:100]}...",
        )

        # Update decision tracking
        intermediate_decisions = state.get("intermediate_decisions", []).copy()
        intermediate_decisions.append(stakeholder_decision)

        decision_history = state.get("decision_history", []).copy()
        decision_history.append(stakeholder_decision)

        # Update contributions
        contributions = state.get("stakeholder_contributions", {}).copy()
        contributions[active_stakeholder_name] = contribution

        # Mark as completed
        completed = state.get("completed_stakeholders", []).copy()
        completed.append(active_stakeholder_name)

        # Create a message with the contribution
        contribution_message = AIMessage(
            content=f"**{active_stakeholder_name.title()} Stakeholder Analysis:**\n\n"
            f"**Perspective**: {contribution.perspective}\n"
            f"**Analysis**: {contribution.analysis[:500]}...",
            name=active_stakeholder_name,
        )

        return {
            "stakeholder_contributions": contributions,
            "completed_stakeholders": completed,
            "intermediate_decisions": intermediate_decisions,
            "decision_history": decision_history,
            "messages": [contribution_message],
            "message_count": state.get("message_count", 0) + 1,
            "next_action": "coordinate",
        }

    def _synthesize_contributions(self, state: SupervisorState) -> dict[str, Any]:
        """Synthesize all stakeholder contributions"""
        synthesis_attempts = state.get("synthesis_attempts", 0) + 1
        if synthesis_attempts > 3:
            return {"next_action": "end"}

        self.logger.info(f"Synthesizing stakeholder contributions (Attempt {synthesis_attempts})...")

        contributions = state.get("stakeholder_contributions", {})

        if not contributions:
            return {"synthesis_result": "No contributions to synthesize", "next_action": "end"}

        try:
            # Run synthesis
            synthesis_result = self.synthesis_engine.synthesize_contributions(
                contributions=contributions,
                integration_challenge=state.get("integration_challenge", ""),
                charter=state.get("stakeholder_charter", ""),
            )

            # Capture synthesis decisions
            synthesis_decision = self.decision_tracker.capture_synthesis_decision(
                decision=f"Synthesis completed: {synthesis_result.introduction[:100]}...",
                rationale="Synthesized stakeholder contributions into comprehensive architecture",
                context=f"Integration challenge: {state.get('integration_challenge', '')[:100]}...",
                stakeholder_inputs=list(contributions.keys()),
            )

            # Update decision tracking
            intermediate_decisions = state.get("intermediate_decisions", []).copy()
            intermediate_decisions.append(synthesis_decision)

            decision_history = state.get("decision_history", []).copy()
            decision_history.append(synthesis_decision)

            synthesis_message = AIMessage(
                content=f"**Synthesis Result:**\n\n{synthesis_result.introduction}", name="synthesis_engine"
            )

            return {
                "current_phase": "synthesis",
                "synthesis_result": synthesis_result,
                "intermediate_decisions": intermediate_decisions,
                "decision_history": decision_history,
                "messages": [synthesis_message],
                "next_action": "quality_review",
            }

        except Exception as e:
            self.logger.error(f"Error in synthesis: {e}")

            error_message = AIMessage(content=f"**Synthesis Error:** {str(e)}", name="synthesis_engine")

            return {"messages": [error_message], "next_action": "end"}

    def _quality_review(self, state: SupervisorState) -> dict[str, Any]:
        """Run quality gates on the synthesis result with conditional human interrupts"""
        self.logger.info("Running quality review")

        synthesis_result = state.get("synthesis_result")
        if not synthesis_result or not isinstance(synthesis_result, SynthesisResult):
            return {"quality_score": 0.0, "next_action": "retry_synthesis"}

        try:
            # Run quality gates
            quality_result = self.quality_gates.evaluate(
                synthesis_result=synthesis_result,
                integration_challenge=state.get("integration_challenge", ""),
                stakeholder_contributions=state.get("stakeholder_contributions", {}),
            )

            quality_score = quality_result.get("overall_score", 0.0)

            # Capture quality decisions
            quality_decision = self.decision_tracker.capture_quality_decision(
                decision=f"Quality assessment completed with score {quality_score:.2f}",
                rationale=quality_result.get("details", "Quality assessment completed"),
                quality_scores={
                    "overall_score": quality_score,
                    "implementation_readiness": quality_result.get("implementation_readiness", 0.0),
                    "ticket_coverage": quality_result.get("ticket_coverage", 0.0),
                    "stakeholder_balance": quality_result.get("stakeholder_balance", 0.0),
                    "technical_feasibility": quality_result.get("technical_feasibility", 0.0),
                    "clarity_completeness": quality_result.get("clarity_completeness", 0.0),
                },
            )

            # Update decision tracking
            intermediate_decisions = state.get("intermediate_decisions", []).copy()
            intermediate_decisions.append(quality_decision)

            decision_history = state.get("decision_history", []).copy()
            decision_history.append(quality_decision)

            # Check if human interrupt is needed based on quality
            if should_interrupt_for_quality(quality_score):
                self.logger.info(f"Quality score {quality_score} requires human review")
                # Create interrupt for quality review
                updated_state = create_quality_review_interrupt(state)
                updated_state.update(
                    {
                        "quality_score": quality_score,
                        "implementation_readiness": quality_result.get("implementation_readiness", 0.0),
                        "ticket_coverage": quality_result.get("ticket_coverage", 0.0),
                        "intermediate_decisions": intermediate_decisions,
                        "decision_history": decision_history,
                    }
                )
                return updated_state

            quality_message = AIMessage(
                content=f"**Quality Review:**\n\nOverall Score: {quality_result['overall_score']:.2f}\n"
                f"Implementation Readiness: {quality_result['implementation_readiness']:.2f}\n"
                f"Ticket Coverage: {quality_result['ticket_coverage']:.2f}\n\n"
                f"Details: {quality_result['details']}",
                name="quality_gates",
            )

            # Determine next action based on quality scores
            if quality_result["overall_score"] >= 0.8:
                next_action = "finalize"
            elif quality_result["overall_score"] >= 0.6:
                next_action = "retry_synthesis"
            else:
                next_action = "retry_stakeholders"

            return {
                "current_phase": "quality_review",
                "quality_score": quality_result["overall_score"],
                "implementation_readiness": quality_result["implementation_readiness"],
                "ticket_coverage": quality_result["ticket_coverage"],
                "intermediate_decisions": intermediate_decisions,
                "decision_history": decision_history,
                "messages": [quality_message],
                "next_action": next_action,
            }

        except Exception as e:
            self.logger.error(f"Error in quality review: {e}")

            error_message = AIMessage(content=f"**Quality Review Error:** {str(e)}", name="quality_gates")

            return {
                "messages": [error_message],
                "next_action": "finalize",  # Proceed despite error
            }

    def _get_human_approval(self, state: SupervisorState) -> dict[str, Any]:
        """
        Human approval node using LangGraph's native interrupt functionality.

        This node will be interrupted before execution, allowing human input
        to be collected via LangGraph's interrupt mechanism.
        """
        self.logger.info("Human approval required - creating interrupt")

        # Use LangGraph's native interrupt for human approval
        updated_state = create_final_approval_interrupt(state)

        return updated_state

    def _route_human_approval(self, state: SupervisorState) -> str:
        """Route based on human approval."""
        if state.get("human_approved"):
            return "finalize_output"
        return "synthesize"

    def _finalize_output(self, state: SupervisorState) -> dict[str, Any]:
        """Finalize the architecture description output"""
        self.logger.info("Finalizing architecture description output")

        synthesis_result = state.get("synthesis_result")
        if not synthesis_result or not isinstance(synthesis_result, SynthesisResult):
            self.logger.error("No valid synthesis result found")
            return {"architecture_document_path": None}

        stakeholder_contributions = state.get("stakeholder_contributions", {})

        # Format the architecture description using the enhanced ISO/IEEE formatter
        formatted_description = self.synthesis_engine.format_iso_ieee(
            synthesis_result,
            stakeholder_contributions,
            integration_challenge=state.get("integration_challenge", ""),
            architecture_decisions=[],  # Could be enhanced to track formal decisions
        )

        # Save the formatted description to a file
        output_dir = state.get("output_directory", "runs")
        run_id = state.get("run_id", f"run_{int(time.time())}")
        output_path = Path(output_dir) / f"{run_id}_architecture_description.md"

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(formatted_description)
            self.logger.info(f"Architecture description saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save architecture description: {e}")
            return {"architecture_document_path": None}

        # Create ADRs for all decisions made
        adr_manager = ADRManager(state.get("output_directory", "runs"))
        decisions = synthesis_result.decisions
        for dec in decisions:
            adr_manager.create_adr(
                title=dec.decision,
                context=synthesis_result.introduction,
                decision=dec.decision,
                consequences=dec.consequences,
                status="Accepted",
            )
        self.logger.info(f"{len(decisions)} 'Accepted' ADRs created.")

        # Create ADRs for all considerations
        considerations = synthesis_result.architecture_considerations
        for cons in considerations:
            adr_manager.create_adr(
                title=cons.consideration,
                context=synthesis_result.introduction,
                decision=f"This was a consideration that was explored but not chosen as the final decision. Details: {cons.details}",
                consequences="This path was not taken. See the accepted ADR for the chosen path.",
                status="Considered",
            )
        self.logger.info(f"{len(considerations)} 'Considered' ADRs created.")

        return {"architecture_document_path": output_path, "next_action": "end"}

    # Conditional routing functions
    def _should_continue_after_init(self, state: SupervisorState) -> str:
        """Route after initialization"""
        if not state.get("should_continue", True):
            return "end"
        return "stakeholder_analysis"

    def _route_stakeholder_work(self, state: SupervisorState) -> str:
        """Route stakeholder coordination"""
        next_action = state.get("next_action", "end")

        # Check if we've exceeded max messages to prevent infinite loops
        message_count = state.get("message_count", 0)
        max_messages = state.get("max_messages", 100)

        if message_count >= max_messages:
            self.logger.warning(f"Reached max messages ({max_messages}), ending session")
            return "end"

        if next_action == "run_analysis":
            return "run_analysis"
        elif next_action == "synthesize":
            return "synthesize"
        else:
            return "end"

    def _route_quality_review(self, state: SupervisorState) -> str:
        """Route after quality review"""
        quality_score = state.get("quality_score", 0)
        if quality_score >= 0.75:
            return "get_human_approval"

        if state.get("synthesis_attempts", 0) >= 3:
            return "end"

        return "synthesize"

    def _route_human_approval(self, state: SupervisorState) -> str:
        """Route based on human approval."""
        if state.get("human_approved"):
            return "finalize_output"
        return "synthesize"

    def run(
        self, integration_challenge: str, stakeholder_charter: str, thread_id: str, output_directory: str | None = None
    ) -> dict | None:
        """
        Run the multi-stakeholder architecture generation process.

        Args:
            integration_challenge: The challenge/problem to address
            stakeholder_charter: Optional charter for the session
            run_id: Optional run identifier
            output_directory: Optional directory for outputs
            thread_id: Optional thread ID for checkpointing

        Returns:
            Final state with results
        """

        # Generate IDs if not provided
        run_id = f"supervisor_run_{int(time.time())}"
        if not thread_id:
            thread_id = f"supervisor_thread_{int(time.time())}"

        # Create initial state
        initial_state = {
            "messages": [SystemMessage(content=self._get_initial_prompt(integration_challenge, stakeholder_charter))],
            "integration_challenge": integration_challenge,
            "stakeholder_charter": stakeholder_charter,
            "run_id": run_id,
            "thread_id": thread_id,
            "output_directory": output_directory,
        }

        # The main execution loop to handle interruptions
        final_state = None
        human_feedback = HumanFeedback(action=FeedbackAction.APPROVE)  # Default for testing

        # Use a variable to hold the input for the graph. It's `initial_state` on the first
        # run, and `None` on subsequent runs to resume from the last checkpoint.
        graph_input = initial_state

        while True:
            result = self.graph.invoke(
                graph_input, config={"configurable": {"thread_id": thread_id}, "recursion_limit": 50}
            )
            graph_input = None  # Subsequent calls should resume, not restart

            current_graph_state = self.graph.get_state({"configurable": {"thread_id": thread_id}})

            # Check if the graph has finished
            if not current_graph_state.next:
                self.logger.info("Graph execution finished.")
                final_state = result
                break

            # Check if we are at the human approval interrupt
            if "get_human_approval" in current_graph_state.next:
                self.logger.info("Human approval required to proceed.")
                quality_score = result.get("quality_score", 0)
                prompt = f"Quality score is {quality_score:.2f}. Approve to generate final architecture description?"

                approved = human_feedback.get_approval(prompt)

                # Update the state with the feedback and continue the loop to resume execution
                self.graph.update_state({"configurable": {"thread_id": thread_id}}, {"human_approved": approved})
            else:
                # The graph has stopped at an unexpected point.
                self.logger.warning(f"Graph stopped at an unexpected node: {current_graph_state.next}. Ending run.")
                final_state = result
                break

        self.logger.info(f"Supervisor session completed: {run_id}")
        return final_state
