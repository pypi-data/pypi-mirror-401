# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["APIKeyUpdateParams"]


class APIKeyUpdateParams(TypedDict, total=False):
    company_id: Required[Annotated[str, PropertyInfo(alias="companyId")]]

    expires_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Null to set never expires"""

    is_active: bool
    """Set to false to pause the key"""

    name: str

    rate_limit: int

    scopes: List[
        Literal[
            "stores:read", "stores:write", "wait_times:read", "wait_times:write", "queues:read", "queues:write", "*"
        ]
    ]

    team_ids: SequenceNotStr[str]
