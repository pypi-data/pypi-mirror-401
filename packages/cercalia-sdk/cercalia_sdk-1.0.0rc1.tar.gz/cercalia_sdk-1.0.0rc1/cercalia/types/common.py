"""
Common types for Cercalia SDK.

This module contains the base types used across all services,
including geographic primitives, configuration, and error handling.

Example:
    >>> from cercalia.types.common import Coordinate, BoundingBox
    >>> coord = Coordinate(lat=41.3851, lng=2.1734)
    >>> bbox = BoundingBox(min_lat=41.0, min_lng=2.0, max_lat=42.0, max_lng=3.0)
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Coordinate(BaseModel):
    """
    Geographic coordinate with latitude and longitude.

    Represents a point on Earth using WGS84 coordinate system.

    Attributes:
        lat: Latitude in decimal degrees [-90, 90].
        lng: Longitude in decimal degrees [-180, 180].

    Example:
        >>> coord = Coordinate(lat=41.3851, lng=2.1734)
        >>> print(f"Barcelona: {coord.lat}, {coord.lng}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    lat: float = Field(..., description="Latitude in decimal degrees [-90, 90]")
    lng: float = Field(..., description="Longitude in decimal degrees [-180, 180]")


class BoundingBox(BaseModel):
    """
    Bounding box defined by minimum and maximum coordinates.

    Represents a rectangular geographic area using two corner points
    (southwest and northeast).

    Attributes:
        min_lat: Southern boundary latitude.
        min_lng: Western boundary longitude.
        max_lat: Northern boundary latitude.
        max_lng: Eastern boundary longitude.

    Example:
        >>> bbox = BoundingBox(min_lat=41.0, min_lng=2.0, max_lat=42.0, max_lng=3.0)
        >>> print(f"Area covers {bbox.max_lat - bbox.min_lat} degrees latitude")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    min_lat: float = Field(..., description="Minimum latitude (southern boundary)")
    min_lng: float = Field(..., description="Minimum longitude (western boundary)")
    max_lat: float = Field(..., description="Maximum latitude (northern boundary)")
    max_lng: float = Field(..., description="Maximum longitude (eastern boundary)")


class CercaliaConfig(BaseModel):
    """
    Configuration for Cercalia API connection.

    Contains the credentials and endpoint settings required to
    authenticate and communicate with the Cercalia API.

    Attributes:
        api_key: Your Cercalia API key for authentication.
        base_url: Base URL for Cercalia API (defaults to production endpoint).

    Example:
        >>> config = CercaliaConfig(api_key="your-api-key")
        >>> # Or with custom base URL:
        >>> config = CercaliaConfig(
        ...     api_key="your-api-key",
        ...     base_url="https://custom.cercalia.com/api"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    api_key: str = Field(..., description="Cercalia API key for authentication")
    base_url: str = Field(
        default="https://lb.cercalia.com/services/v2/json",
        description="Base URL for Cercalia API endpoint",
    )


class CercaliaError(Exception):
    """
    Custom exception for Cercalia API errors.

    Raised when the Cercalia API returns an error response or
    when there are issues with the request.

    Attributes:
        message: Human-readable error description.
        code: Optional error code from the Cercalia API.

    Example:
        >>> try:
        ...     result = service.geocode(options)
        ... except CercaliaError as e:
        ...     print(f"Error {e.code}: {e.message}")
    """

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        """
        Initialize a CercaliaError.

        Args:
            message: Human-readable error description.
            code: Optional error code from the Cercalia API.
        """
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        """Return a formatted string representation of the error."""
        if self.code:
            return f"Cercalia error [{self.code}]: {self.message}"
        return f"Cercalia error: {self.message}"
