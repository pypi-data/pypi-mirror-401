# stainless-custom-start
from .._models import BaseModel

__all__ = ["StreamChunk"]


class StreamChunk(BaseModel):
    """A chunk from a streaming response."""

    chunk: str
    """Text chunk from the stream."""
# stainless-custom-end
