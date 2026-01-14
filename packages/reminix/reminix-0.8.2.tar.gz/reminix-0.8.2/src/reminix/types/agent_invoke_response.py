# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AgentInvokeResponse"]


class AgentInvokeResponse(BaseModel):
    output: Optional[object] = None
    """Output from the agent. Structure depends on agent implementation."""
