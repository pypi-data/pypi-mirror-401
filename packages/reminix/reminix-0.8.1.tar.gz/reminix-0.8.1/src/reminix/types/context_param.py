# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["ContextParam"]


class ContextParam(TypedDict, total=False):
    """Optional request context passed to the agent handler."""

    conversation_id: str
    """ID to track multi-turn conversations"""

    custom: Dict[str, Optional[object]]
    """Additional custom context fields"""

    user_id: str
    """ID of the user making the request"""
