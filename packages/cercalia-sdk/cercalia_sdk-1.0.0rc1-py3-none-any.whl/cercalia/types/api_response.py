"""
Base types for Cercalia API JSON responses.

Cercalia API uses a specific JSON format where:
- Attributes are prefixed with '@' (e.g., "@id", "@version")
- Values can be in different formats: { value: string }, { $valor: string }, or plain string
- All responses are wrapped in a `cercalia` root object
"""

from typing import Any, Optional, TypedDict, Union

from pydantic import BaseModel, Field

# ============================================================================
# Raw API Response Types (TypedDict for parsing raw JSON)
# ============================================================================


class CercaliaValueDict(TypedDict, total=False):
    """Cercalia value object - values can be in multiple formats."""

    value: str
    # Note: TypedDict doesn't support @ prefix in keys, so we handle these in helper functions


class CercaliaErrorDict(TypedDict, total=False):
    """Cercalia error object from API response."""

    value: str


class CercaliaCoordDict(TypedDict, total=False):
    """Cercalia coordinate object from API response."""

    pass  # @x and @y handled via helper functions


class CercaliaAdminEntityDict(TypedDict, total=False):
    """Administrative entity (city, region, etc.) from API response."""

    value: str


class CercaliaGeographicElementDict(TypedDict, total=False):
    """Geographic element in Cercalia responses."""

    name: CercaliaValueDict
    housenumber: CercaliaValueDict
    postalcode: CercaliaAdminEntityDict
    city: CercaliaAdminEntityDict
    district: CercaliaAdminEntityDict
    municipality: CercaliaAdminEntityDict
    subregion: CercaliaAdminEntityDict
    region: CercaliaAdminEntityDict
    country: CercaliaAdminEntityDict
    coord: CercaliaCoordDict


class CercaliaCandidateDict(TypedDict, total=False):
    """Candidate in geocoding responses."""

    ge: CercaliaGeographicElementDict


# ============================================================================
# Pydantic Models for SDK Output
# ============================================================================


class CercaliaValue(BaseModel):
    """Cercalia value object model."""

    value: Optional[str] = None
    at_value: Optional[str] = Field(None, alias="@value")
    dollar_valor: Optional[str] = Field(None, alias="$valor")


class CercaliaCoord(BaseModel):
    """Cercalia coordinate object model."""

    x: str = Field(..., alias="@x")
    y: str = Field(..., alias="@y")

    model_config = {"populate_by_name": True}


class CercaliaAdminEntity(BaseModel):
    """Administrative entity (city, region, etc.)."""

    id: Optional[str] = Field(None, alias="@id")
    value: Optional[str] = None
    dollar_valor: Optional[str] = Field(None, alias="$valor")

    model_config = {"populate_by_name": True}


class CercaliaGeographicElement(BaseModel):
    """Geographic element in Cercalia responses."""

    type: Optional[str] = Field(None, alias="@type")
    id: Optional[str] = Field(None, alias="@id")
    name: Optional[Union[CercaliaValue, str]] = None
    housenumber: Optional[Union[CercaliaValue, str]] = None
    postalcode: Optional[CercaliaAdminEntity] = None
    city: Optional[CercaliaAdminEntity] = None
    district: Optional[CercaliaAdminEntity] = None
    municipality: Optional[CercaliaAdminEntity] = None
    subregion: Optional[CercaliaAdminEntity] = None
    region: Optional[CercaliaAdminEntity] = None
    country: Optional[CercaliaAdminEntity] = None
    coord: Optional[CercaliaCoord] = None

    model_config = {"populate_by_name": True}


# ============================================================================
# Coordinate System and Language Types
# ============================================================================

CercaliaCoordinateSystem = str
"""
Coordinate system types supported by Cercalia:
- 'EPSG:4326' - WGS84 (lat/lng)
- 'EPSG:3857' - Web Mercator
- 'gdd' - Geographic Decimal Degrees
- '4326' - Short form of EPSG:4326
- '3857' - Short form of EPSG:3857
"""

CercaliaLanguageCode = str
"""
Supported language codes for Cercalia API:
es, en, fr, de, it, pt, ca, eu, gl, nl, pl, ru, ar, zh, ja, ko
"""


# ============================================================================
# Helper functions for parsing Cercalia responses
# ============================================================================


def get_cercalia_attr(obj: Optional[Any], key: str) -> Optional[str]:
    """
    Extract attribute value from Cercalia object.

    Handles both @attr and attr formats since Cercalia API prefixes
    attributes with '@' (e.g., "@id", "@type").

    NOTE: This function only extracts SCALAR attributes (strings, numbers).
    For nested objects, use dict.get() directly.

    Args:
        obj: The object to extract from (dict or any object with dict-like access)
        key: The attribute key (without @ prefix)

    Returns:
        The attribute value as string, or None if not found or if value is a complex type

    Example:
        >>> obj = {"@id": "123", "@type": "poi"}
        >>> get_cercalia_attr(obj, "id")
        '123'
    """
    if obj is None:
        return None

    if isinstance(obj, dict):
        # Try @key format first (most common in Cercalia responses)
        value = obj.get(f"@{key}")
        if value is not None and not isinstance(value, (dict, list)):
            return str(value) if value else None

        # Fallback to key without @ (only for scalar values)
        value = obj.get(key)
        if value is not None and not isinstance(value, (dict, list)):
            return str(value) if value else None

    return None


def get_cercalia_value(obj: Optional[Any]) -> Optional[str]:
    """
    Extract value from Cercalia value object.

    Handles multiple formats since Cercalia API can return values as:
    - Plain string
    - Object with 'value' key
    - Object with '$valor' key
    - Object with '@value' key

    Args:
        obj: The value object (dict, string, or None)

    Returns:
        The extracted string value, or None if not found

    Example:
        >>> get_cercalia_value({"value": "Barcelona"})
        'Barcelona'
        >>> get_cercalia_value({"$valor": "Madrid"})
        'Madrid'
        >>> get_cercalia_value("Direct string")
        'Direct string'
    """
    if obj is None:
        return None

    if isinstance(obj, str):
        return obj

    if isinstance(obj, dict):
        # Try all possible value formats
        for key in ("$valor", "value", "@value"):
            value = obj.get(key)
            if value is not None:
                return str(value)

    return None


def ensure_cercalia_array(item: Optional[Any]) -> list[Any]:
    """
    Ensure array from Cercalia response.

    Handles both single item and array responses since Cercalia API
    may return a single object or an array depending on result count.

    Args:
        item: Single item, list of items, or None

    Returns:
        List of items (empty list if None)

    Example:
        >>> ensure_cercalia_array(None)
        []
        >>> ensure_cercalia_array({"id": "1"})
        [{'id': '1'}]
        >>> ensure_cercalia_array([{"id": "1"}, {"id": "2"}])
        [{'id': '1'}, {'id': '2'}]
    """
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]
