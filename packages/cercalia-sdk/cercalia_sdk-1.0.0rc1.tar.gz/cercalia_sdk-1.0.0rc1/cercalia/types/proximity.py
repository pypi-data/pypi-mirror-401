"""
Proximity types for Cercalia SDK.

This module contains types for proximity search operations, which find
the nearest points of interest from a given location.

Example:
    >>> from cercalia.types.proximity import ProximityOptions, ProximityResult
    >>> from cercalia.types.common import Coordinate
    >>> options = ProximityOptions(
    ...     center=Coordinate(lat=41.38, lng=2.17),
    ...     categories=["C001", "C007"],
    ...     count=10,
    ...     max_radius=5000
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate
from .poi import PoiGeographicElement


class ProximityOptions(BaseModel):
    """
    Options for proximity search.

    Defines the parameters for searching POIs near a center point.

    Attributes:
        center: Center coordinate for the search.
        count: Maximum number of results to return.
        categories: POI category codes to filter by.
        max_radius: Maximum search radius in meters.
        include_routing: Whether to include route distance/time.
        route_weight: Route optimization when routing is enabled.

    Example:
        >>> options = ProximityOptions(
        ...     center=Coordinate(lat=41.38, lng=2.17),
        ...     categories=["C001"],  # Gas stations
        ...     count=5,
        ...     max_radius=10000,
        ...     include_routing=True,
        ...     route_weight="time"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    center: Coordinate = Field(..., description="Center coordinate for the search")
    count: Optional[int] = Field(None, description="Maximum number of results")
    categories: Optional[list[str]] = Field(None, description="POI category codes to search for")
    max_radius: Optional[int] = Field(None, description="Maximum search radius in meters")
    include_routing: Optional[bool] = Field(None, description="Include routing information")
    route_weight: Optional[Literal["time", "distance"]] = Field(
        None, description="Route weight type when routing is enabled"
    )


class ProximityItem(BaseModel):
    """
    A single item from proximity search results.

    Represents a POI found near the search center with distance
    and optional routing information.

    Following Golden Rules:
        - Coordinates are required (strict, no default 0,0)
        - Uses locality instead of city (with locality_code)
        - Direct mapping from API response

    Attributes:
        id: Unique POI identifier.
        name: POI name or business name.
        coord: Geographic coordinates of the POI.
        distance: Straight-line distance in meters from search center.
        position: Result position (1-based index).
        category_code: POI category code.
        subcategory_code: POI subcategory code.
        geometry: Geometry type of the POI.
        info: Additional information about the POI.
        ge: Geographic element with address details.
        route_distance: Route distance in meters (when routing enabled).
        route_time: Route time in seconds (when routing enabled).
        route_realtime: Route time with traffic (when available).
        route_weight: Route weight value used.

    Example:
        >>> for item in result.items:
        ...     print(f"{item.name}: {item.distance}m away")
        ...     if item.route_time:
        ...         print(f"  Driving time: {item.route_time // 60} min")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="POI unique identifier")
    name: str = Field(..., description="POI name")
    coord: Coordinate = Field(..., description="POI coordinates")
    distance: int = Field(..., description="Straight-line distance in meters from search center")
    position: Optional[int] = Field(None, description="Result position (1-based)")
    category_code: Optional[str] = Field(None, description="POI category code")
    subcategory_code: Optional[str] = Field(None, description="POI subcategory code")
    geometry: Optional[str] = Field(None, description="Geometry type")
    info: Optional[str] = Field(None, description="Additional POI information")
    ge: Optional[PoiGeographicElement] = Field(
        None, description="Geographic element (address information)"
    )
    route_distance: Optional[int] = Field(
        None, description="Route distance in meters (when routing enabled)"
    )
    route_time: Optional[int] = Field(None, description="Route time in seconds (when routing enabled)")
    route_realtime: Optional[int] = Field(None, description="Route time with real-time traffic")
    route_weight: Optional[int] = Field(None, description="Route weight value")


class ProximityResult(BaseModel):
    """
    Result of proximity search.

    Contains the list of POIs found and search metadata.

    Attributes:
        items: List of POIs found near the center.
        center: The search center coordinate used.
        total_found: Total number of items found.

    Example:
        >>> result = service.search(options)
        >>> print(f"Found {result.total_found} POIs")
        >>> for item in result.items:
        ...     print(f"  {item.name}: {item.distance}m")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    items: list[ProximityItem] = Field(..., description="List of proximity items")
    center: Coordinate = Field(..., description="Search center coordinate")
    total_found: int = Field(..., description="Total number of items found")
