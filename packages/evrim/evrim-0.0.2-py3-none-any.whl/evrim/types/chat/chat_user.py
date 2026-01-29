# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["ChatUser"]


class ChatUser(BaseModel):
    """Represents a user in the chat application tied to supabase auth."""

    id: str
    """Unique identifier for the user"""

    email: str
    """Email address of the user"""
