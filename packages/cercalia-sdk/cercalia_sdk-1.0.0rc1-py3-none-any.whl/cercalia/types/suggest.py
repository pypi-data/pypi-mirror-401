"""
Suggest types for Cercalia SDK.

This module contains types for address and POI autocomplete operations,
providing real-time suggestions as users type addresses or location names.

Example:
    >>> from cercalia.types.suggest import SuggestOptions, SuggestResult
    >>> options = SuggestOptions(
    ...     text="Gran Via",
    ...     country_code="ESP",
    ...     geo_type="st"
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate

# Type aliases for suggest
SuggestGeoType = Literal["st", "ct", "poi", "all"]
"""
Suggestion type filter:
- st: Streets only
- ct: Cities/localities only
- poi: Points of interest only
- all: All types
"""


class StreetInfo(BaseModel):
    """
    Street information from suggest result.

    Contains detailed street data including code, name, and type.

    Attributes:
        code: Unique street identifier (calle_id).
        name: Street name (calle_nombre).
        description: Full street description with type prefix.
        type: Street type (Carrer, Paseo, Avenida, Calle, etc.).
        article: Street article (de, de la, del, etc.).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="Street ID (calle_id)")
    name: Optional[str] = Field(None, description="Street name (calle_nombre)")
    description: Optional[str] = Field(None, description="Full street description (calle_descripcion)")
    type: Optional[str] = Field(None, description="Street type (Carrer, Paseo, Avenida, etc.)")
    article: Optional[str] = Field(None, description="Street article (de, de la, etc.)")


class CityInfo(BaseModel):
    """
    City/locality information from suggest result.

    Attributes:
        code: Unique city identifier (localidad_id).
        name: City name (localidad_nombre).
        bracket_locality: District or neighborhood name within the city.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="City ID (localidad_id)")
    name: Optional[str] = Field(None, description="City name (localidad_nombre)")
    bracket_locality: Optional[str] = Field(None, description="District name (distrito_nombre)")


class MunicipalityInfo(BaseModel):
    """
    Municipality information from suggest result.

    Attributes:
        code: Municipality identifier (municipio_id).
        name: Municipality name (municipio_nombre).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="Municipality ID (municipio_id)")
    name: Optional[str] = Field(None, description="Municipality name (municipio_nombre)")


class SubregionInfo(BaseModel):
    """
    Subregion/province information from suggest result.

    Attributes:
        code: Province identifier (provincia_id).
        name: Province name (provincia_nombre).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="Province ID (provincia_id)")
    name: Optional[str] = Field(None, description="Province name (provincia_nombre)")


class RegionInfo(BaseModel):
    """
    Region information from suggest result.

    Attributes:
        code: Region identifier (comunidad_id).
        name: Region name (comunidad_nombre).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="Region ID (comunidad_id)")
    name: Optional[str] = Field(None, description="Region name (comunidad_nombre)")


class CountryInfo(BaseModel):
    """
    Country information from suggest result.

    Attributes:
        code: Country code (pais_id), typically ISO 3166-1 alpha-3.
        name: Country name (pais_nombre).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="Country code (pais_id)")
    name: Optional[str] = Field(None, description="Country name (pais_nombre)")


class HouseNumberInfo(BaseModel):
    """
    House number information for street suggestions.

    Provides range and availability information for house numbers
    on a suggested street, useful for building address completion UIs.

    Attributes:
        available: Whether house numbers are available for this street.
        min: Minimum house number on this street.
        max: Maximum house number on this street.
        current: User-entered house number (portal).
        adjusted: Adjusted/validated house number (portal_disponible).
        is_english_format: Whether to use English numbering format.
        hint: Hint text showing the valid house number range.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    available: bool = Field(..., description="Whether house numbers are available")
    min: Optional[int] = Field(None, description="Minimum house number (portal_min)")
    max: Optional[int] = Field(None, description="Maximum house number (portal_max)")
    current: Optional[int] = Field(None, description="User-entered house number (portal)")
    adjusted: Optional[int] = Field(None, description="Adjusted house number (portal_disponible)")
    is_english_format: Optional[bool] = Field(None, description="English format flag (portal_en)")
    hint: Optional[str] = Field(None, description="Hint text for house number range")


class PoiInfo(BaseModel):
    """
    POI-specific information from suggest result.

    Contains POI identification and categorization data.

    Attributes:
        code: Unique POI identifier.
        name: POI name or business name.
        category_code: POI category code (e.g., 'C014' for restaurants).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    code: Optional[str] = Field(None, description="POI ID")
    name: Optional[str] = Field(None, description="POI name")
    category_code: Optional[str] = Field(None, description="POI category code")


class SuggestResult(BaseModel):
    """
    Normalized suggestion result from Cercalia Suggest API.

    Represents a single autocomplete suggestion with full administrative
    hierarchy and optional coordinate information.

    Following Golden Rules:
        - Uses *_code suffix for all identifiers (not *_id)
        - Direct 1:1 mapping from API fields
        - No fallbacks between administrative levels

    Attributes:
        id: Unique identifier for this suggestion.
        display_text: Human-readable text built from address components.
        type: Type of suggestion (street, city, poi, address).
        street: Street information (if type is street or address).
        city: City/locality information.
        postal_code: Postal code.
        municipality: Municipality information.
        subregion: Subregion/province information.
        region: Region information.
        country: Country information.
        coord: Geographic coordinates (when available).
        house_numbers: House number range for streets.
        poi: POI-specific data (if type is poi).
        is_official: Whether this is an official name.
        score: Relevance score from the search.

    Example:
        >>> for suggestion in results:
        ...     print(f"{suggestion.display_text} ({suggestion.type})")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique identifier for this suggestion")
    display_text: str = Field(
        ..., description="Human-readable display text built from address components"
    )
    type: Literal["street", "city", "poi", "address"] = Field(..., description="Type of suggestion")

    # Street information
    street: Optional[StreetInfo] = Field(None, description="Street information")

    # City/locality information
    city: Optional[CityInfo] = Field(None, description="City/locality information")

    # Postal code
    postal_code: Optional[str] = Field(None, description="Postal code (codigo_postal)")

    # Municipality information
    municipality: Optional[MunicipalityInfo] = Field(None, description="Municipality information")

    # Subregion/province information
    subregion: Optional[SubregionInfo] = Field(None, description="Subregion/province information")

    # Region information
    region: Optional[RegionInfo] = Field(None, description="Region information")

    # Country information
    country: Optional[CountryInfo] = Field(None, description="Country information")

    # Coordinates
    coord: Optional[Coordinate] = Field(
        None, description="Coordinates (from coord field, format: 'lat,lng')"
    )

    # House numbers
    house_numbers: Optional[HouseNumberInfo] = Field(
        None, description="House number information for streets"
    )

    # POI specific data
    poi: Optional[PoiInfo] = Field(None, description="POI-specific data")

    # Metadata
    is_official: Optional[bool] = Field(
        None, description="Whether this is an official name (from 'oficial' field)"
    )
    score: Optional[float] = Field(
        None, description="Relevance score from search (from 'score' field)"
    )


class SuggestOptions(BaseModel):
    """
    Options for suggest search.

    Configures the autocomplete search including text query,
    geographic filters, and result customization.

    Attributes:
        text: Search text to autocomplete.
        geo_type: Filter by geographic type (streets, cities, POIs, or all).
        country_code: Filter by country code.
        region_code: Filter by region code.
        subregion_code: Filter by subregion/province code.
        municipality_code: Filter by municipality code.
        street_code: Filter by street code (for address completion).
        postal_code_prefix: Filter by postal code prefix.
        language: Language code for results.
        center: Center point for proximity-based sorting.
        radius: Search radius in meters (requires center).
        poi_categories: List of POI category codes to include.

    Example:
        >>> options = SuggestOptions(
        ...     text="Gran Via",
        ...     country_code="ESP",
        ...     geo_type="st"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    text: str = Field(..., description="Search text")
    geo_type: Optional[SuggestGeoType] = Field(
        None, description="Filter by geo type (st, ct, poi, all)"
    )
    country_code: Optional[str] = Field(None, description="Country code filter")
    region_code: Optional[str] = Field(None, description="Region code filter")
    subregion_code: Optional[str] = Field(None, description="Subregion code filter")
    municipality_code: Optional[str] = Field(None, description="Municipality code filter")
    street_code: Optional[str] = Field(None, description="Street code filter")
    postal_code_prefix: Optional[str] = Field(None, description="Postal code prefix filter")
    language: Optional[str] = Field(None, description="Language code for results")
    center: Optional[Coordinate] = Field(None, description="Center point for proximity search")
    radius: Optional[float] = Field(None, description="Search radius in meters")
    poi_categories: Optional[list[str]] = Field(None, description="POI category codes filter")


class SuggestGeocodeOptions(BaseModel):
    """
    Options for suggest geocode.

    Used to geocode a selected suggestion into exact coordinates.

    Attributes:
        city_code: City code from the suggestion.
        postal_code: Postal code.
        street_code: Street code from the suggestion.
        street_number: House/street number to geocode.
        country_code: Country code for validation.

    Example:
        >>> options = SuggestGeocodeOptions(
        ...     city_code="08019",
        ...     street_code="12345",
        ...     street_number="10",
        ...     country_code="ESP"
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    city_code: Optional[str] = Field(None, description="City code (from suggestion)")
    postal_code: Optional[str] = Field(None, description="Postal code")
    street_code: Optional[str] = Field(None, description="Street code (from suggestion)")
    street_number: Optional[str] = Field(None, description="House/street number")
    country_code: Optional[str] = Field(None, description="Country code")


class SuggestGeocodeResult(BaseModel):
    """
    Geocoded result from Cercalia Suggest Geocode API.

    Contains the exact coordinates and address details for a
    geocoded suggestion.

    Following Golden Rules:
        - Uses *_code suffix for all identifiers
        - Every administrative name has its corresponding code
        - Coordinates are required (strict)

    Attributes:
        coord: Exact coordinates of the geocoded address.
        formatted_address: Full formatted address string.
        name: Short name of the location.
        street_code: Street identifier.
        street_name: Street name.
        house_number: Geocoded house number.
        postal_code: Postal code.
        city_code: City/locality code.
        city_name: City/locality name.
        municipality_code: Municipality code.
        municipality_name: Municipality name.
        subregion_code: Subregion/province code.
        subregion_name: Subregion/province name.
        region_code: Region/community code.
        region_name: Region/community name.
        country_code: Country code.
        country_name: Country name.

    Example:
        >>> result = service.geocode_suggestion(options)
        >>> print(f"{result.formatted_address}")
        >>> print(f"Coordinates: {result.coord.lat}, {result.coord.lng}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    coord: Coordinate = Field(..., description="Exact coordinates of the geocoded address")
    formatted_address: str = Field(..., description="Full formatted address (from 'desc' field)")
    name: Optional[str] = Field(None, description="Short name (from 'name' field)")

    # Street
    street_code: Optional[str] = Field(None, description="Street code")
    street_name: Optional[str] = Field(None, description="Street name")

    # Address details
    house_number: Optional[str] = Field(None, description="House number that was geocoded")
    postal_code: Optional[str] = Field(None, description="Postal code")

    # City/locality
    city_code: Optional[str] = Field(None, description="City/locality code")
    city_name: Optional[str] = Field(None, description="City/locality name")

    # Municipality
    municipality_code: Optional[str] = Field(None, description="Municipality code")
    municipality_name: Optional[str] = Field(None, description="Municipality name")

    # Subregion
    subregion_code: Optional[str] = Field(None, description="Subregion/province code")
    subregion_name: Optional[str] = Field(None, description="Subregion/province name")

    # Region
    region_code: Optional[str] = Field(None, description="Region/community code")
    region_name: Optional[str] = Field(None, description="Region/community name")

    # Country
    country_code: Optional[str] = Field(None, description="Country code")
    country_name: Optional[str] = Field(None, description="Country name")
