"""
Base Cercalia API client.

Provides the foundation for all Cercalia service implementations.
"""

from abc import ABC
from typing import Any, Optional
from urllib.parse import urlencode

import requests

from ..config import CercaliaConfig
from ..types.api_response import get_cercalia_attr, get_cercalia_value
from ..types.common import CercaliaError
from ..utils.logger import logger
from ..utils.retry import retry_request


class CercaliaClient(ABC):
    """
    Abstract base class for Cercalia API services.

    Provides common HTTP request functionality with retry logic,
    error handling, and response parsing.

    All Cercalia services should inherit from this class.
    """

    def __init__(self, config: CercaliaConfig) -> None:
        """
        Initialize the Cercalia client.

        Args:
            config: Cercalia API configuration with api_key and base_url
        """
        self.config = config

    def _request(
        self,
        params: dict[str, str],
        operation_name: str = "Cercalia Request",
        base_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Make a request to the Cercalia API.

        Handles:
        - URL construction with query parameters
        - Retry logic with exponential backoff
        - JSON parsing and validation
        - Cercalia-specific error handling

        Args:
            params: Query parameters for the API request
            operation_name: Name of the operation for logging
            base_url: Optional override for the base URL

        Returns:
            The parsed response data (contents of 'cercalia' key)

        Raises:
            CercaliaError: If the API returns an error response
            ValueError: If the response format is invalid
            requests.RequestException: If the HTTP request fails
        """
        # Add API key to params
        all_params = {"key": self.config.api_key, **params}

        # Build URL
        url = f"{base_url or self.config.base_url}?{urlencode(all_params)}"
        logger.debug(f"[{operation_name}] Request URL: {url}")

        def make_request() -> dict[str, Any]:
            response = requests.get(url, timeout=30)

            if not response.ok:
                logger.error(
                    f"[{operation_name}] HTTP Error {response.status_code}: {response.text}"
                )
                raise requests.HTTPError(
                    f"Cercalia API error: {response.status_code} {response.reason}"
                )

            raw_data = response.text
            # Log truncated response for debugging
            logger.debug(f"[{operation_name}] Response: {raw_data[:500]}...")

            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"[{operation_name}] Invalid JSON response: {raw_data}")
                raise ValueError("Invalid JSON response from Cercalia API") from e

            cercalia = data.get("cercalia")
            if not cercalia:
                raise ValueError('Invalid response format: missing "cercalia" root property')

            # Check for API errors
            error = cercalia.get("error")
            if error:
                error_code = get_cercalia_attr(error, "id")
                error_msg = get_cercalia_value(error)
                raise CercaliaError(error_msg or "Unknown error", error_code)

            return cercalia

        try:
            return retry_request(
                make_request,
                max_attempts=3,
                delay_ms=500,
                log_retries=True,
                operation_name=operation_name,
            )
        except CercaliaError:
            # Re-raise CercaliaError as-is
            raise
        except Exception as e:
            logger.error(f"[{operation_name}] Failed: {e}")
            raise
