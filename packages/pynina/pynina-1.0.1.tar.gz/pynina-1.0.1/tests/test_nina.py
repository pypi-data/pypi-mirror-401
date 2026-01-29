from unittest.mock import patch

import pytest

from pynina import Nina, Warning
from tests import load_fixture


@pytest.mark.asyncio
async def test_nina_update_no_regions():
    """Test if the update method handles no regions correctly."""
    with (
        patch("pynina.warning_fetcher.WarningFetcher.fetch_warnings") as fetcher_mock,
        patch("pynina.label_matcher.ActionLabelMatcher.init") as matcher_mock,
    ):
        nina = Nina()

        assert len(nina.warnings) == 0

        await nina.update()

        assert len(nina.warnings) == 0
        fetcher_mock.assert_not_called()
        matcher_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_nina_update_with_regions():
    """Test if the update method handles multiple regions updates."""
    dummy_warning = Warning(
        "id",
        "headline",
        "severity",
        "description",
        "sender",
        [],
        [],
        "web",
        "sent",
        "start",
        "expires",
    )

    with (
        patch(
            "pynina.warning_fetcher.WarningFetcher.fetch_warnings",
            return_value=[dummy_warning, dummy_warning],
        ) as fetcher_mock,
        patch("pynina.label_matcher.ActionLabelMatcher.init") as matcher_mock,
    ):
        nina = Nina()

        assert len(nina.warnings) == 0

        regions = ["10000", "20000"]

        for region in regions:
            nina.add_region(region)

        await nina.update()

        assert len(nina.warnings) == len(regions)
        matcher_mock.assert_awaited_once()

        for region in regions:
            fetcher_mock.assert_any_call(region)


@pytest.mark.asyncio
async def test_regional_codes():
    """Test if the regional codes are fetched correctly and the codes are shorted properly."""
    region_data = load_fixture("region_codes.json")

    with patch("pynina.nina_api.NinaAPI.get_region_codes", return_value=region_data):
        nina = Nina()

        result = await nina.get_all_regional_codes()
        assert len(result)

        assert result["Waltenhofen (Oberallgäu - Bayern)"] == "097800000000"


@pytest.mark.asyncio
async def test_regional_codes_add_county():
    """Test if counties are added to the list correctly."""
    region_data = load_fixture("region_codes.json")

    with patch("pynina.nina_api.NinaAPI.get_region_codes", return_value=region_data):
        nina = Nina()

        result = await nina.get_all_regional_codes()

        assert (
            result["Brunsbüttel, Stadt (Dithmarschen - Schleswig-Holstein)"]
            == "010510000000"
        )
