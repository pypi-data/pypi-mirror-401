# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProjectRetrieveResponse"]


class ProjectRetrieveResponse(BaseModel):
    id: str
    """Unique identifier for the project"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """ISO 8601 timestamp when the project was created"""

    name: str
    """Human-readable name of the project"""

    organization_id: str = FieldInfo(alias="organizationId")
    """ID of the organization that owns this project"""

    slug: str
    """URL-friendly identifier for the project"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """ISO 8601 timestamp when the project was last updated"""
