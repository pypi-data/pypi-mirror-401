"""
Proximity Service for Cercalia SDK.

This service provides methods to search for nearest POIs based on location,
optionally including routing information.
"""

from typing import Any, Literal

from ..config import CercaliaConfig
from ..types.api_response import (
    ensure_cercalia_array,
    get_cercalia_attr,
    get_cercalia_value,
)
from ..types.common import Coordinate
from ..types.poi import PoiGeographicElement
from ..types.proximity import ProximityItem, ProximityOptions, ProximityResult
from .cercalia_client import CercaliaClient


class ProximityService(CercaliaClient):
    """
    Service for proximity-based POI searches.

    Provides methods to find nearest points of interest from a given location,
    with optional routing distance/time calculations.
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the Proximity service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def find_nearest(self, options: ProximityOptions) -> ProximityResult:
        """
        Find nearest POIs from a center point.

        Args:
            options: Search options including center, categories, count, etc.

        Returns:
            ProximityResult with list of nearby POIs

        Raises:
            CercaliaError: If the API returns an error
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
            "mo": f"{options.center.lat},{options.center.lng}",
        }

        if options.count is not None:
            params["num"] = str(options.count)

        if options.max_radius is not None:
            params["rad"] = str(options.max_radius)

        if options.categories:
            params["rqpoicats"] = ",".join(options.categories)

        if options.include_routing and options.route_weight:
            params["weight"] = options.route_weight

        data = self._request(params, "Proximity")
        return self._parse_response(data, options.center)

    def find_nearest_by_category(
        self,
        center: Coordinate,
        category_code: str,
        count: int = 5,
    ) -> ProximityResult:
        """
        Find nearest POIs of a specific category.

        Convenience method for single-category searches.

        Args:
            center: Center coordinate for the search
            category_code: POI category code (e.g., 'C001' for gas stations)
            count: Maximum number of results (default: 5)

        Returns:
            ProximityResult with list of nearby POIs
        """
        return self.find_nearest(
            ProximityOptions(
                center=center,
                categories=[category_code],
                count=count,
            )
        )

    def find_nearest_with_routing(
        self,
        center: Coordinate,
        category_code: str,
        weight: Literal["time", "distance"] = "time",
        count: int = 5,
    ) -> ProximityResult:
        """
        Find nearest POIs with routing information.

        Returns POIs sorted by actual route distance/time rather than
        straight-line distance.

        Args:
            center: Center coordinate for the search
            category_code: POI category code
            weight: Route optimization ('time' or 'distance')
            count: Maximum number of results (default: 5)

        Returns:
            ProximityResult with routing info in each item
        """
        return self.find_nearest(
            ProximityOptions(
                center=center,
                categories=[category_code],
                count=count,
                include_routing=True,
                route_weight=weight,
            )
        )

    def _parse_response(self, data: dict[str, Any], center: Coordinate) -> ProximityResult:
        """
        Parse the API response into a ProximityResult.

        Args:
            data: Raw API response (cercalia object)
            center: Original search center

        Returns:
            Parsed ProximityResult
        """
        proximity = data.get("proximity")
        if not proximity or not proximity.get("poilist"):
            return ProximityResult(items=[], center=center, total_found=0)

        poi_list = proximity.get("poilist", {})
        pois = poi_list.get("poi")

        if not pois:
            return ProximityResult(items=[], center=center, total_found=0)

        poi_array = ensure_cercalia_array(pois)
        items = [self._parse_item(poi) for poi in poi_array]

        return ProximityResult(
            items=items,
            center=center,
            total_found=len(items),
        )

    def _parse_item(self, poi: dict[str, Any]) -> ProximityItem:
        """
        Parse a single POI from the API response.

        GOLDEN RULES:
        - Strict coordinates (no defaults)
        - All name fields have corresponding ID fields
        - Direct mapping without fallbacks

        Args:
            poi: Raw POI data from API

        Returns:
            Parsed ProximityItem

        Raises:
            ValueError: If coordinates are missing
        """
        # GOLDEN RULE: Strict coordinates - no defaults
        coord_obj = poi.get("coord", {})
        coord_y = get_cercalia_attr(coord_obj, "y")
        coord_x = get_cercalia_attr(coord_obj, "x")

        if not coord_y or not coord_x:
            raise ValueError("Invalid POI: missing coordinates")

        coord = Coordinate(lat=float(coord_y), lng=float(coord_x))

        # Build item with required fields
        item = ProximityItem(
            id=get_cercalia_attr(poi, "id") or "",
            name=get_cercalia_value(poi.get("name")) or "",
            coord=coord,
            distance=int(get_cercalia_attr(poi, "dist") or "0"),
        )

        # Position in results
        position = get_cercalia_attr(poi, "pos")
        if position:
            item.position = int(position)

        # Category codes
        category_code = get_cercalia_attr(poi, "category_id")
        if category_code:
            item.category_code = category_code

        subcategory_code = get_cercalia_attr(poi, "subcategory_id")
        if subcategory_code and subcategory_code != "-1":
            item.subcategory_code = subcategory_code

        # Geometry type (for transparency)
        geometry = get_cercalia_attr(poi, "geometry")
        if geometry:
            item.geometry = geometry

        # Info field
        info = get_cercalia_value(poi.get("info"))
        if info:
            item.info = info

        # Geographic element (address)
        if poi.get("ge"):
            item.ge = self._parse_geographic_element(poi["ge"])

        # Routing data
        route_dist = get_cercalia_attr(poi, "routedist")
        if route_dist:
            item.route_distance = int(route_dist)

        route_time = get_cercalia_attr(poi, "routetime")
        if route_time:
            item.route_time = int(route_time)

        route_realtime = get_cercalia_attr(poi, "routerealtime")
        if route_realtime:
            item.route_realtime = int(route_realtime)

        route_weight = get_cercalia_attr(poi, "routeweight")
        if route_weight:
            item.route_weight = int(route_weight)

        return item

    def _parse_geographic_element(self, ge: dict[str, Any]) -> PoiGeographicElement:
        """
        Parse geographic element (address) from POI.

        GOLDEN RULES:
        - Use locality instead of city
        - All names have corresponding ID fields
        - No fallback values

        Args:
            ge: Raw geographic element data

        Returns:
            Parsed PoiGeographicElement
        """
        result = PoiGeographicElement()

        # House number
        if ge.get("housenumber"):
            result.house_number = get_cercalia_value(ge["housenumber"])

        # Street with code
        if ge.get("street"):
            street_obj = ge["street"]
            result.street = get_cercalia_value(street_obj) or get_cercalia_attr(street_obj, "name")
            result.street_code = get_cercalia_attr(street_obj, "id")

        # GOLDEN RULE: Use locality instead of city
        if ge.get("city"):
            city_obj = ge["city"]
            result.locality = get_cercalia_value(city_obj)
            result.locality_code = get_cercalia_attr(city_obj, "id")

        # Municipality with code
        if ge.get("municipality"):
            municipality_obj = ge["municipality"]
            result.municipality = get_cercalia_value(municipality_obj)
            result.municipality_code = get_cercalia_attr(municipality_obj, "id")

        # Subregion with code
        if ge.get("subregion"):
            subregion_obj = ge["subregion"]
            result.subregion = get_cercalia_value(subregion_obj)
            result.subregion_code = get_cercalia_attr(subregion_obj, "id")

        # Region with code
        if ge.get("region"):
            region_obj = ge["region"]
            result.region = get_cercalia_value(region_obj)
            result.region_code = get_cercalia_attr(region_obj, "id")

        # Country with code
        if ge.get("country"):
            country_obj = ge["country"]
            result.country = get_cercalia_value(country_obj)
            result.country_code = get_cercalia_attr(country_obj, "id")

        return result
