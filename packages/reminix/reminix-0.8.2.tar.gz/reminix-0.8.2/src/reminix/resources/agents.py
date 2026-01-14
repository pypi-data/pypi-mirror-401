# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional

import httpx

from ..types import agent_chat_params, agent_invoke_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream  # stainless-custom
from .._base_client import make_request_options
from ..types.stream_chunk import StreamChunk  # stainless-custom
from ..types.context_param import ContextParam
from ..types.agent_chat_response import AgentChatResponse
from ..types.agent_invoke_response import AgentInvokeResponse

__all__ = ["AgentsResource", "AsyncAgentsResource"]


class AgentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/reminix-ai/reminix-python#accessing-raw-response-data-eg-headers
        """
        return AgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/reminix-ai/reminix-python#with_streaming_response
        """
        return AgentsResourceWithStreamingResponse(self)

    def chat(
        self,
        name: str,
        *,
        messages: Iterable[agent_chat_params.Message],
        context: ContextParam | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentChatResponse:
        """Have a conversational interaction with an agent.

        This endpoint maintains
        conversation context through the messages array, allowing for multi-turn
        conversations.

        **Timeout:** Chat requests have a 60-second timeout. If the agent takes longer
        to respond, you will receive a 504 Gateway Timeout error. For long-running
        conversations, consider using streaming mode which does not have the same
        timeout constraints.

        **Idempotency:** For non-streaming requests, send an `Idempotency-Key` header
        with a unique value (e.g., UUID) to ensure duplicate requests return the same
        response. Keys are valid for 24 hours. Streaming responses are not cached.

        **Use cases:**

        - Customer support chatbots
        - AI assistants with memory
        - Multi-step question answering
        - Conversational agents that need context

        **Message format:** Follows OpenAI-compliant message structure with support for:

        - `system`, `user`, `assistant`, and `tool` roles
        - Multimodal content (text + images)
        - Tool/function calling

        **Streaming:** Set `stream: true` in the request body to receive Server-Sent
        Events (SSE) stream with incremental chunks. Perfect for ChatGPT-like real-time
        chat interfaces.

        Args:
          name: Unique, URL-safe agent name within the project

          messages: Conversation history. Must include at least one message.

          context: Optional request context passed to the agent handler.

          stream: Whether to stream the response as SSE.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            f"/agents/{name}/chat",
            body=maybe_transform(
                {
                    "messages": messages,
                    "context": context,
                    "stream": stream,
                },
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentChatResponse,
        )

    def invoke(
        self,
        name: str,
        *,
        input: Dict[str, Optional[object]],
        context: ContextParam | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentInvokeResponse:
        """Execute a one-shot task with an agent.

        This endpoint is designed for
        task-oriented operations where you provide input and receive a complete output.

        **Timeout:** Agent invocations have a 60-second timeout. If the agent takes
        longer to respond, you will receive a 504 Gateway Timeout error. For
        long-running tasks, consider using streaming mode which does not have the same
        timeout constraints.

        **Idempotency:** For non-streaming requests, send an `Idempotency-Key` header
        with a unique value (e.g., UUID) to ensure duplicate requests return the same
        response. Keys are valid for 24 hours. Streaming responses are not cached.

        **Use cases:**

        - Data analysis and processing
        - Content generation (with streaming for long outputs)
        - One-time operations that don't require conversation history
        - API-like operations

        **Streaming:** Set `stream: true` in the request body to receive Server-Sent
        Events (SSE) stream with incremental chunks. Useful for long-running tasks or
        real-time progress updates.

        Args:
          name: Unique, URL-safe agent name within the project

          input: Input data for the agent. Structure depends on agent implementation.

          context: Optional request context passed to the agent handler.

          stream: Whether to stream the response as SSE.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            f"/agents/{name}/invoke",
            body=maybe_transform(
                {
                    "input": input,
                    "context": context,
                    "stream": stream,
                },
                agent_invoke_params.AgentInvokeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentInvokeResponse,
        )

    # stainless-custom-start
    def chat_stream(
        self,
        name: str,
        *,
        messages: Iterable[agent_chat_params.Message],
        context: ContextParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[StreamChunk]:
        """Streaming variant of chat(). Returns an iterable of chunks.

        Have a conversational interaction with an agent with real-time streaming.
        Each chunk contains a portion of the response as it's generated.

        Args:
          name: Unique, URL-safe agent name within the project

          messages: Conversation history. Must include at least one message.

          context: Optional request context passed to the agent handler.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            f"/agents/{name}/chat",
            body=maybe_transform(
                {"messages": messages, "context": context, "stream": True},
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=Stream[StreamChunk],
        )

    def invoke_stream(
        self,
        name: str,
        *,
        input: Dict[str, Optional[object]],
        context: ContextParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[StreamChunk]:
        """Streaming variant of invoke(). Returns an iterable of chunks.

        Execute a one-shot task with an agent with real-time streaming.
        Each chunk contains a portion of the response as it's generated.

        Args:
          name: Unique, URL-safe agent name within the project

          input: Input data for the agent. Structure depends on agent implementation.

          context: Optional request context passed to the agent handler.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            f"/agents/{name}/invoke",
            body=maybe_transform(
                {"input": input, "context": context, "stream": True},
                agent_invoke_params.AgentInvokeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=Stream[StreamChunk],
        )
    # stainless-custom-end


class AsyncAgentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/reminix-ai/reminix-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/reminix-ai/reminix-python#with_streaming_response
        """
        return AsyncAgentsResourceWithStreamingResponse(self)

    async def chat(
        self,
        name: str,
        *,
        messages: Iterable[agent_chat_params.Message],
        context: ContextParam | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentChatResponse:
        """Have a conversational interaction with an agent.

        This endpoint maintains
        conversation context through the messages array, allowing for multi-turn
        conversations.

        **Timeout:** Chat requests have a 60-second timeout. If the agent takes longer
        to respond, you will receive a 504 Gateway Timeout error. For long-running
        conversations, consider using streaming mode which does not have the same
        timeout constraints.

        **Idempotency:** For non-streaming requests, send an `Idempotency-Key` header
        with a unique value (e.g., UUID) to ensure duplicate requests return the same
        response. Keys are valid for 24 hours. Streaming responses are not cached.

        **Use cases:**

        - Customer support chatbots
        - AI assistants with memory
        - Multi-step question answering
        - Conversational agents that need context

        **Message format:** Follows OpenAI-compliant message structure with support for:

        - `system`, `user`, `assistant`, and `tool` roles
        - Multimodal content (text + images)
        - Tool/function calling

        **Streaming:** Set `stream: true` in the request body to receive Server-Sent
        Events (SSE) stream with incremental chunks. Perfect for ChatGPT-like real-time
        chat interfaces.

        Args:
          name: Unique, URL-safe agent name within the project

          messages: Conversation history. Must include at least one message.

          context: Optional request context passed to the agent handler.

          stream: Whether to stream the response as SSE.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            f"/agents/{name}/chat",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "context": context,
                    "stream": stream,
                },
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentChatResponse,
        )

    async def invoke(
        self,
        name: str,
        *,
        input: Dict[str, Optional[object]],
        context: ContextParam | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentInvokeResponse:
        """Execute a one-shot task with an agent.

        This endpoint is designed for
        task-oriented operations where you provide input and receive a complete output.

        **Timeout:** Agent invocations have a 60-second timeout. If the agent takes
        longer to respond, you will receive a 504 Gateway Timeout error. For
        long-running tasks, consider using streaming mode which does not have the same
        timeout constraints.

        **Idempotency:** For non-streaming requests, send an `Idempotency-Key` header
        with a unique value (e.g., UUID) to ensure duplicate requests return the same
        response. Keys are valid for 24 hours. Streaming responses are not cached.

        **Use cases:**

        - Data analysis and processing
        - Content generation (with streaming for long outputs)
        - One-time operations that don't require conversation history
        - API-like operations

        **Streaming:** Set `stream: true` in the request body to receive Server-Sent
        Events (SSE) stream with incremental chunks. Useful for long-running tasks or
        real-time progress updates.

        Args:
          name: Unique, URL-safe agent name within the project

          input: Input data for the agent. Structure depends on agent implementation.

          context: Optional request context passed to the agent handler.

          stream: Whether to stream the response as SSE.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            f"/agents/{name}/invoke",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "context": context,
                    "stream": stream,
                },
                agent_invoke_params.AgentInvokeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentInvokeResponse,
        )

    # stainless-custom-start
    async def chat_stream(
        self,
        name: str,
        *,
        messages: Iterable[agent_chat_params.Message],
        context: ContextParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[StreamChunk]:
        """Async streaming variant of chat(). Returns an async iterable of chunks.

        Have a conversational interaction with an agent with real-time streaming.
        Each chunk contains a portion of the response as it's generated.

        Args:
          name: Unique, URL-safe agent name within the project

          messages: Conversation history. Must include at least one message.

          context: Optional request context passed to the agent handler.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            f"/agents/{name}/chat",
            body=await async_maybe_transform(
                {"messages": messages, "context": context, "stream": True},
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=AsyncStream[StreamChunk],
        )

    async def invoke_stream(
        self,
        name: str,
        *,
        input: Dict[str, Optional[object]],
        context: ContextParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[StreamChunk]:
        """Async streaming variant of invoke(). Returns an async iterable of chunks.

        Execute a one-shot task with an agent with real-time streaming.
        Each chunk contains a portion of the response as it's generated.

        Args:
          name: Unique, URL-safe agent name within the project

          input: Input data for the agent. Structure depends on agent implementation.

          context: Optional request context passed to the agent handler.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            f"/agents/{name}/invoke",
            body=await async_maybe_transform(
                {"input": input, "context": context, "stream": True},
                agent_invoke_params.AgentInvokeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=AsyncStream[StreamChunk],
        )
    # stainless-custom-end


class AgentsResourceWithRawResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.chat = to_raw_response_wrapper(
            agents.chat,
        )
        self.invoke = to_raw_response_wrapper(
            agents.invoke,
        )


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.chat = async_to_raw_response_wrapper(
            agents.chat,
        )
        self.invoke = async_to_raw_response_wrapper(
            agents.invoke,
        )


class AgentsResourceWithStreamingResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.chat = to_streamed_response_wrapper(
            agents.chat,
        )
        self.invoke = to_streamed_response_wrapper(
            agents.invoke,
        )


class AsyncAgentsResourceWithStreamingResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.chat = async_to_streamed_response_wrapper(
            agents.chat,
        )
        self.invoke = async_to_streamed_response_wrapper(
            agents.invoke,
        )
