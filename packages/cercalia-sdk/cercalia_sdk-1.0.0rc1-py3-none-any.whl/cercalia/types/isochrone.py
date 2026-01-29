"""
Isochrone types for Cercalia SDK.

This module contains types for isochrone (service area) calculations,
which determine the reachable area from a point within a given time
or distance threshold.

Example:
    >>> from cercalia.types.isochrone import IsochroneOptions, IsochroneResult
    >>> options = IsochroneOptions(
    ...     value=15,  # 15 minutes
    ...     weight="time",
    ...     method="concavehull"
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate

IsochroneWeight = Literal["time", "distance"]
"""
Weight type for isochrone calculation:
- time: Calculate area reachable within X minutes
- distance: Calculate area reachable within X meters
"""

IsochroneMethod = Literal["convexhull", "concavehull", "net"]
"""
Method used to calculate the isochrone polygon boundary:
- convexhull: Faster, creates a convex polygon (no concave edges)
- concavehull: More accurate, creates a polygon that follows the actual reachable area
- net: Logistics network (only for truck routing)
"""


class IsochroneOptions(BaseModel):
    """
    Options for isochrone calculation.

    Defines the parameters for calculating an isochrone polygon
    from a center point.

    Attributes:
        value: Threshold value in minutes (for time) or meters (for distance).
        weight: Calculation type - 'time' or 'distance'.
        method: Polygon generation method - 'convexhull', 'concavehull', or 'net'.

    Example:
        >>> options = IsochroneOptions(
        ...     value=30,  # 30 minutes or meters depending on weight
        ...     weight="time",
        ...     method="concavehull"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    value: int = Field(..., description="Value in minutes (for time) or meters (for distance)")
    weight: Optional[IsochroneWeight] = Field(
        None, description="Weight type: 'time' or 'distance'. Default: 'time'"
    )
    method: Optional[IsochroneMethod] = Field(
        None,
        description="Method for polygon calculation. Default: 'concavehull'",
    )


class IsochroneMultipleOptions(BaseModel):
    """
    Options for multiple isochrone calculation.

    Used when calculating multiple isochrones with different values
    from the same center point. The value is provided separately
    for each isochrone.

    Attributes:
        weight: Calculation type - 'time' or 'distance'.
        method: Polygon generation method.

    Example:
        >>> options = IsochroneMultipleOptions(
        ...     weight="time",
        ...     method="concavehull"
        ... )
        >>> # Then calculate isochrones for 5, 10, 15 minutes
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    weight: Optional[IsochroneWeight] = Field(
        None, description="Weight type: 'time' or 'distance'. Default: 'time'"
    )
    method: Optional[IsochroneMethod] = Field(
        None,
        description="Method for polygon calculation. Default: 'concavehull'",
    )


class IsochroneResult(BaseModel):
    """
    Result of an isochrone calculation.

    Contains the polygon geometry and metadata for the calculated
    service area.

    Following Golden Rules:
        - Direct mapping from API response (no transformations)
        - Include raw level value for transparency
        - Coordinates are required (no fallback to 0,0)

    Attributes:
        wkt: WKT (Well-Known Text) geometry of the isochrone polygon.
        center: Center coordinate from which the isochrone was calculated.
        value: Value used for calculation (minutes or meters).
        weight: Weight type used ('time' or 'distance').
        level: Raw level value from Cercalia API (ms for time, m for distance).

    Example:
        >>> result = service.calculate(center, options)
        >>> print(f"Reachable area in {result.value} minutes")
        >>> # Use result.wkt with a GIS library for visualization
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    wkt: str = Field(..., description="WKT geometry of the isochrone polygon")
    center: Coordinate = Field(..., description="Center coordinate of the isochrone")
    value: int = Field(
        ...,
        description="Value used for calculation (minutes for time, meters for distance)",
    )
    weight: IsochroneWeight = Field(
        ..., description="Weight type: 'time' (minutes) or 'distance' (meters)"
    )
    level: str = Field(
        ...,
        description="Level value returned by Cercalia API (raw value in ms for time, m for distance)",
    )
