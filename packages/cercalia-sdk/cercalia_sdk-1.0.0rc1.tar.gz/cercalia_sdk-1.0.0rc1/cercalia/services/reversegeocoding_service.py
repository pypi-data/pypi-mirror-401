"""
Reverse geocoding service for Cercalia SDK.

Provides coordinate to address conversion, timezone lookup, and polygon intersection queries.
"""

from typing import Any, Literal, Optional

from ..config import CercaliaConfig
from ..types.api_response import ensure_cercalia_array, get_cercalia_attr, get_cercalia_value
from ..types.common import CercaliaError, Coordinate
from ..types.geocoding import GeocodingCandidate, GeocodingCandidateType, GeocodingLevel
from ..types.reversegeocoding import (
    ReverseGeocodeOptions,
    ReverseGeocodeResult,
    SigpacInfo,
    TimezoneInfo,
    TimezoneOptions,
    TimezoneResult,
)
from .cercalia_client import CercaliaClient


class ReverseGeocodingService(CercaliaClient):
    """
    Reverse geocoding service for converting coordinates to addresses.

    Provides methods for:
    - Single coordinate reverse geocoding
    - Batch coordinate reverse geocoding (up to 100)
    - Timezone lookup for coordinates
    - Polygon intersection queries (find regions/municipalities)

    Example:
        >>> service = ReverseGeocodingService(config)
        >>> result = service.reverse_geocode(Coordinate(lat=41.3874, lng=2.1700))
        >>> print(result.ge.municipality)  # "Barcelona"
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the reverse geocoding service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def reverse_geocode(
        self,
        coord: Coordinate,
        options: Optional[ReverseGeocodeOptions] = None,
    ) -> Optional[ReverseGeocodeResult]:
        """
        Reverse geocode a single coordinate to get address information.

        Args:
            coord: Coordinate to reverse geocode
            options: Optional parameters (level, date_time, category)

        Returns:
            ReverseGeocodeResult if found, None if no results

        Example:
            >>> result = service.reverse_geocode(
            ...     Coordinate(lat=41.3874, lng=2.1700),
            ...     ReverseGeocodeOptions(level="adr")
            ... )
        """
        results = self.reverse_geocode_batch([coord], options)
        return results[0] if results else None

    def reverse_geocode_batch(
        self,
        coords: list[Coordinate],
        options: Optional[ReverseGeocodeOptions] = None,
    ) -> list[ReverseGeocodeResult]:
        """
        Reverse geocode multiple coordinates in a single request.

        Args:
            coords: List of coordinates (max 100)
            options: Optional parameters (level, date_time, category)

        Returns:
            List of ReverseGeocodeResult for each coordinate

        Raises:
            ValueError: If more than 100 coordinates provided

        Example:
            >>> results = service.reverse_geocode_batch([
            ...     Coordinate(lat=41.3874, lng=2.1700),  # Barcelona
            ...     Coordinate(lat=40.4169, lng=-3.7035),  # Madrid
            ... ])
        """
        if not coords:
            return []

        if len(coords) > 100:
            raise ValueError("Maximum 100 coordinates allowed per request")

        options = options or ReverseGeocodeOptions()

        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
        }

        # Single vs batch coordinate format
        if len(coords) == 1:
            params["mo"] = f"{coords[0].lat},{coords[0].lng}"
        else:
            params["molist"] = ",".join(f"[{c.lat},{c.lng}]" for c in coords)

        # Set level (default to 'adr' if no level or category specified)
        if options.level:
            params["rqge"] = options.level
        elif not options.category:
            params["rqge"] = "adr"

        # Special category (census, sigpac)
        if options.category:
            params["rqpoicats"] = options.category

        # DateTime for timezone
        if options.date_time:
            params["datetime"] = options.date_time

        try:
            response = self._request(params, "ReverseGeocoding")

            proximity = response.get("proximity")
            if not proximity:
                return []

            type_val = get_cercalia_attr(proximity, "type")

            # POI response (census/sigpac)
            if type_val == "poi":
                poi_list = proximity.get("poilist", {}).get("poi", [])
                pois = ensure_cercalia_array(poi_list)
                return [self._map_poi_to_result(p) for p in pois]

            # Geographic element responses (timezone, municipality, etc.)
            if type_val in ("timezone", "mun", "ct", "subreg", "reg", "ctry"):
                ge_list = proximity.get("gelist", {}).get("ge", [])
                ges = ensure_cercalia_array(ge_list)
                return [self._map_ge_to_result(g, type_val) for g in ges]

            # Default address-level responses (adr, cadr, st)
            mo_list = proximity.get("molist", {}).get("mo")
            if mo_list:
                mos = ensure_cercalia_array(mo_list)
                results = []
                for mo in mos:
                    # Get nested ge object directly (not using get_cercalia_attr as it's for string attrs)
                    ge_obj = mo.get("ge") if isinstance(mo, dict) else None
                    if ge_obj:
                        results.append(self._map_ge_to_result(ge_obj, type_val or "adr"))
                return results

            # Fallback to gelist
            ge_list = proximity.get("gelist", {}).get("ge")
            if ge_list:
                ges = ensure_cercalia_array(ge_list)
                return [self._map_ge_to_result(g, type_val or "adr") for g in ges]

            return []

        except CercaliaError as e:
            # Handle "No results" gracefully
            if e.code == "30006":
                return []
            raise

    def get_intersecting_regions(
        self,
        wkt: str,
        level: Literal["ct", "mun", "subreg", "reg"] = "mun",
    ) -> list[ReverseGeocodeResult]:
        """
        Get regions/municipalities intersecting a polygon (WKT).

        Args:
            wkt: Well-Known Text representation of the polygon
            level: Geographic level to query ("ct", "mun", "subreg", "reg")

        Returns:
            List of ReverseGeocodeResult for intersecting regions

        Example:
            >>> wkt = "POLYGON((2.10 41.35, 2.20 41.35, 2.20 41.45, 2.10 41.45, 2.10 41.35))"
            >>> results = service.get_intersecting_regions(wkt, "mun")
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "cs": "4326",
            "wkt": wkt,
            "rqge": level,
        }

        try:
            response = self._request(params, "IntersectingRegions")

            ge_list = response.get("proximity", {}).get("gelist", {}).get("ge", [])
            ges = ensure_cercalia_array(ge_list)
            return [self._map_ge_to_result(g, level) for g in ges]

        except CercaliaError as e:
            # Handle "No results" gracefully
            if e.code == "30006":
                return []
            raise

    def get_timezone(
        self,
        coord: Coordinate,
        options: Optional[TimezoneOptions] = None,
    ) -> Optional[TimezoneResult]:
        """
        Get timezone information for a coordinate.

        Args:
            coord: Coordinate to get timezone for
            options: Optional datetime in ISO 8601 format

        Returns:
            TimezoneResult with timezone info, None if not found

        Example:
            >>> result = service.get_timezone(
            ...     Coordinate(lat=41.3874, lng=2.1700),
            ...     TimezoneOptions(date_time="2019-09-27T14:30:12Z")
            ... )
            >>> print(result.id)  # "Europe/Madrid"
        """
        options = options or TimezoneOptions()

        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
            "mo": f"{coord.lat},{coord.lng}",
            "rqge": "timezone",
        }

        if options.date_time:
            params["datetime"] = options.date_time

        try:
            response = self._request(params, "Timezone")

            proximity = response.get("proximity")
            if not proximity:
                return None

            ge_list = proximity.get("gelist", {}).get("ge", [])
            ges = ensure_cercalia_array(ge_list)
            if not ges:
                return None

            # Timezone response has no coordinates, all data in attributes
            ge_obj = ges[0]

            return TimezoneResult(
                coord=coord,
                id=get_cercalia_attr(ge_obj, "id") or "",
                name=get_cercalia_attr(ge_obj, "name") or "",
                local_date_time=get_cercalia_attr(ge_obj, "localdatetime") or "",
                utc_date_time=get_cercalia_attr(ge_obj, "utcdatetime") or "",
                utc_offset=int(get_cercalia_attr(ge_obj, "utctimeoffset") or "0"),
                daylight_saving_time=int(get_cercalia_attr(ge_obj, "daylightsavingtime") or "0"),
            )

        except CercaliaError as e:
            # Handle "No results" gracefully
            if e.code == "30006":
                return None
            raise

    def _map_ge_to_result(self, ge: Any, type_val: str) -> ReverseGeocodeResult:
        """Map a geographic element to ReverseGeocodeResult."""
        ge_obj = ge if isinstance(ge, dict) else {}

        # GOLDEN RULE: Strict coordinates - validate existence
        coord_obj = ge_obj.get("coord", {})
        coord_y = get_cercalia_attr(coord_obj, "y")
        coord_x = get_cercalia_attr(coord_obj, "x")

        if not coord_y or not coord_x:
            raise ValueError("Invalid geographic element: missing coordinates")

        # Build GeocodingCandidate with all administrative info
        candidate = GeocodingCandidate(
            id=get_cercalia_attr(ge_obj, "id") or "unknown",
            name=get_cercalia_attr(ge_obj, "name")
            or get_cercalia_value(ge_obj.get("name"))
            or "Unknown",
            municipality=get_cercalia_value(ge_obj.get("municipality")),
            district=get_cercalia_value(ge_obj.get("district")),
            subregion=get_cercalia_value(ge_obj.get("subregion")),
            region=get_cercalia_value(ge_obj.get("region")),
            country=get_cercalia_value(ge_obj.get("country")),
            house_number=get_cercalia_value(ge_obj.get("housenumber")),
            coord=Coordinate(
                lat=float(coord_y),
                lng=float(coord_x),
            ),
            type=self._map_candidate_type(get_cercalia_attr(ge_obj, "frc") or type_val),
            level=self._map_level(get_cercalia_attr(ge_obj, "type") or type_val),
        )

        # GOLDEN RULE: ID Integrity - include all codes
        # Map city -> locality with locality_code
        if ge_obj.get("city"):
            city_obj = ge_obj["city"]
            candidate.locality = get_cercalia_value(city_obj)
            candidate.locality_code = get_cercalia_attr(city_obj, "id")

        # Municipality code
        if ge_obj.get("municipality"):
            mun_obj = ge_obj["municipality"]
            candidate.municipality_code = get_cercalia_attr(mun_obj, "id")

        # Street with street_code
        if ge_obj.get("street"):
            street_obj = ge_obj["street"]
            candidate.street = get_cercalia_value(street_obj) or get_cercalia_attr(
                street_obj, "name"
            )
            candidate.street_code = get_cercalia_attr(street_obj, "id")

        # District code
        if ge_obj.get("district"):
            district_obj = ge_obj["district"]
            candidate.district_code = get_cercalia_attr(district_obj, "id")

        # Subregion code
        if ge_obj.get("subregion"):
            subregion_obj = ge_obj["subregion"]
            candidate.subregion_code = get_cercalia_attr(subregion_obj, "id")

        # Region code
        if ge_obj.get("region"):
            region_obj = ge_obj["region"]
            candidate.region_code = get_cercalia_attr(region_obj, "id")

        # Country code
        if ge_obj.get("country"):
            country_obj = ge_obj["country"]
            candidate.country_code = get_cercalia_attr(country_obj, "id")

        # Postal code handling
        pc = get_cercalia_value(ge_obj.get("postalcode"))
        if isinstance(pc, dict):
            pc = get_cercalia_value(pc) or get_cercalia_attr(pc, "id")
        elif not pc and ge_obj.get("postalcode"):
            pc = get_cercalia_attr(ge_obj.get("postalcode"), "id")
        candidate.postal_code = pc

        # Build result
        result = ReverseGeocodeResult(ge=candidate)

        # Distance
        dist = get_cercalia_attr(ge_obj, "dist")
        if dist:
            result.distance = float(dist)

        # Speed
        kmh = get_cercalia_attr(ge_obj, "kmh")
        if kmh:
            result.max_speed = int(float(kmh))

        # Milestone
        km = get_cercalia_value(ge_obj.get("km"))
        if km:
            result.km = km

        # Direction
        direction = get_cercalia_value(ge_obj.get("direction"))
        if direction:
            result.direction = direction

        # Timezone specific
        if type_val == "timezone":
            result.timezone = TimezoneInfo(
                id=get_cercalia_attr(ge_obj, "id") or "",
                name=get_cercalia_attr(ge_obj, "name") or "",
                local_date_time=get_cercalia_attr(ge_obj, "localdatetime") or "",
                utc_date_time=get_cercalia_attr(ge_obj, "utcdatetime") or "",
                utc_offset=int(get_cercalia_attr(ge_obj, "utctimeoffset") or "0"),
                daylight_saving_time=int(get_cercalia_attr(ge_obj, "daylightsavingtime") or "0"),
            )

        return result

    def _map_poi_to_result(self, poi: Any) -> ReverseGeocodeResult:
        """Map a POI element to ReverseGeocodeResult."""
        poi_obj = poi if isinstance(poi, dict) else {}

        # GOLDEN RULE: Strict coordinates
        coord_obj = poi_obj.get("coord", {})
        coord_y = get_cercalia_attr(coord_obj, "y")
        coord_x = get_cercalia_attr(coord_obj, "x")

        if not coord_y or not coord_x:
            raise ValueError("Invalid POI: missing coordinates")

        category = get_cercalia_attr(poi_obj, "category_id")
        ge = poi_obj.get("ge", {})

        candidate = GeocodingCandidate(
            id=get_cercalia_attr(poi_obj, "id") or "",
            name=get_cercalia_value(poi_obj.get("name")) or "",
            municipality=get_cercalia_value(ge.get("municipality")),
            subregion=get_cercalia_value(ge.get("subregion")),
            region=get_cercalia_value(ge.get("region")),
            country=get_cercalia_value(ge.get("country")),
            coord=Coordinate(
                lat=float(coord_y),
                lng=float(coord_x),
            ),
            type="poi",
        )

        # GOLDEN RULE: ID Integrity
        # Map city -> locality
        if ge.get("city"):
            city_obj = ge["city"]
            candidate.locality = get_cercalia_value(city_obj)
            candidate.locality_code = get_cercalia_attr(city_obj, "id")

        # Municipality code
        if ge.get("municipality"):
            mun_obj = ge["municipality"]
            candidate.municipality_code = get_cercalia_attr(mun_obj, "id")

        # Subregion code
        if ge.get("subregion"):
            subregion_obj = ge["subregion"]
            candidate.subregion_code = get_cercalia_attr(subregion_obj, "id")

        # Region code
        if ge.get("region"):
            region_obj = ge["region"]
            candidate.region_code = get_cercalia_attr(region_obj, "id")

        # Country code
        if ge.get("country"):
            country_obj = ge["country"]
            candidate.country_code = get_cercalia_attr(country_obj, "id")

        result = ReverseGeocodeResult(ge=candidate)

        # Census ID
        if category == "D00SECCEN":
            result.census_id = get_cercalia_value(poi_obj.get("info")) or get_cercalia_value(
                poi_obj.get("name")
            )

        # SIGPAC info
        elif category == "D00SIGPAC":
            info = get_cercalia_value(poi_obj.get("info")) or ""
            parts = info.split("|")
            result.sigpac = SigpacInfo(
                id=get_cercalia_value(poi_obj.get("name")) or "",
                municipality_code=parts[0] if len(parts) > 0 else "",
                usage=parts[1] if len(parts) > 1 else "",
                extension_ha=float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
                vulnerable_type=parts[3] if len(parts) > 3 else None,
                vulnerable_code=parts[4] if len(parts) > 4 else None,
            )

        return result

    def _map_candidate_type(self, type_val: Optional[str]) -> GeocodingCandidateType:
        """Map API type to SDK type."""
        if not type_val:
            return "address"

        t = type_val.lower()
        if t in ("ap", "av", "na1", "a2", "pl", "ep", "cl", "pt"):
            return "road"
        if t in ("poi", "timezone"):
            return "poi"
        if t in ("ct", "municipality", "mun"):
            return "municipality"
        return "address"

    def _map_level(self, type_val: Optional[str]) -> Optional[GeocodingLevel]:
        """Map API type to GeocodingLevel."""
        if not type_val:
            return None

        t = type_val.lower()
        level_map: dict[str, GeocodingLevel] = {
            "adr": "adr",
            "cadr": "adr",
            "st": "st",
            "ct": "ct",
            "pcode": "pcode",
            "mun": "mun",
            "subreg": "subreg",
            "reg": "reg",
            "ctry": "ctry",
            "rd": "rd",
            "pk": "pk",
            "poi": "poi",
            "timezone": "poi",
        }
        return level_map.get(t)
