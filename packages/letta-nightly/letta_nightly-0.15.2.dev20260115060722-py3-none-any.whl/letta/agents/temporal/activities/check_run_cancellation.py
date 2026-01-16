from temporalio import activity

from letta.agents.temporal.metrics import track_activity_metrics
from letta.agents.temporal.types import CheckRunCancellationParams, CheckRunCancellationResult
from letta.schemas.enums import RunStatus
from letta.services.run_manager import RunManager


@activity.defn(name="check_run_cancellation")
@track_activity_metrics
async def check_run_cancellation(params: CheckRunCancellationParams) -> CheckRunCancellationResult:
    """
    Check if a run has been cancelled by the client.

    This allows workflows to gracefully terminate when the user cancels
    a long-running agent execution. Workflows should check this at the
    start of each step iteration.

    Location in V3: lines 493-497 of letta_agent_v3.py

    Returns:
        CheckRunCancellationResult with is_cancelled=True if run status is cancelled
    """
    run_manager = RunManager()

    try:
        run = await run_manager.get_run_by_id(run_id=params.run_id, actor=params.actor)
        is_cancelled = run.status == RunStatus.cancelled
    except Exception as e:
        # Log but don't fail - if we can't check status, assume not cancelled
        activity.logger.warning(f"Failed to check run cancellation status for run {params.run_id}: {e}")
        is_cancelled = False

    return CheckRunCancellationResult(is_cancelled=is_cancelled)


# TODO: refactor above to shared function across letta_agent_v3 and this activity
