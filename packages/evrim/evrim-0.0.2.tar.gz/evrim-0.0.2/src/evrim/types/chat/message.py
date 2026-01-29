# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..response import Response
from .chat_user import ChatUser

__all__ = ["Message"]


class Message(BaseModel):
    """Represents a chat message."""

    id: str
    """Unique identifier for the message"""

    content: str
    """The content of the message"""

    sender: ChatUser
    """The sender of the message"""

    error_message: Optional[str] = None
    """Error message if processing failed"""

    response: Optional[Response] = None
    """Response to a message from the chat agent."""

    session_id: Optional[str] = None
    """
    Identifier for the session this message belongs to (null for new sessions until
    processed)
    """

    status: Optional[Literal["pending", "running", "completed", "failed"]] = None
    """Processing status of the message (pending, running, completed, failed)"""

    timestamp: Optional[str] = None
    """The timestamp of the message"""
