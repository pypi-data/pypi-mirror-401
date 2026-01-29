from typing import Any

from pynina.api_client import APIClient
from pynina.const import (
    ENDPOINT_DE_LABELS,
    ENDPOINT_NINA_BASE,
    ENDPOINT_REGIONAL_CODE,
    ENDPOINT_WARNING_DETAIL,
    _LOGGER,
)


class NinaAPI:
    """Class to bundle NINA API requests."""

    def __init__(self, client: APIClient):
        """Initialize."""
        self._client = client

    async def get_warnings(self, region_code: str) -> list[dict[str, Any]]:
        """Fetch warnings for the given region."""
        _LOGGER.debug(f"Update region: {region_code}")
        url: str = ENDPOINT_NINA_BASE + region_code + ".json"
        data = await self._client.make_request(url)
        return data

    async def get_warning_details(self, warning_id: str) -> dict[str, str]:
        """Fetch warning details for the given warning."""
        _LOGGER.debug(f"Fetch details for {warning_id}")
        url: str = ENDPOINT_WARNING_DETAIL + warning_id + ".json"
        data = await self._client.make_request(url)
        return data

    async def get_region_codes(self) -> dict[str, Any]:
        """Fetch region codes."""
        _LOGGER.debug("Get all regional codes")
        return await self._client.make_request(ENDPOINT_REGIONAL_CODE)

    async def get_labels(self) -> dict[str, str]:
        """Fetch labels for recommended actions."""
        _LOGGER.debug("Get all action labels")
        return await self._client.make_request(ENDPOINT_DE_LABELS)
