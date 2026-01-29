"""
Static Maps types for Cercalia SDK.

This module contains type definitions for the Static Maps API,
which generates map images with markers, shapes, and labels.

Example:
    >>> from cercalia.types.staticmaps import (
    ...     StaticMapOptions, StaticMapMarker, StaticMapCircle, RGBAColor
    ... )
    >>> from cercalia.types.common import Coordinate
    >>> options = StaticMapOptions(
    ...     width=800,
    ...     height=600,
    ...     center=Coordinate(lat=41.38, lng=2.17),
    ...     markers=[
    ...         StaticMapMarker(coord=Coordinate(lat=41.38, lng=2.17), icon=1)
    ...     ]
    ... )
"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate


class RGBAColor(BaseModel):
    """
    RGBA color representation.

    Defines a color using red, green, blue, and optional alpha components.

    Attributes:
        r: Red component (0-255).
        g: Green component (0-255).
        b: Blue component (0-255).
        a: Alpha/transparency component (0-255, optional).

    Example:
        >>> red = RGBAColor(r=255, g=0, b=0)
        >>> semi_transparent_blue = RGBAColor(r=0, g=0, b=255, a=128)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    r: int = Field(..., ge=0, le=255, description="Red component (0-255)")
    g: int = Field(..., ge=0, le=255, description="Green component (0-255)")
    b: int = Field(..., ge=0, le=255, description="Blue component (0-255)")
    a: Optional[int] = Field(None, ge=0, le=255, description="Alpha component (0-255, optional)")


class StaticMapMarker(BaseModel):
    """
    Marker to be placed on the map.

    Represents a point marker with optional icon customization.

    Attributes:
        coord: Geographic coordinate where the marker is placed.
        icon: Icon number for the marker style.

    Example:
        >>> marker = StaticMapMarker(
        ...     coord=Coordinate(lat=41.38, lng=2.17),
        ...     icon=1
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Coordinate of the marker")
    icon: Optional[int] = Field(None, description="Icon number for the marker")


class StaticMapExtent(BaseModel):
    """
    Map extent defined by bounding box corners.

    Defines the visible area of the map using two corner coordinates.

    Attributes:
        upper_left: Upper-left (northwest) corner coordinate.
        lower_right: Lower-right (southeast) corner coordinate.

    Example:
        >>> extent = StaticMapExtent(
        ...     upper_left=Coordinate(lat=41.5, lng=2.0),
        ...     lower_right=Coordinate(lat=41.3, lng=2.3)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    upper_left: Coordinate = Field(..., description="Upper-left corner coordinate")
    lower_right: Coordinate = Field(..., description="Lower-right corner coordinate")


ShapeType = Literal["CIRCLE", "RECTANGLE", "SECTOR", "LINE", "POLYLINE", "LABEL"]
"""
Type of shape that can be drawn on a static map:
- CIRCLE: Circle defined by center and radius
- RECTANGLE: Rectangle defined by two corners
- SECTOR: Ring segment (arc between two radii)
- LINE: Straight line between two points
- POLYLINE: Connected line through multiple points
- LABEL: Text label at a coordinate
"""


class StaticMapShapeBase(BaseModel):
    """
    Base class for all static map shapes.

    Provides common styling properties shared by all shape types.
    Subclasses must define their own `type` field with a specific Literal value.

    Attributes:
        outline_color: Color of the shape outline.
        outline_size: Width of the outline in pixels.
        fill_color: Color used to fill the shape interior.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    outline_color: RGBAColor = Field(..., description="Outline color")
    outline_size: int = Field(..., description="Outline size in pixels")
    fill_color: RGBAColor = Field(..., description="Fill color")


class StaticMapCircle(StaticMapShapeBase):
    """
    Circle shape for static maps.

    Draws a circle on the map with specified center and radius.

    Attributes:
        type: Always 'CIRCLE'.
        center: Center coordinate of the circle.
        radius: Circle radius in meters.
        outline_color: Outline color (inherited).
        outline_size: Outline width (inherited).
        fill_color: Fill color (inherited).

    Example:
        >>> circle = StaticMapCircle(
        ...     center=Coordinate(lat=41.38, lng=2.17),
        ...     radius=1000,  # 1km radius
        ...     outline_color=RGBAColor(r=255, g=0, b=0),
        ...     outline_size=2,
        ...     fill_color=RGBAColor(r=255, g=0, b=0, a=50)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    type: Literal["CIRCLE"] = "CIRCLE"
    center: Coordinate = Field(..., description="Center coordinate of the circle")
    radius: float = Field(..., description="Radius in meters")


class StaticMapRectangle(StaticMapShapeBase):
    """
    Rectangle shape for static maps.

    Draws a rectangle defined by two corner coordinates.

    Attributes:
        type: Always 'RECTANGLE'.
        upper_left: Upper-left corner coordinate.
        lower_right: Lower-right corner coordinate.
        outline_color: Outline color (inherited).
        outline_size: Outline width (inherited).
        fill_color: Fill color (inherited).

    Example:
        >>> rect = StaticMapRectangle(
        ...     upper_left=Coordinate(lat=41.4, lng=2.1),
        ...     lower_right=Coordinate(lat=41.3, lng=2.2),
        ...     outline_color=RGBAColor(r=0, g=0, b=255),
        ...     outline_size=2,
        ...     fill_color=RGBAColor(r=0, g=0, b=255, a=30)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    type: Literal["RECTANGLE"] = "RECTANGLE"
    upper_left: Coordinate = Field(..., description="Upper-left corner coordinate")
    lower_right: Coordinate = Field(..., description="Lower-right corner coordinate")


class StaticMapSector(StaticMapShapeBase):
    """
    Sector (ring segment) shape for static maps.

    Draws an arc segment between two radii at different distances from center.

    Attributes:
        type: Always 'SECTOR'.
        center: Center coordinate of the sector.
        inner_radius: Inner radius in meters.
        outer_radius: Outer radius in meters.
        start_angle: Start angle in degrees (0=East, counter-clockwise).
        end_angle: End angle in degrees.
        outline_color: Outline color (inherited).
        outline_size: Outline width (inherited).
        fill_color: Fill color (inherited).

    Example:
        >>> sector = StaticMapSector(
        ...     center=Coordinate(lat=41.38, lng=2.17),
        ...     inner_radius=500,
        ...     outer_radius=1000,
        ...     start_angle=0,
        ...     end_angle=90,
        ...     outline_color=RGBAColor(r=0, g=255, b=0),
        ...     outline_size=1,
        ...     fill_color=RGBAColor(r=0, g=255, b=0, a=100)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    type: Literal["SECTOR"] = "SECTOR"
    center: Coordinate = Field(..., description="Center coordinate of the sector")
    inner_radius: float = Field(..., description="Inner radius in meters")
    outer_radius: float = Field(..., description="Outer radius in meters")
    start_angle: float = Field(..., description="Start angle in degrees")
    end_angle: float = Field(..., description="End angle in degrees")


class StaticMapLine(StaticMapShapeBase):
    """
    Line shape for static maps.

    Draws a straight line between two points.

    Attributes:
        type: Always 'LINE'.
        start: Starting coordinate.
        end: Ending coordinate.
        outline_color: Line color (inherited).
        outline_size: Line width (inherited).
        fill_color: Not used for lines but required by base.

    Example:
        >>> line = StaticMapLine(
        ...     start=Coordinate(lat=41.38, lng=2.17),
        ...     end=Coordinate(lat=41.40, lng=2.20),
        ...     outline_color=RGBAColor(r=0, g=0, b=0),
        ...     outline_size=3,
        ...     fill_color=RGBAColor(r=0, g=0, b=0)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    type: Literal["LINE"] = "LINE"
    start: Coordinate = Field(..., description="Start coordinate")
    end: Coordinate = Field(..., description="End coordinate")


class StaticMapPolyline(StaticMapShapeBase):
    """
    Polyline shape for static maps.

    Draws a connected line through multiple coordinates.

    Attributes:
        type: Always 'POLYLINE'.
        coordinates: List of coordinates forming the polyline.
        outline_color: Line color (inherited).
        outline_size: Line width (inherited).
        fill_color: Fill color if closed polygon.

    Example:
        >>> polyline = StaticMapPolyline(
        ...     coordinates=[
        ...         Coordinate(lat=41.38, lng=2.17),
        ...         Coordinate(lat=41.39, lng=2.18),
        ...         Coordinate(lat=41.40, lng=2.17),
        ...     ],
        ...     outline_color=RGBAColor(r=255, g=165, b=0),
        ...     outline_size=2,
        ...     fill_color=RGBAColor(r=255, g=165, b=0, a=50)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    type: Literal["POLYLINE"] = "POLYLINE"
    coordinates: list[Coordinate] = Field(
        ..., description="List of coordinates forming the polyline"
    )


class StaticMapLabel(StaticMapShapeBase):
    """
    Label shape for static maps.

    Places text at a specific coordinate on the map.

    Attributes:
        type: Always 'LABEL'.
        center: Coordinate where the label is placed.
        text: Text content of the label.
        outline_color: Text outline/border color (inherited).
        outline_size: Text outline width (inherited).
        fill_color: Text fill color (inherited).

    Example:
        >>> label = StaticMapLabel(
        ...     center=Coordinate(lat=41.38, lng=2.17),
        ...     text="Barcelona",
        ...     outline_color=RGBAColor(r=255, g=255, b=255),
        ...     outline_size=1,
        ...     fill_color=RGBAColor(r=0, g=0, b=0)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    type: Literal["LABEL"] = "LABEL"
    center: Coordinate = Field(..., description="Center coordinate of the label")
    text: str = Field(..., description="Label text")


# Union type for all shapes
StaticMapShape = Union[
    StaticMapCircle,
    StaticMapRectangle,
    StaticMapSector,
    StaticMapLine,
    StaticMapPolyline,
    StaticMapLabel,
]
"""Union type representing any valid static map shape."""


class StaticMapOptions(BaseModel):
    """
    Options for generating a static map.

    Configures the map image dimensions, center, and overlay elements.

    Attributes:
        width: Image width in pixels.
        height: Image height in pixels.
        city_name: City name for auto-centering the map.
        country_code: Country code (e.g., 'ESP') for city lookup.
        coordinate_system: Coordinate system (default: 'gdd').
        extent: Map extent (bounding box).
        center: Center coordinate for the map.
        label_op: Label operation mode (0 or 1).
        markers: List of markers to place on the map.
        shapes: List of shapes to draw on the map.
        return_image: If True, return raw image bytes.

    Example:
        >>> options = StaticMapOptions(
        ...     width=800,
        ...     height=600,
        ...     center=Coordinate(lat=41.38, lng=2.17),
        ...     markers=[
        ...         StaticMapMarker(coord=Coordinate(lat=41.38, lng=2.17))
        ...     ],
        ...     return_image=True
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    width: Optional[int] = Field(None, description="Image width in pixels")
    height: Optional[int] = Field(None, description="Image height in pixels")
    city_name: Optional[str] = Field(None, description="City name for centering the map")
    country_code: Optional[str] = Field(None, description="Country code (e.g., 'ESP')")
    coordinate_system: Optional[str] = Field("gdd", description="Coordinate system (e.g., 'gdd')")
    extent: Optional[StaticMapExtent] = Field(None, description="Map extent")
    center: Optional[Coordinate] = Field(None, description="Center coordinate")
    label_op: Optional[Literal[0, 1]] = Field(None, description="Label operation (0 or 1)")
    markers: Optional[list[StaticMapMarker]] = Field(None, description="List of markers")
    shapes: Optional[list[StaticMapShape]] = Field(None, description="List of shapes")
    return_image: bool = Field(False, description="Return image data directly")


class StaticMapResult(BaseModel):
    """
    Result of a static map generation.

    Contains the generated map image URL or raw bytes, plus metadata.

    Attributes:
        image_url: Full URL to the generated map image.
        image_path: Path portion of the image URL.
        width: Actual image width in pixels.
        height: Actual image height in pixels.
        format: Image format ('gif', 'png', or 'jpg').
        scale: Map scale factor.
        center: Actual map center coordinate.
        extent: Actual map extent.
        label: Map label if set.
        image_data: Raw image bytes (when return_image=True).

    Example:
        >>> result = service.generate(options)
        >>> if result.image_data:
        ...     with open("map.png", "wb") as f:
        ...         f.write(result.image_data)
        >>> else:
        ...     print(f"Map URL: {result.image_url}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    image_url: Optional[str] = Field(None, description="URL to the generated map image")
    image_path: Optional[str] = Field(None, description="Path portion of the image URL")
    width: Optional[int] = Field(None, description="Image width in pixels")
    height: Optional[int] = Field(None, description="Image height in pixels")
    format: Optional[Literal["gif", "png", "jpg"]] = Field(None, description="Image format")
    scale: Optional[int] = Field(None, description="Map scale")
    center: Optional[Coordinate] = Field(None, description="Map center coordinate")
    extent: Optional[StaticMapExtent] = Field(None, description="Map extent")
    label: Optional[str] = Field(None, description="Map label")
    image_data: Optional[bytes] = Field(None, description="Raw image data bytes")
