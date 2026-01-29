# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["McpTokenListResponse", "McpTokenListResponseItem"]


class McpTokenListResponseItem(BaseModel):
    """Model for listing MCP tokens (metadata only, no token string)"""

    id: str

    created_at: datetime

    expires_at: datetime

    name: str

    token_prefix: str
    """First 8 characters of token for identification"""

    last_used_at: Optional[datetime] = None

    revoked_at: Optional[datetime] = None


McpTokenListResponse: TypeAlias = List[McpTokenListResponseItem]
