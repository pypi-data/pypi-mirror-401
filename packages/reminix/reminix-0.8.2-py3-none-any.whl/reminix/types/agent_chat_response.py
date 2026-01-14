# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AgentChatResponse", "Message", "MessageContentUnionMember1", "MessageContentUnionMember1ImageURL"]


class MessageContentUnionMember1ImageURL(BaseModel):
    url: str


class MessageContentUnionMember1(BaseModel):
    type: Literal["text", "image_url"]

    image_url: Optional[MessageContentUnionMember1ImageURL] = None

    text: Optional[str] = None


class Message(BaseModel):
    content: Union[str, List[MessageContentUnionMember1], Dict[str, Optional[object]]]
    """Message content. Can be string, array (multimodal), or object (tool)."""

    role: Literal["system", "user", "assistant", "tool"]
    """Message role"""

    name: Optional[str] = None
    """Tool name (required when role is "tool")"""

    tool_call_id: Optional[str] = None
    """Tool call ID (for tool role)"""


class AgentChatResponse(BaseModel):
    messages: List[Message]
    """Full conversation history including the assistant response"""

    output: str
    """Final assistant response text"""
