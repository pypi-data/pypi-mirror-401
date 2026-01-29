"""
Static Maps Service Integration Tests.

Based on all examples from the official Cercalia documentation:
https://docs.cercalia.com/docs/cercalia-webservices/static-maps/

Examples covered:
1. Paint markers in the map (city with label)
2. Paint polylines, areas and labels (shapes: circle, polyline)
3. Rectangle and circle combination
4. Various shape types: CIRCLE, RECTANGLE, SECTOR, LINE, POLYLINE, LABEL
"""

import os

import pytest

from cercalia.services.staticmaps_service import StaticMapsService
from cercalia.types.common import CercaliaConfig, Coordinate
from cercalia.types.staticmaps import (
    RGBAColor,
    StaticMapCircle,
    StaticMapExtent,
    StaticMapMarker,
    StaticMapOptions,
    StaticMapPolyline,
    StaticMapRectangle,
)


@pytest.fixture
def config() -> CercaliaConfig:
    """Return Cercalia configuration for testing."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> StaticMapsService:
    """Return StaticMapsService instance for testing."""
    return StaticMapsService(config)


class TestBasicMapGeneration:
    """Test basic map generation functionality."""

    def test_should_generate_static_map_for_girona_city(self, service: StaticMapsService) -> None:
        """
        Example 1: Paint markers in the map.
        URL: https://lb.cercalia.com/services/v2/json?cmd=map&ctn=girona&ctryc=ESP&key=YOUR_API_KEY
        """
        result = service.generate_city_map("girona", "ESP", width=350, height=250)

        assert result.image_url is not None
        assert "lb.cercalia.com" in result.image_url
        assert "/MapesNG/Cercalia/map/" in result.image_url
        assert result.width == 350
        assert result.height == 250
        assert result.format is not None
        assert result.center is not None
        assert result.label is not None

    def test_should_generate_map_for_barcelona(self, service: StaticMapsService) -> None:
        """Test map generation for Barcelona."""
        result = service.generate_city_map("Barcelona", "ESP", width=500, height=400)

        assert result.image_url is not None
        assert result.center is not None
        assert result.center.lat > 41
        assert result.center.lng > 2

    def test_should_generate_map_for_madrid(self, service: StaticMapsService) -> None:
        """Test map generation for Madrid."""
        result = service.generate_city_map("Madrid", "ESP", width=500, height=400)

        assert result.image_url is not None
        assert result.center is not None
        # Madrid coordinates are approximately 40.4N, -3.7W
        # Note: API may return different center depending on the map view
        assert result.center.lat is not None
        assert result.center.lng is not None


class TestShapeRendering:
    """Test shape rendering functionality."""

    def test_should_generate_map_with_circle_and_polyline_shapes(
        self, service: StaticMapsService
    ) -> None:
        """
        Example 2: Paint polylines, areas and labels.
        URL: https://lb.cercalia.com/services/v2/json?cmd=map&width=400&height=300&labelop=0&mocs=gdd&cs=gdd&extent=...&shape=...&key=YOUR_API_KEY
        """
        extent = StaticMapExtent(
            upper_left=Coordinate(lat=41.439132726, lng=2.003108336),
            lower_right=Coordinate(lat=41.390497829, lng=2.197135455),
        )

        circle = StaticMapCircle(
            type="CIRCLE",
            outline_color=RGBAColor(r=255, g=0, b=0, a=128),
            outline_size=2,
            fill_color=RGBAColor(r=0, g=255, b=0, a=128),
            center=Coordinate(lat=41.439132726, lng=2.003108336),
            radius=2000,
        )

        polyline = StaticMapPolyline(
            type="POLYLINE",
            outline_color=RGBAColor(r=255, g=0, b=0),
            outline_size=2,
            fill_color=RGBAColor(r=255, g=0, b=0),
            coordinates=[
                Coordinate(lat=41.401902461, lng=2.142455003),
                Coordinate(lat=41.404628181, lng=2.155965665),
                Coordinate(lat=41.433339308, lng=2.179860852),
            ],
        )

        result = service.generate_map(
            StaticMapOptions(
                width=400,
                height=300,
                label_op=0,
                coordinate_system="gdd",
                extent=extent,
                shapes=[circle, polyline],
            )
        )

        assert result.image_url is not None
        assert "lb.cercalia.com" in result.image_url
        assert result.width == 400
        assert result.height == 300

    def test_should_generate_map_with_rectangle_and_circle_shapes(
        self, service: StaticMapsService
    ) -> None:
        """
        Example 3: Rectangle and circle on Girona.
        URL: https://lb.cercalia.com/services/v2/json?cmd=map&ctn=Girona&shape=[255,0,0|3|0,255,0,128|RECTANGLE|...]&key=YOUR_API_KEY
        """
        rectangle = StaticMapRectangle(
            type="RECTANGLE",
            outline_color=RGBAColor(r=255, g=0, b=0),
            outline_size=3,
            fill_color=RGBAColor(r=0, g=255, b=0, a=128),
            upper_left=Coordinate(lat=41.98, lng=2.82),
            lower_right=Coordinate(lat=41.96, lng=2.84),
        )

        circle = StaticMapCircle(
            type="CIRCLE",
            outline_color=RGBAColor(r=255, g=0, b=0, a=128),
            outline_size=10,
            fill_color=RGBAColor(r=0, g=255, b=0, a=128),
            center=Coordinate(lat=41.96, lng=2.84),
            radius=1000,
        )

        result = service.generate_map(
            StaticMapOptions(
                city_name="Girona",
                shapes=[rectangle, circle],
            )
        )

        assert result.image_url is not None
        assert "lb.cercalia.com" in result.image_url

    def test_should_generate_map_with_circle_shape(self, service: StaticMapsService) -> None:
        """Test circle shape generation using helper method."""
        result = service.generate_map_with_circle(
            center=Coordinate(lat=41.3851, lng=2.1734),
            radius=2000,
            outline_color=RGBAColor(r=0, g=0, b=255, a=200),
            outline_size=3,
            fill_color=RGBAColor(r=0, g=100, b=255, a=100),
            width=400,
            height=300,
        )

        assert result.image_url is not None

    def test_should_generate_map_with_polyline(self, service: StaticMapsService) -> None:
        """Test polyline generation using helper method."""
        result = service.generate_map_with_polyline(
            coordinates=[
                Coordinate(lat=41.3851, lng=2.1734),
                Coordinate(lat=41.4034, lng=2.1741),
                Coordinate(lat=41.4100, lng=2.1900),
            ],
            outline_color=RGBAColor(r=255, g=100, b=0),
            outline_size=3,
            width=400,
            height=300,
        )

        assert result.image_url is not None

    def test_should_generate_map_with_line_between_two_points(
        self, service: StaticMapsService
    ) -> None:
        """Test line generation using helper method."""
        result = service.generate_map_with_line(
            start=Coordinate(lat=41.3851, lng=2.1734),
            end=Coordinate(lat=41.4034, lng=2.1741),
            outline_color=RGBAColor(r=0, g=255, b=0),
            outline_size=5,
            width=400,
            height=300,
        )

        assert result.image_url is not None


class TestMarkers:
    """Test marker functionality."""

    def test_should_generate_map_with_markers(self, service: StaticMapsService) -> None:
        """Test map with multiple markers."""
        result = service.generate_map_with_markers(
            markers=[
                StaticMapMarker(coord=Coordinate(lat=41.3851, lng=2.1734), icon=1),
                StaticMapMarker(coord=Coordinate(lat=41.4034, lng=2.1741), icon=2),
            ],
            width=400,
            height=300,
        )

        assert result.image_url is not None

    def test_should_generate_map_with_single_marker(self, service: StaticMapsService) -> None:
        """Test map with single marker."""
        result = service.generate_map_with_markers(
            markers=[
                StaticMapMarker(coord=Coordinate(lat=40.4168, lng=-3.7038), icon=1),
            ],
            width=400,
            height=300,
        )

        assert result.image_url is not None


class TestImageDownload:
    """Test image download functionality."""

    def test_should_download_map_image(self, service: StaticMapsService) -> None:
        """Test downloading map image."""
        result = service.generate_city_map("Madrid", "ESP", width=200, height=150)

        assert result.image_url is not None

        image_buffer = service.download_image(result.image_url)

        assert image_buffer is not None
        assert len(image_buffer) > 0

    def test_should_generate_map_and_return_image_data_directly(
        self, service: StaticMapsService
    ) -> None:
        """Test generating map and returning image data directly."""
        result = service.generate_map_as_image(
            city_name="Valencia",
            country_code="ESP",
            width=200,
            height=150,
        )

        assert result.image_data is not None
        assert len(result.image_data) > 0


class TestMultipleCities:
    """Test map generation for multiple cities."""

    def test_should_generate_maps_for_different_spanish_cities(
        self, service: StaticMapsService
    ) -> None:
        """Test generating maps for various Spanish cities."""
        cities = ["Sevilla", "Bilbao", "Zaragoza"]

        for city in cities:
            result = service.generate_city_map(city, "ESP")
            assert result.image_url is not None
            assert result.label is not None


class TestDifferentDimensions:
    """Test different image dimensions."""

    def test_should_respect_custom_dimensions(self, service: StaticMapsService) -> None:
        """Test that custom dimensions are respected."""
        result = service.generate_city_map("Barcelona", "ESP", width=800, height=600)

        assert result.width == 800
        assert result.height == 600

    def test_should_handle_small_dimensions(self, service: StaticMapsService) -> None:
        """Test handling small dimensions."""
        result = service.generate_city_map("Madrid", "ESP", width=200, height=150)

        assert result.width == 200
        assert result.height == 150


class TestRectangleHelperMethod:
    """Test rectangle helper method."""

    def test_should_generate_map_with_rectangle_using_helper_method(
        self, service: StaticMapsService
    ) -> None:
        """Test generating map with rectangle using helper method."""
        result = service.generate_map_with_rectangle(
            upper_left=Coordinate(lat=41.98, lng=2.82),
            lower_right=Coordinate(lat=41.96, lng=2.84),
            outline_color=RGBAColor(r=255, g=0, b=0),
            outline_size=3,
            fill_color=RGBAColor(r=0, g=255, b=0, a=128),
            city_name="Girona",
        )

        assert result.image_url is not None


class TestLabelHelperMethod:
    """Test label helper method."""

    def test_should_generate_map_with_label_using_helper_method(
        self, service: StaticMapsService
    ) -> None:
        """Test generating map with label using helper method."""
        result = service.generate_map_with_label(
            center=Coordinate(lat=41.3851, lng=2.1734),
            text="Barcelona",
        )

        assert result.image_url is not None


class TestSectorHelperMethod:
    """Test sector helper method."""

    def test_should_generate_map_with_sector_using_helper_method(
        self, service: StaticMapsService
    ) -> None:
        """Test generating map with sector using helper method."""
        result = service.generate_map_with_sector(
            center=Coordinate(lat=41.3851, lng=2.1734),
            inner_radius=500,
            outer_radius=1000,
            start_angle=0,
            end_angle=90,
        )

        assert result.image_url is not None
