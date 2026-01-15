"""
Python client wrapper for the War Track Dashboard API.
"""

from uruwat.client import Client
from uruwat.exceptions import (
    WarTrackAPIError,
    WarTrackAuthenticationError,
    WarTrackForbiddenError,
    WarTrackNotFoundError,
    WarTrackRateLimitError,
    WarTrackServerError,
)
from uruwat.models import (
    AllEquipment,
    AllSystem,
    Country,
    Equipment,
    EquipmentType,
    Status,
    System,
)

__version__ = "0.1.0"

__all__ = [
    "Client",
    "WarTrackAPIError",
    "WarTrackAuthenticationError",
    "WarTrackForbiddenError",
    "WarTrackNotFoundError",
    "WarTrackRateLimitError",
    "WarTrackServerError",
    "Country",
    "EquipmentType",
    "Status",
    "Equipment",
    "AllEquipment",
    "System",
    "AllSystem",
]
