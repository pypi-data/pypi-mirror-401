# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from reminix import Reminix, AsyncReminix
from tests.utils import assert_matches_type
from reminix.types import AgentChatResponse, AgentInvokeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_chat(self, client: Reminix) -> None:
        agent = client.agents.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        )
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_chat_with_all_params(self, client: Reminix) -> None:
        agent = client.agents.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                    "name": "name",
                    "tool_call_id": "tool_call_id",
                }
            ],
            context={
                "conversation_id": "conversation_id",
                "custom": {"foo": "bar"},
                "user_id": "user_id",
            },
            stream=False,
        )
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_chat(self, client: Reminix) -> None:
        response = client.agents.with_raw_response.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_chat(self, client: Reminix) -> None:
        with client.agents.with_streaming_response.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentChatResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_chat(self, client: Reminix) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.agents.with_raw_response.chat(
                name="",
                messages=[
                    {
                        "content": "What is the weather today?",
                        "role": "user",
                    }
                ],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_invoke(self, client: Reminix) -> None:
        agent = client.agents.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        )
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_invoke_with_all_params(self, client: Reminix) -> None:
        agent = client.agents.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
            context={
                "conversation_id": "conversation_id",
                "custom": {"foo": "bar"},
                "user_id": "user_id",
            },
            stream=False,
        )
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_invoke(self, client: Reminix) -> None:
        response = client.agents.with_raw_response.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_invoke(self, client: Reminix) -> None:
        with client.agents.with_streaming_response.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentInvokeResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_invoke(self, client: Reminix) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.agents.with_raw_response.invoke(
                name="",
                input={
                    "task": "bar",
                    "data": "bar",
                },
            )


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_chat(self, async_client: AsyncReminix) -> None:
        agent = await async_client.agents.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        )
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_chat_with_all_params(self, async_client: AsyncReminix) -> None:
        agent = await async_client.agents.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                    "name": "name",
                    "tool_call_id": "tool_call_id",
                }
            ],
            context={
                "conversation_id": "conversation_id",
                "custom": {"foo": "bar"},
                "user_id": "user_id",
            },
            stream=False,
        )
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_chat(self, async_client: AsyncReminix) -> None:
        response = await async_client.agents.with_raw_response.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentChatResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_chat(self, async_client: AsyncReminix) -> None:
        async with async_client.agents.with_streaming_response.chat(
            name="name",
            messages=[
                {
                    "content": "What is the weather today?",
                    "role": "user",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentChatResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_chat(self, async_client: AsyncReminix) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.agents.with_raw_response.chat(
                name="",
                messages=[
                    {
                        "content": "What is the weather today?",
                        "role": "user",
                    }
                ],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_invoke(self, async_client: AsyncReminix) -> None:
        agent = await async_client.agents.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        )
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_invoke_with_all_params(self, async_client: AsyncReminix) -> None:
        agent = await async_client.agents.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
            context={
                "conversation_id": "conversation_id",
                "custom": {"foo": "bar"},
                "user_id": "user_id",
            },
            stream=False,
        )
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_invoke(self, async_client: AsyncReminix) -> None:
        response = await async_client.agents.with_raw_response.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentInvokeResponse, agent, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_invoke(self, async_client: AsyncReminix) -> None:
        async with async_client.agents.with_streaming_response.invoke(
            name="name",
            input={
                "task": "bar",
                "data": "bar",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentInvokeResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_invoke(self, async_client: AsyncReminix) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.agents.with_raw_response.invoke(
                name="",
                input={
                    "task": "bar",
                    "data": "bar",
                },
            )
