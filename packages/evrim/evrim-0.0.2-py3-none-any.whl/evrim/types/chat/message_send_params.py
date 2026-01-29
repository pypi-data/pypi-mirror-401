# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["MessageSendParams"]


class MessageSendParams(TypedDict, total=False):
    message: Required[str]
    """User's message content"""

    session_id: Optional[str]
    """Claude session ID for continuing conversation"""
