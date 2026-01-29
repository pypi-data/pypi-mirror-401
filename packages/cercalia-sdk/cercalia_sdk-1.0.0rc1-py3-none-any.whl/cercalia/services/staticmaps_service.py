"""
Static Maps Service for Cercalia SDK.

Provides functionality to generate static map images with markers, shapes, and labels.

Example:
    >>> from cercalia import StaticMapsService, CercaliaConfig, Coordinate
    >>> from cercalia.types.staticmaps import StaticMapOptions, StaticMapMarker
    >>> config = CercaliaConfig(api_key="your-api-key")
    >>> service = StaticMapsService(config)
    >>> result = service.generate_city_map("Barcelona", "ESP", width=800, height=600)
    >>> print(result.image_url)
"""

from typing import Any, Optional
from urllib.parse import urlparse

import requests

from ..types.common import CercaliaConfig, Coordinate
from ..types.staticmaps import (
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
)
from ..utils.logger import logger
from .cercalia_client import CercaliaClient


class StaticMapsService(CercaliaClient):
    """
    Static Maps Service for generating static map images.

    Features:
    - Paint markers on the map
    - Draw shapes: circles, rectangles, sectors, lines, polylines
    - Add labels
    - Get image URL or raw image data

    Based on the Cercalia Static Maps API:
    https://docs.cercalia.com/docs/cercalia-webservices/static-maps/
    """

    MAX_WIDTH = 1680
    MAX_HEIGHT = 1280

    def __init__(self, config: CercaliaConfig) -> None:
        """Initialize the Static Maps service."""
        super().__init__(config)

    def generate_map(self, options: StaticMapOptions) -> StaticMapResult:
        """
        Generate a static map with optional markers and shapes.

        Args:
            options: Static map generation options including dimensions,
                center/extent, markers, and shapes.

        Returns:
            StaticMapResult with image URL or image data (if return_image=True).

        Raises:
            ValueError: If no valid map data is returned or candidate lookup fails.
            requests.RequestException: If the API request fails.

        Example:
            >>> result = service.generate_map(StaticMapOptions(
            ...     city_name="girona",
            ...     country_code="ESP",
            ...     width=350,
            ...     height=250,
            ... ))
            >>> print(result.image_url)
        """
        coord_system = options.coordinate_system or "gdd"
        params: dict[str, str] = {
            "cmd": "map",
            "mocs": coord_system,
            "cs": coord_system,
        }

        # Image dimensions
        if options.width:
            params["width"] = str(min(options.width, self.MAX_WIDTH))
        if options.height:
            params["height"] = str(min(options.height, self.MAX_HEIGHT))

        # Location by city name
        if options.city_name:
            params["ctn"] = options.city_name
        if options.country_code:
            params["ctryc"] = options.country_code

        # Map extent
        if options.extent:
            extent_str = (
                f"{options.extent.upper_left.lat},{options.extent.upper_left.lng}|"
                f"{options.extent.lower_right.lat},{options.extent.lower_right.lng}"
            )
            params["extent"] = extent_str

        # Center coordinate
        if options.center:
            params["mo"] = f"{options.center.lat},{options.center.lng}"

        # Label options
        if options.label_op is not None:
            params["labelop"] = str(options.label_op)

        # Markers
        if options.markers:
            params["molist"] = self._format_markers(options.markers)

        # Shapes
        if options.shapes:
            params["shape"] = self._format_shapes(options.shapes)

        try:
            data = self._request(params, "StaticMaps")

            # Handle returnImage option
            if options.return_image:
                # Handle candidates case
                if data.get("candidates") and not data.get("map"):
                    candidates = data["candidates"].get("candidate", [])
                    if candidates:
                        first_candidate = (
                            candidates[0] if isinstance(candidates, list) else candidates
                        )
                        url_params = first_candidate.get("urlparams", {}).get("param", [])
                        ctc_param = next(
                            (p for p in url_params if p.get("@name") == "ctc"),
                            None,
                        )
                        if ctc_param:
                            logger.info(
                                f"[DEBUG] StaticMaps: Using candidate {first_candidate.get('@desc')} "
                                f"with ctc={ctc_param.get('@value')} for image"
                            )
                            new_params: dict[str, str] = {
                                "cmd": "map",
                                "mocs": options.coordinate_system or "gdd",
                                "ctc": ctc_param["@value"],
                            }
                            if options.width:
                                new_params["width"] = str(min(options.width, self.MAX_WIDTH))
                            if options.height:
                                new_params["height"] = str(min(options.height, self.MAX_HEIGHT))

                            retry_data = self._request(new_params, "StaticMaps (Retry)")

                            if retry_data.get("map", {}).get("img", {}).get("@href"):
                                parsed_url = urlparse(self.config.base_url)
                                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                                image_url = f"{base_url}{retry_data['map']['img']['@href']}"
                                image_response = requests.get(image_url, timeout=30)
                                return StaticMapResult(
                                    image_data=image_response.content,
                                    format="gif",
                                )

                    raise ValueError("No valid candidate found for image generation")

                # If we have map data, download the image from href
                if data.get("map", {}).get("img", {}).get("@href"):
                    parsed_url = urlparse(self.config.base_url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    image_url = f"{base_url}{data['map']['img']['@href']}"
                    image_response = requests.get(image_url, timeout=30)
                    return StaticMapResult(image_data=image_response.content, format="gif")

                raise ValueError("No image data available in response")

            # Handle candidates case (JSON response)
            if data.get("candidates") and not data.get("map"):
                candidates = data["candidates"].get("candidate", [])
                if candidates:
                    first_candidate = candidates[0] if isinstance(candidates, list) else candidates
                    url_params = first_candidate.get("urlparams", {}).get("param", [])
                    ctc_param = next(
                        (p for p in url_params if p.get("@name") == "ctc"),
                        None,
                    )
                    if ctc_param:
                        logger.info(
                            f"[DEBUG] StaticMaps: Using candidate {first_candidate.get('@desc')} "
                            f"with ctc={ctc_param.get('@value')}"
                        )
                        new_params = {
                            "cmd": "map",
                            "ctc": ctc_param["@value"],
                        }
                        if options.width:
                            new_params["width"] = str(min(options.width, self.MAX_WIDTH))
                        if options.height:
                            new_params["height"] = str(min(options.height, self.MAX_HEIGHT))
                        if options.coordinate_system:
                            new_params["mocs"] = options.coordinate_system
                            new_params["cs"] = options.coordinate_system
                        if options.shapes:
                            new_params["shape"] = self._format_shapes(options.shapes)
                        if options.markers:
                            new_params["molist"] = self._format_markers(options.markers)

                        retry_data = self._request(new_params, "StaticMaps (Retry Candidate)")

                        if not retry_data.get("map", {}).get("img"):
                            raise ValueError("No map data in response after retry")

                        return self._parse_map_response(retry_data)

                raise ValueError(
                    "No map data in response - received candidates but no valid ctc parameter"
                )

            map_data = data.get("map")
            if not map_data or not map_data.get("img"):
                raise ValueError("No map data in response")

            return self._parse_map_response(data)

        except Exception as e:
            logger.error(f"[StaticMaps] Error: {e}")
            raise

    def generate_city_map(
        self,
        city_name: str,
        country_code: str = "ESP",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map centered on a city with a label.

        Args:
            city_name: Name of the city (e.g., 'Barcelona', 'Madrid').
            country_code: ISO 3166-1 alpha-3 country code (default: 'ESP').
            width: Optional image width in pixels (max 1680).
            height: Optional image height in pixels (max 1280).

        Returns:
            StaticMapResult with image URL and metadata.

        Raises:
            ValueError: If the city cannot be found.
            requests.RequestException: If the API request fails.

        Example:
            >>> result = service.generate_city_map("Girona", "ESP", width=350, height=250)
            >>> print(f"Map URL: {result.image_url}")
            >>> print(f"Scale: 1:{result.scale}")
        """
        return self.generate_map(
            StaticMapOptions(
                city_name=city_name,
                country_code=country_code,
                width=width,
                height=height,
            )
        )

    def generate_map_with_circle(
        self,
        center: Coordinate,
        radius: float,
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        fill_color: Optional[RGBAColor] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a circle shape.

        Args:
            center: Center coordinate of the circle.
            radius: Radius in meters.
            outline_color: Circle outline color (default: red).
            outline_size: Outline width in pixels (default: 2).
            fill_color: Circle fill color (default: semi-transparent green).
            width: Optional image width in pixels.
            height: Optional image height in pixels.

        Returns:
            StaticMapResult with image URL.

        Raises:
            ValueError: If the map cannot be generated.
            requests.RequestException: If the API request fails.

        Example:
            >>> result = service.generate_map_with_circle(
            ...     center=Coordinate(lat=41.38, lng=2.17),
            ...     radius=1000,  # 1km
            ...     width=400, height=300
            ... )
        """
        circle = StaticMapCircle(
            type="CIRCLE",
            center=center,
            radius=radius,
            outline_color=outline_color or RGBAColor(r=255, g=0, b=0),
            outline_size=outline_size or 2,
            fill_color=fill_color or RGBAColor(r=0, g=255, b=0, a=128),
        )

        return self.generate_map(
            StaticMapOptions(
                center=center,
                shapes=[circle],
                width=width,
                height=height,
                coordinate_system="gdd",
            )
        )

    def generate_map_with_rectangle(
        self,
        upper_left: Coordinate,
        lower_right: Coordinate,
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        fill_color: Optional[RGBAColor] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        city_name: Optional[str] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a rectangle shape.

        Args:
            upper_left: Upper-left corner coordinate
            lower_right: Lower-right corner coordinate
            outline_color: Optional outline color
            outline_size: Optional outline size
            fill_color: Optional fill color
            width: Optional image width
            height: Optional image height
            city_name: Optional city name for centering

        Returns:
            StaticMapResult with image URL
        """
        rectangle = StaticMapRectangle(
            type="RECTANGLE",
            upper_left=upper_left,
            lower_right=lower_right,
            outline_color=outline_color or RGBAColor(r=255, g=0, b=0),
            outline_size=outline_size or 3,
            fill_color=fill_color or RGBAColor(r=0, g=255, b=0, a=128),
        )

        return self.generate_map(
            StaticMapOptions(
                city_name=city_name,
                shapes=[rectangle],
                width=width,
                height=height,
            )
        )

    def generate_map_with_polyline(
        self,
        coordinates: list[Coordinate],
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a polyline.

        Args:
            coordinates: List of coordinates forming the polyline
            outline_color: Optional outline color
            outline_size: Optional outline size
            width: Optional image width
            height: Optional image height

        Returns:
            StaticMapResult with image URL
        """
        color = outline_color or RGBAColor(r=255, g=0, b=0)
        polyline = StaticMapPolyline(
            type="POLYLINE",
            coordinates=coordinates,
            outline_color=color,
            outline_size=outline_size or 2,
            fill_color=color,
        )

        # Calculate extent from coordinates
        lats = [c.lat for c in coordinates]
        lngs = [c.lng for c in coordinates]
        padding = 0.01

        return self.generate_map(
            StaticMapOptions(
                extent=StaticMapExtent(
                    upper_left=Coordinate(lat=max(lats) + padding, lng=min(lngs) - padding),
                    lower_right=Coordinate(lat=min(lats) - padding, lng=max(lngs) + padding),
                ),
                shapes=[polyline],
                width=width,
                height=height,
                coordinate_system="gdd",
                label_op=0,
            )
        )

    def generate_map_with_markers(
        self,
        markers: list[StaticMapMarker],
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with markers.

        Args:
            markers: List of markers to place on the map
            width: Optional image width
            height: Optional image height

        Returns:
            StaticMapResult with image URL
        """
        # Calculate extent from markers
        lats = [m.coord.lat for m in markers]
        lngs = [m.coord.lng for m in markers]
        padding = 0.01

        return self.generate_map(
            StaticMapOptions(
                extent=StaticMapExtent(
                    upper_left=Coordinate(lat=max(lats) + padding, lng=min(lngs) - padding),
                    lower_right=Coordinate(lat=min(lats) - padding, lng=max(lngs) + padding),
                ),
                markers=markers,
                width=width,
                height=height,
                coordinate_system="gdd",
            )
        )

    def generate_map_with_label(
        self,
        center: Coordinate,
        text: str,
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        fill_color: Optional[RGBAColor] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a label at a specific position.

        Args:
            center: Center coordinate of the label
            text: Label text
            outline_color: Optional outline color
            outline_size: Optional outline size
            fill_color: Optional fill color
            width: Optional image width
            height: Optional image height

        Returns:
            StaticMapResult with image URL
        """
        label = StaticMapLabel(
            type="LABEL",
            center=center,
            text=text,
            outline_color=outline_color or RGBAColor(r=0, g=0, b=0),
            outline_size=outline_size or 1,
            fill_color=fill_color or RGBAColor(r=255, g=255, b=255),
        )

        return self.generate_map(
            StaticMapOptions(
                center=center,
                shapes=[label],
                width=width,
                height=height,
                coordinate_system="gdd",
            )
        )

    def generate_map_with_sector(
        self,
        center: Coordinate,
        inner_radius: float,
        outer_radius: float,
        start_angle: float,
        end_angle: float,
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        fill_color: Optional[RGBAColor] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a sector shape.

        Args:
            center: Center coordinate of the sector
            inner_radius: Inner radius in meters
            outer_radius: Outer radius in meters
            start_angle: Start angle in degrees
            end_angle: End angle in degrees
            outline_color: Optional outline color
            outline_size: Optional outline size
            fill_color: Optional fill color
            width: Optional image width
            height: Optional image height

        Returns:
            StaticMapResult with image URL
        """
        sector = StaticMapSector(
            type="SECTOR",
            center=center,
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            start_angle=start_angle,
            end_angle=end_angle,
            outline_color=outline_color or RGBAColor(r=255, g=0, b=0),
            outline_size=outline_size or 2,
            fill_color=fill_color or RGBAColor(r=0, g=255, b=0, a=128),
        )

        return self.generate_map(
            StaticMapOptions(
                center=center,
                shapes=[sector],
                width=width,
                height=height,
                coordinate_system="gdd",
            )
        )

    def generate_map_with_line(
        self,
        start: Coordinate,
        end: Coordinate,
        outline_color: Optional[RGBAColor] = None,
        outline_size: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> StaticMapResult:
        """
        Generate a map with a line between two points.

        Args:
            start: Start coordinate
            end: End coordinate
            outline_color: Optional outline color
            outline_size: Optional outline size
            width: Optional image width
            height: Optional image height

        Returns:
            StaticMapResult with image URL
        """
        line = StaticMapLine(
            type="LINE",
            start=start,
            end=end,
            outline_color=outline_color or RGBAColor(r=255, g=0, b=0),
            outline_size=outline_size or 2,
            fill_color=RGBAColor(r=0, g=0, b=0),  # Not used for lines
        )

        padding = 0.01
        lats = [start.lat, end.lat]
        lngs = [start.lng, end.lng]

        return self.generate_map(
            StaticMapOptions(
                extent=StaticMapExtent(
                    upper_left=Coordinate(lat=max(lats) + padding, lng=min(lngs) - padding),
                    lower_right=Coordinate(lat=min(lats) - padding, lng=max(lngs) + padding),
                ),
                shapes=[line],
                width=width,
                height=height,
                coordinate_system="gdd",
            )
        )

    def download_image(self, image_url: str) -> bytes:
        """
        Download the static map image as bytes.

        Args:
            image_url: URL to the map image

        Returns:
            Image data as bytes

        Raises:
            requests.HTTPError: If the download fails
        """
        response = requests.get(image_url, timeout=30)
        if not response.ok:
            raise requests.HTTPError(
                f"Failed to download image: {response.status_code} {response.reason}"
            )
        return response.content

    def generate_map_as_image(
        self,
        city_name: Optional[str] = None,
        country_code: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        extent: Optional[StaticMapExtent] = None,
        center: Optional[Coordinate] = None,
        markers: Optional[list[StaticMapMarker]] = None,
        shapes: Optional[list[StaticMapShape]] = None,
    ) -> StaticMapResult:
        """
        Generate map and return image data directly.

        Args:
            city_name: Optional city name
            country_code: Optional country code
            width: Optional image width
            height: Optional image height
            extent: Optional map extent
            center: Optional center coordinate
            markers: Optional list of markers
            shapes: Optional list of shapes

        Returns:
            StaticMapResult with image_data containing raw bytes
        """
        return self.generate_map(
            StaticMapOptions(
                city_name=city_name,
                country_code=country_code,
                width=width,
                height=height,
                extent=extent,
                center=center,
                markers=markers,
                shapes=shapes,
                return_image=True,
            )
        )

    # ============================================
    # Private Helper Methods
    # ============================================

    def _parse_map_response(self, data: dict[str, Any]) -> StaticMapResult:
        """Parse map response into StaticMapResult."""
        map_data = data["map"]
        img = map_data["img"]
        href = img["@href"]
        parsed_url = urlparse(self.config.base_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        image_url = f"{base_url}{href}"

        # Parse extent from response
        response_extent: Optional[StaticMapExtent] = None
        extent_data = img.get("extent", {})
        coords = extent_data.get("coord", [])
        if coords and len(coords) >= 2:
            response_extent = StaticMapExtent(
                upper_left=Coordinate(
                    lat=float(coords[0]["@y"]),
                    lng=float(coords[0]["@x"]),
                ),
                lower_right=Coordinate(
                    lat=float(coords[1]["@y"]),
                    lng=float(coords[1]["@x"]),
                ),
            )

        # Parse center
        center: Optional[Coordinate] = None
        center_str = img.get("@center")
        if center_str:
            lng_str, lat_str = center_str.split(",")
            center = Coordinate(lat=float(lat_str), lng=float(lng_str))

        # Parse label
        label: Optional[str] = None
        label_data = map_data.get("label", {})
        if label_data.get("value"):
            label = label_data["value"]

        return StaticMapResult(
            image_url=image_url,
            image_path=href,
            width=int(img["@width"]),
            height=int(img["@height"]),
            format=img["@format"],
            scale=int(img["@scale"]),
            center=center,
            extent=response_extent,
            label=label,
        )

    def _format_color(self, color: RGBAColor) -> str:
        """Format RGBA color to Cercalia format: 'R,G,B,A' or 'R,G,B'."""
        if color.a is not None:
            return f"{color.r},{color.g},{color.b},{color.a}"
        return f"{color.r},{color.g},{color.b}"

    def _format_markers(self, markers: list[StaticMapMarker]) -> str:
        """
        Format markers for molist parameter.
        Format: [Y,X|icon],[Y,X|icon],...
        """
        formatted = []
        for m in markers:
            coord = f"{m.coord.lat},{m.coord.lng}"
            if m.icon is not None:
                formatted.append(f"[{coord}|{m.icon}]")
            else:
                formatted.append(f"[{coord}]")
        return ",".join(formatted)

    def _format_shapes(self, shapes: list[StaticMapShape]) -> str:
        """
        Format shapes for shape parameter.
        Format: [outline color|outline size|fill color|shape type|specific params],...
        """
        return ",".join(self._format_shape(shape) for shape in shapes)

    def _format_shape(self, shape: StaticMapShape) -> str:
        """Format a single shape."""
        outline_color = self._format_color(shape.outline_color)
        outline_size = shape.outline_size
        fill_color = self._format_color(shape.fill_color)

        if shape.type == "CIRCLE":
            circle = shape  # type: StaticMapCircle
            # Format: [outlineColor|outlineSize|fillColor|CIRCLE|Y,X|radius]
            return (
                f"[{outline_color}|{outline_size}|{fill_color}|CIRCLE|"
                f"{circle.center.lat},{circle.center.lng}|{circle.radius}]"
            )

        if shape.type == "RECTANGLE":
            rect = shape  # type: StaticMapRectangle
            # Format: [outlineColor|outlineSize|fillColor|RECTANGLE|Y1,X1|Y2,X2]
            return (
                f"[{outline_color}|{outline_size}|{fill_color}|RECTANGLE|"
                f"{rect.upper_left.lat},{rect.upper_left.lng}|"
                f"{rect.lower_right.lat},{rect.lower_right.lng}]"
            )

        if shape.type == "SECTOR":
            sector = shape  # type: StaticMapSector
            # Format: [outlineColor|outlineSize|fillColor|SECTOR|center|innerRadius|outerRadius|startAngle|endAngle]
            return (
                f"[{outline_color}|{outline_size}|{fill_color}|SECTOR|"
                f"{sector.center.lat},{sector.center.lng}|"
                f"{sector.inner_radius}|{sector.outer_radius}|"
                f"{sector.start_angle}|{sector.end_angle}]"
            )

        if shape.type == "LINE":
            line = shape  # type: StaticMapLine
            # Format: [outlineColor|outlineSize|fillColor|LINE|startY,startX|endY,endX]
            return (
                f"[{outline_color}|{outline_size}|{fill_color}|LINE|"
                f"{line.start.lat},{line.start.lng}|{line.end.lat},{line.end.lng}]"
            )

        if shape.type == "POLYLINE":
            polyline = shape  # type: StaticMapPolyline
            # Format: [outlineColor|outlineSize|fillColor|POLYLINE|Y1,X1|Y2,X2|...|Yn,Xn]
            coords = "|".join(f"{c.lat},{c.lng}" for c in polyline.coordinates)
            return f"[{outline_color}|{outline_size}|{fill_color}|POLYLINE|{coords}]"

        if shape.type == "LABEL":
            label = shape  # type: StaticMapLabel
            # Format: [outlineColor|outlineSize|fillColor|LABEL|Y,X|text]
            return (
                f"[{outline_color}|{outline_size}|{fill_color}|LABEL|"
                f"{label.center.lat},{label.center.lng}|{label.text}]"
            )

        raise ValueError(f"Unknown shape type: {shape.type}")
