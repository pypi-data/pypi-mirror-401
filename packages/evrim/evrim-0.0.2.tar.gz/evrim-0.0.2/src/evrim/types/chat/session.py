# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .message import Message
from ..._models import BaseModel
from .chat_user import ChatUser

__all__ = ["Session"]


class Session(BaseModel):
    """Represents a session between the user and the chat agent."""

    id: str
    """Unique identifier for the conversation"""

    created_at: str
    """Timestamp when the conversation was created"""

    messages: List[Message]
    """List of messages in the conversation"""

    user: ChatUser
    """The user participating in the conversation"""
