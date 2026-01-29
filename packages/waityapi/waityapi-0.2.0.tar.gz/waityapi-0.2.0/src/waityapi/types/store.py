# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["Store"]


class Store(BaseModel):
    id: str

    address: str

    category: str

    city: str

    country: str

    latitude: float

    logo_url: str

    longitude: float

    name: str

    phone: str

    postal_code: str

    state: str

    website: str
