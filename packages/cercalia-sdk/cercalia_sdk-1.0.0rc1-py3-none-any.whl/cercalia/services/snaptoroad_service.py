"""
SnapToRoad Service for Cercalia SDK.

This service matches raw GPS coordinates to the road network, providing
"snapped" geometries that follow actual roads. Essential for fleet management,
vehicle tracking, and trip analysis applications.
"""

from typing import Any, Optional

from ..config import CercaliaConfig
from ..types.api_response import (
    get_cercalia_attr,
    get_cercalia_value,
)
from ..types.common import Coordinate
from ..types.snaptoroad import (
    SnapToRoadOptions,
    SnapToRoadPoint,
    SnapToRoadResult,
    SnapToRoadSegment,
)
from ..utils.logger import logger
from .cercalia_client import CercaliaClient


class SnapToRoadService(CercaliaClient):
    """
    Service for GPS track map matching.

    Matches raw GPS coordinates to the road network, providing snapped
    geometries that follow actual roads.

    ## Key Features
    - Map Matching: Snap GPS points to the nearest road network
    - Speed Detection: Identify speed violations based on road limits
    - Segment Grouping: Group results by custom attributes
    - Geometry Simplification: Control output complexity with tolerance

    ## Use Cases
    - Fleet vehicle tracking
    - Trip reconstruction from GPS logs
    - Speed violation analysis
    - Road usage statistics
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the SnapToRoad service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def match(
        self,
        points: list[SnapToRoadPoint],
        options: Optional[SnapToRoadOptions] = None,
    ) -> SnapToRoadResult:
        """
        Match GPS track points to the road network.

        Takes an array of GPS points and returns road-matched geometries.
        Points should be in temporal order for best matching results.

        Args:
            points: Array of GPS track points (minimum 2 required)
            options: Map matching options

        Returns:
            Matched road segments with distances and optional speeding info

        Raises:
            ValueError: If fewer than 2 points provided
            CercaliaError: If API returns an error
        """
        if not points or len(points) < 2:
            raise ValueError("SnapToRoad requires at least 2 GPS points")

        options = options or SnapToRoadOptions()

        params: dict[str, str] = {
            "cmd": "geomtrack",
            "srs": "EPSG:4326",
        }

        # Build track parameter
        params["track"] = self._build_track_string(points)

        # Weight type (distance or time)
        if options.weight:
            params["weight"] = options.weight

        # Country net
        if options.net:
            params["net"] = options.net

        # Geometry coordinate system
        if options.geometry_srs:
            params["geometrysrs"] = options.geometry_srs

        # Geometry simplification
        if options.geometry_tolerance is not None:
            params["geometrytolerance"] = str(options.geometry_tolerance)

        # Return original GPS points displaced on road
        if options.points:
            params["points"] = "true"

        # Speeding detection
        if options.speeding:
            params["speeding"] = "true"
            if options.speed_tolerance is not None:
                params["speedtolerance"] = str(options.speed_tolerance)

        # Low-level control parameters
        if options.only_track:
            params["onlytrack"] = "true"

        if options.max_direction_search_distance is not None:
            params["maxdirectionsearchdistance"] = str(options.max_direction_search_distance)

        if options.max_search_distance is not None:
            params["maxsearchdistance"] = str(options.max_search_distance)

        if options.factor is not None:
            params["factor"] = str(options.factor)

        try:
            data = self._request(params, "SnapToRoadService")
            return self._parse_response(data)
        except Exception as e:
            logger.error(f"[SnapToRoadService] Match error: {e}")
            raise

    def match_with_groups(
        self,
        points: list[Coordinate],
        group_size: int = 10,
        options: Optional[SnapToRoadOptions] = None,
    ) -> SnapToRoadResult:
        """
        Match GPS track with automatic segment grouping by attribute.

        Convenience method that automatically assigns attributes to points
        for segment grouping. Useful for identifying distinct trip legs.

        Args:
            points: Array of GPS coordinates
            group_size: Number of points per group (default: 10)
            options: Map matching options

        Returns:
            Matched segments grouped by attribute
        """
        grouped_points = [
            SnapToRoadPoint(
                coord=coord,
                attribute=chr(65 + i // group_size),  # A, B, C, ...
            )
            for i, coord in enumerate(points)
        ]

        return self.match(grouped_points, options)

    def match_with_speeding_detection(
        self,
        points: list[SnapToRoadPoint],
        tolerance_kmh: int = 10,
    ) -> SnapToRoadResult:
        """
        Match GPS track with speed data for violation detection.

        Convenience method that enables speeding detection with sensible defaults.

        Args:
            points: Array of GPS points with speed data
            tolerance_kmh: Speed tolerance in km/h (default: 10)

        Returns:
            Matched segments with speeding flags
        """
        return self.match(
            points,
            SnapToRoadOptions(speeding=True, speed_tolerance=tolerance_kmh),
        )

    def match_simplified(
        self,
        points: list[SnapToRoadPoint],
        tolerance: int = 50,
    ) -> SnapToRoadResult:
        """
        Get a simplified/generalized track matching.

        Convenience method for getting a simplified geometry suitable for display.
        Higher tolerance values produce simpler geometries with fewer points.

        Args:
            points: Array of GPS points
            tolerance: Simplification tolerance in meters (default: 50)

        Returns:
            Matched segments with simplified geometries
        """
        return self.match(points, SnapToRoadOptions(geometry_tolerance=tolerance))

    # ============================================
    # PRIVATE HELPERS
    # ============================================

    def _build_track_string(self, points: list[SnapToRoadPoint]) -> str:
        """
        Build the track parameter string from GPS points.

        Cercalia format: [lng,lat@compass,angle@@speed@@@attribute]

        Each point is enclosed in brackets and contains:
        - lng,lat (required)
        - @compass,angle (optional - heading direction)
        - @@speed (optional - speed in km/h)
        - @@@attribute (optional - grouping identifier)
        """
        result_parts: list[str] = []

        for p in points:
            # Start with coordinates
            point_str = f"{p.coord.lng},{p.coord.lat}"

            # Add compass and angle if provided
            if p.compass is not None and p.angle is not None:
                point_str += f"@{p.compass},{p.angle}"
            elif p.compass is not None:
                # If only compass is provided, use 0 for angle
                point_str += f"@{p.compass},0"

            # Add speed if provided
            if p.speed is not None:
                point_str += f"@@{p.speed}"

            # Add attribute if provided
            if p.attribute is not None:
                point_str += f"@@@{p.attribute}"

            # Each point must be in brackets
            result_parts.append(f"[{point_str}]")

        return ",".join(result_parts)

    def _parse_response(self, data: dict[str, Any]) -> SnapToRoadResult:
        """
        Parse the Cercalia geomtrack API response.

        Response structure:
        {
          "track": {
            "geometry": [{
              "@attribute": "A",
              "@distance": "0.97",
              "@speeding": "true",
              "@speedinglevel": "2",
              "wkt": { "value": "LINESTRING(...)" }
            }]
          }
        }
        """
        track = data.get("track")
        if not track:
            raise ValueError("Cercalia SnapToRoad: No track data in response")

        geometries = track.get("geometry")
        if not geometries:
            return SnapToRoadResult(segments=[], total_distance=0.0)

        # Normalize to array
        if not isinstance(geometries, list):
            geometries = [geometries]

        segments = [self._parse_segment(g) for g in geometries]
        total_distance = sum(seg.distance for seg in segments)

        return SnapToRoadResult(segments=segments, total_distance=total_distance)

    def _parse_segment(self, g: dict[str, Any]) -> SnapToRoadSegment:
        """Parse a single geometry segment from the response."""
        # Extract WKT - handle different response formats
        wkt_value = get_cercalia_value(g.get("wkt"))
        if not wkt_value and isinstance(g.get("wkt"), dict):
            wkt_value = g["wkt"].get("value", "")
        wkt = wkt_value or ""

        # Distance
        distance_str = get_cercalia_attr(g, "distance") or "0"
        distance = float(distance_str)

        segment = SnapToRoadSegment(wkt=wkt, distance=distance)

        # Attribute
        attr = get_cercalia_attr(g, "attribute")
        if attr:
            segment.attribute = attr

        # Speeding flags
        speeding = get_cercalia_attr(g, "speeding")
        if speeding == "true" or speeding == "1":
            segment.speeding = True
            level = get_cercalia_attr(g, "speedinglevel")
            if level is not None:
                segment.speeding_level = int(level)
        elif speeding is not None:
            segment.speeding = False

        return segment
