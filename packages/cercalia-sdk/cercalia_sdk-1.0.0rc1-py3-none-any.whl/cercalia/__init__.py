"""
Cercalia SDK for Python.

A modern, type-safe Python SDK for interacting with Cercalia Web Services API v2.
Provides access to geocoding, routing, POI search, isochrones, and other
geospatial services.

Example:
    Basic usage with geocoding::

        >>> from cercalia import GeocodingService, CercaliaConfig, GeocodingOptions
        >>> config = CercaliaConfig(api_key="your-api-key")
        >>> service = GeocodingService(config)
        >>> results = service.geocode(GeocodingOptions(
        ...     street="Gran Via 1",
        ...     locality="Madrid",
        ...     country_code="ESP"
        ... ))
        >>> for candidate in results:
        ...     print(f"{candidate.name}: {candidate.coord}")

    Configuration from environment variables::

        >>> import os
        >>> os.environ["CERCALIA_API_KEY"] = "your-api-key"
        >>> from cercalia import get_config
        >>> config = get_config()  # Reads from environment

    Multiple services with shared config::

        >>> from cercalia import (
        ...     CercaliaConfig,
        ...     GeocodingService,
        ...     RoutingService,
        ...     PoiService
        ... )
        >>> config = CercaliaConfig(api_key="your-api-key")
        >>> geocoding = GeocodingService(config)
        >>> routing = RoutingService(config)
        >>> poi = PoiService(config)

Available Services:
    - GeocodingService: Convert addresses to coordinates
    - ReverseGeocodingService: Convert coordinates to addresses
    - RoutingService: Calculate routes between points
    - SuggestService: Autocomplete addresses and POIs
    - PoiService: Search for Points of Interest
    - IsochroneService: Calculate reachable areas
    - ProximityService: Find nearest POIs
    - GeofencingService: Point-in-polygon operations
    - GeomentService: Get administrative geometries
    - SnapToRoadService: Match GPS tracks to roads
    - StaticMapsService: Generate map images

For detailed documentation, see:
    https://docs.cercalia.com/docs/cercalia-webservices/
"""

from .config import get_config, set_config, validate_config
from .services import (
    CercaliaClient,
    GeocodingService,
    GeofencingService,
    GeomentService,
    IsochroneService,
    PoiService,
    ProximityService,
    ReverseGeocodingService,
    RoutingService,
    SnapToRoadService,
    StaticMapsService,
    SuggestService,
)
from .types import (
    # Common types
    BoundingBox,
    CercaliaConfig,
    CercaliaError,
    Coordinate,
    # Geocoding types
    GeocodingCandidate,
    GeocodingOptions,
    # Geofencing types
    GeofenceMatch,
    GeofenceOptions,
    GeofencePoint,
    GeofenceResult,
    GeofenceShape,
    # Geoment types
    GeographicElementResult,
    GeomentMunicipalityOptions,
    GeomentPoiOptions,
    GeomentPostalCodeOptions,
    # Isochrone types
    IsochroneOptions,
    IsochroneResult,
    # POI types
    Poi,
    PoiGeographicElement,
    # Proximity types
    ProximityItem,
    ProximityOptions,
    ProximityResult,
    # Reverse geocoding types
    ReverseGeocodingOptions,
    ReverseGeocodingResult,
    # StaticMaps types
    RGBAColor,
    RouteResult,
    RouteStep,
    # Routing types
    RoutingOptions,
    RoutingWaypoint,
    # SnapToRoad types
    SnapToRoadOptions,
    SnapToRoadPoint,
    SnapToRoadResult,
    SnapToRoadSegment,
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
    # Suggest types
    SuggestGeocodeResult,
    SuggestOptions,
    SuggestResult,
    WeatherForecast,
)

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Config
    "get_config",
    "set_config",
    "validate_config",
    # Services
    "CercaliaClient",
    "GeocodingService",
    "GeofencingService",
    "GeomentService",
    "IsochroneService",
    "PoiService",
    "ProximityService",
    "ReverseGeocodingService",
    "RoutingService",
    "SnapToRoadService",
    "StaticMapsService",
    "SuggestService",
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
