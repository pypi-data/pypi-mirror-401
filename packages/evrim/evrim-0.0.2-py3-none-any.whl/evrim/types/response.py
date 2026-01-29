# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Response"]


class Response(BaseModel):
    """Response to a message from the chat agent."""

    id: str
    """Unique identifier for the response"""

    success: bool
    """Indicates if the operation was successful"""

    content: Optional[str] = None
    """JSON-serialized ChatAgentResponse data"""

    created_at: Optional[str] = None
    """Timestamp when response was created"""
