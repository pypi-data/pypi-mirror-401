from langchain_core.tools import tool

from src.graphs.open_swe_tools_graph import OpenSWEToolsGraph
from src.tools.openswe.code_tools import CodeTools

from ..graphs.aider_graph import AiderGraph
from .aider.wrapper import AiderctlWrapper
from .code_analyzer import CodeAnalyzer
from .edit_engine import EditEngine
from .git_ops import GitOps

# Import all Open SWE tools from the organized openswe package
from .openswe import (
    advanced_shell,
    apply_patch,
    command_safety_evaluator,
    conversation_history_summary,
    diagnose_error,
    execute_bash,
    get_url_content,
    # Development Tools
    grep_search,
    http_request,
    install_dependencies,
    mark_task_completed,
    mark_task_not_completed,
    open_pr,
    # GitHub Tools
    reply_to_review_comment,
    request_human_help,
    review_started,
    # Workflow Tools
    scratchpad,
    search_documents_for,
    session_plan,
    text_editor,
    update_plan,
    view,
    web_search,
    write_default_tsconfig,
    write_technical_notes,
)
from .shell_runner import ShellRunner


def create_langchain_tool_adapters(
    shell_runner: ShellRunner,
    edit_engine: EditEngine,
    git_ops: GitOps,
    code_analyzer: CodeAnalyzer,
    aider_wrapper: AiderctlWrapper,
    aider_graph: AiderGraph,
    code_tools: "CodeTools" = None,  # NEW
    open_swe_graph: "OpenSWEToolsGraph" = None,  # NEW
    include_aider_tools: bool = True,
) -> list:
    """Creates a list of LangChain-compatible tools from our internal services."""
    from .commands import (
        address_evaluation,
        commit_and_push,
        create_plan,
        evaluate_implementation,
        implement_plan,
        research_codebase,
        run_tests,
        update_plan,
    )

    try:
        from src.deep_agents.cycle_tools import signal_cycle_complete
    except ModuleNotFoundError:
        try:
            from ..deep_agents.cycle_tools import signal_cycle_complete
        except ModuleNotFoundError:
            signal_cycle_complete = None

    @tool
    def list_files(path: str = ".") -> str:
        """Lists files in a directory to understand the codebase structure."""
        return code_analyzer.list_files(path)

    @tool
    def read_file(file_path: str) -> str:
        """Reads the content of a specific file."""
        try:
            return edit_engine.env.read_file(file_path)
        except FileNotFoundError:
            return f"[ERROR] File not found: {file_path}"
        except Exception as exc:
            return f"[ERROR] Failed to read file {file_path}: {exc}"

    @tool
    async def run_aider_pipeline(
        instruction: str,
        target_files: list[str],
    ) -> str:
        """
        Runs the complete, stateful AIDER pipeline for a given instruction.
        This pipeline includes repo map generation, planning, human approval, editing, validation, and safe commit/rollback.
        Use this for any task that requires code modification.
        """
        final_state = await aider_graph.run(instruction, target_files)

        # The final_state is the full state dict from the last node
        if final_state.get("commit_hash"):
            commit_hash = final_state["commit_hash"]
            return f"Pipeline completed successfully. Commit hash: {commit_hash}"
        elif final_state.get("error_message"):
            return f"Pipeline failed with error: {final_state['error_message']}\nRollback status: {final_state.get('rollback_successful', 'N/A')}"
        else:
            # Check for rollback info if no commit or error
            if final_state.get("rollback_successful"):
                return f"Pipeline finished with a rollback. Reason: {final_state.get('reason', 'N/A')}"
            return "Pipeline finished without a commit. This might be due to a rejection or an unknown issue."

    @tool
    async def generate_repo_map() -> str:
        """
        Generates a repository map using aiderctl, providing a high-level overview
        of the codebase structure and symbols.
        """
        repo_map = await aider_wrapper.get_map(subtree="src")
        return repo_map or "Failed to generate repository map."

    @tool
    async def ask_about_codebase(question: str, files: list[str]) -> str:
        """
        Asks a question about the specified files in the codebase.
        This is a read-only operation and will not make any changes.
        """
        return await aider_wrapper.ask(question, files)

    @tool
    def check_git_status() -> str:
        """Checks the current git status of the repository."""
        return git_ops.git_status()

    @tool
    def view_git_diff() -> str:
        """Views the current git diff of the repository."""
        return git_ops.git_diff()

    @tool
    def execute_shell_command(command: str) -> str:
        """Executes a shell command. Use this for general-purpose tasks."""
        result = shell_runner.execute(command)
        return f"Exit: {result.exit_code}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Individual AIDER Command Tools
    # These provide granular control over specific aiderctl operations

    @tool
    async def aider_architect(instruction: str, files: list[str]) -> str:
        """
        Uses AIDER's architect mode for complex multi-file redesigns and architecture analysis.
        This is ideal for high-level structural changes, refactoring, and architectural planning.

        Args:
            instruction: The architectural instruction or question
            files: List of files to analyze or modify

        Returns:
            The architectural analysis or modification results
        """
        try:
            result = await aider_wrapper.edit(message=instruction, files=files, mode="architect")
            return f"Architecture analysis completed:\n{result}"
        except Exception as e:
            return f"Architect command failed: {str(e)}"

    @tool
    async def aider_edit(instruction: str, files: list[str]) -> str:
        """
        Uses AIDER's edit mode for targeted code modifications.
        This is ideal for specific code changes, bug fixes, and feature implementations.

        Args:
            instruction: The specific code modification instruction
            files: List of files to modify

        Returns:
            The edit results and any generated patches
        """
        try:
            result = await aider_wrapper.edit(message=instruction, files=files, mode="edit")
            return f"Edit completed:\n{result}"
        except Exception as e:
            return f"Edit command failed: {str(e)}"

    @tool
    async def aider_lint() -> str:
        """
        Runs AIDER's linting validation on the current codebase.
        This provides standalone linting without modifying any files.

        Returns:
            Linting results and any issues found
        """
        try:
            success, output = await aider_wrapper.lint()
            status = "PASSED" if success else "FAILED"
            return f"Linting {status}:\n{output}"
        except Exception as e:
            return f"Lint command failed: {str(e)}"

    @tool
    async def aider_test() -> str:
        """
        Runs AIDER's test execution on the current codebase.
        This provides standalone test execution without modifying any files.

        Returns:
            Test results and any failures
        """
        try:
            success, output = await aider_wrapper.test()
            status = "PASSED" if success else "FAILED"
            return f"Testing {status}:\n{output}"
        except Exception as e:
            return f"Test command failed: {str(e)}"

    base_tools = [
        list_files,
        read_file,
        check_git_status,
        view_git_diff,
        execute_shell_command,
    ]

    if include_aider_tools:
        base_tools.extend(
            [
                run_aider_pipeline,
                generate_repo_map,
                ask_about_codebase,
                aider_architect,
                aider_edit,
                aider_lint,
                aider_test,
            ]
        )

    # Store the tools list for potential extension
    tools = [
        *base_tools,
        # CCE Commands Integration
        research_codebase,
        create_plan,
        update_plan,
        implement_plan,
        evaluate_implementation,
        address_evaluation,
        run_tests,
        commit_and_push,
        # Open SWE Tools Integration (Organized)
        # Core Tools
        execute_bash,
        http_request,
        web_search,
        # File Tools
        text_editor,
        view,
        apply_patch,
        write_default_tsconfig,
        # Development Tools
        grep_search,
        install_dependencies,
        advanced_shell,
        command_safety_evaluator,
        # Web Tools
        get_url_content,
        search_documents_for,
        # Workflow Tools
        scratchpad,
        request_human_help,
        session_plan,
        mark_task_completed,
        mark_task_not_completed,
        diagnose_error,
        write_technical_notes,
        conversation_history_summary,
        # GitHub Tools
        reply_to_review_comment,
        open_pr,
        review_started,
    ]

    if signal_cycle_complete is not None:
        tools.append(signal_cycle_complete)

    # NEW: Add native execution tools if available
    if code_tools is not None and open_swe_graph is not None:
        try:
            # Import here to avoid circular imports
            from langchain_core.tools import tool as langchain_tool

            @langchain_tool
            def run_native_pipeline(instruction: str, target_files: list, auto_approve: bool = True) -> str:
                """Run the native OpenSWE tools execution pipeline."""
                try:
                    import asyncio

                    result = asyncio.run(open_swe_graph.run(instruction, target_files, auto_approve))
                    return f"Native pipeline completed: {result}"
                except Exception as e:
                    return f"Native pipeline failed: {str(e)}"

            @langchain_tool
            def propose_diff_native(goal: str, files: list, response_format: str = "concise") -> str:
                """Generate a diff using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.propose_diff(goal, files, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Diff generation failed: {str(e)}"

            @langchain_tool
            def apply_patch_native(diff_path: str, response_format: str = "concise") -> str:
                """Apply a patch using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.apply_patch(diff_path, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Patch application failed: {str(e)}"

            @langchain_tool
            def lint_native(paths: list = None, response_format: str = "concise") -> str:
                """Run linting using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.lint(paths, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Linting failed: {str(e)}"

            @langchain_tool
            def test_native(cmd: str = None, response_format: str = "concise") -> str:
                """Run tests using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.test(cmd, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Testing failed: {str(e)}"

            @langchain_tool
            def grep_native(pattern: str, paths: list = None, response_format: str = "concise") -> str:
                """Search for patterns using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.grep(pattern, paths, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Grep search failed: {str(e)}"

            @langchain_tool
            def read_file_native(path: str, response_format: str = "concise") -> str:
                """Read a file using native CodeTools operations."""
                try:
                    import asyncio

                    result = asyncio.run(code_tools.read_file(path, response_format=response_format))
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"File read failed: {str(e)}"

            @langchain_tool
            def propose_diff_with_context(
                goal: str, files: list = None, policy: str = "conservative", response_format: str = "concise"
            ) -> str:
                """Generate context-aware diff using repository indexer."""
                try:
                    import asyncio

                    result = asyncio.run(
                        code_tools.propose_diff_with_context(
                            goal, files, policy=policy, response_format=response_format
                        )
                    )
                    return f"Status: {result.status}\nResult: {result.result}"
                except Exception as e:
                    return f"Context-aware diff generation failed: {str(e)}"

            @langchain_tool
            def build_repo_index(force_rebuild: bool = False) -> str:
                """Build comprehensive repository index for advanced code analysis."""
                try:
                    import asyncio

                    from src.tools.repo_indexer import get_repo_indexer

                    indexer = get_repo_indexer()
                    index = asyncio.run(indexer.build_index(force_rebuild=force_rebuild))
                    return f"Repository index built: {index.total_files} files, {index.total_symbols} symbols, {len(index.languages)} languages"
                except Exception as e:
                    return f"Repository indexing failed: {str(e)}"

            @langchain_tool
            def query_symbols(query: str, kind: str = "all", max_results: int = 20) -> str:
                """Query symbols in the repository index."""
                try:
                    from src.tools.repo_indexer import get_repo_indexer

                    indexer = get_repo_indexer()
                    matches = indexer.query_symbols(query, kind=kind, max_results=max_results)
                    if not matches:
                        return f"No symbols found for query: {query}"

                    result_lines = [f"Found {len(matches)} symbols for '{query}':"]
                    for match in matches[:max_results]:
                        result_lines.append(
                            f"- {match.symbol_name} ({match.symbol_type}) in {match.file_path}:{match.line_number}"
                        )

                    return "\n".join(result_lines)
                except Exception as e:
                    return f"Symbol query failed: {str(e)}"

            @langchain_tool
            def validate_code_comprehensive(files: list, include_tests: bool = True) -> str:
                """Run comprehensive validation pipeline on files."""
                try:
                    import asyncio

                    from src.tools.validation_pipeline import get_validation_pipeline

                    pipeline = get_validation_pipeline()
                    result = asyncio.run(pipeline.validate_all(files, include_tests=include_tests))

                    summary = (
                        f"Validation complete: {result.errors} errors, {result.warnings} warnings, {result.info} info"
                    )
                    if result.issues:
                        summary += "\n\nIssues found:"
                        for issue in result.issues[:10]:  # Show first 10 issues
                            summary += f"\n- {issue.severity.upper()}: {issue.message} in {issue.file_path}"
                            if issue.line_number:
                                summary += f":{issue.line_number}"

                    return summary
                except Exception as e:
                    return f"Comprehensive validation failed: {str(e)}"

            # Add native tools to the list
            tools.extend(
                [
                    run_native_pipeline,
                    propose_diff_native,
                    apply_patch_native,
                    lint_native,
                    test_native,
                    grep_native,
                    read_file_native,
                    # Advanced Phase 5 features
                    propose_diff_with_context,
                    build_repo_index,
                    query_symbols,
                    validate_code_comprehensive,
                ]
            )
        except Exception as e:
            print(f"Error adding native tools: {e}")
            import traceback

            print(f"Traceback: {traceback.format_exc()}")

    return tools
