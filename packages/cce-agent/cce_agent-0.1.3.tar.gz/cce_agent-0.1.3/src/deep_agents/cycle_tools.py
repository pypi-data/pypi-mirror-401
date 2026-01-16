"""Tools for signaling execution cycle completion."""

from langchain_core.tools import tool


@tool
def signal_cycle_complete(
    summary: str,
    work_remaining: str = "",
    next_focus_suggestion: str = "",
    tests_run: str = "",
    issues_found: str = "",
    artifacts: str = "",
) -> str:
    """
    Signal that you are ready to end this execution cycle.

    Call this after completing wrap-up activities (tests, linting, polish).

    Args:
        summary: Brief summary of what you accomplished this cycle
        work_remaining: Any work that could not be completed this cycle
        next_focus_suggestion: Suggested focus for the next cycle
        tests_run: Tests run and results (optional)
        issues_found: Issues or risks identified (optional)
        artifacts: Artifacts or files changed (optional)

    Returns:
        Confirmation that the cycle end has been signaled
    """
    return "Cycle end signaled. Reconciliation will begin."


CYCLE_TOOLS = [signal_cycle_complete]
