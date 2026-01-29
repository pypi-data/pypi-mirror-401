"""
Isochrone service for Cercalia SDK.

Provides isochrone (service area) calculations using Cercalia API.
"""

from typing import Any, Optional

from ..config import CercaliaConfig
from ..types.api_response import get_cercalia_attr, get_cercalia_value
from ..types.common import Coordinate
from ..types.isochrone import (
    IsochroneMethod,
    IsochroneMultipleOptions,
    IsochroneOptions,
    IsochroneResult,
    IsochroneWeight,
)
from .cercalia_client import CercaliaClient


class IsochroneService(CercaliaClient):
    """
    Isochrone (service area) calculations using Cercalia API.

    An isochrone is a polygon representing the area reachable from a center point
    within a given time or distance constraint.

    Example:
        >>> service = IsochroneService(config)
        >>>
        >>> # 10-minute driving time isochrone
        >>> result = service.calculate(
        ...     Coordinate(lat=41.9723144, lng=2.8260807),
        ...     IsochroneOptions(value=10, weight="time")
        ... )
        >>>
        >>> # 1000-meter distance isochrone
        >>> result = service.calculate(
        ...     Coordinate(lat=41.9723144, lng=2.8260807),
        ...     IsochroneOptions(value=1000, weight="distance")
        ... )
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the isochrone service.

        Args:
            config: Cercalia API configuration
        """
        super().__init__(config)

    def calculate(self, center: Coordinate, options: IsochroneOptions) -> IsochroneResult:
        """
        Calculate a single isochrone (service area) from a center point.

        Args:
            center: Center coordinate for the isochrone (WGS84)
            options: Isochrone calculation options (value, weight, method)

        Returns:
            IsochroneResult with WKT polygon geometry

        Raises:
            ValueError: If value is less than or equal to zero

        Example:
            >>> # 10-minute driving time isochrone
            >>> result = service.calculate(
            ...     Coordinate(lat=41.9723144, lng=2.8260807),
            ...     IsochroneOptions(value=10, weight="time")
            ... )
            >>> print(result.wkt)  # POLYGON((...))
        """
        if options.value <= 0:
            raise ValueError("Isochrone value must be greater than zero")

        weight: IsochroneWeight = options.weight or "time"

        # Convert value to API format:
        # - time: minutes -> milliseconds
        # - distance: meters (no conversion)
        api_value = options.value * 60 * 1000 if weight == "time" else options.value

        params: dict[str, str] = {
            "cmd": "isochrone",
            "mo": f"{center.lng},{center.lat}",
            "isolevels": str(api_value),
            "weight": weight,
            "method": options.method or "concavehull",
            "mocs": "4326",
            "ocs": "4326",
        }

        response = self._request(params, "Isochrone")

        isochrones = response.get("isochrones")
        if not isochrones or not isochrones.get("isochrone"):
            raise ValueError("No isochrone data found in response")

        # Handle both single and array responses
        isochrone_data = isochrones["isochrone"]
        isochrone_list = isochrone_data if isinstance(isochrone_data, list) else [isochrone_data]

        first_isochrone = isochrone_list[0]
        return self._map_isochrone_level(first_isochrone, center, options.value, weight)

    def calculate_multiple(
        self,
        center: Coordinate,
        values: list[int],
        options: Optional[IsochroneMultipleOptions] = None,
    ) -> list[IsochroneResult]:
        """
        Calculate multiple isochrones (concentric service areas).

        This method allows you to calculate multiple isochrone levels in a single API request.
        For example, 5, 10, and 15-minute travel time isochrones.

        Args:
            center: Center coordinate (WGS84)
            values: List of values (e.g., [5, 10, 15] for 5, 10, 15 minutes)
            options: Base options (weight, method)

        Returns:
            List of IsochroneResult, one for each value

        Example:
            >>> # Multiple time-based isochrones
            >>> results = service.calculate_multiple(
            ...     Coordinate(lat=41.9723144, lng=2.8260807),
            ...     [5, 10, 15],
            ...     IsochroneMultipleOptions(weight="time")
            ... )
            >>>
            >>> # Multiple distance-based isochrones
            >>> results = service.calculate_multiple(
            ...     Coordinate(lat=41.9723144, lng=2.8260807),
            ...     [500, 1000, 2000],
            ...     IsochroneMultipleOptions(weight="distance", method="convexhull")
            ... )
        """
        weight: IsochroneWeight = options.weight if options and options.weight else "time"
        method: IsochroneMethod = options.method if options and options.method else "concavehull"

        # Convert values to API format
        api_values = [v * 60 * 1000 for v in values] if weight == "time" else values

        params: dict[str, str] = {
            "cmd": "isochrone",
            "mo": f"{center.lng},{center.lat}",
            "isolevels": ",".join(str(v) for v in api_values),
            "weight": weight,
            "method": method,
            "mocs": "4326",
            "ocs": "4326",
        }

        response = self._request(params, "Multi-Isochrone")

        isochrones = response.get("isochrones")
        if not isochrones or not isochrones.get("isochrone"):
            raise ValueError("No isochrone data found in response")

        # Handle both single and array responses
        isochrone_data = isochrones["isochrone"]
        isochrone_list = isochrone_data if isinstance(isochrone_data, list) else [isochrone_data]

        return [
            self._map_isochrone_level(level, center, values[index], weight)
            for index, level in enumerate(isochrone_list)
        ]

    def _map_isochrone_level(
        self,
        level: dict[str, Any],
        center: Coordinate,
        value: int,
        weight: IsochroneWeight,
    ) -> IsochroneResult:
        """
        Map a Cercalia isochrone level to the SDK IsochroneResult format.

        Following Golden Rules:
        1. Direct Mapping: No fallbacks, if API returns null we raise error
        2. Transparency: Include raw level value from API

        Args:
            level: Raw isochrone level from Cercalia API
            center: Center coordinate
            value: Original value in user units (minutes or meters)
            weight: Weight type

        Returns:
            Mapped IsochroneResult
        """
        # Extract WKT polygon using helper (direct mapping)
        wkt = get_cercalia_value(level)
        if not wkt:
            raise ValueError("No WKT polygon found in isochrone response")

        # Extract level attribute (transparency of geometry type)
        level_value = get_cercalia_attr(level, "level")
        if not level_value:
            raise ValueError("No level attribute found in isochrone response")

        return IsochroneResult(
            wkt=wkt,
            center=center,
            value=value,
            weight=weight,
            level=level_value,
        )
