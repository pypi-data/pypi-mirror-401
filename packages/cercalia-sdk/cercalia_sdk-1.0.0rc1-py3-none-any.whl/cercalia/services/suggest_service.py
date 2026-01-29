"""
Suggest service for Cercalia SDK.

Provides address and POI autocomplete using Cercalia Suggest API.
"""

from typing import Any, Optional
from urllib.parse import urlencode

import requests

from ..config import CercaliaConfig
from ..types.common import Coordinate
from ..types.suggest import (
    CityInfo,
    CountryInfo,
    HouseNumberInfo,
    MunicipalityInfo,
    PoiInfo,
    RegionInfo,
    StreetInfo,
    SubregionInfo,
    SuggestGeocodeOptions,
    SuggestGeocodeResult,
    SuggestOptions,
    SuggestResult,
)
from ..utils.logger import logger
from ..utils.retry import retry_request
from .cercalia_client import CercaliaClient

# Base URL for Cercalia Suggest API (different from main services)
SUGGEST_BASE_URL = "https://lb.cercalia.com/suggest/SuggestServlet"


class SuggestService(CercaliaClient):
    """
    Address and POI autocomplete using Cercalia Suggest API.

    This service provides real-time autocomplete suggestions for addresses,
    streets, cities, and POIs. It's designed for typeahead search experiences.

    Key Features:
    - Street suggestions: Autocomplete street names with house number availability
    - City suggestions: Find cities/localities by partial name
    - POI suggestions: Search points of interest with category filtering
    - Geocoding: Convert suggestions to precise coordinates

    Example:
        >>> service = SuggestService(config)
        >>>
        >>> # Basic address autocomplete
        >>> results = service.search(SuggestOptions(text="Provença 5"))
        >>>
        >>> # Filter by country and type
        >>> streets = service.search(SuggestOptions(
        ...     text="Gran Via",
        ...     country_code="ESP",
        ...     geo_type="st"
        ... ))
        >>>
        >>> # Geocode a specific result
        >>> coords = service.geocode(SuggestGeocodeOptions(
        ...     street_code=results[0].street.code,
        ...     street_number="589",
        ...     city_code=results[0].city.code
        ... ))
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the suggest service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def search(self, options: SuggestOptions) -> list[SuggestResult]:
        """
        Search for address/POI suggestions based on partial text input.

        Use this method for autocomplete/typeahead functionality. Returns suggestions
        ordered by relevance. Minimum 3 characters recommended for best results.

        Args:
            options: Search configuration

        Returns:
            List of suggestions ordered by relevance

        Example:
            >>> # Search streets in Barcelona
            >>> results = service.search(SuggestOptions(
            ...     text="Diagonal",
            ...     country_code="ESP",
            ...     geo_type="st"
            ... ))

            >>> # Search POIs near a location
            >>> pois = service.search(SuggestOptions(
            ...     text="Restaurant",
            ...     geo_type="poi",
            ...     center=Coordinate(lat=41.39, lng=2.15),
            ...     radius=5000
            ... ))
        """
        if not options.text or len(options.text) < 1:
            return []

        params: dict[str, str] = {"t": options.text}

        # Geographic type filter
        if options.geo_type:
            params["getype"] = options.geo_type

        # Geographic filters
        if options.country_code:
            params["ctryc"] = options.country_code.upper()
        if options.region_code:
            params["regc"] = options.region_code
        if options.subregion_code:
            params["subregc"] = options.subregion_code
        if options.municipality_code:
            params["munc"] = options.municipality_code
        if options.street_code:
            params["rsc"] = options.street_code
        if options.postal_code_prefix:
            params["rscp"] = options.postal_code_prefix

        # Language
        if options.language:
            params["lang"] = options.language

        # Proximity search
        if options.center:
            params["pt"] = f"{options.center.lat},{options.center.lng}"
            if options.radius:
                params["d"] = str(options.radius)

        # POI categories
        if options.poi_categories and len(options.poi_categories) > 0:
            params["poicat"] = ",".join(options.poi_categories)

        try:
            data = self._request_suggest(params, "SuggestService")
            return self._parse_suggest_response(data)
        except Exception as e:
            logger.error(f"[SuggestService] Search error: {e}")
            raise

    def search_streets(self, text: str, country_code: Optional[str] = None) -> list[SuggestResult]:
        """
        Search for street suggestions only.

        Convenience method for street-only autocomplete.

        Args:
            text: Search text
            country_code: Optional country code filter

        Returns:
            List of street suggestions

        Example:
            >>> streets = service.search_streets("Gran Via", "ESP")
        """
        return self.search(SuggestOptions(text=text, geo_type="st", country_code=country_code))

    def search_cities(self, text: str, country_code: Optional[str] = None) -> list[SuggestResult]:
        """
        Search for city/locality suggestions only.

        Convenience method for city-only autocomplete.

        Args:
            text: Search text
            country_code: Optional country code filter

        Returns:
            List of city suggestions

        Example:
            >>> cities = service.search_cities("Barcel", "ESP")
        """
        return self.search(SuggestOptions(text=text, geo_type="ct", country_code=country_code))

    def search_pois(
        self,
        text: str,
        country_code: Optional[str] = None,
        center: Optional[Coordinate] = None,
        radius: Optional[float] = None,
        poi_categories: Optional[list[str]] = None,
    ) -> list[SuggestResult]:
        """
        Search for POI suggestions only.

        Convenience method for POI-only autocomplete.

        Args:
            text: Search text
            country_code: Optional country code filter
            center: Center point for proximity search
            radius: Search radius in meters
            poi_categories: POI category codes filter

        Returns:
            List of POI suggestions

        Example:
            >>> # Search restaurants near Barcelona
            >>> pois = service.search_pois(
            ...     "Restaurant",
            ...     center=Coordinate(lat=41.39, lng=2.15),
            ...     radius=5000,
            ...     poi_categories=["C014"]
            ... )
        """
        return self.search(
            SuggestOptions(
                text=text,
                geo_type="poi",
                country_code=country_code,
                center=center,
                radius=radius,
                poi_categories=poi_categories,
            )
        )

    def geocode(self, options: SuggestGeocodeOptions) -> SuggestGeocodeResult:
        """
        Geocode a suggestion to get precise coordinates.

        After selecting a suggestion from `search()`, use this method to get
        the exact coordinates for the address. For streets, you can specify
        a house number to get the precise location.

        Args:
            options: Geocode options with codes from suggestion

        Returns:
            Geocoded result with coordinates and full address

        Raises:
            ValueError: If geocoding fails or no results found

        Example:
            >>> # First search for suggestions
            >>> suggestions = service.search(SuggestOptions(text="Provença 5"))
            >>>
            >>> # Then geocode the selected suggestion with specific number
            >>> location = service.geocode(SuggestGeocodeOptions(
            ...     street_code=suggestions[0].street.code,
            ...     street_number="589",
            ...     city_code=suggestions[0].city.code,
            ...     country_code="ESP"
            ... ))
            >>> print(location.coord)  # Coordinate(lat=41.41, lng=2.18)
        """
        params: dict[str, str] = {}

        if options.city_code:
            params["ctc"] = options.city_code
        if options.postal_code:
            params["pcode"] = options.postal_code
        if options.street_code:
            params["stc"] = options.street_code
        if options.street_number:
            params["stnum"] = options.street_number
        if options.country_code:
            params["ctryc"] = options.country_code.upper()

        try:
            data = self._request_suggest(params, "SuggestGeocode")
            return self._parse_geocode_response(data)
        except Exception as e:
            logger.error(f"[SuggestService] Geocode error: {e}")
            raise

    def find_and_geocode(
        self,
        text: str,
        country_code: Optional[str] = None,
        street_number: Optional[str] = None,
    ) -> Optional[SuggestGeocodeResult]:
        """
        Combined search and geocode - finds and geocodes the best match.

        This is a convenience method that combines search and geocode in one call.
        Useful when you need coordinates directly from a text query.

        Args:
            text: Address text to search
            country_code: Optional country code filter
            street_number: Optional house number to geocode

        Returns:
            Geocoded result of the best match, or None if no results

        Example:
            >>> location = service.find_and_geocode(
            ...     "Provença 589, Barcelona",
            ...     country_code="ESP"
            ... )
            >>> if location:
            ...     print(location.coord)  # Coordinate(lat=41.41, lng=2.18)
        """
        suggestions = self.search(SuggestOptions(text=text, country_code=country_code))

        if not suggestions:
            return None

        best = suggestions[0]

        # If suggestion already has coordinates, return them
        if best.coord:
            return SuggestGeocodeResult(
                coord=best.coord,
                formatted_address=best.display_text,
                name=best.display_text,
                street_code=best.street.code if best.street else None,
                street_name=best.street.name if best.street else None,
                city_code=best.city.code if best.city else None,
                city_name=best.city.name if best.city else None,
                municipality_code=best.municipality.code if best.municipality else None,
                municipality_name=best.municipality.name if best.municipality else None,
                subregion_code=best.subregion.code if best.subregion else None,
                subregion_name=best.subregion.name if best.subregion else None,
                region_code=best.region.code if best.region else None,
                region_name=best.region.name if best.region else None,
                country_code=best.country.code if best.country else None,
                country_name=best.country.name if best.country else None,
                postal_code=best.postal_code,
            )

        # Otherwise geocode the suggestion
        return self.geocode(
            SuggestGeocodeOptions(
                street_code=best.street.code if best.street else None,
                city_code=best.city.code if best.city else None,
                street_number=street_number,
                country_code=best.country.code if best.country else country_code,
            )
        )

    def _request_suggest(
        self, params: dict[str, str], operation_name: str = "SuggestService"
    ) -> dict[str, Any]:
        """
        Custom request method for Suggest API (uses Solr JSON format).
        """
        all_params = {"key": self.config.api_key, **params}
        url = f"{SUGGEST_BASE_URL}?{urlencode(all_params)}"
        logger.debug(f"[{operation_name}] Request URL: {url}")

        def make_request() -> dict[str, Any]:
            response = requests.get(url, timeout=30)

            if not response.ok:
                logger.error(
                    f"[{operation_name}] HTTP Error {response.status_code}: {response.text}"
                )
                raise requests.HTTPError(
                    f"Cercalia API error: {response.status_code} {response.reason}"
                )

            raw_data = response.text
            logger.debug(f"[{operation_name}] Response: {raw_data[:500]}...")

            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"[{operation_name}] Invalid JSON response: {raw_data}")
                raise ValueError("Invalid JSON response from Suggest API") from e

            # Validate Solr response format
            if "response" not in data:
                raise ValueError("Invalid Solr response format: missing response object")

            return data

        return retry_request(
            make_request,
            max_attempts=3,
            delay_ms=500,
            log_retries=True,
            operation_name=operation_name,
        )

    def _parse_suggest_response(self, data: dict[str, Any]) -> list[SuggestResult]:
        """Parse the Suggest API response into normalized SuggestResult array."""
        # Handle error responses
        if data.get("responseHeader", {}).get("status", 0) != 0:
            raise ValueError(
                f"Cercalia Suggest API error: status {data['responseHeader']['status']}"
            )

        docs = data.get("response", {}).get("docs", [])
        if not isinstance(docs, list) or len(docs) == 0:
            return []

        return [self._parse_suggestion(doc) for doc in docs]

    def _parse_suggestion(self, s: dict[str, Any]) -> SuggestResult:
        """Parse a single suggestion document from Solr response."""
        id_val = s.get("id", "")

        # Build display text from available fields
        display_text = self._build_display_text(s)

        # Determine type based on available fields
        type_val = self._determine_type(s)

        result = SuggestResult(
            id=id_val,
            display_text=display_text,
            type=type_val,
        )

        # Street information - DIRECT MAPPING from API fields
        if s.get("calle_id") or s.get("calle_nombre") or s.get("calle_descripcion"):
            result.street = StreetInfo(
                code=s.get("calle_id"),
                name=s.get("calle_nombre"),
                description=s.get("calle_descripcion"),
                type=s.get("calle_tipo"),
                article=s.get("calle_articulo"),
            )

        # City/locality information - DIRECT MAPPING
        if s.get("localidad_id") or s.get("localidad_nombre"):
            result.city = CityInfo(
                code=s.get("localidad_id"),
                name=s.get("localidad_nombre"),
                bracket_locality=s.get("distrito_nombre"),
            )

        # Postal code - DIRECT MAPPING
        if s.get("codigo_postal"):
            result.postal_code = s.get("codigo_postal")

        # Municipality - DIRECT MAPPING
        if s.get("municipio_id") or s.get("municipio_nombre"):
            result.municipality = MunicipalityInfo(
                code=s.get("municipio_id"),
                name=s.get("municipio_nombre"),
            )

        # Subregion/Province - DIRECT MAPPING
        if s.get("provincia_id") or s.get("provincia_nombre"):
            result.subregion = SubregionInfo(
                code=s.get("provincia_id"),
                name=s.get("provincia_nombre"),
            )

        # Region - DIRECT MAPPING
        if s.get("comunidad_id") or s.get("comunidad_nombre"):
            result.region = RegionInfo(
                code=s.get("comunidad_id"),
                name=s.get("comunidad_nombre"),
            )

        # Country - DIRECT MAPPING
        if s.get("pais_id") or s.get("pais_nombre"):
            result.country = CountryInfo(
                code=s.get("pais_id"),
                name=s.get("pais_nombre"),
            )

        # Coordinates (format: "lat,lng" as string)
        coord_str = s.get("coord")
        if coord_str and isinstance(coord_str, str) and "," in coord_str:
            parts = coord_str.split(",")
            try:
                lat = float(parts[0])
                lng = float(parts[1])
                result.coord = Coordinate(lat=lat, lng=lng)
            except ValueError:
                pass

        # House numbers availability - DIRECT MAPPING
        if (
            s.get("portal_min") is not None
            or s.get("portal_max") is not None
            or s.get("portal") is not None
            or s.get("portal_disponible") is not None
        ):
            result.house_numbers = HouseNumberInfo(
                available=s.get("portal_min") is not None or s.get("portal_max") is not None,
                min=s.get("portal_min"),
                max=s.get("portal_max"),
                current=self._parse_portal(s.get("portal")),
                adjusted=self._parse_portal(s.get("portal_disponible")),
                is_english_format=s.get("portal_en"),
            )

            # Build hint from portal range
            if s.get("portal_min") is not None and s.get("portal_max") is not None:
                result.house_numbers.hint = f"{s.get('portal_min')}-{s.get('portal_max')}"

        # Official name flag
        if s.get("oficial") == "Y":
            result.is_official = True

        # Relevance score
        if s.get("score") is not None:
            result.score = s.get("score")

        # POI specific data
        if type_val == "poi" and (
            s.get("poi_id") or s.get("poi_name") or s.get("poi_cat") or s.get("category_id")
        ):
            result.poi = PoiInfo(
                code=s.get("poi_id") or id_val,
                name=s.get("poi_name") or s.get("nombre") or display_text,
                category_code=s.get("poi_cat") or s.get("category_id"),
            )

        return result

    def _build_display_text(self, s: dict[str, Any]) -> str:
        """Build a human-readable display text from suggestion fields."""
        parts: list[str] = []

        # Street (use descripcion which includes type like "Carrer de Provença")
        street = s.get("calle_descripcion") or s.get("calle_nombre")
        if street:
            number = s.get("portal")
            parts.append(f"{street}, {number}" if number else street)

        # City/locality (with optional district)
        city = s.get("localidad_nombre")
        if city:
            district = s.get("distrito_nombre")
            parts.append(f"{city} ({district})" if district else city)

        # Municipality (if different from city)
        mun = s.get("municipio_nombre")
        if mun and mun != city:
            parts.append(mun)

        # Province
        prov = s.get("provincia_nombre")
        if prov:
            parts.append(prov)

        # Country
        country = s.get("pais_nombre")
        if country:
            parts.append(country)

        # Fallback to name field or id
        if not parts:
            return s.get("nombre") or s.get("id") or ""

        return ", ".join(parts)

    def _determine_type(self, s: dict[str, Any]) -> str:
        """Determine the type of suggestion based on available fields."""
        # POI type
        if s.get("poi_id") or s.get("poi_cat") or s.get("category_id"):
            return "poi"

        # Has street ID = street suggestion
        if s.get("calle_id"):
            # If has portal number, it's an address
            if s.get("portal") is not None:
                return "address"
            return "street"

        # Has city/locality but no street = city suggestion
        if s.get("localidad_id") and not s.get("calle_id") and not s.get("calle_nombre"):
            return "city"

        # Default to street for results from Suggest API
        if s.get("calle_nombre") or s.get("calle_descripcion"):
            return "street"

        # Default fallback
        return "address"

    def _parse_portal(self, val: Any) -> Optional[int]:
        """Parse portal value (API may return string or number)."""
        if val is None:
            return None
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    def _parse_geocode_response(self, data: dict[str, Any]) -> SuggestGeocodeResult:
        """Parse geocode response into normalized result."""
        # Check for API error status
        if data.get("responseHeader", {}).get("status", 0) != 0:
            raise ValueError(
                f"Cercalia Suggest Geocode API error: status {data['responseHeader']['status']}"
            )

        resp = data.get("response", {})

        # GOLDEN RULE: Extract coordinate (required - throw if missing)
        coord: Optional[Coordinate] = None

        c = resp.get("coord")
        if c:
            if isinstance(c, str) and "," in c:
                parts = c.split(",")
                coord = Coordinate(lat=float(parts[0]), lng=float(parts[1]))
            elif isinstance(c, dict) and c.get("x") is not None and c.get("y") is not None:
                coord = Coordinate(lat=float(c["y"]), lng=float(c["x"]))

        if not coord:
            raise ValueError("Cercalia Suggest Geocode: No coordinates in response")

        # Extract all fields from response - DIRECT MAPPING
        desc = resp.get("desc")
        name = resp.get("name")
        housenumber = resp.get("housenumber")
        postalcode = resp.get("postalcode")

        return SuggestGeocodeResult(
            coord=coord,
            formatted_address=desc or name or "Unknown address",
            name=name,
            house_number=housenumber,
            postal_code=postalcode,
            # Note: The basic geocode response doesn't include administrative codes
            street_code=None,
            street_name=None,
            city_code=None,
            city_name=None,
            municipality_code=None,
            municipality_name=None,
            subregion_code=None,
            subregion_name=None,
            region_code=None,
            region_name=None,
            country_code=None,
            country_name=None,
        )
