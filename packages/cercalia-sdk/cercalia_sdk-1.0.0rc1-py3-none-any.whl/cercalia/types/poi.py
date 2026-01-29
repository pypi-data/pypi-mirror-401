"""
POI types for Cercalia SDK.

This module contains types for Points of Interest (POI) operations including
searching, filtering by category, and weather information retrieval.

Example:
    >>> from cercalia.types.poi import Poi, PoiNearestOptions
    >>> from cercalia.types.common import Coordinate
    >>> options = PoiNearestOptions(
    ...     categories=["C001", "C007"],  # Gas stations and parking
    ...     radius=5000,
    ...     limit=10
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate

# Type aliases for POI categories
PoiCategoryCode = str
"""
POI category codes (e.g., 'C001' for gas stations, 'C009' for hospitals).
Some common codes:
- C001: Gas station
- C007: Parking
- C009: Hospital
- C013: Hotel
- C014: Restaurant
- C024: ATM
- D00GAS: Gas station with daily prices (Spain)
- D00M05: Weather info
"""

PoiRouteWeight = Literal["time", "distance", "money", "realtime", "fast", "short"]
"""Route optimization weight for POI searches with routing."""


class PoiGeographicElement(BaseModel):
    """
    Geographic element (address) information for a POI.

    Contains the address components where the POI is located.

    Attributes:
        house_number: House or building number.
        street: Street name.
        street_code: Street identifier.
        locality: City or locality name.
        locality_code: City or locality identifier.
        municipality: Municipality name.
        municipality_code: Municipality identifier.
        subregion: Subregion or province name.
        subregion_code: Subregion or province identifier.
        region: Region name.
        region_code: Region identifier.
        country: Country name.
        country_code: Country code (ISO 3166-1 alpha-3).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    house_number: Optional[str] = Field(None, description="House/building number")
    street: Optional[str] = Field(None, description="Street name")
    street_code: Optional[str] = Field(None, description="Street ID")
    locality: Optional[str] = Field(None, description="City/locality name")
    locality_code: Optional[str] = Field(None, description="City/locality ID")
    municipality: Optional[str] = Field(None, description="Municipality name")
    municipality_code: Optional[str] = Field(
        None, description="Municipality ID (note: typo in original API)"
    )
    subregion: Optional[str] = Field(None, description="Subregion/province name")
    subregion_code: Optional[str] = Field(None, description="Subregion/province ID")
    region: Optional[str] = Field(None, description="Region name")
    region_code: Optional[str] = Field(None, description="Region ID")
    country: Optional[str] = Field(None, description="Country name")
    country_code: Optional[str] = Field(None, description="Country code")


class PoiPixels(BaseModel):
    """
    Pixel coordinates for map rendering.

    Used when POI results include map image data.

    Attributes:
        x: X pixel coordinate on the map image.
        y: Y pixel coordinate on the map image.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    x: int = Field(..., description="X pixel coordinate")
    y: int = Field(..., description="Y pixel coordinate")


class Poi(BaseModel):
    """
    Point of Interest result from Cercalia API.

    Represents a single POI with location, category, and optional
    routing information when route-based search was used.

    Following Golden Rules:
        - Coordinates are required (strict)
        - All administrative levels have their corresponding IDs
        - Direct mapping from API response

    Attributes:
        id: Unique POI identifier.
        name: POI name or business name.
        info: Additional information about the POI.
        category_code: POI category code (e.g., 'C001' for gas stations).
        subcategory_code: POI subcategory code for finer classification.
        geometry: Geometry type of the POI.
        distance: Straight-line distance from search center in meters.
        position: Result position (1-based) in the result set.
        route_distance: Route distance in meters (when routing is used).
        route_time: Route time in seconds (when routing is used).
        route_realtime: Route time with traffic (when available).
        route_weight: Route weight value used in calculation.
        coord: Geographic coordinates of the POI.
        ge: Geographic element with address information.
        pixels: Pixel coordinates for map rendering.

    Example:
        >>> for poi in results:
        ...     print(f"{poi.name} - {poi.distance}m away")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="POI unique identifier")
    name: str = Field(..., description="POI name")
    info: Optional[str] = Field(None, description="Additional POI information")
    category_code: str = Field(..., description="POI category code")
    subcategory_code: Optional[str] = Field(None, description="POI subcategory code")
    geometry: Optional[str] = Field(None, description="Geometry type")
    distance: Optional[int] = Field(
        None, description="Straight-line distance in meters from search center"
    )
    position: Optional[int] = Field(None, description="Result position (1-based)")
    route_distance: Optional[int] = Field(
        None, description="Route distance in meters (when using routing)"
    )
    route_time: Optional[int] = Field(None, description="Route time in seconds (when using routing)")
    route_realtime: Optional[int] = Field(
        None, description="Route time with real-time traffic (when available)"
    )
    route_weight: Optional[int] = Field(None, description="Route weight value")
    coord: Coordinate = Field(..., description="POI coordinates")
    ge: Optional[PoiGeographicElement] = Field(
        None, description="Geographic element (address information)"
    )
    pixels: Optional[PoiPixels] = Field(None, description="Pixel coordinates for map rendering")


class PoiNearestOptions(BaseModel):
    """
    Options for nearest POI search.

    Searches for POIs near a given coordinate using straight-line distance.

    Attributes:
        categories: List of POI category codes to search for.
        limit: Maximum number of results to return.
        radius: Search radius in meters from the center point.

    Example:
        >>> options = PoiNearestOptions(
        ...     categories=["C001", "C007"],
        ...     radius=5000,
        ...     limit=10
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    categories: list[PoiCategoryCode] = Field(..., description="POI category codes to search for")
    limit: Optional[int] = Field(None, description="Maximum number of results")
    radius: Optional[int] = Field(None, description="Search radius in meters")


class PoiNearestWithRoutingOptions(BaseModel):
    """
    Options for nearest POI search with routing.

    Searches for POIs considering actual driving/walking distance and time
    rather than straight-line distance.

    Attributes:
        categories: List of POI category codes to search for.
        weight: Route optimization criteria (time, distance, etc.).
        limit: Maximum number of results to return.
        radius: Search radius in meters.
        inverse: Route direction (0=center to POI, 1=POI to center).
        include_realtime: Include real-time traffic data in calculations.
        departure_time: Departure time for traffic-aware calculations.

    Example:
        >>> options = PoiNearestWithRoutingOptions(
        ...     categories=["C001"],
        ...     weight="time",
        ...     radius=10000,
        ...     include_realtime=True
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    categories: list[PoiCategoryCode] = Field(..., description="POI category codes to search for")
    weight: PoiRouteWeight = Field(..., description="Route optimization weight")
    limit: Optional[int] = Field(None, description="Maximum number of results")
    radius: Optional[int] = Field(None, description="Search radius in meters")
    inverse: Optional[Literal[0, 1]] = Field(
        None, description="Route direction (0=center to POI, 1=POI to center)"
    )
    include_realtime: Optional[bool] = Field(None, description="Include real-time traffic data")
    departure_time: Optional[str] = Field(None, description="Departure time for route calculation")


class PoiAlongRouteOptions(BaseModel):
    """
    Options for POI search along a route.

    Finds POIs along a previously calculated route within a buffer distance.

    Attributes:
        route_id: Route ID from a previous routing calculation.
        route_weight: Route weight used in the original calculation.
        categories: List of POI category codes to search for.
        buffer: Buffer distance from route in meters.
        tolerance: Route tolerance value for geometric matching.

    Example:
        >>> options = PoiAlongRouteOptions(
        ...     route_id="route_abc123",
        ...     route_weight="time",
        ...     categories=["C001", "C003"],  # Gas stations and service areas
        ...     buffer=500
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    route_id: str = Field(..., description="Route ID from previous routing calculation")
    route_weight: PoiRouteWeight = Field(..., description="Route weight used in calculation")
    categories: list[PoiCategoryCode] = Field(..., description="POI category codes to search for")
    buffer: Optional[int] = Field(None, description="Buffer distance from route in meters")
    tolerance: Optional[int] = Field(None, description="Route tolerance value")


class MapExtent(BaseModel):
    """
    Map extent defined by upper-left and lower-right corners.

    Represents a rectangular map view area for POI searches.

    Attributes:
        upper_left: Upper-left (northwest) corner coordinate.
        lower_right: Lower-right (southeast) corner coordinate.

    Example:
        >>> extent = MapExtent(
        ...     upper_left=Coordinate(lat=41.5, lng=2.0),
        ...     lower_right=Coordinate(lat=41.3, lng=2.3)
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    upper_left: Coordinate = Field(..., description="Upper-left corner")
    lower_right: Coordinate = Field(..., description="Lower-right corner")


class PoiInExtentOptions(BaseModel):
    """
    Options for POI search in map extent.

    Searches for POIs within a rectangular map view area.

    Attributes:
        categories: List of POI category codes to search for.
        include_map: Include map image data in response.
        grid_size: Grid size for zoom-level filtering (clustering).

    Example:
        >>> options = PoiInExtentOptions(
        ...     categories=["C007"],  # Parking
        ...     grid_size=50
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    categories: list[PoiCategoryCode] = Field(..., description="POI category codes to search for")
    include_map: Optional[bool] = Field(None, description="Include map image data")
    grid_size: Optional[int] = Field(None, description="Grid size for zoom-level filtering")


class PoiInPolygonOptions(BaseModel):
    """
    Options for POI search in polygon.

    Searches for POIs within a custom polygon geometry.

    Attributes:
        categories: List of POI category codes to search for.
        wkt: WKT (Well-Known Text) polygon geometry string.

    Example:
        >>> options = PoiInPolygonOptions(
        ...     categories=["C009"],  # Hospitals
        ...     wkt="POLYGON((2.0 41.3, 2.3 41.3, 2.3 41.5, 2.0 41.5, 2.0 41.3))"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    categories: list[PoiCategoryCode] = Field(..., description="POI category codes to search for")
    wkt: str = Field(..., description="WKT polygon geometry")


class WeatherDayForecast(BaseModel):
    """
    Weather forecast for a single day.

    Contains meteorological data for a 24-hour period split into
    00-12h and 12-24h intervals.

    Attributes:
        date: Forecast date in YYYY-MM-DD format.
        precipitation_chance_00_12: Precipitation probability 00-12h (%).
        precipitation_chance_12_24: Precipitation probability 12-24h (%).
        snow_level_00_12: Snow level altitude 00-12h (meters).
        snow_level_12_24: Snow level altitude 12-24h (meters).
        sky_conditions_00_12: Sky condition code for 00-12h.
        sky_conditions_12_24: Sky condition code for 12-24h.
        wind_speed_00_12: Wind speed 00-12h (km/h).
        wind_speed_12_24: Wind speed 12-24h (km/h).
        temperature_max: Maximum temperature in Celsius.
        temperature_min: Minimum temperature in Celsius.

    Note:
        Use SKY_CONDITIONS dict to convert sky condition codes to text.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
    )

    date: str = Field(..., description="Forecast date (YYYY-MM-DD)")
    precipitation_chance_00_12: Optional[int] = Field(
        None, description="Precipitation chance 00-12h (%)"
    )
    precipitation_chance_12_24: Optional[int] = Field(
        None, description="Precipitation chance 12-24h (%)"
    )
    snow_level_00_12: Optional[int] = Field(None, description="Snow level 00-12h (meters)")
    snow_level_12_24: Optional[int] = Field(None, description="Snow level 12-24h (meters)")
    sky_conditions_00_12: Optional[int] = Field(None, description="Sky condition code 00-12h")
    sky_conditions_12_24: Optional[int] = Field(None, description="Sky condition code 12-24h")
    wind_speed_00_12: Optional[int] = Field(None, description="Wind speed 00-12h (km/h)")
    wind_speed_12_24: Optional[int] = Field(None, description="Wind speed 12-24h (km/h)")
    temperature_max: Optional[int] = Field(None, description="Maximum temperature (C)")
    temperature_min: Optional[int] = Field(None, description="Minimum temperature (C)")


class WeatherForecast(BaseModel):
    """
    Weather forecast result for a location.

    Contains multi-day weather forecast data for a specific geographic location.

    Attributes:
        location_name: Name of the forecast location (municipality).
        coord: Geographic coordinates of the location.
        last_update: Timestamp of the last data update.
        forecasts: List of daily forecasts (typically up to 6 days).

    Example:
        >>> forecast = service.get_weather(Coordinate(lat=41.38, lng=2.17))
        >>> print(f"Weather for {forecast.location_name}:")
        >>> for day in forecast.forecasts:
        ...     print(f"  {day.date}: {day.temperature_min}-{day.temperature_max}C")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    location_name: str = Field(..., description="Location name")
    coord: Coordinate = Field(..., description="Location coordinates")
    last_update: Optional[str] = Field(None, description="Last update timestamp")
    forecasts: list[WeatherDayForecast] = Field(..., description="Daily forecasts (up to 6 days)")


# Sky condition codes mapping
SKY_CONDITIONS: dict[int, str] = {
    11: "Clear",
    12: "Slightly cloudy",
    13: "Cloudy intervals",
    14: "Cloudy",
    15: "Very cloudy",
    16: "Very cloudy",
    17: "Thin clouds",
    23: "Cloudy intervals with rain",
    24: "Cloudy with rain",
    25: "Very cloudy with rain",
    26: "Cloudy with rain",
    33: "Cloudy intervals with snow",
    34: "Cloudy with snow",
    35: "Very cloudy with snow",
    36: "Cloudy with snow",
    43: "Cloudy intervals with rain",
    44: "Cloudy with light rain",
    45: "Very cloudy with light rain",
    46: "Cloudy with light rain",
    51: "Cloudy intervals with storm",
    52: "Cloudy with storm",
    53: "Very cloudy with storm",
    54: "Cloudy with storm",
    61: "Cloudy intervals with storm and light rain",
    62: "Cloudy with storm and light rain",
    63: "Very cloudy with storm and light rain",
    64: "Cloudy with storm and light rain",
    71: "Cloudy intervals with light snow",
    72: "Cloudy with light snow",
    73: "Very cloudy with light snow",
    74: "Cloudy with light snow",
}

# POI category names mapping
POI_CATEGORY_NAMES: dict[str, str] = {
    "C001": "Gas station",
    "C002": "Parking & rest area",
    "C003": "Service area",
    "C004": "Train station",
    "C005": "Airport",
    "C006": "Ferry terminal",
    "C007": "Parking",
    "C008": "Car sales",
    "C009": "Hospital",
    "C010": "Mall",
    "C011": "Post Office",
    "C012": "Public administration",
    "C013": "Hotel",
    "C014": "Restaurant",
    "C015": "Stadium",
    "C016": "Airport access",
    "C017": "Mountain pass",
    "C018": "Embassy",
    "C019": "Border crossing",
    "C020": "Mountain peak",
    "C021": "Panoramic view",
    "C022": "Beach",
    "C023": "Camping",
    "C024": "ATM",
    "C025": "Cinema",
    "C026": "Pharmacy",
    "C027": "University / School",
    "C028": "Mechanical workshop",
    "C029": "Tourist information",
    "C030": "Museum",
    "C031": "Theater",
    "C032": "Sports Center",
    "C033": "Police station",
    "C034": "Pool",
    "C035": "Place of worship",
    "C036": "Casino",
    "C037": "Tourist attraction",
    "C038": "Ice skating rink",
    "C039": "Park and recreation area",
    "C040": "Courthouse",
    "C041": "Opera",
    "C042": "Concert hall",
    "C043": "Convention Center",
    "C044": "Leisure port",
    "C045": "Theme park",
    "C046": "Golf course",
    "C047": "Library",
    "C048": "Zoo",
    "C049": "Subway",
    "C050": "Industrial Estate",
    "C051": "Tram stop",
    "C052": "Windshield workshop",
    "C053": "Tire repair shop",
    "C054": "Motorcycle workshop",
    "C055": "Truck workshop",
    "C056": "Car dealership",
    "C057": "Motorcycle dealer",
    "C058": "Yacht dealer",
    "C059": "RV dealer",
    "C060": "Truck dealer",
    "C061": "Van dealer",
    "C062": "Coach dealer",
    "C063": "Snow vehicle dealer",
    "C064": "Transport & logistics company",
    "C065": "Healthcare company",
    "C066": "Mining & Oil & Gas company",
    "C067": "Construction company",
    "C068": "Business & offices",
    "C069": "Coastal park",
    "C070": "Ski resort",
    "C071": "Bus & taxi services",
    "C072": "Botanic park",
    "C074": "Water park",
    "C075": "Wildlife park",
    "C076": "Bed & Breakfast",
    "C077": "Hotel resort",
    "C078": "Supermarket & Hypermarket",
    "C079": "Military airport",
    "C080": "Airfield",
    "C081": "Interurban bus stop",
    "C082": "Taxi stop",
    "C083": "Coach stop",
    "C084": "Bookstore",
    "C085": "CD & DVD store",
    "C086": "Clothing & accessories",
    "C087": "Convenience store",
    "C088": "Electronics store",
    "C089": "Real estate",
    "C090": "Outlet store",
    "C091": "Florist",
    "C092": "Food store",
    "C093": "Gift shop",
    "C094": "Home & garden store",
    "C095": "Jewelry store",
    "C096": "Kiosk",
    "C097": "Optical store",
    "C098": "Sports equipment store",
    "C099": "Toy store",
    "C100": "Travel agency",
    "C101": "Building materials store",
    "C102": "Other store",
    "C103": "Mobile phone store",
    "C105": "Car rental",
    "C106": "Bank",
    "C107": "Market",
    "C108": "Truck parking",
    "C109": "Car wash",
    "C110": "Industry",
    "C111": "Car rental parking",
    "C112": "Public transport stop",
    "D00GAS": "Gas station with daily prices (Spain)",
    "D00GNC": "CNG gas station (Spain)",
    "D104": "EV charging point",
    "D00CAP": "Primary care center (Spain)",
    "D00TRA": "Tramway (Spain)",
    "D00BUS": "Urban bus stop",
    "D00GUA": "Nursery",
    "D00ESC": "School",
    "D00RAD": "Speed camera (Spain)",
    "D00PNG": "Dangerous road point (Spain)",
    "D00CAM": "Traffic camera",
    "D00M05": "Weather info",
}
