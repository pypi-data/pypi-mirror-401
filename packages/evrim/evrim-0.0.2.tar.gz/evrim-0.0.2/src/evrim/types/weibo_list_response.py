# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .weibo.weibo import Weibo

__all__ = ["WeiboListResponse"]

WeiboListResponse: TypeAlias = List[Weibo]
