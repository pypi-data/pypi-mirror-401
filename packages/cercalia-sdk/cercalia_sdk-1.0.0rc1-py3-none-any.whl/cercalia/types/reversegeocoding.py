"""
Reverse geocoding types for Cercalia SDK.

This module contains types for reverse geocoding operations, which convert
geographic coordinates into human-readable addresses and location information.

Example:
    >>> from cercalia.types.reversegeocoding import ReverseGeocodingOptions
    >>> from cercalia.types.common import Coordinate
    >>> options = ReverseGeocodingOptions(
    ...     coord=Coordinate(lat=41.3851, lng=2.1734),
    ...     radius=100
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate
from .geocoding import GeocodingCandidate

# Type alias for reverse geocode level
ReverseGeocodeLevel = Literal[
    "cadr",  # Address (streets/roads with name, no road number)
    "adr",  # Address/road (including road number) and milestone
    "st",  # Street (no house number)/road (no milestone)
    "ct",  # City/locality
    "pcode",  # Postal code
    "mun",  # Municipality
    "subreg",  # Sub-Region (province)
    "reg",  # Region
    "ctry",  # Country
    "timezone",  # Time zone info
]
"""
Level of detail for reverse geocoding requests.

Determines what geographic level to snap the coordinate to:
    - cadr: Address (streets/roads with name, no road number)
    - adr: Address/road (including road number) and milestone
    - st: Street (no house number)/road (no milestone)
    - ct: City/locality
    - pcode: Postal code
    - mun: Municipality
    - subreg: Sub-Region (province)
    - reg: Region
    - ctry: Country
    - timezone: Time zone info
"""


class ReverseGeocodingOptions(BaseModel):
    """
    Basic reverse geocoding options for simple use cases.

    Attributes:
        coord: Geographic coordinate to reverse geocode.
        radius: Search radius in meters around the coordinate.
        language: Language code for localized results (e.g., 'es', 'en').

    Example:
        >>> options = ReverseGeocodingOptions(
        ...     coord=Coordinate(lat=41.3851, lng=2.1734),
        ...     radius=100,
        ...     language="es"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Coordinate to reverse geocode")
    radius: Optional[int] = Field(None, description="Search radius in meters")
    language: Optional[str] = Field(None, description="Language code for results")


class ReverseGeocodeOptions(BaseModel):
    """
    Extended reverse geocoding options with all API parameters.

    Provides advanced options for controlling the reverse geocoding
    behavior including precision level and special data categories.

    Attributes:
        level: Precision level for the result (address, street, city, etc.).
        date_time: ISO 8601 datetime for timezone calculations.
        category: Special category for Spain-specific data (censal, sigpac).

    Example:
        >>> options = ReverseGeocodeOptions(
        ...     level="adr",
        ...     date_time="2024-01-15T12:00:00Z"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    level: Optional[ReverseGeocodeLevel] = Field(None, description="Level of detail for the result")
    date_time: Optional[str] = Field(
        None, description="DateTime for timezone lookup (ISO 8601 format)"
    )
    category: Optional[Literal["d00seccen", "d00sigpac"]] = Field(
        None, description="Special categories (censal section, sigpac - Spain only)"
    )


class TimezoneInfo(BaseModel):
    """
    Timezone information returned when level='timezone'.

    Contains detailed timezone data including local time, UTC offset,
    and daylight saving time information.

    Attributes:
        id: IANA timezone identifier (e.g., 'Europe/Madrid').
        name: Human-readable timezone name.
        local_date_time: Local date/time at the coordinate.
        utc_date_time: Corresponding UTC date/time.
        utc_offset: UTC offset in seconds.
        daylight_saving_time: DST offset in seconds (0 if not in DST).

    Example:
        >>> if result.timezone:
        ...     print(f"Timezone: {result.timezone.id}")
        ...     print(f"Local time: {result.timezone.local_date_time}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Timezone ID (e.g., 'Europe/Madrid')")
    name: str = Field(..., description="Human-readable timezone name")
    local_date_time: str = Field(..., description="Local date/time at the coordinate")
    utc_date_time: str = Field(..., description="UTC date/time")
    utc_offset: int = Field(..., description="UTC offset in seconds")
    daylight_saving_time: int = Field(..., description="Daylight saving time offset in seconds")


class TimezoneOptions(BaseModel):
    """
    Options for timezone requests.

    Attributes:
        date_time: ISO 8601 datetime to check. If provided, returns
            local time at that specific moment (useful for DST handling).

    Example:
        >>> options = TimezoneOptions(date_time="2024-06-15T12:00:00Z")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    date_time: Optional[str] = Field(
        None,
        description="DateTime to check (ISO 8601 format). If provided, returns local time at that moment",
    )


class TimezoneResult(TimezoneInfo):
    """
    Timezone-specific result with no geographic element.

    Extends TimezoneInfo to include the input coordinate used for the query.
    This is returned when only timezone data is requested without full
    reverse geocoding.

    Attributes:
        coord: Input coordinate used for the timezone lookup.

    Example:
        >>> result = service.get_timezone(Coordinate(lat=40.4168, lng=-3.7038))
        >>> print(f"Madrid timezone: {result.id}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Input coordinate used for the query")


class SigpacInfo(BaseModel):
    """
    SIGPAC agricultural parcel information (Spain only).

    Contains data from the Spanish Agricultural Parcels Geographic
    Information System (SIGPAC).

    Attributes:
        id: Unique parcel identifier.
        municipality_code: Municipality code where the parcel is located.
        usage: Land usage code indicating the type of agricultural use.
        extension_ha: Parcel area in hectares.
        vulnerable_type: Type of vulnerable zone (if applicable).
        vulnerable_code: Code of the vulnerable zone (if applicable).

    Note:
        This data is only available for coordinates within Spain
        when using category='d00sigpac'.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Parcel ID")
    municipality_code: str = Field(..., description="Municipality ID")
    usage: str = Field(..., description="Land usage code")
    extension_ha: float = Field(..., description="Extension in hectares")
    vulnerable_type: Optional[str] = Field(None, description="Vulnerable zone type")
    vulnerable_code: Optional[str] = Field(None, description="Vulnerable zone code")


class ReverseGeocodingResult(BaseModel):
    """
    Simple reverse geocoding result for basic use cases.

    Contains the essential location information from a reverse geocoding
    query in a flat, easy-to-use structure.

    Following Golden Rules:
        - No fallback values for administrative fields
        - All name fields have corresponding code/ID fields
        - Strict coordinates (no defaults)

    Attributes:
        coord: Geographic coordinates of the result.
        formatted_address: Full formatted address string.
        street_name: Street name (if available).
        house_number: Building/house number (if available).
        postal_code: Postal or ZIP code.
        locality: City or town name.
        municipality: Municipality name.
        subregion: Subregion or province name.
        region: Region or state name.
        country: Country name.
        distance: Distance from input coordinate in meters.

    Example:
        >>> result = service.reverse_geocode(options)
        >>> print(result.formatted_address)
        >>> print(f"Distance: {result.distance}m")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Coordinate of the result")
    formatted_address: str = Field(..., description="Full formatted address string")
    street_name: Optional[str] = Field(None, description="Street name")
    street_code: Optional[str] = Field(None, description="Street code/ID")
    house_number: Optional[str] = Field(None, description="House/building number")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code")
    locality: Optional[str] = Field(None, description="City/town name")
    locality_code: Optional[str] = Field(None, description="City/town code")
    municipality: Optional[str] = Field(None, description="Municipality name")
    municipality_code: Optional[str] = Field(None, description="Municipality code")
    subregion: Optional[str] = Field(None, description="Subregion/province name")
    subregion_code: Optional[str] = Field(None, description="Subregion/province code")
    region: Optional[str] = Field(None, description="Region/state name")
    region_code: Optional[str] = Field(None, description="Region/state code")
    country: Optional[str] = Field(None, description="Country name")
    country_code: Optional[str] = Field(None, description="Country code")
    distance: Optional[float] = Field(None, description="Distance from input coordinate in meters")


class ReverseGeocodeResult(BaseModel):
    """
    Extended reverse geocoding result with all possible data.

    Provides comprehensive reverse geocoding information including
    geographic element, road-specific data, timezone, and Spain-specific
    census and agricultural parcel information.

    Attributes:
        ge: Geographic element as a GeocodingCandidate with full hierarchy.
        distance: Distance from input coordinate to the feature in meters.
        km: Road milestone (KM) if the result is on a highway/road.
        direction: Road direction (A=ascending, D=descending).
        max_speed: Speed limit on the road in km/h.
        timezone: Timezone information (when level='timezone').
        census_id: Census section ID (Spain only, category='d00seccen').
        sigpac: SIGPAC agricultural parcel info (Spain only).

    Example:
        >>> result = service.reverse_geocode_extended(coord, options)
        >>> print(f"Location: {result.ge.name}")
        >>> if result.max_speed:
        ...     print(f"Speed limit: {result.max_speed} km/h")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    ge: GeocodingCandidate = Field(
        ..., description="The geographic information as a GeocodingCandidate"
    )
    distance: Optional[float] = Field(
        None, description="Distance from input coordinate to the feature in meters"
    )
    km: Optional[str] = Field(None, description="Milestone (KM) if available (for roads)")
    direction: Optional[str] = Field(None, description="Road direction (A=ascending/D=descending)")
    max_speed: Optional[int] = Field(None, description="Maximum speed limit on the road in km/h")
    timezone: Optional[TimezoneInfo] = Field(
        None, description="Timezone information (when level='timezone')"
    )
    census_id: Optional[str] = Field(
        None, description="Census section ID (Spain only, when category='d00seccen')"
    )
    sigpac: Optional[SigpacInfo] = Field(
        None, description="SIGPAC agricultural parcel info (Spain only, when category='d00sigpac')"
    )
