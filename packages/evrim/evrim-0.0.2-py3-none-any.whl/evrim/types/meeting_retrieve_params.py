# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["MeetingRetrieveParams"]


class MeetingRetrieveParams(TypedDict, total=False):
    full: bool
    """Whether to include related organizations, participants, and location"""
