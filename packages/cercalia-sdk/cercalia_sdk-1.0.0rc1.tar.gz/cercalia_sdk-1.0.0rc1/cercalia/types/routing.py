"""
Routing types for Cercalia SDK.

This module contains types for route calculation operations including
car, truck, and pedestrian routing with support for waypoints, time windows,
traffic conditions, and toll cost optimization.

Example:
    >>> from cercalia.types.routing import RoutingOptions, RoutingWaypoint
    >>> from cercalia.types.common import Coordinate
    >>> options = RoutingOptions(
    ...     vehicle_type="car",
    ...     weight="time",
    ...     avoid_tolls=True
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate

# Type aliases for routing
VehicleType = Literal["car", "truck", "walking"]
"""
Vehicle type for routing:
- car: Standard car routing
- truck: Truck routing with logistics network
- walking: Pedestrian routing
"""

RouteNetwork = Literal["car", "logistics", "espw", "usaw"]
"""
Network type for routing:
- car: Standard car network (default)
- logistics: Truck/logistics network with weight/height restrictions
- espw: Spanish walking network
- usaw: USA walking network
"""

RouteWeight = Literal[
    "time",
    "distance",
    "money",
    "realtime",
    "fast",
    "short",
    "sptime",
    "spmoney",
    "timerimp",
]
"""
Weight/optimization criteria for route calculation:
- time: Optimize for shortest time
- distance: Optimize for shortest distance
- money: Optimize for lowest toll cost
- realtime: Use real-time traffic data
- fast: Fast route (may be longer in distance)
- short: Short route (may be longer in time)
- sptime: Scheduled/predictive time (requires departure_time)
- spmoney: Scheduled/predictive toll cost (requires departure_time)
- timerimp: Time with traffic impedance
"""


class RouteStep(BaseModel):
    """
    A single step in a route with turn-by-turn instruction.

    Represents one maneuver or navigation instruction within a calculated
    route, including the instruction text, distance, duration, and location.

    Attributes:
        instruction: Human-readable turn-by-turn instruction.
        distance: Distance of this step in meters.
        duration: Duration of this step in seconds.
        coord: Geographic coordinate at the start of this step.

    Example:
        >>> for step in route.steps:
        ...     print(f"{step.instruction} ({step.distance}m)")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    instruction: str = Field(..., description="Turn-by-turn instruction text")
    distance: float = Field(..., description="Distance of this step in meters")
    duration: float = Field(..., description="Duration of this step in seconds")
    coord: Coordinate = Field(..., description="Coordinate at this step")


class RouteResult(BaseModel):
    """
    Result of a route calculation.

    Contains the complete route information including geometry, distance,
    duration, turn-by-turn instructions, and optional toll cost information.

    Attributes:
        wkt: Route geometry as WKT MULTILINESTRING for map rendering.
        distance: Total route distance in meters.
        duration: Total route duration in seconds.
        steps: Optional list of turn-by-turn navigation instructions.
        origin: Starting coordinate of the route.
        destination: Ending coordinate of the route.
        waypoints: Intermediate waypoints (if any were specified).
        toll_cost: Total toll cost (if weight includes toll calculation).
        currency: Currency code for toll_cost (e.g., 'EUR').

    Example:
        >>> route = service.calculate_route(origin, destination, options)
        >>> print(f"Distance: {route.distance / 1000:.1f} km")
        >>> print(f"Duration: {route.duration / 60:.0f} minutes")
        >>> if route.toll_cost:
        ...     print(f"Tolls: {route.toll_cost} {route.currency}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    wkt: str = Field(..., description="Route geometry as WKT MULTILINESTRING")
    distance: float = Field(..., description="Total distance in meters")
    duration: float = Field(..., description="Total duration in seconds")
    steps: Optional[list[RouteStep]] = Field(None, description="Turn-by-turn instructions")
    origin: Coordinate = Field(..., description="Route origin coordinate")
    destination: Coordinate = Field(..., description="Route destination coordinate")
    waypoints: Optional[list[Coordinate]] = Field(None, description="Intermediate waypoints")
    toll_cost: Optional[float] = Field(None, description="Total toll cost")
    currency: Optional[str] = Field(None, description="Currency for toll cost")


class RoutingWaypoint(BaseModel):
    """
    A waypoint with optional time window constraints.

    Used for route optimization with delivery time windows. When time
    windows are specified, the routing algorithm will try to reach
    each waypoint within its designated time slot.

    Attributes:
        coord: Geographic coordinate of the waypoint.
        time_window_start: Earliest arrival time (HH:MM format).
        time_window_end: Latest arrival time (HH:MM format).

    Example:
        >>> waypoint = RoutingWaypoint(
        ...     coord=Coordinate(lat=41.3851, lng=2.1734),
        ...     time_window_start="09:00",
        ...     time_window_end="12:00"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Waypoint coordinate")
    time_window_start: Optional[str] = Field(None, description="Start of time window (HH:MM)")
    time_window_end: Optional[str] = Field(None, description="End of time window (HH:MM)")


class RoutingOptions(BaseModel):
    """
    Options for route calculation.

    Comprehensive configuration for route calculation including vehicle type,
    optimization criteria, network selection, and various routing preferences.

    Attributes:
        vehicle_type: Type of vehicle (car, truck, walking).
        weight: Optimization criteria (time, distance, money, etc.).
        net: Network type to use for routing.
        avoid_tolls: Whether to avoid toll roads.
        report: Include detailed route report.
        departure_time: ISO 8601 departure time for time-based routing.
        alternatives: Number of alternative routes to calculate (1-3).
        direction: Route direction (forward/backward).
        reorder: Enable TSP optimization for waypoints.
        waypoints: Intermediate waypoints for the route.

    Example:
        >>> # Simple car routing
        >>> options = RoutingOptions(
        ...     vehicle_type="car",
        ...     weight="time",
        ...     avoid_tolls=True
        ... )
        >>> # Truck routing with dimensions
        >>> options = RoutingOptions(
        ...     vehicle_type="truck",
        ...     net="logistics",
        ...     truck_weight=40000,
        ...     truck_height=400,
        ...     block_truck_height=True
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    # Vehicle and network
    vehicle_type: Optional[VehicleType] = Field(None, description="Vehicle type (car, truck, walking)")
    weight: Optional[RouteWeight] = Field(
        None, description="Optimization criteria (time, distance, money, etc.)"
    )
    net: Optional[RouteNetwork] = Field(None, description="Network type (car, logistics, espw, usaw)")

    # Route preferences
    avoid_tolls: Optional[bool] = Field(None, description="Avoid toll roads")
    report: Optional[bool] = Field(None, description="Include detailed report")

    # Time-based options
    departure_time: Optional[str] = Field(
        None,
        description="Departure time in ISO 8601 format (required for sptime/spmoney)",
    )

    # Alternative routes
    alternatives: Optional[int] = Field(
        None, description="Number of alternative routes (1-3)", ge=1, le=3
    )

    # Route direction
    direction: Optional[Literal["forward", "backward"]] = Field(
        None, description="Route direction from origin"
    )

    # Waypoint reordering (TSP)
    reorder: Optional[bool] = Field(
        None, description="Enable waypoint reordering for optimal route (TSP)"
    )
    start_window: Optional[str] = Field(
        None, description="Start of time window for optimization (HH:MM)"
    )
    end_window: Optional[str] = Field(None, description="End of time window for optimization (HH:MM)")

    # Real-time traffic
    block_realtime: Optional[bool] = Field(None, description="Block roads with real-time issues")
    avoid_realtime: Optional[bool] = Field(None, description="Avoid roads with real-time issues")

    # Ferries
    block_ferries: Optional[bool] = Field(None, description="Block ferry routes")
    avoid_ferries: Optional[bool] = Field(None, description="Avoid ferry routes")

    # Truck dimensions (in SI units)
    truck_weight: Optional[float] = Field(None, description="Truck total weight in kg")
    truck_axle_weight: Optional[float] = Field(None, description="Truck axle weight in kg")
    truck_height: Optional[float] = Field(None, description="Truck height in cm")
    truck_width: Optional[float] = Field(None, description="Truck width in cm")
    truck_length: Optional[float] = Field(None, description="Truck length in cm")
    truck_max_velocity: Optional[float] = Field(None, description="Truck max velocity in km/h")

    # Truck restriction handling
    block_truck_weight: Optional[bool] = Field(
        None, description="Block roads with weight restrictions"
    )
    avoid_truck_weight: Optional[bool] = Field(
        None, description="Avoid roads with weight restrictions"
    )
    block_truck_axle_weight: Optional[bool] = Field(
        None, description="Block roads with axle weight restrictions"
    )
    avoid_truck_axle_weight: Optional[bool] = Field(
        None, description="Avoid roads with axle weight restrictions"
    )
    block_truck_height: Optional[bool] = Field(
        None, description="Block roads with height restrictions"
    )
    avoid_truck_height: Optional[bool] = Field(
        None, description="Avoid roads with height restrictions"
    )
    block_truck_length: Optional[bool] = Field(
        None, description="Block roads with length restrictions"
    )
    avoid_truck_length: Optional[bool] = Field(
        None, description="Avoid roads with length restrictions"
    )
    block_truck_width: Optional[bool] = Field(None, description="Block roads with width restrictions")
    avoid_truck_width: Optional[bool] = Field(None, description="Avoid roads with width restrictions")

    # Waypoints (for convenience, can also be passed directly to calculate_route)
    waypoints: Optional[list[Coordinate]] = Field(None, description="Intermediate waypoints")
