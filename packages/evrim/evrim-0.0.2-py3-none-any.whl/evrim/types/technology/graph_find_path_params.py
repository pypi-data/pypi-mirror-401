# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["GraphFindPathParams"]


class GraphFindPathParams(TypedDict, total=False):
    source: Required[str]
    """Source community UUID"""

    target: Required[str]
    """Target community UUID"""

    max_depth: int
    """Maximum path depth"""
