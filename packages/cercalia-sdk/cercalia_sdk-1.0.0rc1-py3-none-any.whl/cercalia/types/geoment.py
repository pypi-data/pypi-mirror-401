"""
Geoment types for Cercalia SDK.

This module contains types for geographic element geometry retrieval,
which allows fetching WKT geometries for municipalities, postal codes,
and other administrative divisions.

Example:
    >>> from cercalia.types.geoment import (
    ...     GeomentMunicipalityOptions,
    ...     GeographicElementResult
    ... )
    >>> options = GeomentMunicipalityOptions(
    ...     munc="08019",  # Barcelona municipality code
    ...     tolerance=100
    ... )
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

GeographicElementType = Literal["municipality", "postal_code", "poi", "region"]
"""
Type of geographic element:
- municipality: Municipal boundary
- postal_code: Postal code area
- poi: Point of Interest geometry
- region: Region/province boundary
"""


class GeomentMunicipalityOptions(BaseModel):
    """
    Options for municipality/region geometry request.

    Used to retrieve the boundary geometry of a municipality or subregion.

    Attributes:
        munc: Municipality code (e.g., '08019' for Barcelona).
        subregc: Subregion/province code.
        tolerance: Geometry simplification tolerance in meters.

    Example:
        >>> options = GeomentMunicipalityOptions(
        ...     munc="08019",
        ...     tolerance=50  # Simplify geometry
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    munc: Optional[str] = Field(None, description="Municipality code")
    subregc: Optional[str] = Field(None, description="Subregion code")
    tolerance: Optional[int] = Field(None, description="Tolerance for geometry simplification")


class GeomentPostalCodeOptions(BaseModel):
    """
    Options for postal code geometry request.

    Used to retrieve the boundary geometry of a postal code area.

    Attributes:
        pcode: Postal code (e.g., '08001').
        ctryc: Country code (e.g., 'ESP').
        tolerance: Geometry simplification tolerance in meters.

    Example:
        >>> options = GeomentPostalCodeOptions(
        ...     pcode="08001",
        ...     ctryc="ESP",
        ...     tolerance=50
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    pcode: str = Field(..., description="Postal code")
    ctryc: Optional[str] = Field(None, description="Country code")
    tolerance: Optional[int] = Field(None, description="Tolerance for geometry simplification")


class GeomentPoiOptions(BaseModel):
    """
    Options for POI geometry request.

    Used to retrieve the geometry of a specific Point of Interest.

    Attributes:
        poic: POI code/identifier.
        tolerance: Geometry simplification tolerance in meters.

    Example:
        >>> options = GeomentPoiOptions(
        ...     poic="poi_12345",
        ...     tolerance=10
        ... )
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    poic: str = Field(..., description="POI code")
    tolerance: Optional[int] = Field(None, description="Tolerance for geometry simplification")


class GeographicElementResult(BaseModel):
    """
    Result from Geoment service.

    Contains the WKT geometry and metadata for the requested
    geographic element.

    Following Golden Rules:
        - Direct mapping from API (no fallbacks)
        - Code suffix for identifiers (_code pattern)
        - level field preserved for geometry type transparency

    Attributes:
        wkt: WKT (Well-Known Text) representation of the geometry.
        code: Geographic element code (from API @id).
        name: Geographic element name (from API @name).
        type: SDK classification of the element type.
        level: Original geometry type from API for transparency.

    Example:
        >>> result = service.get_municipality_geometry(options)
        >>> print(f"Geometry for {result.name} ({result.code})")
        >>> # Use result.wkt with a GIS library
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    wkt: str = Field(..., description="WKT representation of the geometry")
    code: str = Field(..., description="Geographic element code (from @id)")
    name: Optional[str] = Field(None, description="Geographic element name (from @name)")
    type: GeographicElementType = Field(..., description="SDK type classification")
    level: Optional[str] = Field(
        None,
        description="Original geometry type from API (@type) - for transparency",
    )
