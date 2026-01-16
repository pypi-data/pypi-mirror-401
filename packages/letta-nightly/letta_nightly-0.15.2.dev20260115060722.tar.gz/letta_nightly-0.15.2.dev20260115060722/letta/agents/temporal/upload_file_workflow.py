from temporalio import workflow

# Import activity and types through passthrough for workflow sandbox compatibility
with workflow.unsafe.imports_passed_through():
    from letta.agents.temporal.activities.upload_file_to_folder import (
        upload_file_to_folder_activity,
    )
    from letta.agents.temporal.metrics import WorkflowMetrics
    from letta.agents.temporal.types import UploadFileToFolderParams, UploadFileToFolderResult
    from letta.log import get_logger


logger = get_logger(__name__)


def get_workflow_time_ns() -> int:
    return int(workflow.now().timestamp() * 1e9)


@workflow.defn
class UploadFileToFolderWorkflow:
    @workflow.run
    async def run(self, params: UploadFileToFolderParams) -> UploadFileToFolderResult:
        workflow_type = self.__class__.__name__
        workflow_id = workflow.info().workflow_id
        start_ns = get_workflow_time_ns()

        WorkflowMetrics.record_workflow_start(workflow_type, workflow_id)

        try:
            # Execute single activity that does everything
            result: UploadFileToFolderResult = await workflow.execute_activity(
                upload_file_to_folder_activity,
                params,
                start_to_close_timeout=workflow.timedelta(minutes=30),
                schedule_to_close_timeout=workflow.timedelta(hours=1),
            )

            duration_ns = get_workflow_time_ns() - start_ns
            WorkflowMetrics.record_workflow_success(workflow_type, workflow_id, duration_ns)
            return result
        except Exception as e:
            duration_ns = get_workflow_time_ns() - start_ns
            WorkflowMetrics.record_workflow_failure(
                workflow_type,
                workflow_id,
                type(e).__name__,
                duration_ns,
            )
            raise
