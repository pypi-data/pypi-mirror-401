# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .context_param import ContextParam

__all__ = ["AgentInvokeParams"]


class AgentInvokeParams(TypedDict, total=False):
    input: Required[Dict[str, Optional[object]]]
    """Input data for the agent. Structure depends on agent implementation."""

    context: ContextParam
    """Optional request context passed to the agent handler."""

    stream: bool
    """Whether to stream the response as SSE."""
