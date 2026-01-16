from temporalio import activity
from temporalio.exceptions import ApplicationError

from letta.adapters.letta_llm_request_adapter import LettaLLMRequestAdapter
from letta.agents.temporal.metrics import track_activity_metrics
from letta.agents.temporal.types import LLMCallResultV3, LLMRequestParamsV3
from letta.errors import (
    ContextWindowExceededError,
    LLMAuthenticationError,
    LLMBadRequestError,
    LLMConnectionError,
    LLMError,
    LLMJSONParsingError,
    LLMNotFoundError,
    LLMPermissionDeniedError,
    LLMRateLimitError,
    LLMServerError,
    LLMTimeoutError,
    LLMUnprocessableEntityError,
)
from letta.helpers.datetime_helpers import get_utc_timestamp_ns
from letta.llm_api.llm_client import LLMClient
from letta.schemas.letta_message_content import OmittedReasoningContent, ReasoningContent, TextContent
from letta.schemas.openai.chat_completion_response import UsageStatistics


@activity.defn(name="llm_request_v3")
@track_activity_metrics
async def llm_request_v3(params: LLMRequestParamsV3) -> LLMCallResultV3:
    """
    Build and execute a non-streaming LLM request for V3 workflow.

    V3 Enhancements:
    - Returns multiple tool calls (parallel execution support)
    - Supports content-only responses (no forced tool calls)
    - Passes tool return truncation chars to request builder
    - Passes parallel tool call configuration

    Location in V3: lines 562-602 of letta_agent_v3.py
    """
    agent_state = params.agent_state
    llm_config = agent_state.llm_config

    llm_client = LLMClient.create(
        provider_type=llm_config.model_endpoint_type,
        put_inner_thoughts_first=True,
        actor=params.actor,
    )
    llm_adapter = LettaLLMRequestAdapter(llm_client=llm_client, llm_config=llm_config)

    # V3: Pass additional parameters for tool return truncation and parallel tool calls
    request_data = llm_client.build_request_data(
        agent_type=agent_state.agent_type,
        messages=params.messages,
        llm_config=llm_config,
        tools=params.allowed_tools,
        force_tool_call=params.force_tool_call,
        requires_subsequent_tool_call=params.requires_subsequent_tool_call,
        tool_return_truncation_chars=params.tool_return_truncation_chars,
    )

    # Configure parallel tool calling based on provider (lines 514-557 in V3)
    try:
        # Check if parallel tool calls should be allowed
        # Parallel tool calls are only allowed when there are no tool rules OR only "requires_approval" rules
        no_tool_rules = not agent_state.tool_rules or len([t for t in agent_state.tool_rules if t.type != "requires_approval"]) == 0

        # Anthropic/Bedrock: disable_parallel_tool_use field in tool_choice
        if llm_config.model_endpoint_type in ["anthropic", "bedrock"]:
            if isinstance(request_data.get("tool_choice"), dict) and "disable_parallel_tool_use" in request_data["tool_choice"]:
                # Gate parallel tool use on both: no tool rules and toggled on in config
                if no_tool_rules and llm_config.parallel_tool_calls:
                    request_data["tool_choice"]["disable_parallel_tool_use"] = False
                else:
                    # Explicitly disable when tool rules present or llm_config toggled off
                    request_data["tool_choice"]["disable_parallel_tool_use"] = True

        # OpenAI: parallel_tool_calls field
        elif llm_config.model_endpoint_type == "openai":
            # For OpenAI, we control parallel tool calling via parallel_tool_calls field
            # Only allow parallel tool calls when no tool rules and enabled in config
            if "parallel_tool_calls" in request_data:
                if no_tool_rules and llm_config.parallel_tool_calls:
                    request_data["parallel_tool_calls"] = True
                else:
                    request_data["parallel_tool_calls"] = False

        # Gemini (Google AI/Vertex): native parallel tool use support
        elif llm_config.model_endpoint_type in ["google_ai", "google_vertex"]:
            # Gemini supports parallel tool calling natively through multiple parts in the response
            # We just need to ensure the config flag is set for tracking purposes
            # The actual handling happens in GoogleVertexClient.convert_response_to_chat_completion
            pass  # No specific request_data field needed for Gemini
    except Exception:
        # If this fails, we simply don't enable parallel tool use
        pass

    try:
        # Track LLM request timing
        llm_request_start_ns = get_utc_timestamp_ns()
        # Execute the LLM request
        invocation = llm_adapter.invoke_llm(
            request_data=request_data,
            messages=params.messages,
            tools=params.allowed_tools,
            use_assistant_message=params.use_assistant_message,
            requires_approval_tools=params.requires_approval_tools or [],
            step_id=params.step_id,
            actor=params.actor,
        )

        # Iterate through the async generator (non-streaming mode yields once with None)
        async for _ in invocation:
            pass

        # Calculate LLM request duration
        llm_request_end_ns = get_utc_timestamp_ns()
        llm_request_ns = llm_request_end_ns - llm_request_start_ns

        # Extract usage statistics
        usage = llm_adapter.chat_completions_response.usage if llm_adapter.chat_completions_response else UsageStatistics()

        # V3: Extract ALL tool calls (not just the first one)
        tool_calls = []
        if llm_adapter.chat_completions_response and llm_adapter.chat_completions_response.choices[0].message.tool_calls:
            tool_calls = llm_adapter.chat_completions_response.choices[0].message.tool_calls
        # V3: Extract content for content-only responses
        content = None
        if llm_adapter.chat_completions_response and llm_adapter.chat_completions_response.choices[0].message.content:
            content = [TextContent(text=llm_adapter.chat_completions_response.choices[0].message.content)]

        # Extract reasoning content
        reasoning_content = None
        if llm_adapter.chat_completions_response:
            if llm_adapter.chat_completions_response.choices[0].message.reasoning_content:
                reasoning_content = [
                    ReasoningContent(
                        reasoning=llm_adapter.chat_completions_response.choices[0].message.reasoning_content,
                        is_native=True,
                        signature=llm_adapter.chat_completions_response.choices[0].message.reasoning_content_signature,
                    )
                ]
            elif llm_adapter.chat_completions_response.choices[0].message.omitted_reasoning_content:
                reasoning_content = [OmittedReasoningContent()]
            elif llm_adapter.reasoning_content:
                reasoning_content = llm_adapter.reasoning_content

        # Combine reasoning_content + content (matching adapter pattern at simple_llm_request_adapter.py:75)
        if reasoning_content and len(reasoning_content) > 0:
            content = reasoning_content + (content or [])

        return LLMCallResultV3(
            tool_calls=tool_calls,
            content=content,
            assistant_message_id=llm_adapter.message_id,
            usage=usage,
            request_finish_ns=llm_adapter.llm_request_finish_timestamp_ns,
            llm_request_start_ns=llm_request_start_ns,
            llm_request_ns=llm_request_ns,
        )
    except (ValueError, LLMJSONParsingError) as e:
        # Invalid or unparseable LLM response — non-retryable at activity layer
        raise ApplicationError(str(e), type=type(e).__name__, non_retryable=True)
    except ContextWindowExceededError as e:
        # Context window overflow — non-retryable at activity layer; handled by workflow summarization
        raise ApplicationError(str(e), type="ContextWindowExceededError", non_retryable=True)
    except LLMError as e:
        retryable_subtypes = (
            LLMConnectionError,
            LLMRateLimitError,
            LLMServerError,
            LLMTimeoutError,
        )
        non_retryable_subtypes = (
            LLMBadRequestError,
            LLMAuthenticationError,
            LLMPermissionDeniedError,
            LLMNotFoundError,
            LLMUnprocessableEntityError,
        )
        if isinstance(e, retryable_subtypes):
            non_retryable = False
        elif isinstance(e, non_retryable_subtypes):
            non_retryable = True
        else:
            # Default conservatively: do not retry unknown LLMError types
            non_retryable = True
        raise ApplicationError(str(e), type=type(e).__name__, non_retryable=non_retryable)
    except TimeoutError as e:
        raise ApplicationError(str(e), type=type(e).__name__, non_retryable=False)
    except Exception as e:
        # Any unexpected error — do not retry at activity layer
        raise ApplicationError(str(e), type=type(e).__name__, non_retryable=True)
