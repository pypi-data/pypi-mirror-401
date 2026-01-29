# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["APIKeyCreateParams"]


class APIKeyCreateParams(TypedDict, total=False):
    name: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """Optional; null for never expires"""

    rate_limit: int
    """Optional; requests per minute"""

    scopes: List[
        Literal[
            "stores:read", "stores:write", "wait_times:read", "wait_times:write", "queues:read", "queues:write", "*"
        ]
    ]

    team_ids: SequenceNotStr[str]
    """Optional; restrict key to specific stores"""
