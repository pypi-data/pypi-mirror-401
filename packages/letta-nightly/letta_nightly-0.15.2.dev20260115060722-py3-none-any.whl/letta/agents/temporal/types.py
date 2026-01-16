from dataclasses import dataclass
from typing import Dict, List, Optional

from letta.helpers import ToolRulesSolver
from letta.schemas.agent import AgentState
from letta.schemas.enums import DuplicateFileHandling, RunStatus
from letta.schemas.file import FileMetadata
from letta.schemas.letta_message import LettaMessageUnion, MessageType
from letta.schemas.letta_message_content import (
    OmittedReasoningContent,
    ReasoningContent,
    RedactedReasoningContent,
    TextContent,
)
from letta.schemas.letta_stop_reason import LettaStopReason, StopReasonType
from letta.schemas.message import Message, MessageCreate
from letta.schemas.openai.chat_completion_response import ToolCall, UsageStatistics
from letta.schemas.step import Step
from letta.schemas.step_metrics import StepMetrics
from letta.schemas.tool_execution_result import ToolExecutionResult
from letta.schemas.usage import LettaUsageStatistics
from letta.schemas.user import User


@dataclass
class WorkflowInputParams:
    agent_state: AgentState
    messages: list[MessageCreate]
    actor: User
    max_steps: int
    run_id: str
    use_assistant_message: bool = True
    include_return_message_types: list[MessageType] | None = None


@dataclass
class PreparedMessages:
    in_context_messages: List[Message]
    input_messages_to_persist: List[Message]


@dataclass
class FinalResult:
    messages: List[LettaMessageUnion]
    stop_reason: str
    usage: LettaUsageStatistics


@dataclass
class InnerStepResult:
    """Result from a single inner_step execution."""

    stop_reason: StopReasonType
    usage: LettaUsageStatistics
    should_continue: bool
    response_messages: List[Message]
    agent_state: AgentState


# ===== Additional types for activities up to _handle_ai_response =====


@dataclass
class RefreshContextParams:
    """Input to refresh_context_and_system_message activity.

    - agent_state: Current agent state (memory, sources, tools, etc.)
    - in_context_messages: Current message history to potentially rebuild/scrub
    - actor: Requesting user (for DB access control)
    """

    agent_state: AgentState
    in_context_messages: List[Message]
    tool_rules_solver: ToolRulesSolver
    actor: User


@dataclass
class RefreshContextResult:
    """Output from refresh_context_and_system_message activity.

    - messages: Updated in-context messages with refreshed system message
    - agent_state: Updated agent state with refreshed memory
    """

    messages: List[Message]
    agent_state: AgentState


@dataclass
class LLMRequestParams:
    """Input to llm_request activity.

    - agent_state: Needed primarily for llm_config (model, endpoint, etc.)
    - messages: Full prompt messages (context + input + responses if any)
    - allowed_tools: Tools JSON schema list after rules + strict mode + runtime overrides
    - force_tool_call: Optional tool name to force call when only one valid tool exists
    - requires_approval_tools: Optional list of tool names that require approval
    - actor: Requesting user (for audit/tenant context)
    - step_id: Current step id for tracing/telemetry correlation
    - use_assistant_message: Whether to use assistant message format for responses
    """

    agent_state: AgentState
    messages: List[Message]
    allowed_tools: List[dict]
    force_tool_call: Optional[str] = None
    requires_approval_tools: Optional[List[str]] = None
    actor: Optional[User] = None
    step_id: Optional[str] = None
    use_assistant_message: bool = True


@dataclass
class LLMCallResult:
    """Output from llm_request activity.

    - tool_call: Parsed tool call from LLM (None for stub/approval paths)
    - reasoning_content: Optional reasoning/assistant content stream collected
    - assistant_message_id: Optional precomputed assistant message id (if adapter sets)
    - usage: Provider usage statistics for this call
    - request_finish_ns: Provider request finish time (ns) for metrics, if available
    - llm_request_start_ns: Start time of LLM request in nanoseconds
    - llm_request_ns: Duration of LLM request in nanoseconds
    """

    tool_call: Optional[ToolCall]
    reasoning_content: Optional[List[TextContent | ReasoningContent | RedactedReasoningContent | OmittedReasoningContent]]
    assistant_message_id: Optional[str]
    usage: UsageStatistics
    request_finish_ns: Optional[int]
    llm_request_start_ns: Optional[int] = None
    llm_request_ns: Optional[int] = None


@dataclass
class SummarizeParams:
    """Input to summarize_conversation_history activity.

    - agent_state: Current agent state (summarizer config, ids)
    - in_context_messages: Current context window
    - new_letta_messages: Newly generated/persisted messages to consider
    - actor: Requesting user
    - force: Whether to force summarization + clear
    """

    agent_state: AgentState
    in_context_messages: List[Message]
    new_letta_messages: List[Message]
    actor: User
    force: bool = True


# ===== Tool execution and message handling types =====


@dataclass
class ExecuteToolParams:
    """Input to execute_tool_activity.

    - tool_name: Name of the tool to execute
    - tool_args: Arguments to pass to the tool
    - agent_state: Current agent state containing tools and configuration
    - actor: Requesting user for access control
    - step_id: Current step ID for tracing
    """

    tool_name: str
    tool_args: Dict
    agent_state: AgentState
    actor: User
    step_id: Optional[str]


@dataclass
class ExecuteToolResult:
    """Output from execute_tool_activity."""

    tool_execution_result: ToolExecutionResult
    execution_time_ns: int


@dataclass
class CreateStepParams:
    """Input to create_step_activity."""

    agent_state: AgentState
    messages: List[Message]
    actor: User
    run_id: str
    step_id: Optional[str]
    usage: UsageStatistics
    step_ns: Optional[int] = None
    llm_request_ns: Optional[int] = None
    tool_execution_ns: Optional[int] = None
    stop_reason: Optional[str] = None


@dataclass
class CreateStepResult:
    """Output from create_step_activity."""

    step: Step


@dataclass
class CreateMessagesParams:
    """Input to create_messages_activity.

    Persists messages to the database.
    """

    messages: List[Message]
    actor: User
    project_id: Optional[str]
    template_id: Optional[str]


@dataclass
class CreateMessagesResult:
    """Output from create_messages_activity."""

    messages: List[Message]


@dataclass
class PersistMessagesParams:
    """Input to persist_messages_activity.

    Persists messages to database and optionally updates job messages.
    """

    messages: List[Message]
    actor: User
    project_id: Optional[str]
    template_id: Optional[str]
    run_id: Optional[str]


@dataclass
class PersistMessagesResult:
    """Output from persist_messages_activity."""


@dataclass
class UpdateRunParams:
    """Input to update_run_activity."""

    run_id: str
    actor: User
    run_status: RunStatus
    stop_reason: LettaStopReason | None
    persisted_messages: List[Message]
    usage: LettaUsageStatistics
    total_duration_ns: int | None


@dataclass
class UpdateMessageIdsParams:
    """Input to update_message_ids_activity.

    Updates the agent's message IDs in the database.
    Used for immediate approval persistence to prevent bad state.
    """

    agent_id: str
    message_ids: List[str]
    actor: User


@dataclass
class UpdateMessageIdsResult:
    """Output from update_message_ids_activity."""

    success: bool
    agent_state: AgentState
    persisted_messages: List[Message]


# ===== File upload to folder =====


@dataclass
class UploadFileToFolderParams:
    """Input to upload_file_to_folder_activity.

    - folder_id: ID of the folder (source) to upload into
    - actor_id: Acting user ID
    - file_name: Original file name
    - content: Raw file bytes
    - content_type: Optional content-type header value
    - duplicate_handling: How to handle duplicate filenames
    - override_name: Optional override for the stored original filename
    """

    folder_id: str
    actor_id: str
    file_name: str
    content: bytes
    content_type: Optional[str] = None
    duplicate_handling: DuplicateFileHandling = DuplicateFileHandling.SUFFIX
    override_name: Optional[str] = None


@dataclass
class UploadFileToFolderResult:
    """Output from upload_file_to_folder_activity."""

    file_metadata: FileMetadata
    skipped: bool = False


# ===== V3 workflow activities =====


@dataclass
class GetStepMetricsParams:
    """Input to get_step_metrics activity.

    Used in approval flows to retrieve existing step metrics from the database.
    Location in V3: line 490 of letta_agent_v3.py
    """

    step_id: str
    actor: User


@dataclass
class GetStepMetricsResult:
    """Output from get_step_metrics activity."""

    step_metrics: StepMetrics


@dataclass
class CheckRunCancellationParams:
    """Input to check_run_cancellation activity.

    Checks if a run has been cancelled by the client.
    Location in V3: lines 493-497 of letta_agent_v3.py
    """

    run_id: str
    actor: User


@dataclass
class CheckRunCancellationResult:
    """Output from check_run_cancellation activity."""

    is_cancelled: bool


@dataclass
class LLMRequestParamsV3:
    """Input to llm_request_v3 activity - enhanced for V3 features.

    V3 enhancements:
    - requires_subsequent_tool_call: Whether to require a tool call (V3 allows content-only)
    - tool_return_truncation_chars: Dynamic truncation limit for tool returns
    - enable_parallel_tool_calls: Whether to enable parallel tool calling

    Location in V3: lines 507-515 of letta_agent_v3.py
    """

    agent_state: AgentState
    messages: List[Message]
    allowed_tools: List[dict]
    force_tool_call: Optional[str] = None
    requires_subsequent_tool_call: bool = False  # V3: Not required by default
    requires_approval_tools: Optional[List[str]] = None
    tool_return_truncation_chars: Optional[int] = None  # V3: Dynamic truncation
    enable_parallel_tool_calls: bool = False  # V3: Parallel tool calling support
    actor: Optional[User] = None
    step_id: Optional[str] = None
    use_assistant_message: bool = True


@dataclass
class LLMCallResultV3:
    """Output from llm_request_v3 activity - enhanced for V3 features.

    V3 enhancements:
    - tool_calls: List of tool calls (supports parallel execution)
    - content: Combined reasoning + text content (reasoning prepended if present)
      Matches the adapter pattern from simple_llm_request_adapter.py:75

    Location in V3: lines 607-612, 625 of letta_agent_v3.py
    """

    tool_calls: List[ToolCall]  # V3: Multiple tool calls
    content: Optional[
        List[TextContent | ReasoningContent | RedactedReasoningContent | OmittedReasoningContent]
    ]  # V3: Combined content with reasoning prepended
    assistant_message_id: Optional[str]
    usage: UsageStatistics
    request_finish_ns: Optional[int]
    llm_request_start_ns: Optional[int] = None
    llm_request_ns: Optional[int] = None
