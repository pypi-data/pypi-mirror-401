"""
Tests for the Geofencing Service.

Integration tests using real API calls (no mocks).
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.geofencing_service import GeofencingService
from cercalia.types.common import Coordinate
from cercalia.types.geofencing import GeofencePoint, GeofenceShape


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> GeofencingService:
    """Create GeofencingService instance for tests."""
    return GeofencingService(config)


# Test coordinates - Barcelona
BARCELONA_CENTER = Coordinate(lat=41.3874, lng=2.1686)  # Plaça Catalunya
SAGRADA_FAMILIA = Coordinate(lat=41.4036, lng=2.1744)
CAMP_NOU = Coordinate(lat=41.3809, lng=2.1228)
OUTSIDE_BARCELONA = Coordinate(lat=42.0, lng=3.0)  # Far from Barcelona


# Test shapes
def get_circle_zone() -> GeofenceShape:
    """Circular zone around Plaça Catalunya (500m radius)."""
    return GeofenceShape(
        id="center-zone",
        wkt=f"CIRCLE({BARCELONA_CENTER.lng} {BARCELONA_CENTER.lat}, 500)",
    )


def get_polygon_zone() -> GeofenceShape:
    """Polygon covering central Barcelona (Eixample area)."""
    return GeofenceShape(
        id="eixample-zone",
        wkt="POLYGON((2.15 41.38, 2.18 41.38, 2.18 41.41, 2.15 41.41, 2.15 41.38))",
    )


class TestCheck:
    """Tests for check() method."""

    def test_detect_points_inside_circular_zone(self, service: GeofencingService) -> None:
        """Should detect points inside a circular zone."""
        points = [
            GeofencePoint(id="inside", coord=BARCELONA_CENTER),
            GeofencePoint(id="outside", coord=OUTSIDE_BARCELONA),
        ]

        result = service.check([get_circle_zone()], points)

        assert result is not None
        assert result.total_points_checked == 2
        assert result.total_shapes_checked == 1

        # Should have a match for the circle zone with the inside point
        center_match = next((m for m in result.matches if m.shape_id == "center-zone"), None)
        if center_match:
            inside_point_ids = [p.id for p in center_match.points_inside]
            assert "inside" in inside_point_ids
            assert "outside" not in inside_point_ids

    def test_detect_points_inside_polygon_zone(self, service: GeofencingService) -> None:
        """Should detect points inside a polygon zone."""
        points = [
            GeofencePoint(id="sagrada", coord=SAGRADA_FAMILIA),
            GeofencePoint(id="campnou", coord=CAMP_NOU),
            GeofencePoint(id="outside", coord=OUTSIDE_BARCELONA),
        ]

        result = service.check([get_polygon_zone()], points)

        assert result is not None
        assert result.total_points_checked == 3

        # Sagrada Familia should be inside Eixample polygon
        eixample_match = next((m for m in result.matches if m.shape_id == "eixample-zone"), None)
        if eixample_match:
            inside_ids = [p.id for p in eixample_match.points_inside]
            assert "sagrada" in inside_ids
            assert "outside" not in inside_ids

    def test_handle_multiple_shapes_and_points(self, service: GeofencingService) -> None:
        """Should handle multiple shapes and multiple points."""
        shapes = [get_circle_zone(), get_polygon_zone()]
        points = [
            GeofencePoint(id="center", coord=BARCELONA_CENTER),
            GeofencePoint(id="sagrada", coord=SAGRADA_FAMILIA),
            GeofencePoint(id="outside", coord=OUTSIDE_BARCELONA),
        ]

        result = service.check(shapes, points)

        assert result is not None
        assert result.total_points_checked == 3
        assert result.total_shapes_checked == 2

    def test_throw_error_with_no_shapes(self, service: GeofencingService) -> None:
        """Should throw error with no shapes."""
        points = [GeofencePoint(id="test", coord=BARCELONA_CENTER)]

        with pytest.raises(ValueError, match="at least one shape"):
            service.check([], points)

    def test_throw_error_with_no_points(self, service: GeofencingService) -> None:
        """Should throw error with no points."""
        with pytest.raises(ValueError, match="at least one point"):
            service.check([get_circle_zone()], [])


class TestCheckPoint:
    """Tests for check_point() method."""

    def test_return_matching_zone_ids_for_single_point(self, service: GeofencingService) -> None:
        """Should return matching zone IDs for a single point."""
        shapes = [get_circle_zone(), get_polygon_zone()]

        matching_zones = service.check_point(shapes, BARCELONA_CENTER)

        assert isinstance(matching_zones, list)
        # Barcelona center should be in the circle zone at minimum
        assert "center-zone" in matching_zones

    def test_return_empty_list_for_point_outside_all_zones(
        self, service: GeofencingService
    ) -> None:
        """Should return empty array for point outside all zones."""
        shapes = [get_circle_zone()]

        matching_zones = service.check_point(shapes, OUTSIDE_BARCELONA)

        assert isinstance(matching_zones, list)
        assert len(matching_zones) == 0


class TestIsInsideCircle:
    """Tests for is_inside_circle() method."""

    def test_return_true_for_point_inside_circle(self, service: GeofencingService) -> None:
        """Should return true for point inside circle."""
        is_inside = service.is_inside_circle(
            center=BARCELONA_CENTER,
            radius_meters=1000,  # 1km radius
            point=Coordinate(lat=41.388, lng=2.169),  # Very close to center
        )

        assert is_inside is True

    def test_return_false_for_point_outside_circle(self, service: GeofencingService) -> None:
        """Should return false for point outside circle."""
        is_inside = service.is_inside_circle(
            center=BARCELONA_CENTER,
            radius_meters=100,  # 100m radius
            point=OUTSIDE_BARCELONA,
        )

        assert is_inside is False


class TestIsInsidePolygon:
    """Tests for is_inside_polygon() method."""

    def test_return_true_for_point_inside_polygon(self, service: GeofencingService) -> None:
        """Should return true for point inside polygon."""
        polygon_wkt = "POLYGON((2.16 41.39, 2.18 41.39, 2.18 41.41, 2.16 41.41, 2.16 41.39))"

        is_inside = service.is_inside_polygon(polygon_wkt, SAGRADA_FAMILIA)

        assert is_inside is True

    def test_return_false_for_point_outside_polygon(self, service: GeofencingService) -> None:
        """Should return false for point outside polygon."""
        polygon_wkt = "POLYGON((2.16 41.39, 2.18 41.39, 2.18 41.41, 2.16 41.41, 2.16 41.39))"

        is_inside = service.is_inside_polygon(polygon_wkt, OUTSIDE_BARCELONA)

        assert is_inside is False


class TestFilterPointsInShape:
    """Tests for filter_points_in_shape() method."""

    def test_return_only_points_inside_shape(self, service: GeofencingService) -> None:
        """Should return only points inside the shape."""
        points = [
            GeofencePoint(id="center", coord=BARCELONA_CENTER),
            GeofencePoint(id="near", coord=Coordinate(lat=41.388, lng=2.170)),
            GeofencePoint(id="far", coord=OUTSIDE_BARCELONA),
        ]

        # Large circle covering central Barcelona
        large_circle = GeofenceShape(
            id="large",
            wkt=f"CIRCLE({BARCELONA_CENTER.lng} {BARCELONA_CENTER.lat}, 2000)",
        )

        inside_points = service.filter_points_in_shape(large_circle, points)

        assert isinstance(inside_points, list)
        inside_ids = [p.id for p in inside_points]
        assert "center" in inside_ids
        assert "near" in inside_ids
        assert "far" not in inside_ids

    def test_return_empty_list_when_no_points_inside(self, service: GeofencingService) -> None:
        """Should return empty array when no points inside."""
        points = [
            GeofencePoint(id="far1", coord=OUTSIDE_BARCELONA),
            GeofencePoint(id="far2", coord=Coordinate(lat=43.0, lng=4.0)),
        ]

        inside_points = service.filter_points_in_shape(get_circle_zone(), points)

        assert inside_points == []

    def test_return_empty_list_for_empty_points_input(self, service: GeofencingService) -> None:
        """Should return empty array for empty points input."""
        inside_points = service.filter_points_in_shape(get_circle_zone(), [])

        assert inside_points == []


class TestHelperMethods:
    """Tests for helper methods."""

    def test_create_circle_creates_valid_wkt(self, service: GeofencingService) -> None:
        """create_circle() should create valid circle WKT."""
        circle = service.create_circle("test", BARCELONA_CENTER, 1000)

        assert circle.id == "test"
        assert "CIRCLE" in circle.wkt
        assert str(BARCELONA_CENTER.lng) in circle.wkt
        assert str(BARCELONA_CENTER.lat) in circle.wkt
        assert "1000" in circle.wkt

    def test_create_rectangle_creates_valid_polygon_wkt(self, service: GeofencingService) -> None:
        """create_rectangle() should create valid polygon WKT."""
        sw = Coordinate(lat=41.37, lng=2.15)
        ne = Coordinate(lat=41.40, lng=2.19)

        rect = service.create_rectangle("test-rect", sw, ne)

        assert rect.id == "test-rect"
        assert "POLYGON" in rect.wkt
        assert str(sw.lng) in rect.wkt
        assert str(sw.lat) in rect.wkt
        assert str(ne.lng) in rect.wkt
        assert str(ne.lat) in rect.wkt

    def test_create_rectangle_result_works_with_check(self, service: GeofencingService) -> None:
        """create_rectangle() result should work with check()."""
        sw = Coordinate(lat=41.37, lng=2.15)
        ne = Coordinate(lat=41.40, lng=2.19)
        rect = service.create_rectangle("delivery-zone", sw, ne)

        points = [
            GeofencePoint(id="inside", coord=BARCELONA_CENTER),
            GeofencePoint(id="outside", coord=OUTSIDE_BARCELONA),
        ]

        result = service.check([rect], points)

        assert result is not None
        assert result.total_shapes_checked == 1


class TestEdgeCases:
    """Tests for edge cases."""

    def test_handle_very_small_radius_circles(self, service: GeofencingService) -> None:
        """Should handle very small radius circles."""
        tiny_circle = service.create_circle("tiny", BARCELONA_CENTER, 10)  # 10m radius

        result = service.check(
            [tiny_circle],
            [GeofencePoint(id="exact", coord=BARCELONA_CENTER)],
        )

        assert result is not None
        # Point at exact center should be inside
        match = next((m for m in result.matches if m.shape_id == "tiny"), None)
        if match:
            assert len(match.points_inside) > 0

    def test_handle_large_radius_circles(self, service: GeofencingService) -> None:
        """Should handle large radius circles."""
        large_circle = service.create_circle("large", BARCELONA_CENTER, 50000)  # 50km radius

        points = [
            GeofencePoint(id="barcelona", coord=BARCELONA_CENTER),
            GeofencePoint(id="sagrada", coord=SAGRADA_FAMILIA),
            GeofencePoint(id="campnou", coord=CAMP_NOU),
        ]

        result = service.check([large_circle], points)

        assert result is not None
        # All Barcelona points should be inside
        match = next((m for m in result.matches if m.shape_id == "large"), None)
        if match:
            assert len(match.points_inside) == 3

    def test_handle_complex_polygon_with_many_vertices(self, service: GeofencingService) -> None:
        """Should handle complex polygon with many vertices."""
        # Star-shaped polygon
        star_polygon = GeofenceShape(
            id="star",
            wkt="POLYGON((2.16 41.39, 2.17 41.40, 2.18 41.39, 2.175 41.385, 2.18 41.38, 2.17 41.375, 2.16 41.38, 2.165 41.385, 2.16 41.39))",
        )

        result = service.check(
            [star_polygon],
            [GeofencePoint(id="center", coord=Coordinate(lat=41.385, lng=2.17))],
        )

        assert result is not None
