# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .context_param import ContextParam

__all__ = ["AgentChatParams", "Message", "MessageContentUnionMember1", "MessageContentUnionMember1ImageURL"]


class AgentChatParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """Conversation history. Must include at least one message."""

    context: ContextParam
    """Optional request context passed to the agent handler."""

    stream: bool
    """Whether to stream the response as SSE."""


class MessageContentUnionMember1ImageURL(TypedDict, total=False):
    url: Required[str]


class MessageContentUnionMember1(TypedDict, total=False):
    type: Required[Literal["text", "image_url"]]

    image_url: MessageContentUnionMember1ImageURL

    text: str


class Message(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageContentUnionMember1], Dict[str, Optional[object]]]]
    """Message content. Can be string, array (multimodal), or object (tool)."""

    role: Required[Literal["system", "user", "assistant", "tool"]]
    """Message role"""

    name: str
    """Tool name (required when role is "tool")"""

    tool_call_id: str
    """Tool call ID (for tool role)"""
