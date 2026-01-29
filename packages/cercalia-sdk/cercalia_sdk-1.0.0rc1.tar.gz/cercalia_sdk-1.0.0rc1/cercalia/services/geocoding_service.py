"""
Geocoding service for Cercalia SDK.

Provides address geocoding, road milestone geocoding, and postal code lookup.
"""

import re
from typing import Any, Optional

from ..config import CercaliaConfig
from ..types.api_response import get_cercalia_attr, get_cercalia_value
from ..types.common import CercaliaError, Coordinate
from ..types.geocoding import (
    GeocodingCandidate,
    GeocodingCandidateType,
    GeocodingOptions,
    PostalCodeCity,
)
from ..utils.logger import logger
from .cercalia_client import CercaliaClient


class GeocodingService(CercaliaClient):
    """
    Geocoding service for converting addresses to coordinates.

    Provides methods for:
    - Address geocoding (structured and unstructured)
    - Road milestone geocoding (PK)
    - Postal code to cities lookup

    Example:
        >>> service = GeocodingService(config)
        >>> results = service.geocode(GeocodingOptions(
        ...     street="Provença 589",
        ...     locality="Barcelona",
        ...     country_code="ESP"
        ... ))
        >>> print(results[0].coord)
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the geocoding service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def geocode(self, options: GeocodingOptions) -> list[GeocodingCandidate]:
        """
        Geocode an address using Cercalia API.

        Supports both structured search (individual fields like street, locality)
        and unstructured search (free-form query).

        Args:
            options: Geocoding options with address information

        Returns:
            List of geocoding candidates matching the query

        Example:
            >>> results = service.geocode(GeocodingOptions(
            ...     street="Gran Vía 1",
            ...     locality="Madrid",
            ...     country_code="ESP"
            ... ))
        """
        params: dict[str, str] = {
            "cmd": "cand",
            "detcand": "1",
            "priorityfilter": "1",
            "mode": "0",  # mode 0 for structured search
            "cleanadr": "1",
            "ctryc": (options.country_code or "ESP").upper(),
        }

        if options.locality:
            params["ctn"] = options.locality

        if options.municipality:
            params["munn"] = options.municipality

        if options.street:
            params["adr"] = options.street

        if options.postal_code:
            params["pcode"] = options.postal_code

        if options.region:
            params["regn"] = options.region

        if options.subregion:
            params["subregn"] = options.subregion

        if options.country:
            params["ctryn"] = options.country

        if options.limit:
            params["num"] = str(options.limit)

        if options.full_search:
            params["fullsearch"] = "3"

        try:
            response = self._request(params, "Cercalia Geocoding")

            candidates_obj = response.get("candidates", {})
            candidates = candidates_obj.get("candidate", [])

            # Ensure array
            if not isinstance(candidates, list):
                candidates = [candidates] if candidates else []

            # Filter valid candidates
            valid_candidates = []
            for cand in candidates:
                ge = cand.get("ge")
                if not ge or not ge.get("coord"):
                    continue

                type_val = get_cercalia_attr(ge, "type")
                id_val = get_cercalia_attr(ge, "id")
                name_val = get_cercalia_value(ge.get("name"))

                # Filter out country-level results when searching for specific addresses
                is_country = (
                    type_val in ("ctry", "country")
                    or (id_val and len(id_val) == 3)
                    or (name_val and name_val.lower() in ("españa", "spain"))
                )

                if is_country and (options.locality or options.street or options.postal_code):
                    # Allow if locality matches or is very short (like country code)
                    if options.locality and name_val:
                        if (
                            options.locality.lower() == name_val.lower()
                            or len(options.locality) <= 3
                        ):
                            valid_candidates.append(cand)
                    continue

                valid_candidates.append(cand)

            return [self._map_candidate(cand) for cand in valid_candidates]

        except CercaliaError as e:
            # Handle "No candidates found" gracefully
            if e.code == "30006":
                return []
            logger.error(f"[Cercalia Geocoding] Error: {e}")
            raise

    def geocode_road(
        self,
        road_name: str,
        km: float,
        options: Optional[GeocodingOptions] = None,
    ) -> list[GeocodingCandidate]:
        """
        Geocode a road milestone (PK).

        Args:
            road_name: Road identifier (e.g., "M-45", "A-231")
            km: Kilometer marker
            options: Additional geocoding options

        Returns:
            List of geocoding candidates for the milestone

        Example:
            >>> results = service.geocode_road("M-45", 12, GeocodingOptions(country_code="ESP"))
            >>> print(results[0].coord)
        """
        options = options or GeocodingOptions()

        params: dict[str, str] = {
            "cmd": "cand",
            "detcand": "1",
            "rdn": road_name,
            "km": str(km),
            "ctryc": (options.country_code or "ESP").upper(),
        }

        if options.subregion:
            params["subregn"] = options.subregion
        if options.municipality:
            params["munn"] = options.municipality
        if options.postal_code:
            params["pcode"] = options.postal_code

        try:
            response = self._request(params, "GeocodingRoad")

            candidates = response.get("candidates", {}).get("candidate", [])
            if not isinstance(candidates, list):
                candidates = [candidates] if candidates else []

            results = []
            for cand in candidates:
                ge = cand.get("ge")
                if not ge or not ge.get("coord"):
                    continue

                type_val = get_cercalia_attr(ge, "type")
                desc = get_cercalia_attr(cand, "desc")
                coord = ge["coord"]

                results.append(
                    GeocodingCandidate(
                        id=get_cercalia_attr(ge, "id") or road_name,
                        name=get_cercalia_value(ge.get("name")) or f"{road_name} KM {km}",
                        label=desc,
                        locality=get_cercalia_value(ge.get("city")),
                        locality_code=get_cercalia_attr(ge.get("city"), "id"),
                        house_number=get_cercalia_value(ge.get("housenumber")),
                        municipality=get_cercalia_value(ge.get("municipality")),
                        municipality_code=get_cercalia_attr(ge.get("municipality"), "id"),
                        district=get_cercalia_value(ge.get("district")),
                        district_code=get_cercalia_attr(ge.get("district"), "id"),
                        subregion=get_cercalia_value(ge.get("subregion")),
                        subregion_code=get_cercalia_attr(ge.get("subregion"), "id"),
                        region=get_cercalia_value(ge.get("region")),
                        region_code=get_cercalia_attr(ge.get("region"), "id"),
                        country=get_cercalia_value(ge.get("country")),
                        country_code=get_cercalia_attr(ge.get("country"), "id"),
                        postal_code=(
                            get_cercalia_attr(ge.get("postalcode"), "id")
                            or get_cercalia_value(ge.get("postalcode"))
                        ),
                        coord=Coordinate(
                            lat=float(get_cercalia_attr(coord, "y")),  # type: ignore[arg-type]
                            lng=float(get_cercalia_attr(coord, "x")),  # type: ignore[arg-type]
                        ),
                        type="milestone",
                        level=type_val,  # type: ignore[arg-type]
                    )
                )

            return results

        except Exception as e:
            logger.error(f"[GeocodingRoad] Error: {e}")
            raise

    def geocode_cities_by_postal_code(
        self,
        postal_code: str,
        country_code: str = "ESP",
    ) -> list[PostalCodeCity]:
        """
        Get list of cities related to a postal code.

        Args:
            postal_code: Postal code to search
            country_code: Country code (default: "ESP")

        Returns:
            List of cities associated with the postal code

        Example:
            >>> cities = service.geocode_cities_by_postal_code("40160", "ESP")
            >>> for city in cities:
            ...     print(city.name, city.municipality)
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "rqge": "ctpcode",
            "ctryc": country_code.upper(),
            "pcode": postal_code,
        }

        try:
            response = self._request(params, "GeocodeCitiesByPostalCode")

            ge_list = response.get("proximity", {}).get("gelist", {}).get("ge", [])
            if not isinstance(ge_list, list):
                ge_list = [ge_list] if ge_list else []

            cities = []
            for ge in ge_list:
                if not ge or not ge.get("coord"):
                    continue

                coord = ge["coord"]
                cities.append(
                    PostalCodeCity(
                        id=get_cercalia_attr(ge, "id") or "unknown",
                        name=get_cercalia_attr(ge, "name") or "Unknown",
                        municipality=get_cercalia_value(ge.get("municipality")),
                        municipality_code=get_cercalia_attr(ge.get("municipality"), "id"),
                        subregion=get_cercalia_value(ge.get("subregion")),
                        subregion_code=get_cercalia_attr(ge.get("subregion"), "id"),
                        region=get_cercalia_value(ge.get("region")),
                        region_code=get_cercalia_attr(ge.get("region"), "id"),
                        country=get_cercalia_value(ge.get("country")),
                        country_code=get_cercalia_attr(ge.get("country"), "id"),
                        coord=Coordinate(
                            lat=float(get_cercalia_attr(coord, "y")),  # type: ignore[arg-type]
                            lng=float(get_cercalia_attr(coord, "x")),  # type: ignore[arg-type]
                        ),
                    )
                )

            return cities

        except Exception as e:
            logger.error(f"[GeocodeCitiesByPostalCode] Error: {e}")
            raise

    def _map_candidate(self, cand: dict[str, Any]) -> GeocodingCandidate:
        """Map raw API candidate to GeocodingCandidate model."""
        ge = cand["ge"]
        type_val = get_cercalia_attr(ge, "type")
        id_val = get_cercalia_attr(ge, "id")
        coord = ge["coord"]

        # Extract postal code from various sources
        pc = get_cercalia_value(ge.get("postalcode"))
        if not pc and ge.get("postalcode"):
            pc = get_cercalia_attr(ge.get("postalcode"), "id")

        desc = get_cercalia_attr(cand, "desc")
        if not pc and desc and re.match(r"^\d{5}$", desc):
            pc = desc

        return GeocodingCandidate(
            id=id_val or get_cercalia_attr(ge.get("country"), "id") or "unknown",
            name=(
                get_cercalia_value(ge.get("name"))
                or get_cercalia_attr(cand, "name")
                or desc
                or "Unknown"
            ),
            label=desc,
            locality=get_cercalia_value(ge.get("city")),
            locality_code=get_cercalia_attr(ge.get("city"), "id"),
            municipality=get_cercalia_value(ge.get("municipality")),
            municipality_code=get_cercalia_attr(ge.get("municipality"), "id"),
            district=get_cercalia_value(ge.get("district")),
            district_code=get_cercalia_attr(ge.get("district"), "id"),
            subregion=get_cercalia_value(ge.get("subregion")),
            subregion_code=get_cercalia_attr(ge.get("subregion"), "id"),
            region=get_cercalia_value(ge.get("region")),
            region_code=get_cercalia_attr(ge.get("region"), "id"),
            country=get_cercalia_value(ge.get("country")),
            country_code=get_cercalia_attr(ge.get("country"), "id"),
            postal_code=pc,
            house_number=get_cercalia_value(ge.get("housenumber")),
            coord=Coordinate(
                lat=float(get_cercalia_attr(coord, "y")),  # type: ignore[arg-type]
                lng=float(get_cercalia_attr(coord, "x")),  # type: ignore[arg-type]
            ),
            type=self._map_candidate_type(type_val),
            level=type_val,  # type: ignore[arg-type]
        )

    def _map_candidate_type(self, type_val: Optional[str]) -> GeocodingCandidateType:
        """Map API type to SDK type."""
        if not type_val:
            return "address"

        type_lower = type_val.lower()
        type_map: dict[str, GeocodingCandidateType] = {
            "poi": "poi",
            "ct": "locality",
            "municipality": "municipality",
            "pcode": "postal_code",
            "postal_code": "postal_code",
            "rd": "road",
            "road": "road",
            "st": "street",
            "pk": "milestone",
            "milestone": "milestone",
            "adr": "address",
        }

        return type_map.get(type_lower, "address")
