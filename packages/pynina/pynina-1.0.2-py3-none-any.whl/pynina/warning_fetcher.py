from typing import Any
import html

from .label_matcher import ActionLabelMatcher
from .nina_api import NinaAPI
from .warning import Warning


class WarningFetcher:
    """Class to fetch warnings for a region."""

    def __init__(self, api: NinaAPI, label_matcher: ActionLabelMatcher):
        """Initialize."""
        self._api = api
        self._label_matcher = label_matcher

    async def fetch_warnings(self, region_code: str) -> list[Warning]:
        """Fetch warnings for the given region."""
        warnings: list[Warning] = []

        raw_warnings = await self._api.get_warnings(region_code)

        for warning_data in raw_warnings:
            warning_details = await self._api.get_warning_details(
                warning_data["payload"]["id"]
            )
            warnings.append(self._build_from_data(warning_data, warning_details))

        return warnings

    def _build_from_data(
        self, warning_data: dict[str, Any], warning_details: dict[str, Any]
    ) -> Warning:
        """Build a Warning object from the data."""
        infos = warning_details["info"][0]

        warning_id: str = warning_data["payload"]["id"]
        headline: str = warning_data["payload"]["data"]["headline"]
        severity: str = warning_data["payload"]["data"]["severity"]

        description: str | None = (
            html.unescape(infos.get("description", ""))
            if "description" in infos
            else None
        )
        sender: str | None = infos.get("senderName", None)
        areas: list[str] = [area["areaDesc"] for area in infos.get("area", [])]
        web: str | None = infos.get("web", None)
        time_send: str = warning_data["sent"]
        time_start: str | None = warning_data.get(
            "effective", warning_data.get("onset", None)
        )
        time_expire: str | None = warning_data.get("expires", None)

        recommended_actions: list[str] = (
            [infos.get("instruction", "").replace("<br/>", " ")]
            if "instruction" in infos
            else []
        )

        if len(recommended_actions) == 0:
            recommended_actions_codes: list[str] = [
                parameter["value"].split(" ")
                for parameter in infos.get("parameter", {})
                if parameter["valueName"] == "instructionCode"
            ]
            recommended_actions = [
                self._label_matcher.match(code) for code in recommended_actions_codes
            ]

        return Warning(
            warning_id,
            headline,
            severity,
            description,
            sender,
            areas,
            recommended_actions,
            web,
            time_send,
            time_start,
            time_expire,
        )
