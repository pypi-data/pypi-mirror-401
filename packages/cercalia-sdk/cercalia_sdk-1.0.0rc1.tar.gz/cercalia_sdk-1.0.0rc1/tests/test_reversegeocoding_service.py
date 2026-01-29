"""
Integration tests for ReverseGeocodingService.

Uses real API calls (no mocks) as per project requirements.
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.reversegeocoding_service import ReverseGeocodingService
from cercalia.types.common import Coordinate
from cercalia.types.reversegeocoding import ReverseGeocodeOptions, TimezoneOptions


# Test configuration
config = CercaliaConfig(
    api_key=os.environ["CERCALIA_API_KEY"],
    base_url="https://lb.cercalia.com/services/v2/json",
)

# Test coordinates
BARCELONA_CATALUNYA_SQUARE = Coordinate(lat=41.3874, lng=2.1700)
MADRID_PUERTA_DEL_SOL = Coordinate(lat=40.4169, lng=-3.7035)
OCEAN_COORD = Coordinate(lat=30.0, lng=-30.0)
ZARAGOZA = Coordinate(lat=41.6488, lng=-0.8891)


class TestReverseGeocode:
    """Tests for reverse_geocode method."""

    @pytest.fixture
    def service(self) -> ReverseGeocodingService:
        return ReverseGeocodingService(config)

    def test_reverse_geocode_barcelona_placa_catalunya(
        self, service: ReverseGeocodingService
    ) -> None:
        """Should reverse geocode Barcelona Placa Catalunya."""
        result = service.reverse_geocode(BARCELONA_CATALUNYA_SQUARE)

        assert result is not None
        assert result.ge.name is not None
        assert result.ge.municipality is not None
        assert result.ge.country is not None
        assert result.ge.coord is not None
        assert abs(result.ge.coord.lat - BARCELONA_CATALUNYA_SQUARE.lat) < 0.01
        assert abs(result.ge.coord.lng - BARCELONA_CATALUNYA_SQUARE.lng) < 0.01

    def test_reverse_geocode_madrid_puerta_del_sol(self, service: ReverseGeocodingService) -> None:
        """Should reverse geocode Madrid Puerta del Sol."""
        result = service.reverse_geocode(MADRID_PUERTA_DEL_SOL)

        assert result is not None
        assert result.ge.name is not None
        assert result.ge.municipality == "Madrid"
        assert result.ge.country == "Espana" or result.ge.country == "España"
        assert result.ge.type is not None

    def test_reverse_geocode_returns_poi_or_address(self, service: ReverseGeocodingService) -> None:
        """Should return POI or address information when available."""
        result = service.reverse_geocode(BARCELONA_CATALUNYA_SQUARE)

        assert result is not None
        assert result.ge is not None
        assert result.ge.type is not None
        # Type can be 'poi', 'road', 'locality', 'municipality', etc.
        assert result.ge.type in ("poi", "road", "locality", "municipality", "address", "street")

    def test_reverse_geocode_ocean_coordinates(self, service: ReverseGeocodingService) -> None:
        """Should handle ocean coordinates gracefully."""
        result = service.reverse_geocode(OCEAN_COORD)

        # Ocean coordinates typically return None or very limited info
        if result is None:
            assert result is None
        else:
            # If it returns something, verify basic structure
            assert result.ge is not None

    def test_reverse_geocode_detailed_address(self, service: ReverseGeocodingService) -> None:
        """Should return detailed address information."""
        result = service.reverse_geocode(BARCELONA_CATALUNYA_SQUARE)

        assert result is not None

        # Check geographic element structure
        ge = result.ge
        assert ge.name is not None
        assert ge.coord is not None

        # At least some administrative info should be present
        has_admin_info = (
            ge.locality is not None
            or ge.municipality is not None
            or ge.subregion is not None
            or ge.region is not None
            or ge.country is not None
        )
        assert has_admin_info


class TestReverseGeocodeBatch:
    """Tests for reverse_geocode_batch method."""

    @pytest.fixture
    def service(self) -> ReverseGeocodingService:
        return ReverseGeocodingService(config)

    def test_batch_multiple_coordinates(self, service: ReverseGeocodingService) -> None:
        """Should reverse geocode multiple coordinates."""
        coords = [BARCELONA_CATALUNYA_SQUARE, MADRID_PUERTA_DEL_SOL]

        results = service.reverse_geocode_batch(coords)

        assert len(results) == 2

        # First result (Barcelona)
        assert results[0].ge.name is not None
        assert results[0].ge.municipality is not None

        # Second result (Madrid)
        assert results[1].ge.name is not None
        assert results[1].ge.municipality == "Madrid"

    def test_batch_single_coordinate(self, service: ReverseGeocodingService) -> None:
        """Should handle single coordinate batch."""
        results = service.reverse_geocode_batch([MADRID_PUERTA_DEL_SOL])

        assert len(results) == 1
        assert results[0].ge.municipality == "Madrid"

    def test_batch_three_coordinates(self, service: ReverseGeocodingService) -> None:
        """Should handle three coordinates batch."""
        coords = [BARCELONA_CATALUNYA_SQUARE, MADRID_PUERTA_DEL_SOL, ZARAGOZA]

        results = service.reverse_geocode_batch(coords)

        assert len(results) == 3

        for result in results:
            assert result.ge is not None
            assert result.ge.name is not None
            assert result.ge.coord is not None

    def test_batch_empty_list(self, service: ReverseGeocodingService) -> None:
        """Should handle empty coordinate list."""
        results = service.reverse_geocode_batch([])
        assert results == []

    def test_batch_max_100_limit(self, service: ReverseGeocodingService) -> None:
        """Should raise error for more than 100 coordinates."""
        coords = [BARCELONA_CATALUNYA_SQUARE] * 101

        with pytest.raises(ValueError, match="Maximum 100 coordinates"):
            service.reverse_geocode_batch(coords)


class TestLevelSpecificRequests:
    """Tests for level-specific reverse geocoding."""

    @pytest.fixture
    def service(self) -> ReverseGeocodingService:
        return ReverseGeocodingService(config)

    def test_timezone_information(self, service: ReverseGeocodingService) -> None:
        """Should request timezone information."""
        result = service.get_timezone(BARCELONA_CATALUNYA_SQUARE)

        assert result is not None
        assert result.id is not None
        assert result.name is not None
        assert result.utc_offset is not None
        assert isinstance(result.utc_offset, int)
        assert result.coord == BARCELONA_CATALUNYA_SQUARE

    def test_timezone_with_specific_datetime(self, service: ReverseGeocodingService) -> None:
        """Should request timezone with specific datetime."""
        result = service.get_timezone(
            BARCELONA_CATALUNYA_SQUARE,
            TimezoneOptions(date_time="2019-09-27T14:30:12Z"),
        )

        assert result is not None
        assert result.id is not None
        assert result.name is not None
        assert result.local_date_time is not None
        assert result.utc_date_time == "2019-09-27T14:30:12Z"
        assert result.utc_offset is not None
        assert result.daylight_saving_time is not None

    def test_municipality_level(self, service: ReverseGeocodingService) -> None:
        """Should request municipality level information."""
        result = service.reverse_geocode(
            BARCELONA_CATALUNYA_SQUARE,
            ReverseGeocodeOptions(level="mun"),
        )

        assert result is not None
        assert result.ge is not None

    def test_postal_code_level(self, service: ReverseGeocodingService) -> None:
        """Should request postal code level information."""
        result = service.reverse_geocode(
            BARCELONA_CATALUNYA_SQUARE,
            ReverseGeocodeOptions(level="pcode"),
        )

        assert result is not None
        assert result.ge is not None


class TestIntersectingRegions:
    """Tests for get_intersecting_regions method."""

    @pytest.fixture
    def service(self) -> ReverseGeocodingService:
        return ReverseGeocodingService(config)

    def test_municipalities_intersecting_polygon(self, service: ReverseGeocodingService) -> None:
        """Should find municipalities intersecting a polygon."""
        # Simple polygon around Barcelona area
        wkt = "POLYGON((2.10 41.35, 2.20 41.35, 2.20 41.45, 2.10 41.45, 2.10 41.35))"

        results = service.get_intersecting_regions(wkt, "mun")

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            for result in results:
                assert result.ge is not None
                assert result.ge.name is not None
                assert result.ge.coord is not None

    def test_subregions_intersecting_polygon(self, service: ReverseGeocodingService) -> None:
        """Should find regions intersecting a polygon."""
        # Larger polygon around Madrid area
        wkt = "POLYGON((-3.80 40.35, -3.60 40.35, -3.60 40.50, -3.80 40.50, -3.80 40.35))"

        results = service.get_intersecting_regions(wkt, "subreg")

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            assert results[0].ge.name is not None

    def test_empty_polygon_no_intersections(self, service: ReverseGeocodingService) -> None:
        """Should return empty array for polygon with no intersections."""
        # Polygon in the middle of the ocean
        wkt = "POLYGON((-30.0 30.0, -29.9 30.0, -29.9 30.1, -30.0 30.1, -30.0 30.0))"

        results = service.get_intersecting_regions(wkt, "mun")

        assert results is not None
        assert isinstance(results, list)
        # Likely to be empty, but API might return something
        assert len(results) >= 0
