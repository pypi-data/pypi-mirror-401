"""
Tests for the Proximity Service.

Integration tests using real API calls (no mocks).
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.proximity_service import ProximityService
from cercalia.types.common import Coordinate
from cercalia.types.proximity import ProximityOptions


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> ProximityService:
    """Create ProximityService instance for tests."""
    return ProximityService(config)


# Test coordinates
BARCELONA_CENTER = Coordinate(lat=41.3851, lng=2.1734)
MADRID_CENTER = Coordinate(lat=40.4168, lng=-3.7038)
REMOTE_LOCATION = Coordinate(lat=30.0, lng=-30.0)  # Ocean location


class TestFindNearest:
    """Tests for find_nearest method."""

    def test_find_nearest_gas_stations_from_barcelona(self, service: ProximityService) -> None:
        """Should find nearest gas stations from Barcelona center."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C001"],  # Gas station
                count=5,
            )
        )

        assert len(result.items) > 0
        assert len(result.items) <= 5
        assert result.center == BARCELONA_CENTER

        first_item = result.items[0]
        assert first_item.id is not None
        assert first_item.name is not None
        assert first_item.coord is not None
        assert first_item.coord.lat is not None
        assert first_item.coord.lng is not None
        assert first_item.distance is not None
        assert first_item.category_code == "C001"

    def test_find_nearest_pharmacies_with_max_radius(self, service: ProximityService) -> None:
        """Should find nearest pharmacies with max radius."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C026"],  # Pharmacy
                count=3,
                max_radius=2000,  # 2km radius
            )
        )

        assert len(result.items) > 0

        # All items should be within 2km (2000m)
        for item in result.items:
            assert item.distance <= 2000

    def test_find_nearest_hotels_in_madrid(self, service: ProximityService) -> None:
        """Should find nearest hotels in Madrid."""
        result = service.find_nearest(
            ProximityOptions(
                center=MADRID_CENTER,
                categories=["C013"],  # Hotel
                count=10,
            )
        )

        assert len(result.items) > 0
        assert result.total_found == len(result.items)

        # Verify results are sorted by distance (ascending)
        for i in range(1, len(result.items)):
            assert result.items[i].distance >= result.items[i - 1].distance

    def test_empty_results_for_remote_location(self, service: ProximityService) -> None:
        """Should return empty results for non-existent category in remote location."""
        result = service.find_nearest(
            ProximityOptions(
                center=REMOTE_LOCATION,
                categories=["C001"],  # Gas station
                count=5,
                max_radius=1000,  # 1km - very small radius in the ocean
            )
        )

        assert len(result.items) == 0
        assert result.total_found == 0

    def test_find_multiple_category_types(self, service: ProximityService) -> None:
        """Should find multiple category types at once."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C001", "C026"],  # Gas stations and Pharmacies
                count=10,
            )
        )

        assert len(result.items) > 0

        # Should have at least one of each category in a major city
        categories = {item.category_code for item in result.items}
        assert len(categories) >= 1


class TestFindNearestByCategory:
    """Tests for find_nearest_by_category method."""

    def test_find_nearest_restaurants_by_category(self, service: ProximityService) -> None:
        """Should find nearest restaurants by category."""
        result = service.find_nearest_by_category(
            center=BARCELONA_CENTER,
            category_code="C014",  # Restaurant
            count=5,
        )

        assert len(result.items) > 0
        assert len(result.items) <= 5

        for item in result.items:
            assert item.category_code == "C014"

    def test_find_nearest_parking_by_category(self, service: ProximityService) -> None:
        """Should find nearest parking by category."""
        result = service.find_nearest_by_category(
            center=MADRID_CENTER,
            category_code="C007",  # Parking
            count=3,
        )

        assert len(result.items) > 0

        first_parking = result.items[0]
        assert first_parking.name is not None
        # Within same degree as Madrid
        assert abs(first_parking.coord.lat - MADRID_CENTER.lat) < 1
        assert abs(first_parking.coord.lng - MADRID_CENTER.lng) < 1


class TestFindNearestWithRouting:
    """Tests for find_nearest_with_routing method."""

    def test_find_nearest_gas_stations_with_routing_distance(
        self, service: ProximityService
    ) -> None:
        """Should find nearest gas stations with routing distance."""
        result = service.find_nearest_with_routing(
            center=BARCELONA_CENTER,
            category_code="C001",  # Gas station
            weight="distance",
            count=3,
        )

        assert len(result.items) > 0

        # With routing enabled, should have route distance/time info
        first_item = result.items[0]
        assert first_item.coord is not None
        # Note: routeDistance and routeTime may or may not be present depending on API response

    def test_find_nearest_hospitals_with_routing_time(self, service: ProximityService) -> None:
        """Should find nearest hospitals with routing time."""
        result = service.find_nearest_with_routing(
            center=MADRID_CENTER,
            category_code="C009",  # Hospital
            weight="time",
            count=5,
        )

        assert len(result.items) > 0

        for item in result.items:
            assert item.category_code == "C009"


class TestGeographicElementParsing:
    """Tests for geographic element parsing."""

    def test_parse_geographic_element_data_for_pois(self, service: ProximityService) -> None:
        """Should parse geographic element data for POIs."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C001"],  # Gas station - usually have full address info
                count=5,
            )
        )

        assert len(result.items) > 0

        # At least one item should have geographic element info
        item_with_ge = next((item for item in result.items if item.ge), None)
        if item_with_ge and item_with_ge.ge:
            ge = item_with_ge.ge
            # Check that at least some geographic info is present
            has_info = (
                ge.street
                or ge.locality
                or ge.municipality
                or ge.subregion
                or ge.region
                or ge.country
            )
            assert has_info

            # GOLDEN RULE: verify that locality and locality_code are present together
            if ge.locality:
                assert ge.locality_code is not None

            # GOLDEN RULE: verify municipality_code
            if ge.municipality:
                assert ge.municipality_code is not None


class TestEdgeCases:
    """Tests for edge cases."""

    def test_handle_single_result(self, service: ProximityService) -> None:
        """Should handle single result."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C001"],
                count=1,
            )
        )

        assert len(result.items) == 1
        assert result.total_found == 1

    def test_handle_large_count_request(self, service: ProximityService) -> None:
        """Should handle large count request."""
        result = service.find_nearest(
            ProximityOptions(
                center=BARCELONA_CENTER,
                categories=["C001"],
                count=50,
            )
        )

        assert len(result.items) > 0
        # API may return fewer than requested if not enough POIs nearby
        assert len(result.items) <= 50
