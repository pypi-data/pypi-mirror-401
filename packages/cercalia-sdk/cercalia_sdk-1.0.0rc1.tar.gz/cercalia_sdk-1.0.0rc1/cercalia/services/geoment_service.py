"""
Geoment Service for Cercalia SDK.

This service downloads polygon geometries of administrative/geographic elements
such as municipalities, regions, postal codes, and points of interest.
"""

from typing import Any, Optional

from ..config import CercaliaConfig
from ..types.api_response import get_cercalia_attr, get_cercalia_value
from ..types.geoment import (
    GeographicElementResult,
    GeographicElementType,
    GeomentMunicipalityOptions,
    GeomentPoiOptions,
    GeomentPostalCodeOptions,
)
from ..utils.logger import logger
from .cercalia_client import CercaliaClient


class GeomentService(CercaliaClient):
    """
    Service for downloading geographic element geometries.

    Supported elements:
    - Municipalities (munc)
    - Regions/Subregions (subregc)
    - Postal Codes (pcode)
    - Points of Interest (poic)

    Following Golden Rules:
    - Direct mapping from API response (no fallbacks)
    - Code suffix for identifiers (@id -> code)
    - Transparency of geometry type via level field
    - Strict coordinate handling (no defaults)
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the Geoment service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def get_municipality_geometry(
        self, options: GeomentMunicipalityOptions
    ) -> GeographicElementResult:
        """
        Get geometry for a municipality or region.

        Args:
            options: Municipality/Region options (munc OR subregc, tolerance)

        Returns:
            GeographicElementResult with WKT polygon

        Example:
            # Madrid municipality
            result = service.get_municipality_geometry(
                GeomentMunicipalityOptions(munc='ESP280796', tolerance=0)
            )

            # Madrid region
            region = service.get_municipality_geometry(
                GeomentMunicipalityOptions(subregc='ESP28', tolerance=0)
            )
        """
        params: dict[str, str] = {}

        if options.munc:
            params["munc"] = options.munc
        if options.subregc:
            params["subregc"] = options.subregc
        if options.tolerance is not None:
            params["tolerance"] = str(options.tolerance)

        element_type: GeographicElementType = "region" if options.subregc else "municipality"
        return self._fetch_geometry(params, element_type)

    def get_postal_code_geometry(
        self, options: GeomentPostalCodeOptions
    ) -> GeographicElementResult:
        """
        Get geometry for a postal code.

        Args:
            options: Postal code options (pcode, ctryc, tolerance)

        Returns:
            GeographicElementResult with WKT polygon

        Example:
            # Spanish postal code
            result = service.get_postal_code_geometry(
                GeomentPostalCodeOptions(pcode='28001', ctryc='ESP', tolerance=0)
            )
        """
        params: dict[str, str] = {"pcode": options.pcode}

        if options.ctryc:
            params["ctryc"] = options.ctryc
        if options.tolerance is not None:
            params["tolerance"] = str(options.tolerance)

        return self._fetch_geometry(params, "postal_code")

    def get_poi_geometry(self, options: GeomentPoiOptions) -> GeographicElementResult:
        """
        Get geometry for a Point of Interest.

        Args:
            options: POI options (poic, tolerance)

        Returns:
            GeographicElementResult with WKT polygon/point

        Example:
            # POI geometry
            result = service.get_poi_geometry(
                GeomentPoiOptions(poic='POI123456', tolerance=0)
            )
        """
        params: dict[str, str] = {"poic": options.poic}

        if options.tolerance is not None:
            params["tolerance"] = str(options.tolerance)

        return self._fetch_geometry(params, "poi")

    def _fetch_geometry(
        self,
        params: dict[str, str],
        element_type: GeographicElementType,
    ) -> GeographicElementResult:
        """
        Fetch geometry from Cercalia API.

        Handles multiple response formats and extracts WKT.
        """
        request_params = {
            **params,
            "cmd": "geoment",
            "cs": "4326",  # Always use Lat/Lng WGS84
        }

        try:
            data = self._request(request_params, "GeomentService")

            # Response can be in two formats:
            # 1. { geographic_elements: { geographic_element: [...] } }
            # 2. { ge: { ... } }
            elements_container = None
            if data.get("geographic_elements"):
                elements_container = data["geographic_elements"].get("geographic_element")
            if not elements_container:
                elements_container = data.get("ge")

            if not elements_container:
                raise ValueError("No geographic elements found in response")

            # Handle array vs single object (Cercalia inconsistency)
            element: dict[str, Any]
            if isinstance(elements_container, list):
                element = elements_container[0]
            else:
                element = elements_container

            if not element:
                raise ValueError("Empty geographic element in response")

            # Extract fields following Golden Rules
            code = get_cercalia_attr(element, "id")
            name = get_cercalia_attr(element, "name")
            level = get_cercalia_attr(element, "type")  # Transparency of geometry type

            # Try multiple possible paths for WKT (Cercalia API inconsistency)
            wkt = self._extract_wkt(element)

            if not wkt:
                logger.error(f"[GeomentService] Missing WKT in element: {element}")
                raise ValueError("Geometry WKT missing in response")

            # Direct mapping - no fallbacks (Golden Rule #1)
            return GeographicElementResult(
                code=code or "",  # Use 'code' suffix instead of 'id' (Golden Rule #2)
                name=name,  # Can be None - no fallback (Golden Rule #1)
                wkt=wkt,
                type=element_type,
                level=level,  # Transparency of geometry type (Golden Rule #6)
            )

        except Exception as e:
            logger.error(f"[GeomentService] Error: {e}")
            raise

    def _extract_wkt(self, element: dict[str, Any]) -> Optional[str]:
        """
        Extract WKT from element, handling multiple response formats.
        """
        wkt: Optional[str] = None

        # Try geometry.wkt path
        geometry = element.get("geometry")
        if geometry and isinstance(geometry, dict):
            wkt_value = geometry.get("wkt")
            if wkt_value:
                wkt = get_cercalia_value(wkt_value)

        # Try geom path (multiple formats)
        if not wkt:
            geom = element.get("geom")
            if geom:
                if isinstance(geom, str):
                    wkt = geom
                elif isinstance(geom, dict):
                    if "wkt" in geom:
                        wkt = get_cercalia_value(geom["wkt"])
                    elif "value" in geom:
                        wkt = get_cercalia_value(geom)

        # Try direct wkt path
        if not wkt:
            direct_wkt = element.get("wkt")
            if direct_wkt:
                wkt = get_cercalia_value(direct_wkt)

        return wkt
