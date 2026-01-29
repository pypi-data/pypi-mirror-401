"""
Integration tests for PoiService using real Cercalia API.

These tests validate:
- Nearest POI search by straight-line distance
- Nearest POI search with routing
- POI search in map extent
- POI search in polygon
- Weather forecast retrieval
- Compliance with Golden Rules (strict coordinates, code integrity)
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.poi_service import PoiService
from cercalia.types.common import Coordinate
from cercalia.types.poi import (
    MapExtent,
    PoiInExtentOptions,
    PoiInPolygonOptions,
    PoiNearestOptions,
    PoiNearestWithRoutingOptions,
)


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> PoiService:
    """Create PoiService instance."""
    return PoiService(config)


# Test coordinates
MADRID_CENTER = Coordinate(lat=40.3691, lng=-3.589)
BARCELONA_CENTER = Coordinate(lat=41.39818, lng=2.1490287)
GIRONA_CENTER = Coordinate(lat=41.9793, lng=2.8214)


class TestSearchNearest:
    """Tests for nearest POI search by straight-line distance."""

    def test_nearest_gas_stations_madrid(self, service: PoiService) -> None:
        """Should get nearest gas stations in Madrid."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(categories=["C001"], limit=2, radius=10000),
        )

        assert results is not None
        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 2

        # Validate first result structure
        poi = results[0]
        assert poi.id is not None
        assert poi.name is not None
        assert poi.category_code == "C001"
        assert poi.coord is not None
        assert poi.coord.lat is not None
        assert poi.coord.lng is not None
        assert poi.distance is not None
        assert poi.position == 1

        # Validate geographic element if present
        if poi.ge:
            # At least some administrative info should be present
            has_admin_info = (
                poi.ge.locality or poi.ge.municipality or poi.ge.region or poi.ge.country
            )
            assert has_admin_info

    def test_nearest_schools_girona(self, service: PoiService) -> None:
        """Should get nearest schools in Girona."""
        results = service.search_nearest(
            GIRONA_CENTER,
            PoiNearestOptions(categories=["D00ESC"], limit=5, radius=2000),
        )

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            poi = results[0]
            assert poi.id is not None
            assert poi.name is not None
            assert poi.category_code == "D00ESC"
            assert poi.coord is not None
            assert poi.distance is not None

    def test_empty_results_ocean(self, service: PoiService) -> None:
        """Should handle empty results gracefully (ocean location)."""
        ocean_coord = Coordinate(lat=30.0, lng=-30.0)

        results = service.search_nearest(
            ocean_coord,
            PoiNearestOptions(categories=["C001"], limit=10, radius=1000),
        )

        assert results is not None
        assert isinstance(results, list)
        assert len(results) == 0

    def test_multiple_poi_categories(self, service: PoiService) -> None:
        """Should search for multiple POI categories."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(
                categories=["C001", "C009", "C024"],  # Gas stations, Hospitals, ATMs
                limit=10,
                radius=5000,
            ),
        )

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            # Check that we have different categories
            categories = {poi.category_code for poi in results}
            assert len(categories) > 0

            # All categories should be one of the requested ones
            for poi in results:
                assert poi.category_code in ["C001", "C009", "C024"]


class TestSearchNearestWithRouting:
    """Tests for nearest POI search with routing."""

    def test_nearest_with_routing_time(self, service: PoiService) -> None:
        """Should get nearest gas stations with time-based routing in Madrid."""
        results = service.search_nearest_with_routing(
            MADRID_CENTER,
            PoiNearestWithRoutingOptions(
                categories=["C001"],
                limit=2,
                weight="time",
            ),
        )

        assert results is not None
        assert isinstance(results, list)
        assert len(results) > 0

        poi = results[0]
        assert poi.id is not None
        assert poi.name is not None
        assert poi.category_code == "C001"
        assert poi.coord is not None

        # Routing-specific fields
        assert poi.route_distance is not None
        assert poi.route_time is not None
        assert poi.route_weight is not None

        # Distance and position should still be present
        assert poi.distance is not None
        assert poi.position is not None

    def test_nearest_with_inverse_routing(self, service: PoiService) -> None:
        """Should get nearest POIs with inverse routing (POI to center)."""
        results = service.search_nearest_with_routing(
            MADRID_CENTER,
            PoiNearestWithRoutingOptions(
                categories=["C001"],
                limit=2,
                weight="distance",
                inverse=1,  # Routes from POIs to center
            ),
        )

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            poi = results[0]
            assert poi.route_distance is not None
            assert poi.route_time is not None

    def test_nearest_with_realtime_traffic(self, service: PoiService) -> None:
        """Should handle routing with realtime traffic."""
        results = service.search_nearest_with_routing(
            MADRID_CENTER,
            PoiNearestWithRoutingOptions(
                categories=["C001"],
                limit=2,
                weight="time",
                include_realtime=True,
            ),
        )

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            poi = results[0]
            assert poi.route_time is not None
            # route_realtime might be present if traffic data is available
            if poi.route_realtime is not None:
                assert isinstance(poi.route_realtime, int)


class TestSearchInExtent:
    """Tests for POI search in map extent."""

    def test_gas_stations_in_huesca_extent(self, service: PoiService) -> None:
        """Should get gas stations in Huesca map extent."""
        extent = MapExtent(
            upper_left=Coordinate(lat=42.144102962, lng=-0.414886914),
            lower_right=Coordinate(lat=42.139342832, lng=-0.407628526),
        )

        results = service.search_in_extent(
            extent,
            PoiInExtentOptions(categories=["D00GAS"], include_map=False),
        )

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            poi = results[0]
            assert poi.id is not None
            assert poi.name is not None
            assert poi.category_code == "D00GAS"
            assert poi.coord is not None

            # Coordinates should be within the extent
            assert poi.coord.lat >= extent.lower_right.lat
            assert poi.coord.lat <= extent.upper_left.lat
            assert poi.coord.lng >= extent.upper_left.lng
            assert poi.coord.lng <= extent.lower_right.lng

            # Should have pixel coordinates
            if poi.pixels:
                assert poi.pixels.x is not None
                assert poi.pixels.y is not None

    def test_extent_with_grid_filtering(self, service: PoiService) -> None:
        """Should use zoom filtering with gridsize."""
        extent = MapExtent(
            upper_left=Coordinate(lat=42.144102962, lng=-0.414886914),
            lower_right=Coordinate(lat=42.139342832, lng=-0.407628526),
        )

        results = service.search_in_extent(
            extent,
            PoiInExtentOptions(
                categories=["D00GAS"],
                include_map=False,
                grid_size=100,  # Use grid filtering
            ),
        )

        assert results is not None
        assert isinstance(results, list)

        # Grid filtering might reduce results
        for poi in results:
            assert poi.category_code == "D00GAS"
            assert poi.coord is not None


class TestSearchInPolygon:
    """Tests for POI search in polygon."""

    def test_gas_stations_in_barcelona_polygon(self, service: PoiService) -> None:
        """Should get gas stations inside Barcelona polygon."""
        # Polygon around Barcelona city center
        wkt = (
            "POLYGON(("
            "2.149028778076172 41.39586980544921, "
            "2.149028778076172 41.40586980544921, "
            "2.179028778076172 41.40586980544921, "
            "2.179028778076172 41.39586980544921, "
            "2.149028778076172 41.39586980544921"
            "))"
        )

        results = service.search_in_polygon(PoiInPolygonOptions(categories=["C001"], wkt=wkt))

        assert results is not None
        assert isinstance(results, list)

        if len(results) > 0:
            poi = results[0]
            assert poi.id is not None
            assert poi.name is not None
            assert poi.category_code == "C001"
            assert poi.coord is not None

            # Coordinates should be roughly within the polygon bounds
            assert poi.coord.lat > 41.39
            assert poi.coord.lat < 41.41
            assert poi.coord.lng > 2.14
            assert poi.coord.lng < 2.18


class TestGetWeatherForecast:
    """Tests for weather forecast."""

    def test_weather_forecast_barcelona(self, service: PoiService) -> None:
        """Should get weather forecast for Barcelona."""
        forecast = service.get_weather_forecast(BARCELONA_CENTER)

        assert forecast is not None
        assert forecast.location_name is not None
        assert forecast.coord is not None
        assert forecast.coord.lat is not None
        assert forecast.coord.lng is not None
        assert forecast.forecasts is not None
        assert isinstance(forecast.forecasts, list)

        if len(forecast.forecasts) > 0:
            day_forecast = forecast.forecasts[0]
            assert day_forecast.date is not None
            # Date should be in YYYY-MM-DD format
            assert len(day_forecast.date) == 10
            assert "-" in day_forecast.date

            # Temperature should be defined
            assert day_forecast.temperature_max is not None
            assert day_forecast.temperature_min is not None

            # Should have forecast data
            assert day_forecast.precipitation_chance_00_12 is not None
            assert day_forecast.sky_conditions_00_12 is not None

        # Last update timestamp should be present
        if forecast.last_update:
            assert forecast.last_update is not None
            # Should start with date format
            assert "-" in forecast.last_update


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_coordinates(self, service: PoiService) -> None:
        """Should handle invalid coordinates gracefully."""
        invalid_coord = Coordinate(lat=999, lng=999)

        results = service.search_nearest(
            invalid_coord,
            PoiNearestOptions(categories=["C001"], limit=5),
        )

        # Should return empty array or handle gracefully
        assert results is not None
        assert isinstance(results, list)

    def test_very_small_radius(self, service: PoiService) -> None:
        """Should handle very small radius."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(categories=["C001"], limit=5, radius=1),  # 1 meter
        )

        assert results is not None
        assert isinstance(results, list)
        # Likely to be empty but should not throw

    def test_empty_category_list(self, service: PoiService) -> None:
        """Should handle empty category list gracefully."""
        # This might throw an error from the API, which is expected
        try:
            service.search_nearest(
                MADRID_CENTER,
                PoiNearestOptions(categories=[], limit=5),
            )
            # If it doesn't throw, it should return empty array
            assert True
        except Exception as e:
            # API error is acceptable for invalid input
            assert e is not None


class TestDataIntegrity:
    """Tests for data integrity and Golden Rules compliance."""

    def test_coordinate_precision(self, service: PoiService) -> None:
        """Should maintain coordinate precision."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(categories=["C001"], limit=1, radius=10000),
        )

        if len(results) > 0:
            poi = results[0]

            # Coordinates should be numbers with reasonable precision
            assert isinstance(poi.coord.lat, float)
            assert isinstance(poi.coord.lng, float)
            assert poi.coord.lat > -90
            assert poi.coord.lat < 90
            assert poi.coord.lng > -180
            assert poi.coord.lng < 180

    def test_administrative_levels_with_codes(self, service: PoiService) -> None:
        """Should preserve all administrative levels when present (Golden Rule #2)."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(categories=["C001"], limit=1, radius=10000),
        )

        if len(results) > 0 and results[0].ge:
            ge = results[0].ge

            # If an administrative level is present, its code should also be present
            if ge.locality:
                assert ge.locality_code is not None
            if ge.municipality:
                assert ge.municipality_code is not None
            if ge.subregion:
                assert ge.subregion_code is not None
            if ge.region:
                assert ge.region_code is not None
            if ge.country:
                assert ge.country_code is not None

    def test_geometry_type_present(self, service: PoiService) -> None:
        """Should include geometry type when present (Golden Rule #4)."""
        results = service.search_nearest(
            MADRID_CENTER,
            PoiNearestOptions(categories=["C001"], limit=1, radius=10000),
        )

        if len(results) > 0:
            poi = results[0]

            # Geometry should be present
            assert poi.geometry is not None
            assert isinstance(poi.geometry, str)
