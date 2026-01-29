"""Tests for Geocoding Service."""

import os
import re

import pytest

from cercalia.services.geocoding_service import GeocodingService
from cercalia.types.common import CercaliaConfig
from cercalia.types.geocoding import GeocodingOptions


class TestGeocodingServiceIntegration:
    """Integration tests for GeocodingService using real API."""

    @pytest.fixture
    def config(self) -> CercaliaConfig:
        """Cercalia configuration for tests."""
        return CercaliaConfig(
            api_key=os.environ["CERCALIA_API_KEY"],
            base_url="https://lb.cercalia.com/services/v2/json",
        )

    @pytest.fixture
    def service(self, config: CercaliaConfig) -> GeocodingService:
        """Geocoding service instance."""
        return GeocodingService(config)

    def test_geocode_real_address_provenca_barcelona(self, service: GeocodingService) -> None:
        """Should geocode a real address (Provença 589, Barcelona)."""
        results = service.geocode(
            GeocodingOptions(street="provença 589", locality="barcelona", country_code="ESP")
        )

        assert len(results) > 0
        best_match = results[0]

        # We expect Barcelona, but let's be more flexible with exact names
        assert best_match.municipality is not None
        assert re.search(r"Barcelona", best_match.municipality, re.IGNORECASE)
        assert best_match.locality is not None
        assert re.search(r"Barcelona", best_match.locality, re.IGNORECASE)
        assert best_match.locality_code is not None
        assert best_match.municipality_code is not None
        assert best_match.country_code == "ESP"
        assert best_match.label is not None
        assert best_match.coord.lat == pytest.approx(41.41, abs=0.1)
        assert best_match.coord.lng == pytest.approx(2.18, abs=0.1)

    def test_handle_city_only_search(self, service: GeocodingService) -> None:
        """Should handle city only search."""
        results = service.geocode(GeocodingOptions(locality="Girona", country_code="ESP"))

        assert len(results) > 0
        best_match = results[0]
        assert best_match.municipality is not None
        assert re.search(r"Girona", best_match.municipality, re.IGNORECASE)
        assert best_match.level is not None

    def test_handle_postal_code_search(self, service: GeocodingService) -> None:
        """Should handle postal code search."""
        results = service.geocode(GeocodingOptions(postal_code="08025", country_code="ESP"))

        assert len(results) > 0
        assert results[0].postal_code == "08025"

    def test_handle_search_by_locality(self, service: GeocodingService) -> None:
        """Should handle search by locality."""
        results = service.geocode(GeocodingOptions(locality="Madrid"))

        assert len(results) > 0
        # The API returns multiple Madrids, but the one in Comunidad de Madrid should be present
        madrid_city = next(
            (
                r
                for r in results
                if r.region and re.search(r"Comunidad de Madrid", r.region, re.IGNORECASE)
            ),
            None,
        )
        assert madrid_city is not None
        assert madrid_city.municipality is not None
        assert re.search(r"Madrid", madrid_city.municipality, re.IGNORECASE)

    def test_geocode_road_milestone_m45_km12(self, service: GeocodingService) -> None:
        """Should geocode a road milestone (M-45 KM 12)."""
        results = service.geocode_road("M-45", 12, GeocodingOptions(country_code="ESP"))

        assert len(results) > 0
        best_match = results[0]

        assert best_match.type == "milestone"
        assert best_match.subregion_code is not None
        assert best_match.region_code is not None
        assert best_match.level is not None
        assert re.match(r"pk|rd", best_match.level)  # Cercalia can return pk or rd for milestones
        # Coordinates for M-45 KM 12 from documentation are around 40.33, -3.66
        assert best_match.coord.lat == pytest.approx(40.33, abs=0.1)
        assert best_match.coord.lng == pytest.approx(-3.66, abs=0.1)

    def test_return_empty_list_for_nonexistent_address(self, service: GeocodingService) -> None:
        """Should return empty list for non-existent address."""
        results = service.geocode(
            GeocodingOptions(locality="ESTOESUNADIRECCIONINEXISTENTE 123456789")
        )
        assert results == []

    def test_handle_multiple_candidates_for_ambiguous_address(
        self, service: GeocodingService
    ) -> None:
        """Should handle multiple candidates for ambiguous address."""
        # Using ctn with a city name that has multiple matches
        results = service.geocode(GeocodingOptions(locality="Madrid", country_code="ESP"))

        assert len(results) > 0
        # Should return at least the main Madrid
        madrid_city = next(
            (
                r
                for r in results
                if r.region and re.search(r"Comunidad de Madrid", r.region, re.IGNORECASE)
            ),
            None,
        )
        assert madrid_city is not None

    def test_geocode_with_region_and_subregion(self, service: GeocodingService) -> None:
        """Should geocode with region and subregion (Sabadell, Cataluña, Barcelona)."""
        results = service.geocode(
            GeocodingOptions(
                locality="Sabadell",
                region="Cataluña",
                subregion="Barcelona",
                country_code="ESP",
            )
        )

        assert len(results) > 0
        best_match = results[0]
        assert best_match.municipality == "Sabadell"
        # The API might return "Catalunya" or "Cataluña"
        assert best_match.region is not None
        assert re.match(r"Catalu[ñn]ya", best_match.region)


class TestDocumentationExamples:
    """Tests based on documentation examples."""

    @pytest.fixture
    def config(self) -> CercaliaConfig:
        """Cercalia configuration for tests."""
        return CercaliaConfig(
            api_key=os.environ["CERCALIA_API_KEY"],
            base_url="https://lb.cercalia.com/services/v2/json",
        )

    @pytest.fixture
    def service(self, config: CercaliaConfig) -> GeocodingService:
        """Geocoding service instance."""
        return GeocodingService(config)

    def test_geocode_diagonal_22_barcelona(self, service: GeocodingService) -> None:
        """Should geocode diagonal 22, barcelona (structured search example)."""
        results = service.geocode(
            GeocodingOptions(street="diagonal 22", locality="barcelona", country_code="esp")
        )

        assert len(results) > 0
        best_match = results[0]
        assert best_match.name is not None
        assert re.search(r"Diagonal", best_match.name, re.IGNORECASE)
        assert best_match.locality == "Barcelona"

    def test_geocode_road_milestone_m45_km12_doc_example(self, service: GeocodingService) -> None:
        """Should geocode road milestone M-45 KM 12 (road milestone example)."""
        results = service.geocode_road(
            "M-45", 12, GeocodingOptions(subregion="Madrid", country_code="ESP")
        )

        assert len(results) > 0
        best_match = results[0]
        assert best_match.type == "milestone"
        assert best_match.name is not None
        assert re.search(r"M-45", best_match.name)
        assert best_match.coord.lat == pytest.approx(40.33, abs=0.1)
        assert best_match.coord.lng == pytest.approx(-3.66, abs=0.1)

    def test_geocode_a231_km13_ambiguous_road(self, service: GeocodingService) -> None:
        """Should geocode A-231 KM 13 (ambiguous road example)."""
        results = service.geocode_road("A-231", 13, GeocodingOptions(country_code="ESP"))

        assert len(results) > 1
        # Example shows 2 candidates: La Fresneda and Villanueva de las Manzanas
        fresneda = next((r for r in results if r.municipality == "La Fresneda"), None)
        villanueva = next(
            (r for r in results if r.municipality == "Villanueva de las Manzanas"), None
        )

        assert fresneda is not None
        assert villanueva is not None

    def test_get_cities_by_postal_code_40160(self, service: GeocodingService) -> None:
        """Should get cities by postal code 40160 (Torrecaballeros example)."""
        cities = service.geocode_cities_by_postal_code("40160", "ESP")

        assert len(cities) > 0
        # According to documentation, should return Torrecaballeros and Cabanillas del Monte
        torrecaballeros = next((c for c in cities if c.name == "Torrecaballeros"), None)
        cabanillas = next((c for c in cities if c.name == "Cabanillas del Monte"), None)

        assert torrecaballeros is not None
        assert torrecaballeros.municipality_code is not None
        assert torrecaballeros.subregion == "Segovia"
        assert torrecaballeros.subregion_code is not None
        assert torrecaballeros.region == "Castilla y León"
        assert torrecaballeros.region_code is not None
        assert torrecaballeros.country_code == "ESP"

        assert cabanillas is not None
