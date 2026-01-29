# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .wechat import Wechat

__all__ = ["SearchBySourceDomainResponse"]

SearchBySourceDomainResponse: TypeAlias = List[Wechat]
