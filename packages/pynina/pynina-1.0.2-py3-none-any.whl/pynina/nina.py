from typing import Any, Dict

from aiohttp import ClientSession

from .api_client import APIClient
from .const import (
    CITY_STATES_CODE,
    COUNTIES,
    _LOGGER,
    ReadOnlyClass,
)
from .label_matcher import ActionLabelMatcher
from .nina_api import NinaAPI
from .warning import Warning
from .warning_fetcher import WarningFetcher


class Nina(metaclass=ReadOnlyClass):
    """Main class to interact with the NINA API"""

    def __init__(self, session: ClientSession | None = None):
        """Initialize."""
        self._api_client: APIClient = APIClient(session)
        self._api: NinaAPI = NinaAPI(self._api_client)
        self._label_matcher: ActionLabelMatcher = ActionLabelMatcher(self._api)
        self._warning_fetcher: WarningFetcher = WarningFetcher(
            self._api, self._label_matcher
        )

        self.warnings: dict[str, list[Warning]] = {}
        self.regions: list = []

    def add_region(self, region_code: str):
        """Add a region to monitor."""
        if region_code not in self.regions:
            self.regions.append(region_code)

    async def update(self):
        """Update the warnings."""
        if not self._label_matcher.initiated:
            await self._label_matcher.init()

        self.warnings.clear()

        for region_code in self.regions:
            _LOGGER.debug(f"Update region: {region_code}")
            self.warnings[region_code] = await self._warning_fetcher.fetch_warnings(
                region_code
            )

    async def get_all_regional_codes(self) -> Dict[str, str]:
        """Fetch all regional codes."""
        _LOGGER.debug("Get all regional codes")
        raw_code_data: dict[str, Any] = await self._api.get_region_codes()

        regional_codes: Dict[str, str] = {}
        for data_block in raw_code_data["daten"]:
            region_id: str = data_block[0]
            name: str = data_block[1]

            if region_id[:5] in COUNTIES:
                name = f"{name} ({COUNTIES[region_id[:5]]})"

            if region_id[:2] not in CITY_STATES_CODE:
                region_id = region_id[: len(region_id) - 7] + "0000000"
                regional_codes[name] = region_id

            if (
                region_id[:2] in CITY_STATES_CODE
                and region_id[:2] + "0" * 10 == region_id
            ):
                regional_codes[name] = region_id

        return regional_codes
