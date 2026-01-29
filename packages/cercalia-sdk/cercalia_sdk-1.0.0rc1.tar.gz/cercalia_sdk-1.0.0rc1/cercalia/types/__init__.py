"""
Cercalia SDK Types.

This module exports all type definitions for the Cercalia SDK.
"""

from .api_response import (
    ensure_cercalia_array,
    get_cercalia_attr,
    get_cercalia_value,
)
from .common import (
    BoundingBox,
    CercaliaConfig,
    CercaliaError,
    Coordinate,
)
from .geocoding import (
    GeocodingCandidate,
    GeocodingOptions,
)
from .geofencing import (
    GeofenceMatch,
    GeofenceOptions,
    GeofencePoint,
    GeofenceResult,
    GeofenceShape,
)
from .geoment import (
    GeographicElementResult,
    GeomentMunicipalityOptions,
    GeomentPoiOptions,
    GeomentPostalCodeOptions,
)
from .isochrone import (
    IsochroneOptions,
    IsochroneResult,
)
from .poi import (
    Poi,
    PoiGeographicElement,
    WeatherForecast,
)
from .proximity import (
    ProximityItem,
    ProximityOptions,
    ProximityResult,
)
from .reversegeocoding import (
    ReverseGeocodingOptions,
    ReverseGeocodingResult,
)
from .routing import (
    RouteResult,
    RouteStep,
    RoutingOptions,
    RoutingWaypoint,
)
from .snaptoroad import (
    SnapToRoadOptions,
    SnapToRoadPoint,
    SnapToRoadResult,
    SnapToRoadSegment,
)
from .staticmaps import (
    RGBAColor,
    StaticMapCircle,
    StaticMapExtent,
    StaticMapLabel,
    StaticMapLine,
    StaticMapMarker,
    StaticMapOptions,
    StaticMapPolyline,
    StaticMapRectangle,
    StaticMapResult,
    StaticMapSector,
    StaticMapShape,
    StaticMapShapeBase,
)
from .suggest import (
    SuggestGeocodeResult,
    SuggestOptions,
    SuggestResult,
)

__all__ = [
    # API Response helpers
    "ensure_cercalia_array",
    "get_cercalia_attr",
    "get_cercalia_value",
    # Common types
    "BoundingBox",
    "CercaliaConfig",
    "CercaliaError",
    "Coordinate",
    # Geocoding types
    "GeocodingCandidate",
    "GeocodingOptions",
    # Geofencing types
    "GeofenceMatch",
    "GeofenceOptions",
    "GeofencePoint",
    "GeofenceResult",
    "GeofenceShape",
    # Geoment types
    "GeographicElementResult",
    "GeomentMunicipalityOptions",
    "GeomentPoiOptions",
    "GeomentPostalCodeOptions",
    # Isochrone types
    "IsochroneOptions",
    "IsochroneResult",
    # POI types
    "Poi",
    "PoiGeographicElement",
    "WeatherForecast",
    # Proximity types
    "ProximityItem",
    "ProximityOptions",
    "ProximityResult",
    # Reverse geocoding types
    "ReverseGeocodingOptions",
    "ReverseGeocodingResult",
    # Routing types
    "RoutingOptions",
    "RouteResult",
    "RouteStep",
    "RoutingWaypoint",
    # SnapToRoad types
    "SnapToRoadOptions",
    "SnapToRoadPoint",
    "SnapToRoadResult",
    "SnapToRoadSegment",
    # StaticMaps types
    "RGBAColor",
    "StaticMapCircle",
    "StaticMapExtent",
    "StaticMapLabel",
    "StaticMapLine",
    "StaticMapMarker",
    "StaticMapOptions",
    "StaticMapPolyline",
    "StaticMapRectangle",
    "StaticMapResult",
    "StaticMapSector",
    "StaticMapShape",
    "StaticMapShapeBase",
    # Suggest types
    "SuggestGeocodeResult",
    "SuggestOptions",
    "SuggestResult",
]
