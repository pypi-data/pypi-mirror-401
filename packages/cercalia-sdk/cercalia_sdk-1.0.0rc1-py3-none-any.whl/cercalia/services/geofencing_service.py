"""
Geofencing Service for Cercalia SDK.

This service provides point-in-polygon geofencing capabilities using the
Cercalia InsideGeoms API. Essential for delivery zone validation, fleet
monitoring, and location-based alerts.
"""

from typing import Any, Optional

from ..config import CercaliaConfig
from ..types.api_response import (
    ensure_cercalia_array,
    get_cercalia_attr,
    get_cercalia_value,
)
from ..types.common import Coordinate
from ..types.geofencing import (
    GeofenceMatch,
    GeofenceOptions,
    GeofencePoint,
    GeofencePointMatch,
    GeofenceResult,
    GeofenceShape,
)
from ..utils.logger import logger
from .cercalia_client import CercaliaClient


class GeofencingService(CercaliaClient):
    """
    Service for point-in-polygon geofencing operations.

    Provides methods to check whether points are inside defined geographic
    zones (geofences), supporting both polygons and circles.

    ## Key Features
    - Polygon Geofences: Define zones using WKT polygon geometries
    - Circle Geofences: Define zones using center point and radius
    - Batch Processing: Check multiple points against multiple zones in one call

    ## Use Cases
    - Delivery zone validation
    - Fleet geofencing alerts
    - Service area verification
    - Restricted zone monitoring
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the Geofencing service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def check(
        self,
        shapes: list[GeofenceShape],
        points: list[GeofencePoint],
        options: Optional[GeofenceOptions] = None,
    ) -> GeofenceResult:
        """
        Check which points are inside which geofence shapes.

        Performs point-in-polygon checks for all combinations of shapes and points.
        Returns only shapes that contain at least one point.

        Args:
            shapes: Array of geofence shapes (polygons or circles)
            points: Array of points to check
            options: Optional coordinate system settings

        Returns:
            Result with matches (shapes containing points)

        Raises:
            ValueError: If no shapes or points provided
            CercaliaError: If API returns an error
        """
        if not shapes:
            raise ValueError("Geofencing requires at least one shape")
        if not points:
            raise ValueError("Geofencing requires at least one point")

        options = options or GeofenceOptions()

        params: dict[str, str] = {"cmd": "insidegeoms"}

        # Build geoms parameter: [WKT|ID],[WKT|ID],...
        params["geoms"] = self._build_geoms_string(shapes)

        # Build molist parameter: [lng,lat|ID],[lng,lat|ID],...
        params["molist"] = self._build_molist_string(points)

        # Coordinate systems
        params["srs"] = options.shape_srs or "EPSG:4326"
        if options.point_srs:
            params["mocs"] = options.point_srs

        try:
            data = self._request(params, "GeofencingService")
            return self._map_response(data, len(shapes), len(points))
        except Exception as e:
            logger.error(f"[GeofencingService] Check error: {e}")
            raise

    def check_point(
        self,
        shapes: list[GeofenceShape],
        point: Coordinate,
    ) -> list[str]:
        """
        Check if a single point is inside any of the given shapes.

        Convenience method for single-point geofence checks.

        Args:
            shapes: Array of geofence shapes
            point: Single point to check

        Returns:
            Array of shape IDs that contain the point
        """
        result = self.check(shapes, [GeofencePoint(id="point", coord=point)])

        return [m.shape_id for m in result.matches if any(p.id == "point" for p in m.points_inside)]

    def is_inside_circle(
        self,
        center: Coordinate,
        radius_meters: int,
        point: Coordinate,
    ) -> bool:
        """
        Check if a point is inside a circular zone.

        Convenience method for circular geofence checks.

        Args:
            center: Center of the circular zone
            radius_meters: Radius of the zone in meters
            point: Point to check

        Returns:
            True if point is inside the circle
        """
        circle_wkt = f"CIRCLE({center.lng} {center.lat}, {radius_meters})"
        zones = self.check_point([GeofenceShape(id="circle", wkt=circle_wkt)], point)
        return "circle" in zones

    def is_inside_polygon(
        self,
        polygon_wkt: str,
        point: Coordinate,
    ) -> bool:
        """
        Check if a point is inside a polygon zone.

        Convenience method for polygon geofence checks.

        Args:
            polygon_wkt: Polygon in WKT format
            point: Point to check

        Returns:
            True if point is inside the polygon
        """
        zones = self.check_point([GeofenceShape(id="polygon", wkt=polygon_wkt)], point)
        return "polygon" in zones

    def filter_points_in_shape(
        self,
        shape: GeofenceShape,
        points: list[GeofencePoint],
    ) -> list[GeofencePoint]:
        """
        Filter points to only those inside a shape.

        Useful for filtering a list of locations to only those within a service area.

        Args:
            shape: Single geofence shape
            points: Array of points to filter

        Returns:
            Only points that are inside the shape
        """
        if not points:
            return []

        result = self.check([shape], points)

        match = next((m for m in result.matches if m.shape_id == shape.id), None)
        if not match:
            return []

        # Map back to original points
        inside_ids = {p.id for p in match.points_inside}
        return [p for p in points if p.id in inside_ids]

    def create_circle(
        self,
        id: str,
        center: Coordinate,
        radius_meters: int,
    ) -> GeofenceShape:
        """
        Create a circular geofence shape helper.

        Args:
            id: Unique identifier for the geofence
            center: Center coordinate
            radius_meters: Radius in meters

        Returns:
            GeofenceShape object
        """
        return GeofenceShape(
            id=id,
            wkt=f"CIRCLE({center.lng} {center.lat}, {radius_meters})",
        )

    def create_rectangle(
        self,
        id: str,
        southwest: Coordinate,
        northeast: Coordinate,
    ) -> GeofenceShape:
        """
        Create a rectangular geofence shape helper.

        Args:
            id: Unique identifier for the geofence
            southwest: Southwest corner coordinate
            northeast: Northeast corner coordinate

        Returns:
            GeofenceShape object with polygon WKT
        """
        sw = southwest
        ne = northeast
        nw = Coordinate(lat=ne.lat, lng=sw.lng)
        se = Coordinate(lat=sw.lat, lng=ne.lng)

        wkt = f"POLYGON(({sw.lng} {sw.lat}, {se.lng} {se.lat}, {ne.lng} {ne.lat}, {nw.lng} {nw.lat}, {sw.lng} {sw.lat}))"

        return GeofenceShape(id=id, wkt=wkt)

    # ============================================
    # PRIVATE HELPERS
    # ============================================

    def _build_geoms_string(self, shapes: list[GeofenceShape]) -> str:
        """
        Build the geoms parameter string from shapes.
        Format: [WKT|ID],[WKT|ID],...
        """
        return ",".join(f"[{s.wkt}|{s.id}]" for s in shapes)

    def _build_molist_string(self, points: list[GeofencePoint]) -> str:
        """
        Build the molist parameter string from points.
        Format: [lng,lat|ID],[lng,lat|ID],...
        """
        return ",".join(f"[{p.coord.lng},{p.coord.lat}|{p.id}]" for p in points)

    def _map_response(
        self,
        data: dict[str, Any],
        total_shapes: int,
        total_points: int,
    ) -> GeofenceResult:
        """
        Map the Cercalia insidegeoms API response to GeofenceResult.

        Following the Golden Rules:
        1. Direct mapping: No fallbacks, map 1:1 from response
        2. Strict coordinates: No default values (0,0)
        """
        insidegeoms = data.get("insidegeoms")
        if not insidegeoms:
            return GeofenceResult(
                matches=[],
                total_points_checked=total_points,
                total_shapes_checked=total_shapes,
            )

        geometries = insidegeoms.get("geometry")
        if not geometries:
            return GeofenceResult(
                matches=[],
                total_points_checked=total_points,
                total_shapes_checked=total_shapes,
            )

        # Normalize to array
        geometry_array = ensure_cercalia_array(geometries)

        matches = [
            self._map_geometry(g) for g in geometry_array if self._map_geometry(g).points_inside
        ]

        return GeofenceResult(
            matches=matches,
            total_points_checked=total_points,
            total_shapes_checked=total_shapes,
        )

    def _map_geometry(self, g: dict[str, Any]) -> GeofenceMatch:
        """
        Map a single geometry from the Cercalia response to a GeofenceMatch.

        Following Golden Rules:
        - Use get_cercalia_attr for @id attributes
        - Use get_cercalia_value for value objects
        - No default values for coordinates
        """
        shape_id = get_cercalia_attr(g, "id") or ""
        shape_wkt = get_cercalia_value(g.get("wkt")) or ""

        points_inside: list[GeofencePointMatch] = []

        molist = g.get("molist")
        if molist and molist.get("mo"):
            mo_array = ensure_cercalia_array(molist["mo"])
            points_inside = [self._map_point(mo) for mo in mo_array]

        return GeofenceMatch(
            shape_id=shape_id,
            shape_wkt=shape_wkt,
            points_inside=points_inside,
        )

    def _map_point(self, mo: dict[str, Any]) -> GeofencePointMatch:
        """
        Map a single point (mo) from the Cercalia response.

        Following Golden Rules:
        - Strict coordinates: validate existence before parsing
        """
        point_id = get_cercalia_attr(mo, "id") or ""
        coord_obj = mo.get("coord")

        if not coord_obj:
            raise ValueError(f"Missing coordinate for point {point_id}")

        x = get_cercalia_attr(coord_obj, "x")
        y = get_cercalia_attr(coord_obj, "y")

        if not x or not y:
            raise ValueError(f"Invalid coordinates for point {point_id}: x={x}, y={y}")

        try:
            lat = float(y)
            lng = float(x)
        except ValueError as e:
            raise ValueError(f"Cannot parse coordinates for point {point_id}: x={x}, y={y}") from e

        return GeofencePointMatch(id=point_id, coord=Coordinate(lat=lat, lng=lng))
