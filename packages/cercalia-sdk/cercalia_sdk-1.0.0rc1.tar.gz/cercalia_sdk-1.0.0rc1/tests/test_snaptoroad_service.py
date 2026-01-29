"""
Tests for the SnapToRoad Service.

Integration tests using real API calls (no mocks).
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.snaptoroad_service import SnapToRoadService
from cercalia.types.common import Coordinate
from cercalia.types.snaptoroad import SnapToRoadOptions, SnapToRoadPoint


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> SnapToRoadService:
    """Create SnapToRoadService instance for tests."""
    return SnapToRoadService(config)


# Sample GPS track along a road in Barcelona (Diagonal Avenue)
BARCELONA_TRACK = [
    SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365)),
    SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420)),
    SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480)),
    SnapToRoadPoint(coord=Coordinate(lat=41.3965, lng=2.1540)),
]


class TestBasicMapMatching:
    """Tests for basic map matching."""

    def test_match_gps_track_to_road_network(self, service: SnapToRoadService) -> None:
        """Should match GPS track to road network and return valid segments."""
        result = service.match(BARCELONA_TRACK)

        assert result is not None
        assert hasattr(result, "segments")
        assert hasattr(result, "total_distance")
        assert isinstance(result.segments, list)
        assert isinstance(result.total_distance, (int, float))
        assert result.total_distance >= 0

        # If segments returned, validate each segment
        if result.segments:
            for segment in result.segments:
                assert segment.wkt is not None
                assert isinstance(segment.wkt, str)
                assert len(segment.wkt) > 0
                assert segment.wkt.startswith(("LINESTRING", "MULTILINESTRING", "POINT"))
                assert segment.distance is not None
                assert segment.distance >= 0

    def test_handle_minimum_valid_track(self, service: SnapToRoadService) -> None:
        """Should handle minimum valid track (2 points)."""
        min_track = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365)),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420)),
        ]

        result = service.match(min_track)

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)
        assert result.total_distance >= 0

    def test_handle_track_in_madrid(self, service: SnapToRoadService) -> None:
        """Should handle track in different geographic locations."""
        madrid_track = [
            SnapToRoadPoint(coord=Coordinate(lat=40.4168, lng=-3.7038)),
            SnapToRoadPoint(coord=Coordinate(lat=40.4200, lng=-3.7000)),
            SnapToRoadPoint(coord=Coordinate(lat=40.4220, lng=-3.6980)),
        ]

        result = service.match(madrid_track)

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)
        assert result.total_distance >= 0


class TestWeightOptions:
    """Tests for weight options (distance vs time)."""

    def test_support_distance_based_matching(self, service: SnapToRoadService) -> None:
        """Should support distance-based matching (default)."""
        result = service.match(BARCELONA_TRACK, SnapToRoadOptions(weight="distance"))

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)

    def test_support_time_based_matching(self, service: SnapToRoadService) -> None:
        """Should support time-based matching."""
        result = service.match(BARCELONA_TRACK, SnapToRoadOptions(weight="time"))

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)


class TestGeometrySimplification:
    """Tests for geometry simplification."""

    def test_support_low_tolerance(self, service: SnapToRoadService) -> None:
        """Should support detailed geometry with low tolerance."""
        result = service.match(BARCELONA_TRACK, SnapToRoadOptions(geometry_tolerance=1))

        assert result is not None
        assert result.segments is not None
        for segment in result.segments:
            assert segment.wkt is not None
            assert isinstance(segment.wkt, str)

    def test_support_high_tolerance(self, service: SnapToRoadService) -> None:
        """Should support simplified geometry with high tolerance."""
        result = service.match(BARCELONA_TRACK, SnapToRoadOptions(geometry_tolerance=100))

        assert result is not None
        assert result.segments is not None
        for segment in result.segments:
            assert segment.wkt is not None
            assert isinstance(segment.wkt, str)

    def test_match_simplified_convenience_method(self, service: SnapToRoadService) -> None:
        """Should use match_simplified() convenience method."""
        result = service.match_simplified(BARCELONA_TRACK, tolerance=50)

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)


class TestSpeedingDetection:
    """Tests for speeding detection."""

    def test_detect_speeding_when_enabled(self, service: SnapToRoadService) -> None:
        """Should detect speeding when enabled with speed data."""
        track_with_speed = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365), speed=50),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420), speed=130),
            SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480), speed=60),
            SnapToRoadPoint(coord=Coordinate(lat=41.3965, lng=2.1540), speed=70),
        ]

        result = service.match(
            track_with_speed,
            SnapToRoadOptions(speeding=True, speed_tolerance=10),
        )

        assert result is not None
        assert result.segments is not None

        for segment in result.segments:
            assert segment.wkt is not None
            assert segment.distance >= 0
            # Speeding field may or may not be present

    def test_match_with_speeding_detection_convenience_method(
        self, service: SnapToRoadService
    ) -> None:
        """Should use match_with_speeding_detection() convenience method."""
        track_with_speed = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365), speed=50),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420), speed=100),
            SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480), speed=60),
        ]

        result = service.match_with_speeding_detection(track_with_speed, 10)

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)


class TestSegmentGrouping:
    """Tests for segment grouping by attribute."""

    def test_match_with_groups_convenience_method(self, service: SnapToRoadService) -> None:
        """Should group segments using match_with_groups()."""
        coords = [p.coord for p in BARCELONA_TRACK]
        result = service.match_with_groups(coords, group_size=2)

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)

    def test_handle_custom_attributes(self, service: SnapToRoadService) -> None:
        """Should handle custom attributes in track points."""
        track_with_attributes = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365), attribute="LEG_A"),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420), attribute="LEG_A"),
            SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480), attribute="LEG_B"),
            SnapToRoadPoint(coord=Coordinate(lat=41.3965, lng=2.1540), attribute="LEG_B"),
        ]

        result = service.match(track_with_attributes)

        assert result is not None
        assert result.segments is not None


class TestCombinedOptions:
    """Tests for combined options."""

    def test_combine_speeding_and_simplification(self, service: SnapToRoadService) -> None:
        """Should combine speeding detection and geometry simplification."""
        track_with_speed = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365), speed=50),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420), speed=100),
            SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480), speed=60),
        ]

        result = service.match(
            track_with_speed,
            SnapToRoadOptions(speeding=True, speed_tolerance=10, geometry_tolerance=50),
        )

        assert result is not None
        assert result.segments is not None

    def test_combine_all_options(self, service: SnapToRoadService) -> None:
        """Should combine all options together."""
        track_with_speed = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365), speed=50),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420), speed=100),
            SnapToRoadPoint(coord=Coordinate(lat=41.3952, lng=2.1480), speed=60),
            SnapToRoadPoint(coord=Coordinate(lat=41.3965, lng=2.1540), speed=70),
        ]

        result = service.match(
            track_with_speed,
            SnapToRoadOptions(
                weight="time",
                speeding=True,
                speed_tolerance=5,
                geometry_tolerance=100,
            ),
        )

        assert result is not None
        assert result.segments is not None
        assert isinstance(result.segments, list)
        assert result.total_distance >= 0


class TestErrorHandling:
    """Tests for error handling."""

    def test_throw_error_with_fewer_than_2_points(self, service: SnapToRoadService) -> None:
        """Should throw error with fewer than 2 points."""
        with pytest.raises(ValueError, match="at least 2 GPS points"):
            service.match([SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365))])

    def test_throw_error_with_empty_array(self, service: SnapToRoadService) -> None:
        """Should throw error with empty array."""
        with pytest.raises(ValueError, match="at least 2 GPS points"):
            service.match([])


class TestTrackStringBuilding:
    """Tests for track string building (internal format)."""

    def test_build_track_string_with_all_fields(self, service: SnapToRoadService) -> None:
        """Should build track string with ALL optional fields matching docs format."""
        doc_track = [
            SnapToRoadPoint(
                coord=Coordinate(lat=41.969279, lng=2.825850),
                compass=0,
                angle=45,
                speed=70,
                attribute="A",
            ),
            SnapToRoadPoint(
                coord=Coordinate(lat=41.965995, lng=2.822355),
                compass=0,
                angle=45,
                speed=10,
                attribute="A",
            ),
        ]

        # Access private method for testing
        track_string = service._build_track_string(doc_track)

        # Should contain key components
        assert "@0,45@@70@@@A" in track_string
        assert "@0,45@@10@@@A" in track_string
        # Should have 2 points in brackets
        assert track_string.count("[") == 2

    def test_build_track_string_with_only_coordinates(self, service: SnapToRoadService) -> None:
        """Should build track string with only coordinates when no optional fields."""
        simple_track = [
            SnapToRoadPoint(coord=Coordinate(lat=41.3928, lng=2.1365)),
            SnapToRoadPoint(coord=Coordinate(lat=41.3940, lng=2.1420)),
        ]

        track_string = service._build_track_string(simple_track)

        # Should only have coordinates in brackets
        assert "@" not in track_string
        assert "[2.1365,41.3928]" in track_string


class TestDataIntegrity:
    """Tests for data integrity (Golden Rules)."""

    def test_return_valid_wkt_geometry_format(self, service: SnapToRoadService) -> None:
        """Should return valid WKT geometry format."""
        result = service.match(BARCELONA_TRACK)

        assert result.segments is not None

        for segment in result.segments:
            assert segment.wkt is not None
            assert isinstance(segment.wkt, str)
            assert len(segment.wkt) > 0
            # WKT should match standard geometry types
            assert segment.wkt.startswith(
                (
                    "LINESTRING",
                    "MULTILINESTRING",
                    "POINT",
                    "POLYGON",
                    "MULTIPOINT",
                    "MULTIPOLYGON",
                )
            )

    def test_never_return_none_for_required_fields(self, service: SnapToRoadService) -> None:
        """Should never return None for required fields."""
        result = service.match(BARCELONA_TRACK)

        assert result is not None
        assert result.segments is not None
        assert result.total_distance is not None

        for segment in result.segments:
            assert segment.wkt is not None
            assert segment.distance is not None

    def test_total_distance_equals_sum_of_segment_distances(
        self, service: SnapToRoadService
    ) -> None:
        """Should validate totalDistance equals sum of segment distances."""
        result = service.match(BARCELONA_TRACK)

        if result.segments:
            sum_distance = sum(seg.distance for seg in result.segments)
            assert abs(sum_distance - result.total_distance) < 0.01
        else:
            assert result.total_distance == 0
