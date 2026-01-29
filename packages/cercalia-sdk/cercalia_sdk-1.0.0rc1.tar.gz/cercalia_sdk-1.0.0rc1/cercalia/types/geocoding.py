"""
Geocoding types for Cercalia SDK.

This module contains types for geocoding operations including address
geocoding, road milestone lookup, and postal code search.

Example:
    >>> from cercalia.types.geocoding import GeocodingOptions, GeocodingCandidate
    >>> options = GeocodingOptions(
    ...     street="Gran Via 1",
    ...     locality="Madrid",
    ...     country_code="ESP"
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import Coordinate

# Type aliases for geocoding
GeocodingCandidateType = Literal[
    "address",
    "street",
    "poi",
    "locality",
    "municipality",
    "road",
    "milestone",
    "postal_code",
]
"""
Type of geocoding result:
- address: Full address with house number
- street: Street without house number
- poi: Point of interest
- locality: City or town
- municipality: Municipality/county
- road: Road or highway
- milestone: Road milestone (PK)
- postal_code: Postal code
"""

GeocodingLevel = Literal[
    "adr",  # Address
    "st",  # Street
    "ct",  # City/locality
    "pcode",  # Postal code
    "pc",  # Postal code (alternate format)
    "mun",  # Municipality
    "subreg",  # Sub-Region (province)
    "reg",  # Region
    "ctry",  # Country
    "rd",  # Road
    "pk",  # Milestone
    "poi",  # POI
]
"""
Geocoding precision level from Cercalia API:
- adr: Address level
- st: Street level
- ct: City/locality level
- pcode/pc: Postal code level
- mun: Municipality level
- subreg: Sub-region (province) level
- reg: Region level
- ctry: Country level
- rd: Road level
- pk: Milestone level
- poi: Point of interest level
"""


class GeocodingCandidate(BaseModel):
    """
    A geocoding result candidate.

    Represents a single match from a geocoding query with all
    administrative hierarchy information and coordinates.

    Following Golden Rules:
        - No fallback values for administrative fields
        - All name fields have corresponding ID fields
        - Strict coordinates (no defaults)
        - Geometry type transparency

    Attributes:
        id: Unique identifier for this candidate.
        name: Primary name of the location.
        label: Full descriptive label (e.g., "Gran Via 1, 28013 Madrid, Spain").
        coord: Geographic coordinates of the location.
        type: Category of the geocoding result.
        level: Original precision level from Cercalia API.

    Example:
        >>> candidate = results[0]
        >>> print(f"{candidate.name} at {candidate.coord.lat}, {candidate.coord.lng}")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique identifier for this candidate")
    name: str = Field(..., description="Primary name of the location")
    label: Optional[str] = Field(None, description="Full descriptive label")

    # Street information
    street: Optional[str] = Field(None, description="Street name")
    street_code: Optional[str] = Field(None, description="Street code/ID")
    house_number: Optional[str] = Field(None, description="House/building number")

    # Administrative hierarchy - following Golden Rules (no fallbacks!)
    locality: Optional[str] = Field(None, description="City/town name")
    locality_code: Optional[str] = Field(None, description="City/town code")
    municipality: Optional[str] = Field(None, description="Municipality name")
    municipality_code: Optional[str] = Field(None, description="Municipality code")
    district: Optional[str] = Field(None, description="District name")
    district_code: Optional[str] = Field(None, description="District code")
    subregion: Optional[str] = Field(None, description="Subregion/province name")
    subregion_code: Optional[str] = Field(None, description="Subregion/province code")
    region: Optional[str] = Field(None, description="Region/state name")
    region_code: Optional[str] = Field(None, description="Region/state code")
    country: Optional[str] = Field(None, description="Country name")
    country_code: Optional[str] = Field(None, description="Country code (ISO 3166-1 alpha-3)")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code")

    # Location
    coord: Coordinate = Field(..., description="Geographic coordinates")

    # Type information - following Golden Rule for geometry transparency
    type: GeocodingCandidateType = Field(..., description="Type of geocoding result")
    level: Optional[GeocodingLevel] = Field(None, description="Original precision level from API")


class GeocodingOptions(BaseModel):
    """
    Options for geocoding queries.

    Supports both structured search (individual fields) and
    unstructured search (free-form query).

    Attributes:
        query: Free-form address query for unstructured search.
        street: Street name with optional number.
        locality: City or town name.
        municipality: Municipality name.
        region: Region or state name.
        subregion: Subregion or province name.
        country: Country name.
        country_code: ISO 3166-1 alpha-3 country code (e.g., 'ESP').
        postal_code: Postal or ZIP code.
        house_number: Building number.
        limit: Maximum number of results to return.
        full_search: Enable broader matching mode.

    Example:
        >>> # Structured search
        >>> options = GeocodingOptions(
        ...     street="Provenca 589",
        ...     locality="Barcelona",
        ...     country_code="ESP"
        ... )
        >>> # Unstructured search
        >>> options = GeocodingOptions(query="Gran Via 1, Madrid")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    # Unstructured search
    query: Optional[str] = Field(None, description="Free-form address query")

    # Structured search fields
    country: Optional[str] = Field(None, description="Country name")
    country_code: Optional[str] = Field(
        None, description="Country code (ISO 3166-1 alpha-3, e.g., 'ESP')"
    )
    locality: Optional[str] = Field(None, description="City/town name")
    municipality: Optional[str] = Field(None, description="Municipality name")
    region: Optional[str] = Field(None, description="Region/state name")
    subregion: Optional[str] = Field(None, description="Subregion/province name")
    street: Optional[str] = Field(None, description="Street name with optional number")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code")
    house_number: Optional[str] = Field(None, description="House/building number")

    # Search options
    limit: Optional[int] = Field(None, description="Maximum number of results", ge=1)
    full_search: Optional[bool] = Field(
        None, description="Enable full search mode for broader matching"
    )


class PostalCodeCity(BaseModel):
    """
    City information associated with a postal code.

    Returned by the geocodeCitiesByPostalCode method when looking up
    cities that share a specific postal code.

    Attributes:
        id: Unique city identifier.
        name: City name.
        municipality: Municipality name.
        municipality_code: Municipality code.
        subregion: Subregion or province name.
        subregion_code: Subregion or province code.
        region: Region or state name.
        region_code: Region or state code.
        country: Country name.
        country_code: Country code.
        coord: Geographic coordinates of the city center.

    Example:
        >>> cities = service.geocode_cities_by_postal_code("08001", "ESP")
        >>> for city in cities:
        ...     print(f"{city.name} ({city.municipality})")
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="City identifier")
    name: str = Field(..., description="City name")

    # Administrative hierarchy
    municipality: Optional[str] = Field(None, description="Municipality name")
    municipality_code: Optional[str] = Field(None, description="Municipality code")
    subregion: Optional[str] = Field(None, description="Subregion/province name")
    subregion_code: Optional[str] = Field(None, description="Subregion/province code")
    region: Optional[str] = Field(None, description="Region/state name")
    region_code: Optional[str] = Field(None, description="Region/state code")
    country: Optional[str] = Field(None, description="Country name")
    country_code: Optional[str] = Field(None, description="Country code")

    # Location
    coord: Coordinate = Field(..., description="Geographic coordinates")
