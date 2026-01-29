"""
Routing service for Cercalia SDK.

Provides route calculation with support for cars, trucks, and walking.
"""

import re
from typing import Optional

from ..config import CercaliaConfig
from ..types.api_response import ensure_cercalia_array, get_cercalia_attr, get_cercalia_value
from ..types.common import Coordinate
from ..types.routing import RouteResult, RoutingOptions, VehicleType
from .cercalia_client import CercaliaClient


class RoutingService(CercaliaClient):
    """
    Routing service for calculating routes between points.

    Provides methods for:
    - Full route calculation with geometry (WKT)
    - Quick distance/time calculation
    - Support for cars, trucks (with logistics network), and walking

    Example:
        >>> service = RoutingService(config)
        >>> result = service.calculate_route(
        ...     origin=Coordinate(lat=41.3851, lng=2.1734),  # Barcelona
        ...     destination=Coordinate(lat=40.4168, lng=-3.7038),  # Madrid
        ...     options=RoutingOptions(avoid_tolls=True)
        ... )
        >>> print(f"Distance: {result.distance / 1000:.1f} km")
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the routing service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def calculate_route(
        self,
        origin: Coordinate,
        destination: Coordinate,
        options: Optional[RoutingOptions] = None,
    ) -> RouteResult:
        """
        Calculate a route between origin and destination.

        Args:
            origin: Starting point coordinate
            destination: End point coordinate
            options: Routing options (vehicle type, avoid tolls, truck dimensions, etc.)

        Returns:
            RouteResult with geometry (WKT), distance, duration, and optional waypoints

        Raises:
            CercaliaError: If route calculation fails
            ValueError: If no route is found

        Example:
            >>> # Simple car route
            >>> result = service.calculate_route(
            ...     Coordinate(lat=41.3851, lng=2.1734),
            ...     Coordinate(lat=40.4168, lng=-3.7038)
            ... )

            >>> # Truck route with dimensions
            >>> result = service.calculate_route(
            ...     Coordinate(lat=41.3851, lng=2.1734),
            ...     Coordinate(lat=40.4168, lng=-3.7038),
            ...     RoutingOptions(
            ...         vehicle_type="truck",
            ...         truck_weight=40000,  # kg
            ...         truck_height=450,    # cm
            ...     )
            ... )
        """
        options = options or RoutingOptions()

        params: dict[str, str] = {
            "cmd": "route",
            "v": "1",
            "srs": "EPSG:4326",
            "mocs": "gdd",
            "mo_o": f"{origin.lat},{origin.lng}",
            "mo_d": f"{destination.lat},{destination.lng}",
            "weight": "money" if options.avoid_tolls else "time",
            "stagegeometry": "1",
            "stagegeometrysrs": "EPSG:4326",
            "report": "0",
            "lang": "en",
        }

        # Add waypoints
        waypoints = options.waypoints or []
        for i, wp in enumerate(waypoints):
            params[f"mo_{i + 1}"] = f"{wp.lat},{wp.lng}"

        # Truck options
        if options.vehicle_type == "truck":
            params["net"] = "logistics"

            # Physical dimensions (kg -> tons, cm -> meters)
            if options.truck_weight:
                params["vweight"] = str(options.truck_weight / 1000)
            if options.truck_axle_weight:
                params["vaxleweight"] = str(options.truck_axle_weight / 1000)
            if options.truck_height:
                params["vheight"] = str(options.truck_height / 100)
            if options.truck_width:
                params["vwidth"] = str(options.truck_width / 100)
            if options.truck_length:
                params["vlength"] = str(options.truck_length / 100)
            if options.truck_max_velocity:
                params["vmaxvel"] = str(options.truck_max_velocity)

            # Restriction handling
            self._add_truck_restriction(
                params, "vweight", options.block_truck_weight, options.avoid_truck_weight
            )
            self._add_truck_restriction(
                params,
                "vaxleweight",
                options.block_truck_axle_weight,
                options.avoid_truck_axle_weight,
            )
            self._add_truck_restriction(
                params, "vheight", options.block_truck_height, options.avoid_truck_height
            )
            self._add_truck_restriction(
                params, "vwidth", options.block_truck_width, options.avoid_truck_width
            )
            self._add_truck_restriction(
                params, "vlength", options.block_truck_length, options.avoid_truck_length
            )

        response = self._request(params, "Routing")

        route = response.get("route")
        if not route:
            raise ValueError("No route found")

        stages = ensure_cercalia_array(route.get("stages", {}).get("stage", []))

        # Combine WKT from all stages into a single MULTILINESTRING
        line_strings = []
        for stage in stages:
            wkt = get_cercalia_value(stage.get("wkt"))
            if wkt:
                # Extract coordinates from LINESTRING(...)
                match = re.match(r"LINESTRING\s*\((.*)\)", wkt)
                if match:
                    line_strings.append(f"({match.group(1)})")

        wkt = f"MULTILINESTRING({', '.join(line_strings)})" if line_strings else ""

        return RouteResult(
            wkt=wkt,
            distance=float(get_cercalia_attr(route, "dist") or "0") * 1000,  # km -> m
            duration=self._parse_time(get_cercalia_attr(route, "time") or "0"),
            steps=[],
            origin=origin,
            destination=destination,
            waypoints=waypoints if waypoints else None,
        )

    def get_distance_time(
        self,
        origin: Coordinate,
        destination: Coordinate,
        vehicle_type: Optional[VehicleType] = None,
    ) -> dict[str, float]:
        """
        Get distance and time between two points (quick calculation without geometry).

        Args:
            origin: Starting point coordinate
            destination: End point coordinate
            vehicle_type: Optional vehicle type (currently unused, kept for API compatibility)

        Returns:
            Dict with 'distance' (meters) and 'duration' (seconds)

        Example:
            >>> result = service.get_distance_time(
            ...     Coordinate(lat=41.3851, lng=2.1734),
            ...     Coordinate(lat=40.4168, lng=-3.7038)
            ... )
            >>> print(f"Distance: {result['distance'] / 1000:.1f} km")
            >>> print(f"Duration: {result['duration'] / 60:.0f} minutes")
        """
        params: dict[str, str] = {
            "cmd": "route",
            "v": "1",
            "srs": "EPSG:4326",
            "mocs": "gdd",
            "mo_o": f"{origin.lat},{origin.lng}",
            "mo_d": f"{destination.lat},{destination.lng}",
            "weight": "time",
            "stagegeometry": "0",
            "report": "0",
        }

        response = self._request(params, "Routing DistanceTime")

        route = response.get("route")
        if not route:
            raise ValueError("No route found")

        return {
            "distance": float(get_cercalia_attr(route, "dist") or "0") * 1000,  # km -> m
            "duration": self._parse_time(get_cercalia_attr(route, "time") or "0"),
        }

    def _add_truck_restriction(
        self,
        params: dict[str, str],
        key: str,
        block_value: Optional[bool],
        avoid_value: Optional[bool],
    ) -> None:
        """Add truck restriction parameters."""
        if block_value:
            params[f"block{key}"] = "true"
        # Default to avoid if not explicitly blocked
        if avoid_value or (avoid_value is None and not block_value):
            params[f"avoid{key}"] = "true"

    def _parse_time(self, time_str: str) -> float:
        """Parse time string to seconds."""
        if ":" in time_str:
            parts = [int(p) for p in time_str.split(":")]
            if len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
        try:
            return float(time_str)
        except ValueError:
            return 0.0
