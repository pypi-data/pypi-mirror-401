# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AgentChatResponse", "Message", "MessageToolCall", "MessageToolCallFunction"]


class MessageToolCallFunction(BaseModel):
    arguments: str

    name: str


class MessageToolCall(BaseModel):
    id: str

    function: MessageToolCallFunction

    type: Literal["function"]


class Message(BaseModel):
    """Assistant message response"""

    content: Union[str, List[Optional[object]], None] = None

    role: Literal["assistant"]

    tool_calls: Optional[List[MessageToolCall]] = None


class AgentChatResponse(BaseModel):
    message: Message
    """Assistant message response"""
