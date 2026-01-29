# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .weibo import Weibo

__all__ = ["SearchBySourceDomainResponse"]

SearchBySourceDomainResponse: TypeAlias = List[Weibo]
