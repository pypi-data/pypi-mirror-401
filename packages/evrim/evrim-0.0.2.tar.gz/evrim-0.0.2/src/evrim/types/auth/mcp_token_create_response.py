# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["McpTokenCreateResponse"]


class McpTokenCreateResponse(BaseModel):
    """Response model when creating a new MCP token (includes the actual token)"""

    id: str

    token: str
    """The actual token string - save this, it won't be shown again"""

    created_at: datetime

    expires_at: datetime

    name: str

    token_prefix: str

    user_id: str
