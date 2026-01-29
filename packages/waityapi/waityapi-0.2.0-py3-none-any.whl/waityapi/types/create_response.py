# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .api_key import APIKey
from .._models import BaseModel

__all__ = ["CreateResponse"]


class CreateResponse(BaseModel):
    api_key: APIKey

    secret_key: str
    """Full API key, returned only once at creation time."""
