"""
Integration tests for IsochroneService using real Cercalia API.

These tests validate:
- Time-based isochrone calculation
- Distance-based isochrone calculation
- Multiple isochrone calculation
- Different methods (concavehull vs convexhull)
- Error handling
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.isochrone_service import IsochroneService
from cercalia.types.common import Coordinate
from cercalia.types.isochrone import IsochroneMultipleOptions, IsochroneOptions


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> IsochroneService:
    """Create IsochroneService instance."""
    return IsochroneService(config)


# Test coordinates
BARCELONA = Coordinate(lat=41.3851, lng=2.1734)
MADRID = Coordinate(lat=40.4168, lng=-3.7038)


class TestCalculate:
    """Tests for single isochrone calculation."""

    def test_time_based_isochrone_10_minutes(self, service: IsochroneService) -> None:
        """Should calculate time-based isochrone correctly (10 minutes)."""
        result = service.calculate(
            BARCELONA,
            IsochroneOptions(value=10, weight="time"),
        )

        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.center == BARCELONA
        assert result.value == 10
        assert result.weight == "time"
        assert result.level == "600000"  # 10 * 60 * 1000 ms

    def test_time_based_isochrone_5_minutes(self, service: IsochroneService) -> None:
        """Should calculate time-based isochrone for different duration (5 minutes)."""
        result = service.calculate(
            MADRID,
            IsochroneOptions(value=5, weight="time"),
        )

        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.center == MADRID
        assert result.value == 5
        assert result.weight == "time"
        assert result.level == "300000"  # 5 * 60 * 1000 ms

    def test_distance_based_isochrone_1000_meters(self, service: IsochroneService) -> None:
        """Should calculate distance-based isochrone correctly (1000 meters)."""
        result = service.calculate(
            BARCELONA,
            IsochroneOptions(value=1000, weight="distance"),
        )

        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.level == "1000"
        assert result.weight == "distance"
        assert result.value == 1000

    def test_distance_based_isochrone_2000_meters(self, service: IsochroneService) -> None:
        """Should calculate distance-based isochrone for 2000 meters."""
        result = service.calculate(
            MADRID,
            IsochroneOptions(value=2000, weight="distance"),
        )

        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.level == "2000"
        assert result.weight == "distance"
        assert result.value == 2000

    def test_default_weight_is_time(self, service: IsochroneService) -> None:
        """Should use default weight (time) when not specified."""
        result = service.calculate(
            BARCELONA,
            IsochroneOptions(value=15),  # 15 minutes (default weight is time)
        )

        assert result.wkt is not None
        assert result.weight == "time"
        assert result.value == 15
        assert result.level == "900000"  # 15 * 60 * 1000 ms


class TestCalculateMultiple:
    """Tests for multiple isochrone calculation."""

    def test_multiple_time_based_isochrones(self, service: IsochroneService) -> None:
        """Should calculate multiple time-based isochrones."""
        values = [5, 10]
        result = service.calculate_multiple(
            BARCELONA,
            values,
            IsochroneMultipleOptions(weight="time"),
        )

        assert len(result) == 2

        # First isochrone (5 minutes)
        assert result[0].value == 5
        assert result[0].level == "300000"  # 5 * 60 * 1000
        assert result[0].wkt is not None
        assert "POLYGON" in result[0].wkt

        # Second isochrone (10 minutes)
        assert result[1].value == 10
        assert result[1].level == "600000"  # 10 * 60 * 1000
        assert result[1].wkt is not None
        assert "POLYGON" in result[1].wkt

    def test_multiple_distance_based_isochrones(self, service: IsochroneService) -> None:
        """Should calculate multiple distance-based isochrones."""
        values = [500, 1000, 1500]
        result = service.calculate_multiple(
            MADRID,
            values,
            IsochroneMultipleOptions(weight="distance"),
        )

        assert len(result) == 3

        assert result[0].value == 500
        assert result[0].level == "500"
        assert result[0].weight == "distance"

        assert result[1].value == 1000
        assert result[1].level == "1000"
        assert result[1].weight == "distance"

        assert result[2].value == 1500
        assert result[2].level == "1500"
        assert result[2].weight == "distance"

    def test_single_value_in_multiple(self, service: IsochroneService) -> None:
        """Should calculate single isochrone with multiple values array."""
        values = [10]
        result = service.calculate_multiple(BARCELONA, values)

        assert len(result) == 1
        assert result[0].wkt is not None
        assert result[0].level == "600000"  # 10 * 60 * 1000


class TestMethodOptions:
    """Tests for method options."""

    def test_concavehull_vs_convexhull(self, service: IsochroneService) -> None:
        """Should respect method option (concavehull vs convexhull)."""
        result_concave = service.calculate(
            BARCELONA,
            IsochroneOptions(value=10, weight="time", method="concavehull"),
        )

        result_convex = service.calculate(
            BARCELONA,
            IsochroneOptions(value=10, weight="time", method="convexhull"),
        )

        assert result_concave.wkt is not None
        assert result_convex.wkt is not None
        # Both should return valid polygons, but shapes may differ


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_coordinates(self, service: IsochroneService) -> None:
        """Should handle invalid coordinates gracefully."""
        invalid_coord = Coordinate(lat=999, lng=999)

        with pytest.raises(Exception):
            service.calculate(invalid_coord, IsochroneOptions(value=10))

    def test_zero_value(self, service: IsochroneService) -> None:
        """Should handle zero value gracefully."""
        with pytest.raises(ValueError) as exc_info:
            service.calculate(BARCELONA, IsochroneOptions(value=0))

        assert "greater than zero" in str(exc_info.value)

    def test_negative_value(self, service: IsochroneService) -> None:
        """Should handle negative value gracefully."""
        with pytest.raises(ValueError) as exc_info:
            service.calculate(BARCELONA, IsochroneOptions(value=-10))

        assert "greater than zero" in str(exc_info.value)
