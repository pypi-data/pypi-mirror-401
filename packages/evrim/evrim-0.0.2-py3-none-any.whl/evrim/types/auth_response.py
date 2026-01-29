# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["AuthResponse", "User"]


class User(BaseModel):
    """Authenticated user model"""

    id: str

    created_at: Optional[str] = None

    email: Optional[str] = None

    user_metadata: Optional[Dict[str, object]] = None


class AuthResponse(BaseModel):
    """Authentication response with tokens"""

    access_token: str

    expires_in: int

    refresh_token: str

    user: User
    """Authenticated user model"""

    token_type: Optional[str] = None
