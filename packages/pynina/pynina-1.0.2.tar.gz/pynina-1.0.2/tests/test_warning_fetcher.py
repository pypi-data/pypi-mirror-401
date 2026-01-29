from unittest.mock import create_autospec

import pytest

from pynina import Warning
from pynina.label_matcher import ActionLabelMatcher
from pynina.nina_api import NinaAPI
from pynina.warning_fetcher import WarningFetcher
from tests import load_fixture


@pytest.mark.asyncio
async def test_fetch_warnings():
    """Test if the warnings are correctly generated."""
    matcher = create_autospec(ActionLabelMatcher)
    api = create_autospec(NinaAPI)

    api.get_warnings.return_value = load_fixture("warnings.json")
    api.get_warning_details.return_value = load_fixture("warnings-details.json")

    fetcher = WarningFetcher(api, matcher)

    result = await fetcher.fetch_warnings("10044")

    assert len(result) == 1
    assert result[0] == Warning(
        "mow.DE-BW-S-SE018-20211102-18-001",
        "Corona-Verordnung des Landes: Warnstufe durch Landesgesundheitsamt ausgerufen",
        "Minor",
        "Die Zahl der mit dem Corona-Virus infizierten Menschen steigt gegenwärtig stark an. Es wächst daher die Gefahr einer weiteren Verbreitung der Infektion und - je nach Einzelfall - auch von schweren Erkrankungen.",
        None,
        [
            "Bundesland: Freie Hansestadt Bremen, Land Berlin, Land Hessen, Land Nordrhein-Westfalen, Land Brandenburg, Freistaat Bayern, Land Mecklenburg-Vorpommern, Land Rheinland-Pfalz, Freistaat Sachsen, Land Schleswig-Holstein, Freie und Hansestadt Hamburg, Freistaat Thüringen, Land Niedersachsen, Land Saarland, Land Sachsen-Anhalt, Land Baden-Württemberg"
        ],
        ["Waschen sich regelmäßig und gründlich die Hände."],
        None,
        "2021-11-02T20:07:16+01:00",
        None,
        None,
    )

    api.get_warnings.assert_called_with("10044")
    api.get_warning_details.assert_called_with("mow.DE-BW-S-SE018-20211102-18-001")
