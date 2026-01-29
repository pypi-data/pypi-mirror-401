# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["APIKey", "Team"]


class Team(BaseModel):
    id: str

    name: str


class APIKey(BaseModel):
    id: str

    created_at: datetime

    is_active: bool

    key_prefix: str

    name: str

    rate_limit: int

    scopes: List[
        Literal[
            "stores:read", "stores:write", "wait_times:read", "wait_times:write", "queues:read", "queues:write", "*"
        ]
    ]

    expires_at: Optional[datetime] = None
    """Null means never expires"""

    last_used_at: Optional[datetime] = None

    team_ids: Optional[List[str]] = None

    teams: Optional[List[Team]] = None
    """Resolved team names for team_ids restrictions"""
