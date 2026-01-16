import asyncio
import json
import uuid
from datetime import timedelta
from typing import Any, Dict, List, Optional, Tuple

from temporalio import workflow
from temporalio.exceptions import ApplicationError

from letta.agents.helpers import (
    _build_rule_violation_result,
    _load_last_function_response,
    _maybe_get_approval_messages,
    _maybe_get_pending_tool_call_message,
    _safe_load_tool_call_str,
    generate_step_id,
    merge_and_validate_prefilled_args,
)
from letta.agents.temporal.activities import (
    check_run_cancellation,
    create_messages,
    create_step,
    execute_tool,
    get_step_metrics,
    llm_request_v3,
    prepare_messages,
    refresh_context_and_system_message,
    summarize_conversation_history,
    update_message_ids,
    update_run,
)
from letta.agents.temporal.constants import (
    CREATE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    CREATE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    CREATE_STEP_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    CREATE_STEP_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    LLM_ACTIVITY_RETRY_POLICY,
    PREPARE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    PREPARE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    REFRESH_CONTEXT_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    REFRESH_CONTEXT_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    SUMMARIZE_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    SUMMARIZE_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    TOOL_EXECUTION_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    TOOL_EXECUTION_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    UPDATE_MESSAGE_IDS_ACTIVITY_START_TO_CLOSE_TIMEOUT,
    UPDATE_RUN_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
    UPDATE_RUN_ACTIVITY_START_TO_CLOSE_TIMEOUT,
)
from letta.agents.temporal.types import (
    CheckRunCancellationParams,
    CheckRunCancellationResult,
    CreateMessagesParams,
    CreateMessagesResult,
    CreateStepParams,
    CreateStepResult,
    ExecuteToolParams,
    ExecuteToolResult,
    FinalResult,
    GetStepMetricsParams,
    GetStepMetricsResult,
    LLMCallResultV3,
    LLMRequestParamsV3,
    PreparedMessages,
    RefreshContextParams,
    RefreshContextResult,
    SummarizeParams,
    UpdateMessageIdsParams,
    UpdateRunParams,
    WorkflowInputParams,
)
from letta.constants import NON_USER_MSG_PREFIX, REQUEST_HEARTBEAT_PARAM, SUMMARIZATION_TRIGGER_MULTIPLIER
from letta.errors import ContextWindowExceededError
from letta.helpers import ToolRulesSolver
from letta.helpers.datetime_helpers import get_utc_timestamp_ns
from letta.helpers.tool_execution_helper import enable_strict_mode
from letta.local_llm.constants import INNER_THOUGHTS_KWARG
from letta.schemas.agent import AgentState
from letta.schemas.enums import RunStatus, StepStatus
from letta.schemas.letta_stop_reason import LettaStopReason, StopReasonType
from letta.schemas.message import ApprovalReturn, Message, ToolReturn
from letta.schemas.openai.chat_completion_response import ToolCall, ToolCallDenial, UsageStatistics
from letta.schemas.tool_execution_result import ToolExecutionResult
from letta.schemas.usage import LettaUsageStatistics
from letta.server.rest_api.utils import (
    create_approval_request_message_from_llm_response,
    create_heartbeat_system_message,
    create_letta_messages_from_llm_response,
    create_parallel_tool_messages_from_llm_response,
)
from letta.services.helpers.tool_parser_helper import runtime_override_tool_json_schema
from letta.settings import summarizer_settings
from letta.system import package_function_response
from letta.utils import validate_function_response


@workflow.defn
class TemporalLettaV1AgentWorkflow:
    """
    Temporal workflow for LettaAgentV3 - simplified loop with tool-call-based continuation.

    Mirrors: letta_agent_v3.py

    V3 Key Features:
    1. No heartbeat mechanism - tool calls = continue
    2. Content-only responses allowed
    3. Proactive summarization
    4. Dynamic truncation
    """

    @workflow.run
    async def run(self, params: WorkflowInputParams) -> FinalResult:
        """
        Main workflow entry point - mirrors letta_agent_v3.py::step() (lines 92-191).

        Executes the agent loop, handling tool execution and context management.
        """
        # Initialize state (line 115 in V3)
        usage = LettaUsageStatistics()
        response_messages: list[Message] = []
        last_step_usage: Optional[LettaUsageStatistics] = None
        stop_reason: Optional[LettaStopReason] = None
        tool_rules_solver = ToolRulesSolver(tool_rules=params.agent_state.tool_rules)

        try:
            # Prepare messages (lines 118-121 in V3)
            prepared: PreparedMessages = await workflow.execute_activity(
                prepare_messages,
                params,
                start_to_close_timeout=PREPARE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                schedule_to_close_timeout=PREPARE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )

            combined_messages = prepared.in_context_messages + prepared.input_messages_to_persist
            input_messages_to_persist = prepared.input_messages_to_persist

            # Main stepping loop (lines 123-162 in V3)
            for step_index in range(params.max_steps):
                # Execute single step
                step_result = await self._step(
                    messages=combined_messages + response_messages,
                    input_messages_to_persist=input_messages_to_persist,
                    agent_state=params.agent_state,
                    tool_rules_solver=tool_rules_solver,
                    run_id=params.run_id,
                    step_index=step_index,
                    max_steps=params.max_steps,
                    actor=params.actor,
                )

                # Update state
                response_messages.extend(step_result["response_messages"])
                usage.completion_tokens += step_result["usage"].completion_tokens
                usage.prompt_tokens += step_result["usage"].prompt_tokens
                usage.total_tokens += step_result["usage"].total_tokens
                # Aggregate cache and reasoning token fields (handle None defaults)
                step_usage = step_result["usage"]
                if step_usage.cached_input_tokens is not None:
                    usage.cached_input_tokens = (usage.cached_input_tokens or 0) + step_usage.cached_input_tokens
                if step_usage.cache_write_tokens is not None:
                    usage.cache_write_tokens = (usage.cache_write_tokens or 0) + step_usage.cache_write_tokens
                if step_usage.reasoning_tokens is not None:
                    usage.reasoning_tokens = (usage.reasoning_tokens or 0) + step_usage.reasoning_tokens
                last_step_usage = step_result["usage"]
                should_continue = step_result["should_continue"]
                stop_reason = step_result.get("stop_reason")

                # V3 FEATURE: Proactive summarization (lines 138-157 in V3)
                if (
                    last_step_usage
                    and last_step_usage.total_tokens > params.agent_state.llm_config.context_window * SUMMARIZATION_TRIGGER_MULTIPLIER
                    and not params.agent_state.message_buffer_autoclear
                ):
                    workflow.logger.warning(
                        f"Step usage ({last_step_usage.total_tokens} tokens) approaching "
                        f"context limit ({params.agent_state.llm_config.context_window}), triggering summarization."
                    )

                    # Summarize during loop (not just at end)
                    summarize_result = await workflow.execute_activity(
                        summarize_conversation_history,
                        SummarizeParams(
                            agent_state=params.agent_state,
                            in_context_messages=combined_messages,
                            new_letta_messages=response_messages,
                            actor=params.actor,
                            force=True,
                        ),
                        start_to_close_timeout=SUMMARIZE_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                        schedule_to_close_timeout=SUMMARIZE_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                    )
                    combined_messages = summarize_result
                    response_messages = []  # Clear after summarization

                # Check stop condition
                if not should_continue:
                    break

                input_messages_to_persist = []  # Reset for next iteration

            # Post-loop summarization (lines 165-177 in V3)
            if not params.agent_state.message_buffer_autoclear and last_step_usage:
                await workflow.execute_activity(
                    summarize_conversation_history,
                    SummarizeParams(
                        agent_state=params.agent_state,
                        in_context_messages=combined_messages,
                        new_letta_messages=response_messages,
                        actor=params.actor,
                        force=False,
                    ),
                    start_to_close_timeout=SUMMARIZE_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                    schedule_to_close_timeout=SUMMARIZE_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                )

            # Finalize (lines 179-191 in V3)
            if stop_reason is None:
                stop_reason = LettaStopReason(stop_reason=StopReasonType.end_turn.value)

            await workflow.execute_activity(
                update_run,
                UpdateRunParams(
                    run_id=params.run_id,
                    actor=params.actor,
                    run_status=RunStatus.completed,
                    stop_reason=stop_reason,
                    persisted_messages=response_messages,
                    usage=usage,
                    total_duration_ns=None,
                ),
                start_to_close_timeout=UPDATE_RUN_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                schedule_to_close_timeout=UPDATE_RUN_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )

            # Convert messages to letta format for response
            from letta.schemas.letta_message import LettaMessageUnion

            letta_messages: list[LettaMessageUnion] = []
            for msg in response_messages:
                letta_messages.extend(msg.to_letta_messages())

            return FinalResult(
                messages=letta_messages,
                stop_reason=stop_reason.stop_reason,
                usage=usage,
            )
        except Exception as e:
            # TODO: add error handling
            raise

    async def _step(
        self,
        messages: list[Message],
        input_messages_to_persist: list[Message],
        agent_state,
        tool_rules_solver: ToolRulesSolver,
        run_id: str,
        step_index: int,
        max_steps: int,
        actor,
    ) -> dict:
        """
        Execute single agent step - mirrors letta_agent_v3.py::_step() (lines 377-750).

        Returns dict with: response_messages, should_continue, usage, stop_reason
        """
        usage = LettaUsageStatistics()

        # Check for approval flow (lines 444-490 in V3)
        approval_request, approval_response = _maybe_get_approval_messages(messages)
        tool_call_denials, tool_returns = [], []
        is_approval_response = False
        step_metrics = None

        # Variables to be set by either approval or normal flow
        tool_calls = []
        content = None
        valid_tools = []
        step_id = None
        pre_computed_assistant_message_id = None

        if approval_request and approval_response:
            # APPROVAL FLOW: Extract data from approval request/response
            is_approval_response = True
            content = approval_request.content

            # Get tool calls that are pending (approved ones)
            backfill_tool_call_id = approval_request.tool_calls[0].id  # legacy case
            if approval_response.approvals:
                approved_tool_call_ids = {
                    backfill_tool_call_id if a.tool_call_id.startswith("message-") else a.tool_call_id
                    for a in approval_response.approvals
                    if isinstance(a, ApprovalReturn) and a.approve
                }
            else:
                approved_tool_call_ids = set()

            tool_calls = [tool_call for tool_call in approval_request.tool_calls if tool_call.id in approved_tool_call_ids]
            pending_tool_call_message = _maybe_get_pending_tool_call_message(messages)
            if pending_tool_call_message:
                tool_calls.extend(pending_tool_call_message.tool_calls)

            # Get tool calls that were denied
            if approval_response.approvals:
                denies = {d.tool_call_id: d for d in approval_response.approvals if isinstance(d, ApprovalReturn) and not d.approve}
            else:
                denies = {}
            tool_call_denials = [
                ToolCallDenial(**t.model_dump(), reason=denies.get(t.id).reason) for t in approval_request.tool_calls if t.id in denies
            ]

            # Get tool calls that were executed client side
            if approval_response.approvals:
                tool_returns = [r for r in approval_response.approvals if isinstance(r, ToolReturn)]

            # Validate that the approval response contains meaningful data
            if not tool_calls and not tool_call_denials and not tool_returns:
                workflow.logger.error(
                    f"Invalid approval response: approval_response.approvals is {approval_response.approvals} "
                    f"but no tool calls, denials, or returns were extracted."
                )
                return {
                    "response_messages": [],
                    "should_continue": False,
                    "usage": usage,
                    "stop_reason": LettaStopReason(stop_reason=StopReasonType.invalid_tool_call.value),
                }

            step_id = approval_request.step_id
            pre_computed_assistant_message_id = approval_request.id

            # Fetch existing step metrics
            step_metrics_result: GetStepMetricsResult = await workflow.execute_activity(
                get_step_metrics,
                GetStepMetricsParams(step_id=step_id, actor=actor),
                start_to_close_timeout=timedelta(seconds=30),
            )
            step_metrics = step_metrics_result.step_metrics

            # Load last function response from message history for tool rules
            last_function_response = _load_last_function_response(messages)

            # Get valid tools
            valid_tools = self._get_valid_tools(agent_state, tool_rules_solver, last_function_response)

        else:
            # NORMAL FLOW: Check cancellation, make LLM call, extract tool calls

            # Check for cancellation (lines 493-497 in V3)
            cancel_result: CheckRunCancellationResult = await workflow.execute_activity(
                check_run_cancellation,
                CheckRunCancellationParams(run_id=run_id, actor=actor),
                start_to_close_timeout=timedelta(seconds=30),
            )

            if cancel_result.is_cancelled:
                return {
                    "response_messages": [],
                    "should_continue": False,
                    "usage": usage,
                    "stop_reason": LettaStopReason(stop_reason=StopReasonType.cancelled.value),
                }

            # Create step (lines 499-502 in V3)
            step_id = generate_step_id(workflow.uuid4())
            step_result: CreateStepResult = await workflow.execute_activity(
                create_step,
                CreateStepParams(
                    agent_state=agent_state,
                    messages=messages,
                    actor=actor,
                    run_id=run_id,
                    step_id=step_id,
                    usage=UsageStatistics(completion_tokens=0, prompt_tokens=0, total_tokens=0),
                    stop_reason=None,
                ),
                start_to_close_timeout=CREATE_STEP_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                schedule_to_close_timeout=CREATE_STEP_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )

            # Refresh messages for external inputs (lines 439-442 in V3)
            refresh_result: RefreshContextResult = await workflow.execute_activity(
                refresh_context_and_system_message,
                RefreshContextParams(
                    agent_state=agent_state,
                    in_context_messages=messages,
                    tool_rules_solver=tool_rules_solver,
                    actor=actor,
                ),
                start_to_close_timeout=REFRESH_CONTEXT_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                schedule_to_close_timeout=REFRESH_CONTEXT_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )
            messages = refresh_result.messages
            agent_state = refresh_result.agent_state

            # Load last function response from message history for tool rules (line 426 in V3)
            last_function_response = _load_last_function_response(messages)

            # Get valid tools (line 427 in V3)
            valid_tools = self._get_valid_tools(agent_state, tool_rules_solver, last_function_response)

            # Build request with V3 features (lines 504-558 in V3)
            force_tool_call = valid_tools[0]["name"] if len(valid_tools) == 1 else None
            truncation_chars = self._compute_tool_return_truncation_chars(agent_state.llm_config.context_window)

            # Make LLM call with retry on context window error (lines 505-597 in V3)
            for summarize_attempt in range(summarizer_settings.max_summarizer_retries + 1):
                try:
                    llm_result: LLMCallResultV3 = await workflow.execute_activity(
                        llm_request_v3,
                        LLMRequestParamsV3(
                            agent_state=agent_state,
                            messages=messages,
                            allowed_tools=valid_tools,
                            force_tool_call=force_tool_call,
                            requires_subsequent_tool_call=False,  # V3: Not required
                            tool_return_truncation_chars=truncation_chars,
                            enable_parallel_tool_calls=False,  # Deprecated: configuration now handled in activity
                            actor=actor,
                            step_id=step_id,
                        ),
                        start_to_close_timeout=timedelta(minutes=5),
                        retry_policy=LLM_ACTIVITY_RETRY_POLICY,
                    )
                    break  # Success, exit retry loop
                except ApplicationError as e:
                    if e.type == "ContextWindowExceededError" and summarize_attempt < summarizer_settings.max_summarizer_retries:
                        # Retry with summarization
                        summarize_result = await workflow.execute_activity(
                            summarize_conversation_history,
                            SummarizeParams(
                                agent_state=agent_state,
                                in_context_messages=messages,
                                new_letta_messages=[],
                                actor=actor,
                                force=True,
                            ),
                            start_to_close_timeout=SUMMARIZE_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                            schedule_to_close_timeout=SUMMARIZE_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                        )
                        messages = summarize_result
                    else:
                        raise

            usage.completion_tokens = llm_result.usage.completion_tokens
            usage.prompt_tokens = llm_result.usage.prompt_tokens
            usage.total_tokens = llm_result.usage.total_tokens
            # usage.prompt_tokens_details = llm_result.usage.prompt_tokens_details
            # usage.completion_tokens_details = llm_result.usage.completion_tokens_details

            # Extract tool calls and content from LLM response
            tool_calls = llm_result.tool_calls
            content = llm_result.content
            pre_computed_assistant_message_id = llm_result.assistant_message_id

        # ALWAYS call _handle_ai_response after the conditional (matches V3 pattern)
        persisted_messages, should_continue, stop_reason = await self._handle_ai_response(
            tool_calls=tool_calls,
            content=content,
            valid_tool_names=[tool["name"] for tool in valid_tools],
            agent_state=agent_state,
            tool_rules_solver=tool_rules_solver,
            pre_computed_assistant_message_id=pre_computed_assistant_message_id,
            step_id=step_id,
            initial_messages=input_messages_to_persist,
            is_final_step=step_index == max_steps - 1,
            run_id=run_id,
            step_metrics=step_metrics,
            is_approval_response=is_approval_response,
            tool_call_denials=tool_call_denials,
            tool_returns=tool_returns,
            actor=actor,
        )

        return {
            "response_messages": persisted_messages,
            "should_continue": should_continue,
            "usage": usage,
            "stop_reason": stop_reason,
        }

    # TODO: standardize with letta_agent_v3
    def _get_valid_tools(self, agent_state, tool_rules_solver: ToolRulesSolver, last_function_response: Optional[str] = None) -> list[dict]:
        """
        Get valid tools based on rules - mirrors letta_agent_v3.py::_get_valid_tools() (lines 1234-1250).
        """
        tools = agent_state.tools
        valid_tool_names = tool_rules_solver.get_allowed_tool_names(
            available_tools=set([t.name for t in tools]),
            last_function_response=last_function_response,
            error_on_empty=False,
        ) or list(set(t.name for t in tools))

        # Convert to JSON schema with strict mode enabled
        allowed_tools = [enable_strict_mode(t.json_schema) for t in tools if t.name in set(valid_tool_names)]

        # Add runtime overrides (terminal tools, response format)
        terminal_tool_names = {rule.tool_name for rule in tool_rules_solver.terminal_tool_rules}
        allowed_tools = runtime_override_tool_json_schema(
            tool_list=allowed_tools,
            response_format=agent_state.response_format,
            request_heartbeat=False,  # V3: No heartbeat parameter
            terminal_tools=terminal_tool_names,
        )
        return allowed_tools

    def _compute_tool_return_truncation_chars(self, context_window: int) -> int:
        """
        Compute dynamic cap for tool returns - mirrors letta_agent_v3.py (lines 74-84).

        Heuristic: ~20% of context window × 4 chars/token, minimum 5k chars.
        """
        try:
            cap = int(context_window * 0.2 * 4)  # 20% of tokens → chars
        except Exception:
            cap = 5000
        return max(5000, cap)

    def _decide_continuation(
        self,
        agent_state,
        tool_call_name: Optional[str],
        tool_rule_violated: bool,
        tool_rules_solver: ToolRulesSolver,
        is_final_step: bool,
    ) -> Tuple[bool, Optional[str], Optional[LettaStopReason]]:
        """
        V3 continuation logic - mirrors letta_agent_v3.py::_decide_continuation() (lines 1167-1232).

        Rules:
        1. No tool call? → Check required tools, else end turn
        2. Tool called? → Continue (check terminal/children rules)
        """
        continue_stepping = True  # Default continue
        continuation_reason: Optional[str] = None
        stop_reason: Optional[LettaStopReason] = None

        if tool_call_name is None:
            # No tool call – if there are required-before-exit tools uncalled, keep stepping
            uncalled = tool_rules_solver.get_uncalled_required_tools(available_tools=set([t.name for t in agent_state.tools]))
            if uncalled and not is_final_step:
                reason = f"{NON_USER_MSG_PREFIX}ToolRuleViolated: You must call {', '.join(uncalled)} at least once to exit the loop."
                return True, reason, None
            # No required tools remaining → end turn
            return False, None, LettaStopReason(stop_reason=StopReasonType.end_turn.value)
        else:
            # Tool called - handle based on rules
            if tool_rule_violated:
                continue_stepping = True
                continuation_reason = f"{NON_USER_MSG_PREFIX}Continuing: tool rule violation."
            else:
                tool_rules_solver.register_tool_call(tool_call_name)

                if tool_rules_solver.is_terminal_tool(tool_call_name):
                    stop_reason = LettaStopReason(stop_reason=StopReasonType.tool_rule.value)
                    continue_stepping = False

                elif tool_rules_solver.has_children_tools(tool_call_name):
                    continue_stepping = True
                    continuation_reason = f"{NON_USER_MSG_PREFIX}Continuing: child tool rule."

                elif tool_rules_solver.is_continue_tool(tool_call_name):
                    continue_stepping = True
                    continuation_reason = f"{NON_USER_MSG_PREFIX}Continuing: continue tool rule."

                # Hard stop overrides
                if is_final_step:
                    continue_stepping = False
                    stop_reason = LettaStopReason(stop_reason=StopReasonType.max_steps.value)
                else:
                    uncalled = tool_rules_solver.get_uncalled_required_tools(available_tools=set([t.name for t in agent_state.tools]))
                    if uncalled:
                        continue_stepping = True
                        continuation_reason = (
                            f"{NON_USER_MSG_PREFIX}Continuing, user expects these tools: [{', '.join(uncalled)}] to be called still."
                        )
                        stop_reason = None  # reset – we're still going

            return continue_stepping, continuation_reason, stop_reason

    async def _handle_ai_response(
        self,
        tool_calls: List[ToolCall],
        content: Optional[List],
        valid_tool_names: List[str],
        agent_state: AgentState,
        tool_rules_solver: ToolRulesSolver,
        pre_computed_assistant_message_id: Optional[str],
        step_id: str,
        initial_messages: Optional[List[Message]],
        is_final_step: bool,
        run_id: str,
        step_metrics,
        is_approval_response: bool,
        tool_call_denials: List[ToolCallDenial],
        tool_returns: List[ToolReturn],
        actor,
    ) -> Tuple[List[Message], bool, Optional[LettaStopReason]]:
        """
        Handle AI response - mirrors letta_agent_v3.py::_handle_ai_response() (lines 752-1164).

        Unified approach: treats single and multi-tool calls uniformly.
        Supports approval flow, parallel tool execution, and client-side tool returns.
        """
        # 1. Handle no-tool cases (content-only or no-op)
        if not tool_calls and not tool_call_denials and not tool_returns:
            # Case 1a: No tool call, no content (LLM no-op)
            if content is None or len(content) == 0:
                # Check if there are required-before-exit tools that haven't been called
                uncalled = tool_rules_solver.get_uncalled_required_tools(available_tools=set([t.name for t in agent_state.tools]))
                if uncalled:
                    heartbeat_reason = (
                        f"{NON_USER_MSG_PREFIX}ToolRuleViolated: You must call {', '.join(uncalled)} at least once to exit the loop."
                    )
                    heartbeat_msg = create_heartbeat_system_message(
                        agent_id=agent_state.id,
                        model=agent_state.llm_config.model,
                        function_call_success=True,
                        timezone=agent_state.timezone,
                        heartbeat_reason=heartbeat_reason,
                        run_id=run_id,
                    )
                    messages_to_persist = (initial_messages or []) + [heartbeat_msg]
                    continue_stepping, stop_reason = True, None
                else:
                    # No required tools remaining, end turn without persisting no-op
                    continue_stepping = False
                    stop_reason = LettaStopReason(stop_reason=StopReasonType.end_turn.value)
                    messages_to_persist = initial_messages or []

            # Case 1b: No tool call but has content
            else:
                continue_stepping, heartbeat_reason, stop_reason = self._decide_continuation(
                    agent_state=agent_state,
                    tool_call_name=None,
                    tool_rule_violated=False,
                    tool_rules_solver=tool_rules_solver,
                    is_final_step=is_final_step,
                )
                assistant_message = create_letta_messages_from_llm_response(
                    agent_id=agent_state.id,
                    model=agent_state.llm_config.model,
                    function_name=None,
                    function_arguments=None,
                    tool_execution_result=None,
                    tool_call_id=None,
                    function_response=None,
                    timezone=agent_state.timezone,
                    continue_stepping=continue_stepping,
                    heartbeat_reason=heartbeat_reason,
                    reasoning_content=content,
                    pre_computed_assistant_message_id=pre_computed_assistant_message_id,
                    step_id=step_id,
                    run_id=run_id,
                    is_approval_response=is_approval_response,
                    force_set_request_heartbeat=False,
                    add_heartbeat_on_continue=bool(heartbeat_reason),
                )
                messages_to_persist = (initial_messages or []) + assistant_message

            # Persist messages for no-tool cases
            for message in messages_to_persist:
                if message.run_id is None:
                    message.run_id = run_id
                if message.step_id is None:
                    message.step_id = step_id

            persisted_messages: CreateMessagesResult = await workflow.execute_activity(
                create_messages,
                CreateMessagesParams(
                    messages=messages_to_persist,
                    actor=actor,
                    project_id=agent_state.project_id,
                    template_id=agent_state.template_id,
                ),
                start_to_close_timeout=CREATE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                schedule_to_close_timeout=CREATE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
            )
            return persisted_messages.messages, continue_stepping, stop_reason

        # 2. Check whether tool call requires approval
        if not is_approval_response:
            requested_tool_calls = [t for t in tool_calls if tool_rules_solver.is_requires_approval_tool(t.function.name)]
            allowed_tool_calls = [t for t in tool_calls if not tool_rules_solver.is_requires_approval_tool(t.function.name)]
            if requested_tool_calls:
                approval_messages = create_approval_request_message_from_llm_response(
                    agent_id=agent_state.id,
                    model=agent_state.llm_config.model,
                    requested_tool_calls=requested_tool_calls,
                    allowed_tool_calls=allowed_tool_calls,
                    reasoning_content=content,
                    pre_computed_assistant_message_id=pre_computed_assistant_message_id,
                    step_id=step_id,
                    run_id=run_id,
                )
                messages_to_persist = (initial_messages or []) + approval_messages

                for message in messages_to_persist:
                    if message.run_id is None:
                        message.run_id = run_id
                    if message.step_id is None:
                        message.step_id = step_id

                persisted_messages = await workflow.execute_activity(
                    create_messages,
                    CreateMessagesParams(
                        messages=messages_to_persist,
                        actor=actor,
                        project_id=agent_state.project_id,
                        template_id=agent_state.template_id,
                    ),
                    start_to_close_timeout=CREATE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                    schedule_to_close_timeout=CREATE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                )
                return persisted_messages.messages, False, LettaStopReason(stop_reason=StopReasonType.requires_approval.value)

        result_tool_returns = []

        # 3. Handle client side tool execution
        if tool_returns:
            # Clamp client-side tool returns before persisting (JSON-aware truncation)
            try:
                cap = self._compute_tool_return_truncation_chars(agent_state.llm_config.context_window)
            except Exception:
                cap = 5000

            for tr in tool_returns:
                try:
                    if tr.func_response and isinstance(tr.func_response, str):
                        parsed = json.loads(tr.func_response)
                        if isinstance(parsed, dict) and "message" in parsed and isinstance(parsed["message"], str):
                            msg = parsed["message"]
                            if len(msg) > cap:
                                original_len = len(msg)
                                parsed["message"] = msg[:cap] + f"... [truncated {original_len - cap} chars]"
                                tr.func_response = json.dumps(parsed)
                                workflow.logger.warning(f"Truncated client-side tool return message from {original_len} to {cap} chars")
                        else:
                            # Fallback to raw string truncation if not a dict with 'message'
                            if len(tr.func_response) > cap:
                                original_len = len(tr.func_response)
                                tr.func_response = tr.func_response[:cap] + f"... [truncated {original_len - cap} chars]"
                                workflow.logger.warning(f"Truncated client-side tool return (raw) from {original_len} to {cap} chars")
                except json.JSONDecodeError:
                    # Non-JSON or unexpected shape; truncate as raw string
                    if tr.func_response and len(tr.func_response) > cap:
                        original_len = len(tr.func_response)
                        tr.func_response = tr.func_response[:cap] + f"... [truncated {original_len - cap} chars]"
                        workflow.logger.warning(f"Truncated client-side tool return (non-JSON) from {original_len} to {cap} chars")
                except Exception as e:
                    # Unexpected error; log and skip truncation for this return
                    workflow.logger.warning(f"Failed to truncate client-side tool return: {e}")

            continue_stepping = True
            stop_reason = None
            result_tool_returns = tool_returns

        # 4. Handle denial cases
        if tool_call_denials:
            for tool_call_denial in tool_call_denials:
                tool_call_id = tool_call_denial.id or f"call_{uuid.uuid4().hex[:8]}"
                packaged_function_response = package_function_response(
                    was_success=False,
                    response_string=f"Error: request to call tool denied. User reason: {tool_call_denial.reason}",
                    timezone=agent_state.timezone,
                )
                tool_return = ToolReturn(
                    tool_call_id=tool_call_id,
                    func_response=packaged_function_response,
                    status="error",
                )
                result_tool_returns.append(tool_return)

        # 5. Unified tool execution path (works for both single and multiple tools)

        # 5a. Validate parallel tool calling constraints
        if len(tool_calls) > 1:
            # No parallel tool calls with tool rules (except requires_approval)
            if agent_state.tool_rules and len([r for r in agent_state.tool_rules if r.type != "requires_approval"]) > 0:
                raise ValueError(
                    "Parallel tool calling is not allowed when tool rules are present. Disable tool rules to use parallel tool calls."
                )

        # 5b. Prepare execution specs for all tools
        exec_specs = []
        for tc in tool_calls:
            call_id = tc.id or f"call_{uuid.uuid4().hex[:8]}"
            name = tc.function.name
            args = _safe_load_tool_call_str(tc.function.arguments)
            args.pop(REQUEST_HEARTBEAT_PARAM, None)
            args.pop(INNER_THOUGHTS_KWARG, None)

            # Validate against allowed tools
            tool_rule_violated = name not in valid_tool_names and not is_approval_response

            # Handle prefilled args if present
            if not tool_rule_violated:
                prefill_args = tool_rules_solver.last_prefilled_args_by_tool.get(name)
                if prefill_args:
                    target_tool = next((t for t in agent_state.tools if t.name == name), None)
                    provenance = tool_rules_solver.last_prefilled_args_provenance.get(name)
                    try:
                        args = merge_and_validate_prefilled_args(
                            tool=target_tool,
                            llm_args=args,
                            prefilled_args=prefill_args,
                        )
                    except ValueError as ve:
                        # Invalid prefilled args - create error result
                        error_prefix = "Invalid prefilled tool arguments from tool rules"
                        prov_suffix = f" (source={provenance})" if provenance else ""
                        err_msg = f"{error_prefix}{prov_suffix}: {str(ve)}"

                        exec_specs.append(
                            {
                                "id": call_id,
                                "name": name,
                                "args": args,
                                "violated": False,
                                "error": err_msg,
                            }
                        )
                        continue

            exec_specs.append(
                {
                    "id": call_id,
                    "name": name,
                    "args": args,
                    "violated": tool_rule_violated,
                    "error": None,
                }
            )

        # 5c. Execute tools using Temporal activities in parallel where possible
        async def _run_parallel(specs: List[Dict[str, Any]]) -> List[Tuple[ToolExecutionResult, int]]:
            """
            Execute multiple tools in parallel using Temporal's activity execution pattern.

            This uses the fan-out/fan-in pattern:
            1. Create all activity tasks upfront (fan-out)
            2. Gather results concurrently (fan-in)
            """

            # Helper to execute a single tool
            async def _execute_single(spec: Dict[str, Any]) -> Tuple[ToolExecutionResult, int]:
                """Execute a single tool and return result + duration"""
                if spec.get("error"):
                    return ToolExecutionResult(status="error", func_return=spec["error"]), 0
                if spec["violated"]:
                    result = _build_rule_violation_result(spec["name"], valid_tool_names, tool_rules_solver)
                    return result, 0

                t0 = get_utc_timestamp_ns()

                # Execute tool via Temporal activity
                execute_result: ExecuteToolResult = await workflow.execute_activity(
                    execute_tool,
                    ExecuteToolParams(
                        tool_name=spec["name"],
                        tool_args=spec["args"],
                        agent_state=agent_state,
                        actor=actor,
                        step_id=step_id,
                    ),
                    start_to_close_timeout=TOOL_EXECUTION_ACTIVITY_START_TO_CLOSE_TIMEOUT,
                    schedule_to_close_timeout=TOOL_EXECUTION_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
                )

                dt = get_utc_timestamp_ns() - t0
                return execute_result.tool_execution_result, dt

            # Fan-out: Create all activity tasks (not awaiting yet)
            tasks = [_execute_single(spec) for spec in specs]

            # Fan-in: Wait for all to complete
            results = await asyncio.gather(*tasks)

            return results

        # Execute tools: single tool sequentially, multiple tools with parallel/serial separation
        if len(exec_specs) == 1:
            # Single tool: execute directly
            results = await _run_parallel([exec_specs[0]])
        else:
            # Multiple tools: separate by parallel execution capability
            parallel_items = []
            serial_items = []

            for idx, spec in enumerate(exec_specs):
                target_tool = next((x for x in agent_state.tools if x.name == spec["name"]), None)
                if target_tool and target_tool.enable_parallel_execution:
                    parallel_items.append((idx, spec))
                else:
                    serial_items.append((idx, spec))

            # Execute all tools with proper separation
            results = [None] * len(exec_specs)
            # Parallel execution using Temporal fan-out/fan-in pattern
            if parallel_items:
                parallel_specs = [spec for _, spec in parallel_items]
                parallel_results = await _run_parallel(parallel_specs)
                for (idx, _), result in zip(parallel_items, parallel_results):
                    results[idx] = result

            # Serial execution (one at a time)
            for idx, spec in serial_items:
                serial_results = await _run_parallel([spec])
                results[idx] = serial_results[0]

        # 5d. Update metrics with execution time
        if step_metrics is not None and results:
            step_metrics.tool_execution_ns = max(dt for _, dt in results)

        # 5e. Process results and compute function responses
        function_responses: List[Optional[str]] = []
        persisted_continue_flags: List[bool] = []
        persisted_stop_reasons: List[Optional[LettaStopReason]] = []

        for idx, spec in enumerate(exec_specs):
            tool_execution_result, _ = results[idx]
            has_prefill_error = bool(spec.get("error"))

            # Validate and format function response
            truncate = spec["name"] not in {"conversation_search", "conversation_search_date", "archival_memory_search"}
            return_char_limit = next((t.return_char_limit for t in agent_state.tools if t.name == spec["name"]), None)
            function_response_string = validate_function_response(
                tool_execution_result.func_return,
                return_char_limit=return_char_limit,
                truncate=truncate,
            )
            function_responses.append(function_response_string)

            # TODO: handle last function response if needed
            # self.last_function_response = package_function_response(
            #     was_success=tool_execution_result.success_flag,
            #     response_string=function_response_string,
            #     timezone=agent_state.timezone,
            # )

            # Register successful tool call with solver
            if not spec["violated"] and not has_prefill_error:
                tool_rules_solver.register_tool_call(spec["name"])

            # Decide continuation for this tool
            if has_prefill_error:
                cont = False
                hb_reason = None
                sr = LettaStopReason(stop_reason=StopReasonType.invalid_tool_call.value)
            else:
                cont, hb_reason, sr = self._decide_continuation(
                    agent_state=agent_state,
                    tool_call_name=spec["name"],
                    tool_rule_violated=spec["violated"],
                    tool_rules_solver=tool_rules_solver,
                    is_final_step=(is_final_step and idx == len(exec_specs) - 1),
                )
            persisted_continue_flags.append(cont)
            persisted_stop_reasons.append(sr)

        # 5f. Create messages using parallel message creation (works for both single and multi)
        tool_call_specs = [{"name": s["name"], "arguments": s["args"], "id": s["id"]} for s in exec_specs]
        tool_execution_results = [res for (res, _) in results]

        # Use the parallel message creation function for both single and multiple tools
        parallel_messages = create_parallel_tool_messages_from_llm_response(
            agent_id=agent_state.id,
            model=agent_state.llm_config.model,
            tool_call_specs=tool_call_specs,
            tool_execution_results=tool_execution_results,
            function_responses=function_responses,
            timezone=agent_state.timezone,
            run_id=run_id,
            step_id=step_id,
            reasoning_content=content,
            pre_computed_assistant_message_id=pre_computed_assistant_message_id,
            is_approval_response=is_approval_response,
            tool_returns=result_tool_returns,
        )

        messages_to_persist: List[Message] = (initial_messages or []) + parallel_messages

        # Set run_id and step_id on all messages before persisting
        for message in messages_to_persist:
            if message.run_id is None:
                message.run_id = run_id
            if message.step_id is None:
                message.step_id = step_id

        # Persist all messages
        persisted_messages = await workflow.execute_activity(
            create_messages,
            CreateMessagesParams(
                messages=messages_to_persist,
                actor=actor,
                project_id=agent_state.project_id,
                template_id=agent_state.template_id,
            ),
            start_to_close_timeout=CREATE_MESSAGES_ACTIVITY_START_TO_CLOSE_TIMEOUT,
            schedule_to_close_timeout=CREATE_MESSAGES_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT,
        )

        # Update message_ids immediately after persistence for approval responses
        if (
            is_approval_response
            and initial_messages
            and len(initial_messages) == 1
            and initial_messages[0].role == "approval"
            and len(persisted_messages.messages) >= 2
            and persisted_messages.messages[0].role == "approval"
            and persisted_messages.messages[1].role == "tool"
        ):
            agent_state.message_ids = agent_state.message_ids + [m.id for m in persisted_messages.messages[:2]]
            await workflow.execute_activity(
                update_message_ids,
                UpdateMessageIdsParams(
                    agent_id=agent_state.id,
                    message_ids=agent_state.message_ids,
                    actor=actor,
                ),
                start_to_close_timeout=UPDATE_MESSAGE_IDS_ACTIVITY_START_TO_CLOSE_TIMEOUT,
            )

        # 5g. Aggregate continuation decisions
        aggregate_continue = any(persisted_continue_flags) if persisted_continue_flags else False
        aggregate_continue = aggregate_continue or bool(tool_call_denials) or bool(tool_returns)

        # Determine aggregate stop reason
        aggregate_stop_reason = None
        for sr in persisted_stop_reasons:
            if sr is not None:
                aggregate_stop_reason = sr

        # For parallel tool calls, always continue to allow the agent to process/summarize results
        # unless a terminal tool was called or we hit max steps
        if len(exec_specs) > 1:
            has_terminal = any(sr and sr.stop_reason == StopReasonType.tool_rule.value for sr in persisted_stop_reasons)
            is_max_steps = any(sr and sr.stop_reason == StopReasonType.max_steps.value for sr in persisted_stop_reasons)

            if not has_terminal and not is_max_steps:
                # Force continuation for parallel tool execution
                aggregate_continue = True
                aggregate_stop_reason = None

        return persisted_messages.messages, aggregate_continue, aggregate_stop_reason
