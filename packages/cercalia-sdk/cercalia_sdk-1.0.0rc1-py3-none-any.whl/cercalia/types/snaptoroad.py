"""
SnapToRoad types for Cercalia SDK.

This module contains types for GPS track map matching operations,
which align GPS traces to road network geometries.

Example:
    >>> from cercalia.types.snaptoroad import (
    ...     SnapToRoadPoint, SnapToRoadOptions, SnapToRoadResult
    ... )
    >>> from cercalia.types.common import Coordinate
    >>> points = [
    ...     SnapToRoadPoint(coord=Coordinate(lat=41.38, lng=2.17), speed=50),
    ...     SnapToRoadPoint(coord=Coordinate(lat=41.39, lng=2.18), speed=55),
    ... ]
    >>> options = SnapToRoadOptions(weight="distance", speeding=True)
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate


class SnapToRoadPoint(BaseModel):
    """
    A GPS point for map matching.

    Represents a single GPS measurement to be snapped to the road network.

    Attributes:
        coord: GPS coordinates (WGS84).
        compass: Compass heading in degrees (0-360, 0=North).
        angle: Angle value for direction.
        speed: Vehicle speed in km/h at this point.
        attribute: Grouping attribute for segmenting results.

    Example:
        >>> point = SnapToRoadPoint(
        ...     coord=Coordinate(lat=41.38, lng=2.17),
        ...     compass=45,  # Northeast
        ...     speed=60
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="GPS coordinates")
    compass: Optional[int] = Field(None, description="Compass heading (0-360)")
    angle: Optional[int] = Field(None, description="Angle value")
    speed: Optional[int] = Field(None, description="Speed in km/h")
    attribute: Optional[str] = Field(None, description="Grouping attribute")


class SnapToRoadOptions(BaseModel):
    """
    Options for snap to road operations.

    Configures how GPS points are matched to the road network
    and what information is included in the result.

    Attributes:
        weight: Route optimization type ('distance' or 'time').
        net: Country network to use for matching.
        geometry_srs: Coordinate system for output geometry.
        geometry_tolerance: Simplification tolerance in meters.
        points: Return displaced GPS points on road.
        speeding: Return separate sections based on speed compliance.
        speed_tolerance: Speed tolerance in km/h for speeding detection.
        only_track: Return multipoint geometry instead of line.
        max_direction_search_distance: Max deviation considering direction (m).
        max_search_distance: Max deviation ignoring direction (m).
        factor: Factor between route and straight-line distance.

    Example:
        >>> options = SnapToRoadOptions(
        ...     weight="distance",
        ...     speeding=True,
        ...     speed_tolerance=5,  # Allow 5 km/h over limit
        ...     geometry_tolerance=10
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    weight: Optional[Literal["distance", "time"]] = Field(
        None, description="Route type (default: 'distance')"
    )
    net: Optional[str] = Field(None, description="Country net used")
    geometry_srs: Optional[str] = Field(
        None, description="Coordinate system of the resulting polyline"
    )
    geometry_tolerance: Optional[int] = Field(
        None, description="Geometry tolerance (simplification) in meters"
    )
    points: Optional[bool] = Field(
        None, description="Return original GPS points displaced on road route"
    )
    speeding: Optional[bool] = Field(
        None, description="Return separate route sections based on speed compliance"
    )
    speed_tolerance: Optional[int] = Field(None, description="Speed tolerance in km/h (default: 0)")
    only_track: Optional[bool] = Field(
        None, description="Return multipoint geometry with route points (default: false)"
    )
    max_direction_search_distance: Optional[int] = Field(
        None,
        description="Max deviation in meters between GPS and road point considering direction (default: 10)",
    )
    max_search_distance: Optional[int] = Field(
        None,
        description="Max deviation in meters between GPS and road point ignoring direction (default: 20)",
    )
    factor: Optional[float] = Field(
        None,
        description="Factor between route distance and straight-line distance (default: 2)",
    )


class SnapToRoadSegment(BaseModel):
    """
    A segment from snap to road results.

    Represents a section of the matched route with its geometry
    and optional speed compliance information.

    Attributes:
        wkt: WKT geometry of the road segment.
        distance: Segment distance in kilometers.
        attribute: Grouping attribute (matches input point attribute).
        speeding: Whether this segment exceeds the speed limit.
        speeding_level: Speed violation severity level.

    Example:
        >>> for segment in result.segments:
        ...     if segment.speeding:
        ...         print(f"Speeding on {segment.distance:.2f}km segment")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    wkt: str = Field(..., description="WKT geometry of the segment")
    distance: float = Field(..., description="Distance in kilometers")
    attribute: Optional[str] = Field(None, description="Grouping attribute")
    speeding: Optional[bool] = Field(None, description="Whether this segment exceeds speed limit")
    speeding_level: Optional[int] = Field(None, description="Speed violation level")


class SnapToRoadResult(BaseModel):
    """
    Result from snap to road operation.

    Contains the matched road segments and total distance.

    Attributes:
        segments: List of road-matched segments.
        total_distance: Total distance of the matched route in kilometers.

    Example:
        >>> result = service.snap(points, options)
        >>> print(f"Total distance: {result.total_distance:.2f} km")
        >>> for segment in result.segments:
        ...     print(f"  Segment: {segment.distance:.2f} km")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    segments: list[SnapToRoadSegment] = Field(..., description="List of road-matched segments")
    total_distance: float = Field(..., description="Total distance in kilometers")
