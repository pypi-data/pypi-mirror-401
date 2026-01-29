"""
Integration tests for RoutingService.

Uses real API calls (no mocks) as per project requirements.
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.routing_service import RoutingService
from cercalia.types.common import Coordinate
from cercalia.types.routing import RoutingOptions


# Test configuration
config = CercaliaConfig(
    api_key=os.environ["CERCALIA_API_KEY"],
    base_url="https://lb.cercalia.com/services/v2/json",
)

# Test coordinates
BARCELONA = Coordinate(lat=41.3851, lng=2.1734)
MADRID = Coordinate(lat=40.4168, lng=-3.7038)
ZARAGOZA = Coordinate(lat=41.6488, lng=-0.8891)
VALENCIA = Coordinate(lat=39.4699, lng=-0.3763)
PLAZA_CATALUNYA = Coordinate(lat=41.3887, lng=2.1734)
LAS_RAMBLAS = Coordinate(lat=41.3809, lng=2.1734)


class TestRoutingService:
    """Tests for RoutingService."""

    @pytest.fixture
    def service(self) -> RoutingService:
        return RoutingService(config)

    def test_calculate_route_barcelona_madrid(self, service: RoutingService) -> None:
        """Should calculate a car route between Barcelona and Madrid."""
        result = service.calculate_route(BARCELONA, MADRID)

        assert result.wkt is not None
        assert result.distance > 600000  # > 600km
        assert result.duration > 18000  # > 5 hours

    def test_calculate_route_with_waypoints(self, service: RoutingService) -> None:
        """Should calculate a route with multiple waypoints."""
        result = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(waypoints=[ZARAGOZA, VALENCIA]),
        )

        assert result is not None
        assert result.waypoints is not None
        assert len(result.waypoints) == 2
        assert result.distance > 800000  # Route via Zaragoza and Valencia is longer
        assert "LINESTRING" in result.wkt

    def test_avoid_tolls_option(self, service: RoutingService) -> None:
        """Should handle avoidTolls option correctly."""
        with_tolls = service.calculate_route(BARCELONA, MADRID, RoutingOptions(avoid_tolls=False))
        without_tolls = service.calculate_route(BARCELONA, MADRID, RoutingOptions(avoid_tolls=True))

        assert with_tolls.distance is not None
        assert without_tolls.distance is not None
        # Both routes should exist, distances may differ

    def test_short_route(self, service: RoutingService) -> None:
        """Should calculate a short car route."""
        result = service.calculate_route(
            PLAZA_CATALUNYA,
            LAS_RAMBLAS,
            RoutingOptions(vehicle_type="car"),
        )

        assert result.distance < 5000  # < 5km
        assert result.duration > 0

    def test_invalid_coordinates(self, service: RoutingService) -> None:
        """Should throw error for invalid coordinates."""
        invalid = Coordinate(lat=999, lng=999)

        with pytest.raises(Exception):  # Could be CercaliaError or ValueError
            service.calculate_route(BARCELONA, invalid)

    def test_truck_restrictions(self, service: RoutingService) -> None:
        """Should handle truck restrictions (height, weight, etc.)."""
        result = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(
                vehicle_type="truck",
                truck_weight=40000,
                truck_height=450,
                truck_width=250,
                truck_length=1800,
            ),
        )

        assert result.distance > 0
        assert result.duration > 0


class TestLogisticsTruckRouting:
    """Tests for logistics truck routing (net=logistics)."""

    @pytest.fixture
    def service(self) -> RoutingService:
        return RoutingService(config)

    def test_heavy_truck_40t(self, service: RoutingService) -> None:
        """Should calculate a route for a heavy truck (40t)."""
        result = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(vehicle_type="truck", truck_weight=40000),  # 40 tons
        )
        assert result.distance > 0

    def test_high_truck_4_5m(self, service: RoutingService) -> None:
        """Should calculate a route for a high truck (4.5m)."""
        result = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(vehicle_type="truck", truck_height=450),  # 4.5 meters
        )
        assert result.distance > 0

    def test_wide_truck(self, service: RoutingService) -> None:
        """Should potentially return a different route for a very wide truck (3m)."""
        normal_truck = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(vehicle_type="truck", truck_width=200),  # 2m
        )
        wide_truck = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(vehicle_type="truck", truck_width=350),  # 3.5m
        )

        assert wide_truck.distance is not None
        # Both should work, distances may differ

    def test_all_logistics_parameters(self, service: RoutingService) -> None:
        """Should handle all logistics parameters together."""
        result = service.calculate_route(
            BARCELONA,
            MADRID,
            RoutingOptions(
                vehicle_type="truck",
                truck_weight=38000,
                truck_height=400,
                truck_width=255,
                truck_length=1650,
            ),
        )
        assert result.distance > 0


class TestMultiStageRouting:
    """Tests for multi-stage routing (WKT aggregation)."""

    @pytest.fixture
    def service(self) -> RoutingService:
        return RoutingService(config)

    def test_wkt_aggregation_with_waypoints(self, service: RoutingService) -> None:
        """Should combine WKTs from multiple stages when using waypoints."""
        result = service.calculate_route(
            BARCELONA,
            VALENCIA,
            RoutingOptions(waypoints=[ZARAGOZA]),
        )

        # Verify the route includes waypoints
        assert result.waypoints is not None
        assert len(result.waypoints) > 0

        # Verify WKT is valid
        assert result.wkt is not None
        assert "LINESTRING" in result.wkt

        # Distance should be reasonable for Barcelona -> Zaragoza -> Valencia
        assert result.distance > 0
        assert result.duration > 0


class TestGetDistanceTime:
    """Tests for get_distance_time method."""

    @pytest.fixture
    def service(self) -> RoutingService:
        return RoutingService(config)

    def test_get_distance_time(self, service: RoutingService) -> None:
        """Should get distance and time without geometry."""
        result = service.get_distance_time(BARCELONA, MADRID)

        assert "distance" in result
        assert "duration" in result
        assert result["distance"] > 600000  # > 600km
        assert result["duration"] > 18000  # > 5 hours

    def test_get_distance_time_short_route(self, service: RoutingService) -> None:
        """Should get distance and time for a short route."""
        result = service.get_distance_time(PLAZA_CATALUNYA, LAS_RAMBLAS)

        assert result["distance"] < 5000  # < 5km
        assert result["duration"] > 0
