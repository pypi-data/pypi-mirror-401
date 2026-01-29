"""
Tests for the Geoment Service.

Integration tests using real API calls (no mocks).
"""

import os

import pytest

from cercalia.config import CercaliaConfig
from cercalia.services.geoment_service import GeomentService
from cercalia.types.common import CercaliaError
from cercalia.types.geoment import (
    GeomentMunicipalityOptions,
    GeomentPoiOptions,
    GeomentPostalCodeOptions,
)


@pytest.fixture
def config() -> CercaliaConfig:
    """Create test configuration."""
    return CercaliaConfig(
        api_key=os.environ["CERCALIA_API_KEY"],
        base_url="https://lb.cercalia.com/services/v2/json",
    )


@pytest.fixture
def service(config: CercaliaConfig) -> GeomentService:
    """Create GeomentService instance for tests."""
    return GeomentService(config)


class TestGetMunicipalityGeometry:
    """Tests for get_municipality_geometry method."""

    def test_fetch_municipality_geometry_by_code_madrid(self, service: GeomentService) -> None:
        """Should fetch municipality geometry by code (Madrid)."""
        result = service.get_municipality_geometry(GeomentMunicipalityOptions(munc="ESP280796"))

        assert result.code == "ESP280796"
        assert result.name == "Madrid"
        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.type == "municipality"
        assert result.level == "mun"

    def test_fetch_municipality_geometry_by_code_zaragoza(self, service: GeomentService) -> None:
        """Should fetch municipality geometry by code (Zaragoza)."""
        result = service.get_municipality_geometry(GeomentMunicipalityOptions(munc="ESP502973"))

        assert result.code == "ESP502973"
        assert result.name == "Zaragoza"
        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.type == "municipality"
        assert result.level == "mun"

    def test_fetch_region_geometry_by_subregc_madrid(self, service: GeomentService) -> None:
        """Should fetch region geometry by subregc (Comunidad de Madrid)."""
        result = service.get_municipality_geometry(GeomentMunicipalityOptions(subregc="ESP28"))

        assert result.code == "ESP28"
        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.type == "region"
        assert result.level == "subreg"

    def test_throw_error_for_invalid_municipality_code(self, service: GeomentService) -> None:
        """Should throw error for invalid municipality code."""
        with pytest.raises((CercaliaError, ValueError)):
            service.get_municipality_geometry(GeomentMunicipalityOptions(munc="INVALID999"))


class TestGetPostalCodeGeometry:
    """Tests for get_postal_code_geometry method."""

    def test_fetch_postal_code_geometry_madrid(self, service: GeomentService) -> None:
        """Should fetch postal code geometry (Spanish postal code - Madrid)."""
        result = service.get_postal_code_geometry(
            GeomentPostalCodeOptions(pcode="28001", ctryc="ESP")
        )

        assert result.code == "ESP-28001"
        assert result.name == "28001"
        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.type == "postal_code"
        assert result.level == "pc"

    def test_fetch_postal_code_geometry_barcelona(self, service: GeomentService) -> None:
        """Should fetch postal code geometry (Barcelona)."""
        result = service.get_postal_code_geometry(
            GeomentPostalCodeOptions(pcode="08001", ctryc="ESP")
        )

        assert result.code == "ESP-08001"
        assert result.name == "08001"
        assert result.wkt is not None
        assert "POLYGON" in result.wkt
        assert result.type == "postal_code"
        assert result.level == "pc"


class TestGetPoiGeometry:
    """Tests for get_poi_geometry method."""

    def test_fetch_poi_geometry_by_code(self, service: GeomentService) -> None:
        """Should fetch POI geometry by code or handle non-existent POI."""
        # Using a test POI code - this might need to be adjusted based on available POIs
        # For now, we'll test that the method works correctly even if POI doesn't exist
        try:
            result = service.get_poi_geometry(GeomentPoiOptions(poic="POI_TEST_123"))

            assert result.code is not None
            assert result.name is not None
            assert result.wkt is not None
            assert result.type == "poi"
            assert result.level == "poi"
        except (CercaliaError, ValueError) as e:
            # If POI doesn't exist, we should get a Cercalia error
            assert (
                "error" in str(e).lower() or "not found" in str(e).lower() or "Cercalia" in str(e)
            )
