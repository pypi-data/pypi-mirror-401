"""
Command Orchestrator for CCE Agent

This module provides command orchestration capabilities for the Constitutional Context Engineering Agent,
enabling the agent to use CCE commands in a coordinated, sequential manner instead of simple LLM calls.

The orchestrator handles:
- Command sequencing and coordination
- State management across command executions
- Error handling and recovery
- Result aggregation and synthesis
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# Import CCE commands
from .commands import (
    address_evaluation,
    commit_and_push,
    create_plan,
    discover_target_files,  # NEW: File discovery command
    evaluate_implementation,
    implement_plan,
    research_codebase,
    run_tests,
    update_plan,
)

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """Result of a single command execution"""

    command_name: str
    success: bool
    result: str
    error: str | None = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OrchestrationResult:
    """Result of a complete command orchestration sequence"""

    sequence_name: str
    success: bool
    commands_executed: list[CommandResult] = field(default_factory=list)
    final_result: str | None = None
    error: str | None = None
    total_time: float = 0.0


@dataclass
class SequenceResult:
    """Result of executing a sequence of commands"""

    success: bool
    results: dict[str, str] = field(default_factory=dict)
    commands_executed: list[CommandResult] = field(default_factory=list)
    error_messages: list[str] = field(default_factory=list)
    total_time: float = 0.0


class CommandOrchestrator:
    """
    Orchestrates CCE command execution for the main agent.

    This class replaces simple LLM calls with structured command sequences
    that implement the CCE architecture patterns.
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CommandOrchestrator")

        # Map command names to their functions
        self.commands = {
            "research_codebase": research_codebase,
            "create_plan": create_plan,
            "update_plan": update_plan,
            "implement_plan": implement_plan,
            "evaluate_implementation": evaluate_implementation,
            "address_evaluation": address_evaluation,
            "run_tests": run_tests,
            "commit_and_push": commit_and_push,
            "discover_target_files": discover_target_files,  # NEW: File discovery command
        }

    async def execute_command(self, command_name: str, **kwargs) -> CommandResult:
        """Execute a single CCE command with error handling"""
        start_time = datetime.now()

        try:
            if command_name not in self.commands:
                raise ValueError(f"Unknown command: {command_name}")

            command_func = self.commands[command_name]
            self.logger.info(f"🔧 Executing command: {command_name}")

            # Execute the command
            self.logger.info(f"🔍 [DEBUG] About to invoke command function: {command_name}")
            self.logger.info(f"🔍 [DEBUG] Command kwargs: {list(kwargs.keys())}")
            if command_name == "research_codebase" and kwargs.get("context") is None:
                kwargs["context"] = ""
            result = await command_func.ainvoke(kwargs)
            self.logger.info(f"🔍 [DEBUG] Command {command_name} result type: {type(result)}")
            self.logger.info(
                f"🔍 [DEBUG] Command {command_name} result length: {len(str(result)) if result else 0} chars"
            )

            execution_time = (datetime.now() - start_time).total_seconds()

            self.logger.info(f"✅ Command {command_name} completed in {execution_time:.2f}s")

            return CommandResult(
                command_name=command_name,
                success=True,
                result=result,
                execution_time=execution_time,
                timestamp=start_time,
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Command {command_name} failed: {str(e)}"

            self.logger.error(f"🔍 [DEBUG] Command {command_name} failed with exception")
            self.logger.error(f"🔍 [DEBUG] Exception type: {type(e)}")
            self.logger.error(f"🔍 [DEBUG] Exception value: {e}")
            self.logger.error(f"🔍 [DEBUG] Exception str: {str(e)}")
            import traceback

            self.logger.error(f"🔍 [DEBUG] Exception traceback: {traceback.format_exc()}")
            self.logger.error(error_msg)

            return CommandResult(
                command_name=command_name,
                success=False,
                result="",
                error=error_msg,
                execution_time=execution_time,
                timestamp=start_time,
            )

    async def orchestrate_planning_sequence(
        self, ticket_description: str, context: str | None = None, workspace_root: str | None = None
    ) -> OrchestrationResult:
        """
        Orchestrate the planning sequence using CCE commands.

        This replaces the simple LLM-based planning_graph with command-driven planning:
        1. Research the codebase to understand current state
        2. Discover target files using funnel methodology
        3. Create an initial plan based on research and discovered files
        4. Update plan based on additional context if needed

        Args:
            ticket_description: The ticket or task description to plan for
            context: Optional additional context or constraints
            workspace_root: Optional workspace root for discovery and planning

        Returns:
            OrchestrationResult with the final plan and execution details
        """
        start_time = datetime.now()
        sequence_name = "planning_sequence"
        commands_executed = []

        try:
            self.logger.info(f"🎯 Starting planning sequence for: {ticket_description[:100]}...")

            # Step 1: Research the codebase
            research_result = await self.execute_command(
                "research_codebase",
                research_question=ticket_description,
                context=context,
                workspace_root=workspace_root,
            )
            commands_executed.append(research_result)

            if not research_result.success:
                raise Exception(f"Research phase failed: {research_result.error}")

            # Step 2: Discover target files
            discovery_result = await self.execute_command(
                "discover_target_files",
                plan_topic=ticket_description,
                research_findings=research_result.result,
                stakeholder_analysis=context,
                workspace_root=workspace_root,
            )
            commands_executed.append(discovery_result)

            # Extract discovered files for plan creation
            discovered_files = []
            if discovery_result.success and isinstance(discovery_result.result, dict):
                discovered_files = discovery_result.result.get("discovered_files", [])

            # Step 3: Create plan based on research and discovered files
            plan_result = await self.execute_command(
                "create_plan",
                plan_topic=ticket_description,
                context=f"Research findings:\n{research_result.result}\n\nAdditional context: {context or 'None'}",
                discovered_files=discovered_files,
                workspace_root=workspace_root,
            )
            commands_executed.append(plan_result)

            if not plan_result.success:
                raise Exception(f"Plan creation failed: {plan_result.error}")

            # Step 4: Validate and refine plan if needed
            # For now, we'll use the created plan directly
            # Future enhancement: Add plan validation and refinement

            total_time = (datetime.now() - start_time).total_seconds()

            self.logger.info(f"✅ Planning sequence completed in {total_time:.2f}s")

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=True,
                commands_executed=commands_executed,
                final_result=plan_result.result,
                total_time=total_time,
            )

        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Planning sequence failed: {str(e)}"

            self.logger.error(error_msg)

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=False,
                commands_executed=commands_executed,
                error=error_msg,
                total_time=total_time,
            )

    async def orchestrate_orientation_sequence(
        self,
        current_plan: str,
        cycle_context: str,
        cycle_results: list[Any],
        stakeholder_insights: str | None = None,
        workspace_root: str | None = None,
    ) -> OrchestrationResult:
        """
        Orchestrate the orientation sequence using CCE commands.

        This replaces simple prompting in orient_for_next_cycle with command-driven orientation:
        1. Research current state and context
        2. Update plan based on new information and cycle results
        3. Generate focused orientation for next cycle

        Args:
            current_plan: The current implementation plan
            cycle_context: Context about the current cycle
            cycle_results: Results from previous cycles
            workspace_root: Optional workspace root for research

        Returns:
            OrchestrationResult with orientation guidance and execution details
        """
        start_time = datetime.now()
        sequence_name = "orientation_sequence"
        commands_executed = []

        try:
            self.logger.info(f"🎯 Starting orientation sequence for cycle...")

            # Step 1: Research current context and state
            research_context = f"Current plan: {current_plan}\nCycle context: {cycle_context}\nPrevious results: {len(cycle_results)} cycles completed"

            # Include stakeholder insights if available
            if stakeholder_insights:
                research_context += f"\nStakeholder insights: {stakeholder_insights[:500]}"

            research_result = await self.execute_command(
                "research_codebase",
                research_question=f"Current implementation state and next steps: {cycle_context}",
                context=research_context,
                workspace_root=workspace_root,
            )
            commands_executed.append(research_result)

            if not research_result.success:
                self.logger.warning(f"Research failed, continuing with available context: {research_result.error}")

            # Step 2: Update plan based on current state and research
            # For now, we'll generate orientation guidance directly
            # Future enhancement: Use update_plan command to refine the plan

            # Generate orientation based on research and context
            orientation_guidance = self._generate_orientation_guidance(
                current_plan,
                cycle_context,
                cycle_results,
                research_result.result if research_result.success else "Research unavailable",
            )

            total_time = (datetime.now() - start_time).total_seconds()

            self.logger.info(f"✅ Orientation sequence completed in {total_time:.2f}s")

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=True,
                commands_executed=commands_executed,
                final_result=orientation_guidance,
                total_time=total_time,
            )

        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Orientation sequence failed: {str(e)}"

            self.logger.error(error_msg)

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=False,
                commands_executed=commands_executed,
                error=error_msg,
                total_time=total_time,
            )

    async def orchestrate_reconciliation_sequence(
        self,
        cycle_result: Any,
        current_plan: str,
        commit_changes: bool = False,
        commit_message: str | None = None,
    ) -> OrchestrationResult:
        """
        Orchestrate the reconciliation sequence using CCE commands.

        This replaces simple logging in reconcile_cycle_results with command-driven evaluation:
        1. Run tests to validate current implementation
        2. Evaluate implementation quality and completeness
        3. Address any issues found during evaluation

        Args:
            cycle_result: Result from the completed execution cycle
            current_plan: The current implementation plan
            commit_changes: Whether to stage and commit changes after tests pass
            commit_message: Optional commit message override

        Returns:
            OrchestrationResult with evaluation findings and next steps
        """
        start_time = datetime.now()
        sequence_name = "reconciliation_sequence"
        commands_executed = []

        try:
            self.logger.info(f"🔄 Starting reconciliation sequence for cycle...")

            # Step 1: Run tests to validate implementation
            test_result = await self.execute_command(
                "run_tests",
                test_pattern=None,
                test_type="changes",
            )
            commands_executed.append(test_result)

            # Step 2: Evaluate implementation (even if tests failed)
            evaluation_context = f"""
            Cycle Result Status: {getattr(cycle_result, "status", "unknown")}
            Cycle Summary: {getattr(cycle_result, "final_thought", "No summary available")[:500]}
                      Current Plan: {current_plan[:1000]}
            """

            eval_result = await self.execute_command(
                "evaluate_implementation",
                github_ticket_url=None,
                context=evaluation_context,
            )
            commands_executed.append(eval_result)

            commit_result = None
            if commit_changes:
                def _tests_passed(result: CommandResult) -> bool:
                    if not result.success:
                        return False
                    text = (result.result or "").lower()
                    return all(token not in text for token in ("failed", "error", "traceback", "failure"))

                if _tests_passed(test_result):
                    from src.tools.git_ops import GitOps
                    from src.tools.shell_runner import ShellRunner
                    from src.workspace_context import get_workspace_root

                    workspace_root = get_workspace_root() or "."
                    git_ops = GitOps(ShellRunner(workspace_root))
                    if git_ops.has_changes():
                        if git_ops.add_all():
                            message = commit_message or "chore: reconcile cycle updates"
                            commit_outcome = git_ops.commit(message)
                            if commit_outcome.success:
                                commit_result = CommandResult(
                                    command_name="commit",
                                    success=True,
                                    result=f"Committed {commit_outcome.commit_sha or 'changes'}",
                                )
                            else:
                                commit_result = CommandResult(
                                    command_name="commit",
                                    success=False,
                                    result="",
                                    error=commit_outcome.error or "Commit failed",
                                )
                        else:
                            commit_result = CommandResult(
                                command_name="commit",
                                success=False,
                                result="",
                                error="Failed to stage changes",
                            )
                    else:
                        commit_result = CommandResult(
                            command_name="commit",
                            success=True,
                            result="No changes to commit",
                        )

                else:
                    commit_result = CommandResult(
                        command_name="commit",
                        success=False,
                        result="",
                        error="Tests did not pass; commit skipped",
                    )

                if commit_result:
                    commands_executed.append(commit_result)

            # # Step 3: Address evaluation findings if issues were found
            # final_result = eval_result.result if eval_result.success else f"Evaluation failed: {eval_result.error}"

            # # Check if evaluation indicates issues that need addressing
            # if eval_result.success and ("issues" in eval_result.result.lower() or "problems" in eval_result.result.lower()):
            #     self.logger.info("🔧 Issues detected, running address_evaluation...")

            #     address_result = await self.execute_command(
            #         'address_evaluation',
            #         evaluation_findings=eval_result.result,
            #         priority="medium"
            #     )
            #     commands_executed.append(address_result)

            #     if address_result.success:
            #         final_result = f"{final_result}\n\nIssue Resolution:\n{address_result.result}"

            total_time = (datetime.now() - start_time).total_seconds()

            test_summary = test_result.result if test_result.success else f"Tests failed: {test_result.error}"
            eval_summary = eval_result.result if eval_result.success else f"Evaluation failed: {eval_result.error}"
            commit_summary = None
            if commit_result:
                commit_summary = commit_result.result if commit_result.success else f"Commit failed: {commit_result.error}"
            final_result_parts = [test_summary, eval_summary]
            if commit_summary:
                final_result_parts.append(commit_summary)
            final_result = "\n\n".join(final_result_parts)

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=True,
                commands_executed=commands_executed,
                final_result=final_result,
                total_time=total_time,
            )

        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Reconciliation sequence failed: {str(e)}"

            self.logger.error(error_msg)

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=False,
                commands_executed=commands_executed,
                error=error_msg,
                total_time=total_time,
            )

    def _generate_orientation_guidance(
        self, current_plan: str, cycle_context: str, cycle_results: list[Any], research_findings: str
    ) -> str:
        """Generate orientation guidance based on available information"""

        # Extract key information
        cycles_completed = len(cycle_results)
        last_cycle_status = getattr(cycle_results[-1], "status", "unknown") if cycle_results else "none"

        # Generate focused guidance
        guidance = f"""
# Cycle Orientation Guidance

## Current Context
- Cycles completed: {cycles_completed}
- Last cycle status: {last_cycle_status}
- Current focus: {cycle_context}

## Research Insights
{research_findings[:500]}...

## Recommended Focus
Based on the current state and research findings, focus on:

1. **Immediate Priority**: Address any issues from the last cycle
2. **Implementation Progress**: Continue with planned implementation tasks
3. **Quality Assurance**: Ensure tests pass and code quality is maintained

## Next Steps
- Review the current plan and adjust if needed
- Focus on incremental progress toward completion
- Validate changes through testing and review
"""

        return guidance.strip()

    async def execute_command_sequence(self, commands: list[dict[str, Any]]) -> "SequenceResult":
        """
        Execute a sequence of commands and return aggregated results.

        Args:
            commands: List of command dictionaries with 'command' and 'params' keys

        Returns:
            SequenceResult with aggregated command results
        """
        start_time = datetime.now()
        results = {}
        commands_executed = []
        success = True
        error_messages = []

        try:
            self.logger.info(f"🔍 [DEBUG] Starting command sequence with {len(commands)} commands")

            for i, cmd_dict in enumerate(commands):
                command_name = cmd_dict.get("command")
                params = cmd_dict.get("params", {})
                self.logger.info(f"🔍 [DEBUG] Command {i + 1}: {command_name}")
                self.logger.info(
                    f"🔍 [DEBUG] Command {i + 1} params keys: {list(params.keys()) if params else 'No params'}"
                )

                if not command_name:
                    error_msg = f"Command dictionary missing 'command' key: {cmd_dict}"
                    self.logger.error(error_msg)
                    error_messages.append(error_msg)
                    success = False
                    continue

                # Execute the command
                self.logger.info(f"🔍 [DEBUG] About to execute command: {command_name}")

                cmd_result = await self.execute_command(command_name, **params)
                self.logger.info(f"🔍 [DEBUG] Command {command_name} completed")
                self.logger.info(f"🔍 [DEBUG] Command {command_name} success: {cmd_result.success}")
                self.logger.info(f"🔍 [DEBUG] Command {command_name} result type: {type(cmd_result.result)}")
                self.logger.info(
                    f"🔍 [DEBUG] Command {command_name} result length: {len(str(cmd_result.result)) if cmd_result.result else 0} chars"
                )
                if not cmd_result.success:
                    self.logger.error(f"🔍 [DEBUG] Command {command_name} error: {cmd_result.error}")
                    self.logger.error(f"🔍 [DEBUG] Command {command_name} error type: {type(cmd_result.error)}")

                commands_executed.append(cmd_result)

                # Store result - maintain data structure contracts during failures
                if cmd_result.success:
                    results[command_name] = cmd_result.result
                else:
                    # Maintain expected data structure even during failures
                    if command_name == "create_plan":
                        results[command_name] = {
                            "markdown_plan": f"Plan creation failed: {cmd_result.error}",
                            "structured_phases": [],
                            "plan_metadata": {"error": str(cmd_result.error), "failed": True},
                        }
                    elif command_name == "research_codebase":
                        results[command_name] = f"Research failed: {cmd_result.error}"
                    else:
                        results[command_name] = f"Command failed: {cmd_result.error}"

                # Track overall success
                if not cmd_result.success:
                    success = False
                    error_messages.append(f"{command_name}: {cmd_result.error}")

            total_time = (datetime.now() - start_time).total_seconds()

            return SequenceResult(
                success=success,
                results=results,
                commands_executed=commands_executed,
                error_messages=error_messages,
                total_time=total_time,
            )

        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Command sequence execution failed: {str(e)}"
            self.logger.error(error_msg)

            return SequenceResult(
                success=False,
                results=results,
                commands_executed=commands_executed,
                error_messages=[error_msg],
                total_time=total_time,
            )

    def get_orchestration_summary(self, result: OrchestrationResult) -> str:
        """Generate a summary of orchestration results for logging/debugging"""

        summary = f"""
Orchestration Summary: {result.sequence_name}
Status: {"✅ Success" if result.success else "❌ Failed"}
Total Time: {result.total_time:.2f}s
Commands Executed: {len(result.commands_executed)}

Command Details:
"""

        for cmd in result.commands_executed:
            status = "✅" if cmd.success else "❌"
            summary += f"  {status} {cmd.command_name} ({cmd.execution_time:.2f}s)\n"

        if result.error:
            summary += f"\nError: {result.error}"

        return summary.strip()

    async def orchestrate_execution_sequence(
        self,
        plan: str,
        cycle_context: str,
        cycle_results: list[Any],
        structured_phases: list[dict[str, Any]] | None = None,
        workspace_root: str | None = None,
    ) -> OrchestrationResult:
        """
        Orchestrate the complete execution sequence using CCE commands.

        This is the main execution flow that combines:
        1. Orientation with research and memory integration
        2. Implementation execution
        3. Reconciliation with evaluation and testing

        Args:
            plan: The current implementation plan
            cycle_context: Context about the current execution cycle
            cycle_results: Results from previous cycles
            workspace_root: Optional workspace root for execution tools

        Returns:
            OrchestrationResult with complete execution guidance and results
        """
        start_time = datetime.now()
        sequence_name = "execution_sequence"
        commands_executed = []

        try:
            self.logger.info(f"🚀 Starting complete execution sequence for cycle...")

            # Phase 1: Orientation with research and memory integration
            self.logger.info("📊 Phase 1: Command-driven orientation with research")
            orientation_result = await self.orchestrate_orientation_sequence(
                current_plan=plan,
                cycle_context=cycle_context,
                cycle_results=cycle_results,
                workspace_root=workspace_root,
            )
            commands_executed.extend(orientation_result.commands_executed)

            if not orientation_result.success:
                self.logger.warning(
                    f"Orientation failed, continuing with available context: {orientation_result.error}"
                )

            # Phase 2: Implementation execution (ENABLED FOR CODE CHANGES)
            self.logger.info("⚡ Phase 2: Command-driven implementation")
            implementation_context = f"""
            Plan: {plan[:1000]}
            Orientation: {orientation_result.final_result if orientation_result.success else "Orientation unavailable"}
            Cycle Context: {cycle_context}
            Previous Cycles: {len(cycle_results)} completed
            """

            # Use structured phases if available, otherwise fall back to full plan
            if structured_phases:
                self.logger.info(f"🔄 Using structured phases for implementation: {len(structured_phases)} phases")
                implement_result = await self.execute_command(
                    "implement_plan",
                    plan_content=plan,  # Still pass plan for context
                    structured_phases=structured_phases,  # Pass structured phases for focused execution
                    context=implementation_context,
                    cycle_number=len(cycle_results) + 1,
                    workspace_root=workspace_root,
                )
            else:
                self.logger.warning("⚠️ No structured phases available, using full plan content")
                implement_result = await self.execute_command(
                    "implement_plan",
                    plan_content=plan,
                    context=implementation_context,
                    cycle_number=len(cycle_results) + 1,
                    workspace_root=workspace_root,
                )
            commands_executed.append(implement_result)

            # Phase 3: Reconciliation with evaluation and testing
            self.logger.info("🔄 Phase 3: Command-driven reconciliation")

            # Create a mock cycle result for reconciliation
            class MockCycleResult:
                def __init__(self, implement_result):
                    self.status = "success" if implement_result.success else "failure"
                    self.final_thought = (
                        implement_result.result
                        if implement_result.success
                        else f"Implementation failed: {implement_result.error}"
                    )

            mock_cycle_result = MockCycleResult(implement_result)
            reconciliation_result = await self.orchestrate_reconciliation_sequence(
                cycle_result=mock_cycle_result,
                current_plan=plan,
            )
            commands_executed.extend(reconciliation_result.commands_executed)

            # Combine all results
            total_time = (datetime.now() - start_time).total_seconds()

            execution_summary = f"""
# Complete Execution Sequence Results

## Phase 1: Orientation
- Status: {"✅ Success" if orientation_result.success else "❌ Failed"}
- Result: {orientation_result.final_result[:500] if orientation_result.success else "Orientation failed"}

## Phase 2: Implementation  
- Status: {"✅ Success" if implement_result.success else "❌ Failed"}
- Result: {implement_result.result[:500] if implement_result.success else f"Implementation failed: {implement_result.error}"}

## Phase 3: Reconciliation
- Status: {"✅ Success" if reconciliation_result.success else "❌ Failed"}
- Result: {reconciliation_result.final_result}

## Overall Execution
- Total Commands Executed: {len(commands_executed)}
- Total Time: {total_time:.2f}s
- Overall Status: {"✅ Success" if all([orientation_result.success, implement_result.success, reconciliation_result.success]) else "❌ Failed"}
"""

            self.logger.info(f"✅ Complete execution sequence completed in {total_time:.2f}s")

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=orientation_result.success
                and implement_result.success
                and reconciliation_result.success,
                commands_executed=commands_executed,
                final_result=execution_summary,
                total_time=total_time,
            )

        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Execution sequence failed: {str(e)}"

            self.logger.error(error_msg)

            return OrchestrationResult(
                sequence_name=sequence_name,
                success=False,
                commands_executed=commands_executed,
                error=error_msg,
                total_time=total_time,
            )
