# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BilibiliListParams"]


class BilibiliListParams(TypedDict, total=False):
    end: int
    """End index for pagination"""

    start: int
    """Start index for pagination"""
