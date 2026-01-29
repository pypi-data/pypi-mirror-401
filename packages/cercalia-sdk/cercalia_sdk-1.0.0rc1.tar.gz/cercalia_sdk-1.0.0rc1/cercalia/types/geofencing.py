"""
Geofencing types for Cercalia SDK.

This module contains types for geofencing (point-in-polygon) operations,
which determine whether points are inside or outside defined geographic areas.

Example:
    >>> from cercalia.types.geofencing import (
    ...     GeofenceShape, GeofencePoint, GeofenceOptions
    ... )
    >>> from cercalia.types.common import Coordinate
    >>> shapes = [
    ...     GeofenceShape(id="zone1", wkt="CIRCLE(2.17 41.38, 1000)"),
    ...     GeofenceShape(id="zone2", wkt="POLYGON((2.1 41.3, 2.2 41.3, 2.2 41.4, 2.1 41.4, 2.1 41.3))")
    ... ]
    >>> points = [
    ...     GeofencePoint(id="vehicle1", coord=Coordinate(lat=41.38, lng=2.17))
    ... ]
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate


class GeofenceShape(BaseModel):
    """
    Geofence shape definition.

    Defines a geographic boundary using WKT (Well-Known Text) format.
    Supports polygons, circles, and other geometries.

    Attributes:
        id: Unique identifier for the shape.
        wkt: Shape geometry in WKT format.

    Example:
        >>> # Circle with 1km radius
        >>> circle = GeofenceShape(
        ...     id="delivery_zone",
        ...     wkt="CIRCLE(2.17 41.38, 1000)"
        ... )
        >>> # Polygon area
        >>> polygon = GeofenceShape(
        ...     id="warehouse_area",
        ...     wkt="POLYGON((2.1 41.3, 2.2 41.3, 2.2 41.4, 2.1 41.4, 2.1 41.3))"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique identifier for the shape")
    wkt: str = Field(
        ...,
        description="Shape geometry in WKT format (e.g., 'CIRCLE(2.17 41.38, 1000)' or 'POLYGON(...)')",
    )


class GeofencePoint(BaseModel):
    """
    Point to check against geofences.

    Represents a geographic point (e.g., vehicle position) to be tested
    for containment within geofence shapes.

    Attributes:
        id: Unique identifier for the point.
        coord: Geographic coordinates of the point.

    Example:
        >>> point = GeofencePoint(
        ...     id="truck_001",
        ...     coord=Coordinate(lat=41.38, lng=2.17)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique identifier for the point")
    coord: Coordinate = Field(..., description="Point coordinates")


class GeofencePointMatch(BaseModel):
    """
    A point that is inside a geofence shape.

    Represents a point that was found to be contained within
    a geofence boundary.

    Attributes:
        id: Point identifier (matches the input point ID).
        coord: Point coordinates as returned by the API.

    Note:
        Coordinates may differ slightly from input due to coordinate
        system projection transformations.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Point identifier")
    coord: Coordinate = Field(
        ...,
        description="Point coordinates (as returned by API, may differ slightly due to projection)",
    )


class GeofenceMatch(BaseModel):
    """
    Match result for a geofence shape that contains points.

    Represents a shape and all the points found inside it.

    Attributes:
        shape_id: Identifier of the geofence shape.
        shape_wkt: WKT geometry of the shape.
        points_inside: List of points contained within this shape.

    Example:
        >>> for match in result.matches:
        ...     print(f"Zone {match.shape_id} contains:")
        ...     for point in match.points_inside:
        ...         print(f"  - {point.id}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    shape_id: str = Field(..., description="Unique identifier of the shape")
    shape_wkt: str = Field(..., description="WKT representation of the shape")
    points_inside: list[GeofencePointMatch] = Field(
        ..., description="Points that are inside this shape"
    )


class GeofenceResult(BaseModel):
    """
    Result of a geofencing check operation.

    Contains all shapes that have at least one point inside them.

    Attributes:
        matches: Shapes that contain at least one point.
        total_points_checked: Number of points tested.
        total_shapes_checked: Number of shapes tested.

    Example:
        >>> result = service.check(shapes, points)
        >>> if result.matches:
        ...     print(f"{len(result.matches)} zones have points inside")
        ... else:
        ...     print("No points inside any zone")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    matches: list[GeofenceMatch] = Field(..., description="Shapes that contain at least one point")
    total_points_checked: Optional[int] = Field(None, description="Total number of points checked")
    total_shapes_checked: Optional[int] = Field(None, description="Total number of shapes checked")


class GeofenceOptions(BaseModel):
    """
    Options for geofencing operations.

    Configures the coordinate reference systems for shapes and points.

    Attributes:
        shape_srs: Coordinate system for shape geometries.
        point_srs: Coordinate system for point coordinates.

    Note:
        Default coordinate system is EPSG:4326 (WGS84 geographic coordinates).

    Example:
        >>> options = GeofenceOptions(
        ...     shape_srs="EPSG:4326",  # WGS84
        ...     point_srs="EPSG:4326"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    shape_srs: Optional[str] = Field(
        None, description="Coordinate system for shape geometries (default: EPSG:4326)"
    )
    point_srs: Optional[str] = Field(
        None, description="Coordinate system for point coordinates (default: EPSG:4326)"
    )
