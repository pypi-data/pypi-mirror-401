from unittest.mock import create_autospec

import pytest

from pynina.api_client import APIClient
from pynina.const import (
    ENDPOINT_DE_LABELS,
    ENDPOINT_NINA_BASE,
    ENDPOINT_REGIONAL_CODE,
    ENDPOINT_WARNING_DETAIL,
)
from pynina.nina_api import NinaAPI


@pytest.mark.asyncio
async def test_get_warnings_url():
    """Test if the correct URL is used for fetching warnings."""
    dummy_data = [{"payload": {"id": "some_id"}}]

    mock = create_autospec(APIClient)
    mock.make_request.return_value = dummy_data

    api = NinaAPI(mock)
    result = await api.get_warnings("10044")

    assert result == dummy_data
    mock.make_request.assert_called_with(ENDPOINT_NINA_BASE + "10044.json")


@pytest.mark.asyncio
async def test_get_warning_details_url():
    """Test if the correct URL is used for fetching warnings details."""
    dummy_data = {"payload": {"id": "some_id"}}

    mock = create_autospec(APIClient)
    mock.make_request.return_value = dummy_data

    api = NinaAPI(mock)
    result = await api.get_warning_details("10044")

    assert result == dummy_data
    mock.make_request.assert_called_with(ENDPOINT_WARNING_DETAIL + "10044.json")


@pytest.mark.asyncio
async def test_get_region_codes_url():
    """Test if the correct URL is used for fetching region codes."""
    dummy_data = {"payload": {"id": "some_id"}}

    mock = create_autospec(APIClient)
    mock.make_request.return_value = dummy_data

    api = NinaAPI(mock)
    result = await api.get_region_codes()

    assert result == dummy_data
    mock.make_request.assert_called_with(ENDPOINT_REGIONAL_CODE)


@pytest.mark.asyncio
async def test_get_labels_url():
    """Test if the correct URL is used for fetching labels."""
    dummy_data = {"payload": {"id": "some_id"}}

    mock = create_autospec(APIClient)
    mock.make_request.return_value = dummy_data

    api = NinaAPI(mock)
    result = await api.get_labels()

    assert result == dummy_data
    mock.make_request.assert_called_with(ENDPOINT_DE_LABELS)
