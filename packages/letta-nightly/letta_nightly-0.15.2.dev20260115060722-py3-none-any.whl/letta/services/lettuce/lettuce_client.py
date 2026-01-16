import os
import uuid

from temporalio.client import Client
from temporalio.common import SearchAttributeKey, SearchAttributePair, TypedSearchAttributes

from letta.agents.temporal.metrics import WorkflowMetrics
from letta.agents.temporal.temporal_agent_workflow import TemporalAgentWorkflow
from letta.agents.temporal.temporal_letta_v1_agent_workflow import TemporalLettaV1AgentWorkflow
from letta.agents.temporal.types import UploadFileToFolderParams, WorkflowInputParams
from letta.agents.temporal.upload_file_workflow import UploadFileToFolderWorkflow
from letta.constants import DEFAULT_MAX_STEPS
from letta.schemas.agent import AgentState
from letta.schemas.enums import AgentType, DuplicateFileHandling
from letta.schemas.letta_message import MessageType
from letta.schemas.message import MessageCreate
from letta.schemas.user import User


class LettuceClient:
    """Client class for Lettuce service."""

    def __init__(self):
        """Initialize the LettuceClient."""
        self.temporal_tls = os.getenv("LETTA_TEMPORAL_TLS", "true").lower() in (
            "true",
            "1",
        )
        self.temporal_api_key = os.getenv("LETTA_TEMPORAL_API_KEY")
        self.temporal_namespace = os.getenv("LETTA_TEMPORAL_NAMESPACE")
        self.temporal_endpoint = os.getenv("LETTA_TEMPORAL_ENDPOINT")
        self.temporal_task_queue = os.getenv("LETTA_TEMPORAL_TASK_QUEUE", "agent_loop_async_task_queue")
        self.temporal_skip_custom_sa = os.getenv("LETTA_TEMPORAL_SKIP_CUSTOM_SA")
        self.client: Client | None = None

    @classmethod
    async def create(cls) -> "LettuceClient":
        """
        Asynchronously creates and connects the temporal client.

        Returns:
            LettuceClient: The created LettuceClient instance.
        """
        instance = cls()
        if instance.temporal_api_key and instance.temporal_endpoint:
            instance.client = await Client.connect(
                instance.temporal_endpoint,
                namespace=instance.temporal_namespace,
                api_key=instance.temporal_api_key,
                tls=instance.temporal_tls,
            )
        else:
            instance.client = await Client.connect(
                instance.temporal_endpoint,
                namespace=instance.temporal_namespace,
                tls=instance.temporal_tls,
            )
        return instance

    def get_client(self) -> Client | None:
        """
        Get the temporal client, if connected.

        Returns:
            Client | None: The temporal client, if connected.
        """
        return self.client

    async def get_status(self, run_id: str) -> str | None:
        """
        Get the status of a run.

        Args:
            run_id (str): The ID of the run.

        Returns:
            str | None: The status of the run or None if not available.
        """
        if not self.client:
            return None

        handle = self.client.get_workflow_handle(run_id)
        desc = await handle.describe()
        return desc.status.name

    async def cancel(self, run_id: str) -> str | None:
        """
        Cancel a run.

        Args:
            run_id (str): The ID of the run to cancel.

        Returns:
            str | None: The ID of the canceled run or None if not available.
        """
        if not self.client:
            return None

        await self.client.cancel_workflow(run_id)

    async def step(
        self,
        agent_state: AgentState,
        actor: User,
        input_messages: list[MessageCreate],
        max_steps: int = DEFAULT_MAX_STEPS,
        run_id: str | None = None,
        use_assistant_message: bool = True,
        include_return_message_types: list[MessageType] | None = None,
        request_start_timestamp_ns: int | None = None,
    ) -> str | None:
        """
        Execute the agent loop on temporal.

        Args:
            agent_state (AgentState): The state of the agent.
            actor (User): The actor.
            input_messages (list[MessageCreate]): The input messages.
            max_steps (int, optional): The maximum number of steps. Defaults to DEFAULT_MAX_STEPS.
            run_id (str | None, optional): The ID of the run. Defaults to None.
            use_assistant_message (bool, optional): Whether to use the assistant message. Defaults to True.
            include_return_message_types (list[MessageType] | None, optional): The message types to include in the return. Defaults to None.
            request_start_timestamp_ns (int | None, optional): The start timestamp of the request. Defaults to None.

        Returns:
            str | None: The ID of the run or None if client is not available.
        """
        if not self.client:
            return None

        workflow_input = WorkflowInputParams(
            agent_state=agent_state,
            messages=input_messages,
            actor=actor,
            max_steps=max_steps,
            run_id=run_id,
        )

        if agent_state.agent_type == AgentType.letta_v1_agent:
            workflow_to_run = TemporalLettaV1AgentWorkflow.run
            workflow_name = "TemporalLettaV1AgentWorkflow"
        else:
            workflow_to_run = TemporalAgentWorkflow.run
            workflow_name = "TemporalAgentWorkflow"

        #
        custom_search_attributes = []
        if not self.temporal_skip_custom_sa:
            organization_id = actor.organization_id
            user_id = actor.id
            agent_id = agent_state.id
            custom_search_attributes = [
                SearchAttributePair(SearchAttributeKey.for_keyword("OrganizationId"), organization_id),
                SearchAttributePair(SearchAttributeKey.for_keyword("AgentId"), agent_id),
                SearchAttributePair(SearchAttributeKey.for_keyword("UserId"), user_id),
            ]

        await self.client.start_workflow(
            workflow_to_run,
            workflow_input,
            id=run_id,
            task_queue=self.temporal_task_queue,
            search_attributes=TypedSearchAttributes(custom_search_attributes),
        )

        WorkflowMetrics.record_workflow_enqueued(workflow_name, run_id)

        return run_id

    async def upload_file_to_folder(
        self,
        *,
        folder_id: str,
        actor_id: str,
        file_name: str,
        content: bytes,
        content_type: str | None = None,
        duplicate_handling: DuplicateFileHandling | None = None,
        override_name: str | None = None,
    ):
        """Execute the single-activity upload workflow and return its result.

        Returns the UploadFileToFolderResult (with file_metadata and skipped flag)
        or None if client is unavailable.
        """
        if not self.client:
            return None

        params = UploadFileToFolderParams(
            folder_id=folder_id,
            actor_id=actor_id,
            file_name=file_name,
            content=content,
            content_type=content_type,
            # The dataclass already defaults to SUFFIX if None
            duplicate_handling=duplicate_handling if duplicate_handling is not None else DuplicateFileHandling.SUFFIX,
            override_name=override_name,
        )

        workflow_id = f"upload-{folder_id}-{uuid.uuid4()}"
        result = await self.client.execute_workflow(
            UploadFileToFolderWorkflow.run,
            params,
            id=workflow_id,
            task_queue=self.temporal_task_queue,
        )

        WorkflowMetrics.record_workflow_enqueued("UploadFileToFolderWorkflow", workflow_id)

        return result
