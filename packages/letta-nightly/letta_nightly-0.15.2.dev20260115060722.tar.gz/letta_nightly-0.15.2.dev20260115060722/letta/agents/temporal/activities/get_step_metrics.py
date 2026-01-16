from temporalio import activity

from letta.agents.temporal.metrics import track_activity_metrics
from letta.agents.temporal.types import GetStepMetricsParams, GetStepMetricsResult
from letta.services.step_manager import StepManager


@activity.defn(name="get_step_metrics")
@track_activity_metrics
async def get_step_metrics(params: GetStepMetricsParams) -> GetStepMetricsResult:
    """
    Fetch existing step metrics from database (used in approval flows).

    When an approval response arrives, we need to retrieve the original step
    metrics that were created when the approval request was first made.
    This allows us to maintain accurate timing data across the approval roundtrip.

    Location in V3: line 490 of letta_agent_v3.py
    """
    step_manager = StepManager()

    # Fetch step metrics from database
    step_metrics = await step_manager.get_step_metrics_async(
        step_id=params.step_id,
        actor=params.actor,
    )

    return GetStepMetricsResult(step_metrics=step_metrics)
