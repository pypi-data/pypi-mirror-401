"""
POI service for Cercalia SDK.

Provides Points of Interest search using Cercalia API.
"""

from typing import Any, Optional, Union

from ..config import CercaliaConfig
from ..types.api_response import get_cercalia_attr, get_cercalia_value
from ..types.common import Coordinate
from ..types.poi import (
    MapExtent,
    Poi,
    PoiAlongRouteOptions,
    PoiGeographicElement,
    PoiInExtentOptions,
    PoiInPolygonOptions,
    PoiNearestOptions,
    PoiNearestWithRoutingOptions,
    PoiPixels,
    WeatherDayForecast,
    WeatherForecast,
)
from .cercalia_client import CercaliaClient


class PoiService(CercaliaClient):
    """
    Points of Interest search using Cercalia API.

    Supports multiple search modes:
    - Nearest POIs by straight-line distance (cmd=prox)
    - Nearest POIs with routing (cmd=prox with weight)
    - POIs along a route (cmd=geom)
    - POIs inside a map extent (cmd=map)
    - POIs inside a polygon (cmd=prox with wkt)
    - Weather forecast (cmd=prox with D00M05 category)

    Example:
        >>> service = PoiService(config)
        >>>
        >>> # Search nearest gas stations
        >>> pois = service.search_nearest(
        ...     Coordinate(lat=40.3691, lng=-3.589),
        ...     PoiNearestOptions(categories=["C001"], limit=5, radius=10000)
        ... )
        >>>
        >>> # Search with routing
        >>> pois = service.search_nearest_with_routing(
        ...     Coordinate(lat=40.3691, lng=-3.589),
        ...     PoiNearestWithRoutingOptions(
        ...         categories=["C001"],
        ...         weight="time",
        ...         limit=5
        ...     )
        ... )
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the POI service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def search_nearest(self, center: Coordinate, options: PoiNearestOptions) -> list[Poi]:
        """
        Get the nearest POIs by straight-line distance.

        Args:
            center: Search center coordinate
            options: Search options (categories, limit, radius)

        Returns:
            List of POI results ordered by proximity

        Example:
            >>> pois = service.search_nearest(
            ...     Coordinate(lat=40.3691, lng=-3.589),
            ...     PoiNearestOptions(categories=["C001"], limit=2, radius=10000)
            ... )
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
            "mo": f"{center.lat},{center.lng}",
            "rqpoicats": ",".join(options.categories),
        }

        if options.limit is not None:
            params["num"] = str(options.limit)
        if options.radius is not None:
            params["rad"] = str(options.radius)

        try:
            data = self._request(params, "POI Nearest")
            return self._parse_poi_response(data)
        except Exception as e:
            # Error 30006 means no results found
            if self._is_no_results_error(e):
                return []
            raise

    def search_nearest_with_routing(
        self, center: Coordinate, options: PoiNearestWithRoutingOptions
    ) -> list[Poi]:
        """
        Get the nearest POIs using routing distance/time.

        Args:
            center: Search center coordinate
            options: Search options including routing weight

        Returns:
            List of POI results with routing info

        Example:
            >>> pois = service.search_nearest_with_routing(
            ...     Coordinate(lat=40.3691, lng=-3.589),
            ...     PoiNearestWithRoutingOptions(
            ...         categories=["C001"],
            ...         weight="time",
            ...         limit=2
            ...     )
            ... )
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
            "mo": f"{center.lat},{center.lng}",
            "rqpoicats": ",".join(options.categories),
            "weight": options.weight,
        }

        if options.limit is not None:
            params["num"] = str(options.limit)
        if options.radius is not None:
            params["rad"] = str(options.radius)
        if options.inverse is not None:
            params["inverse"] = str(options.inverse)
        if options.include_realtime:
            params["iweight"] = "realtime"
        if options.departure_time:
            params["departuretime"] = options.departure_time

        try:
            data = self._request(params, "POI Nearest With Routing")
            return self._parse_poi_response(data)
        except Exception as e:
            if self._is_no_results_error(e):
                return []
            raise

    def search_along_route(self, options: PoiAlongRouteOptions) -> list[Poi]:
        """
        Get POIs along a route.

        Args:
            options: Route and search options

        Returns:
            List of POIs along the route

        Example:
            >>> pois = service.search_along_route(
            ...     PoiAlongRouteOptions(
            ...         route_id="2767920,2778988|0.6167333,0.6414299",
            ...         route_weight="time",
            ...         categories=["C001"],
            ...         buffer=50
            ...     )
            ... )
        """
        params: dict[str, str] = {
            "cmd": "geom",
            "routeid": options.route_id,
            "routeweight": options.route_weight,
            "getpoicats": ",".join(options.categories),
        }

        if options.buffer is not None:
            params["buffer"] = str(options.buffer)
        if options.tolerance is not None:
            params["tolerance"] = str(options.tolerance)

        try:
            data = self._request(params, "POI Along Route")
            return self._parse_geom_poi_response(data)
        except Exception as e:
            if self._is_no_results_error(e):
                return []
            raise

    def search_in_extent(self, extent: MapExtent, options: PoiInExtentOptions) -> list[Poi]:
        """
        Get POIs inside a map extent.

        Args:
            extent: Map extent (upper-left and lower-right corners)
            options: Search options

        Returns:
            List of POIs in the extent

        Example:
            >>> pois = service.search_in_extent(
            ...     MapExtent(
            ...         upper_left=Coordinate(lat=42.14, lng=-0.41),
            ...         lower_right=Coordinate(lat=42.13, lng=-0.40)
            ...     ),
            ...     PoiInExtentOptions(categories=["D00GAS"])
            ... )
        """
        extent_str = (
            f"{extent.upper_left.lat},{extent.upper_left.lng}|"
            f"{extent.lower_right.lat},{extent.lower_right.lng}"
        )

        params: dict[str, str] = {
            "cmd": "map",
            "map": "1" if options.include_map else "0",
            "extent": extent_str,
            "cs": "gdd",
            "mocs": "gdd",
        }

        # Use gpoicats for zoom filtering, getpoicats for no filtering
        if options.grid_size is not None:
            params["gpoicats"] = ",".join(options.categories)
            params["gridsize"] = str(options.grid_size)
        else:
            params["getpoicats"] = ",".join(options.categories)

        try:
            data = self._request(params, "POI In Extent")
            return self._parse_map_poi_response(data, options.grid_size is not None)
        except Exception as e:
            if self._is_no_results_error(e):
                return []
            raise

    def search_in_polygon(self, options: PoiInPolygonOptions) -> list[Poi]:
        """
        Get POIs inside a polygon.

        Args:
            options: Polygon and category options

        Returns:
            List of POIs inside the polygon

        Example:
            >>> pois = service.search_in_polygon(
            ...     PoiInPolygonOptions(
            ...         categories=["C001"],
            ...         wkt="POLYGON((2.14 41.39, 2.14 41.40, 2.17 41.40, 2.17 41.39, 2.14 41.39))"
            ...     )
            ... )
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "cs": "4326",
            "rqpoicats": ",".join(options.categories),
            "wkt": options.wkt,
        }

        try:
            data = self._request(params, "POI In Polygon")
            return self._parse_poi_response(data)
        except Exception as e:
            if self._is_no_results_error(e):
                return []
            raise

    def get_weather_forecast(self, center: Coordinate) -> Optional[WeatherForecast]:
        """
        Get weather forecast for a location.

        Args:
            center: Location coordinate

        Returns:
            Weather forecast data, or None if not available

        Example:
            >>> forecast = service.get_weather_forecast(
            ...     Coordinate(lat=41.39818, lng=2.1490287)
            ... )
            >>> if forecast:
            ...     for day in forecast.forecasts:
            ...         print(f"{day.date}: {day.temperature_max}°C")
        """
        params: dict[str, str] = {
            "cmd": "prox",
            "mocs": "gdd",
            "mo": f"{center.lat},{center.lng}",
            "rqpoicats": "D00M05",
        }

        try:
            data = self._request(params, "Weather Forecast")
            return self._parse_weather_response(data)
        except Exception as e:
            if self._is_no_results_error(e):
                return None
            raise

    def _is_no_results_error(self, error: Exception) -> bool:
        """Check if error is a 'no results found' error (code 30006)."""
        if hasattr(error, "code") and error.code == "30006":  # type: ignore
            return True
        error_str = str(error)
        return "30006" in error_str

    def _parse_poi_response(self, data: dict[str, Any]) -> list[Poi]:
        """Parse standard proximity POI response."""
        cercalia = data.get("cercalia", data)

        # Check for error
        if cercalia.get("error"):
            error = cercalia["error"]
            error_id = get_cercalia_attr(error, "id")
            if error_id == "30006":
                return []
            error_msg = get_cercalia_value(error) or str(error)
            raise ValueError(f"Cercalia error: {error_msg}")

        proximity = cercalia.get("proximity")
        if not proximity or not proximity.get("poilist"):
            return []

        poi_list = proximity["poilist"]
        pois = get_cercalia_attr(poi_list, "poi") or poi_list.get("poi")

        if not pois:
            return []

        poi_array = pois if isinstance(pois, list) else [pois]
        return [self._parse_poi(poi) for poi in poi_array]

    def _parse_geom_poi_response(self, data: dict[str, Any]) -> list[Poi]:
        """Parse geometry (route) POI response."""
        cercalia = data.get("cercalia", data)

        if cercalia.get("error"):
            error = cercalia["error"]
            error_id = get_cercalia_attr(error, "id")
            if error_id == "30006":
                return []
            error_msg = get_cercalia_value(error) or str(error)
            raise ValueError(f"Cercalia error: {error_msg}")

        getpoicats = cercalia.get("getpoicats")
        if not getpoicats or not getpoicats.get("poilist"):
            return []

        poi_list = getpoicats["poilist"]
        pois = get_cercalia_attr(poi_list, "poi") or poi_list.get("poi")

        if not pois:
            return []

        poi_array = pois if isinstance(pois, list) else [pois]
        return [self._parse_poi(poi) for poi in poi_array]

    def _parse_map_poi_response(self, data: dict[str, Any], use_grid_filter: bool) -> list[Poi]:
        """Parse map extent POI response."""
        cercalia = data.get("cercalia", data)

        if cercalia.get("error"):
            error = cercalia["error"]
            error_id = get_cercalia_attr(error, "id")
            if error_id == "30006":
                return []
            error_msg = get_cercalia_value(error) or str(error)
            raise ValueError(f"Cercalia error: {error_msg}")

        map_data = cercalia.get("map")
        if not map_data:
            return []

        # Check for gpoicats (with grid filtering) or getpoicats (without)
        poicats_container = (
            map_data.get("gpoicats") if use_grid_filter else map_data.get("getpoicats")
        )
        if not poicats_container or not poicats_container.get("poilist"):
            return []

        poi_list = poicats_container["poilist"]
        pois = get_cercalia_attr(poi_list, "poi") or poi_list.get("poi")

        if not pois:
            return []

        poi_array = pois if isinstance(pois, list) else [pois]
        return [self._parse_poi(poi) for poi in poi_array]

    def _parse_poi(self, poi: dict[str, Any]) -> Poi:
        """Parse a single POI from API response."""
        # Validate coordinates exist (Golden Rule #3: Strict Coordinates)
        coord = poi.get("coord", {})
        coord_x = get_cercalia_attr(coord, "x")
        coord_y = get_cercalia_attr(coord, "y")

        if not coord_x or not coord_y:
            raise ValueError("POI coordinates are missing")

        coordinate = Coordinate(lat=float(coord_y), lng=float(coord_x))

        # Parse geographic element
        ge_data = poi.get("ge")
        ge = self._parse_geographic_element(ge_data) if ge_data else None

        result = Poi(
            id=get_cercalia_attr(poi, "id") or "",
            name=get_cercalia_value(poi.get("name")) or "",
            category_code=get_cercalia_attr(poi, "category_id") or "",
            coord=coordinate,
        )

        # Optional fields
        info = get_cercalia_value(poi.get("info"))
        if info:
            result.info = info

        sub_code = get_cercalia_attr(poi, "subcategory_id")
        if sub_code and sub_code != "-1":
            result.subcategory_code = sub_code

        geometry = get_cercalia_attr(poi, "geometry")
        if geometry:
            result.geometry = geometry

        dist = get_cercalia_attr(poi, "dist")
        if dist is not None and dist != "":
            result.distance = int(dist)

        pos = get_cercalia_attr(poi, "pos")
        if pos is not None and pos != "":
            result.position = int(pos)

        routedist = get_cercalia_attr(poi, "routedist")
        if routedist:
            result.route_distance = int(routedist)

        routetime = get_cercalia_attr(poi, "routetime")
        if routetime:
            result.route_time = int(routetime)

        routerealtime = get_cercalia_attr(poi, "routerealtime")
        if routerealtime:
            result.route_realtime = int(routerealtime)

        routeweight = get_cercalia_attr(poi, "routeweight")
        if routeweight:
            result.route_weight = int(routeweight)

        if ge:
            result.ge = ge

        pixels = poi.get("pixels")
        if pixels:
            result.pixels = PoiPixels(
                x=int(get_cercalia_attr(pixels, "x") or "0"),
                y=int(get_cercalia_attr(pixels, "y") or "0"),
            )

        return result

    def _parse_geographic_element(self, ge: dict[str, Any]) -> PoiGeographicElement:
        """Parse geographic element from POI."""
        result = PoiGeographicElement()

        if ge.get("housenumber"):
            result.house_number = get_cercalia_value(ge["housenumber"])

        if ge.get("street"):
            result.street = get_cercalia_value(ge["street"]) or get_cercalia_attr(
                ge["street"], "name"
            )
            result.street_code = get_cercalia_attr(ge["street"], "id")

        # Map city -> locality (Golden Rule #4: locality instead of city)
        if ge.get("city"):
            result.locality = get_cercalia_value(ge["city"])
            result.locality_code = get_cercalia_attr(ge["city"], "id")

        if ge.get("municipality"):
            result.municipality = get_cercalia_value(ge["municipality"])
            result.municipality_code = get_cercalia_attr(ge["municipality"], "id")

        if ge.get("subregion"):
            result.subregion = get_cercalia_value(ge["subregion"])
            result.subregion_code = get_cercalia_attr(ge["subregion"], "id")

        if ge.get("region"):
            result.region = get_cercalia_value(ge["region"])
            result.region_code = get_cercalia_attr(ge["region"], "id")

        if ge.get("country"):
            result.country = get_cercalia_value(ge["country"])
            result.country_code = get_cercalia_attr(ge["country"], "id")

        return result

    def _parse_weather_response(self, data: dict[str, Any]) -> Optional[WeatherForecast]:
        """Parse weather forecast response."""
        cercalia = data.get("cercalia", data)

        if cercalia.get("error"):
            error = cercalia["error"]
            error_id = get_cercalia_attr(error, "id")
            if error_id == "30006":
                return None
            error_msg = get_cercalia_value(error) or str(error)
            raise ValueError(f"Cercalia error: {error_msg}")

        proximity = cercalia.get("proximity")
        if not proximity or not proximity.get("poilist"):
            return None

        pois = proximity["poilist"].get("poi")
        if not pois:
            return None

        poi = pois[0] if isinstance(pois, list) else pois

        # Validate coordinates exist (Golden Rule #3: Strict Coordinates)
        coord = poi.get("coord", {})
        coord_x = get_cercalia_attr(coord, "x")
        coord_y = get_cercalia_attr(coord, "y")

        if not coord_x or not coord_y:
            raise ValueError("Weather POI coordinates are missing")

        coordinate = Coordinate(lat=float(coord_y), lng=float(coord_x))

        # Parse the info field which contains weather data
        info_str = get_cercalia_value(poi.get("info")) or ""
        forecasts = self._parse_weather_info(info_str)

        return WeatherForecast(
            location_name=get_cercalia_value(poi.get("name")) or "",
            coord=coordinate,
            last_update=forecasts["last_update"],
            forecasts=forecasts["days"],
        )

    def _parse_weather_info(
        self, info: str
    ) -> dict[str, Optional[Union[str, list[WeatherDayForecast]]]]:
        """Parse weather info string into structured forecast data."""
        if not info:
            return {"last_update": None, "days": []}

        parts = info.split("|")
        if len(parts) < 2:
            return {"last_update": None, "days": []}

        last_update = parts[0]
        days: list[WeatherDayForecast] = []

        i = 1
        day_num = 1

        while i < len(parts) and day_num <= 6:
            date = parts[i]
            if not date or "-" not in date:
                i += 1
                continue

            forecast = WeatherDayForecast(date=date)

            if day_num <= 2:
                # Full format with 00-12 and 12-24 splits
                if i + 10 <= len(parts):
                    forecast.precipitation_chance_00_12 = self._parse_optional_int(parts[i + 1])
                    forecast.precipitation_chance_12_24 = self._parse_optional_int(parts[i + 2])
                    forecast.snow_level_00_12 = self._parse_optional_int(parts[i + 3])
                    forecast.snow_level_12_24 = self._parse_optional_int(parts[i + 4])
                    forecast.sky_conditions_00_12 = self._parse_optional_int(parts[i + 5])
                    forecast.sky_conditions_12_24 = self._parse_optional_int(parts[i + 6])
                    forecast.wind_speed_00_12 = self._parse_optional_int(parts[i + 7])
                    forecast.wind_speed_12_24 = self._parse_optional_int(parts[i + 8])
                    forecast.temperature_max = self._parse_optional_int(parts[i + 9])
                    forecast.temperature_min = self._parse_optional_int(parts[i + 10])
                    i += 11
                else:
                    break
            elif day_num == 3:
                # Day 3 has no wind
                if i + 8 <= len(parts):
                    forecast.precipitation_chance_00_12 = self._parse_optional_int(parts[i + 1])
                    forecast.precipitation_chance_12_24 = self._parse_optional_int(parts[i + 2])
                    forecast.snow_level_00_12 = self._parse_optional_int(parts[i + 3])
                    forecast.snow_level_12_24 = self._parse_optional_int(parts[i + 4])
                    forecast.sky_conditions_00_12 = self._parse_optional_int(parts[i + 5])
                    forecast.sky_conditions_12_24 = self._parse_optional_int(parts[i + 6])
                    forecast.temperature_max = self._parse_optional_int(parts[i + 7])
                    forecast.temperature_min = self._parse_optional_int(parts[i + 8])
                    i += 9
                else:
                    break
            else:
                # Days 4-6 simplified format
                if i + 5 <= len(parts):
                    forecast.precipitation_chance_00_12 = self._parse_optional_int(parts[i + 1])
                    forecast.snow_level_00_12 = self._parse_optional_int(parts[i + 2])
                    forecast.sky_conditions_00_12 = self._parse_optional_int(parts[i + 3])
                    forecast.temperature_max = self._parse_optional_int(parts[i + 4])
                    forecast.temperature_min = self._parse_optional_int(parts[i + 5])
                    i += 6
                else:
                    break

            days.append(forecast)
            day_num += 1

        return {"last_update": last_update, "days": days}

    def _parse_optional_int(self, value: Optional[str]) -> Optional[int]:
        """Parse an optional integer, returning None for empty strings."""
        if not value or value.strip() == "":
            return None
        try:
            return int(float(value))
        except ValueError:
            return None
