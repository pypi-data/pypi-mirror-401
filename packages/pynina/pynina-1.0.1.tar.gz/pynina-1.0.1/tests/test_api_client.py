import asyncio
import json

import pytest
from aiohttp import ClientConnectionError, ClientSession
from aioresponses import aioresponses

from pynina.api_client import APIClient, ApiError

SAMPLE_URL = "https://example.com"
SAMPLE_BODY = {"key": "value"}
SAMPLE_BODY_JSON = json.dumps(SAMPLE_BODY)


@pytest.mark.asyncio
async def test_successful_request():
    client = APIClient()

    with aioresponses() as m:
        m.get(SAMPLE_URL, status=200, body=SAMPLE_BODY_JSON)

        result = await client.make_request(SAMPLE_URL)

        assert result == SAMPLE_BODY


@pytest.mark.asyncio
async def test_failed_request():
    client = APIClient()

    with aioresponses() as m:
        m.get(SAMPLE_URL, status=401)

        with pytest.raises(ApiError, match="Invalid response: 401"):
            await client.make_request(SAMPLE_URL)


@pytest.mark.asyncio
async def test_timed_out_request():
    client = APIClient()

    with aioresponses() as m:
        m.get(SAMPLE_URL, exception=asyncio.TimeoutError())

        with pytest.raises(ApiError, match=f"Could not connect to {SAMPLE_URL}"):
            await client.make_request(SAMPLE_URL)


@pytest.mark.asyncio
async def test_connection_error():
    client = APIClient()

    with aioresponses() as m:
        m.get(SAMPLE_URL, exception=ClientConnectionError())

        with pytest.raises(ApiError, match=f"Could not connect to {SAMPLE_URL}"):
            await client.make_request(SAMPLE_URL)


@pytest.mark.asyncio
async def test_external_session_not_closed():
    session = ClientSession()
    client = APIClient(session)

    with aioresponses() as m:
        m.get(SAMPLE_URL, status=200, body=SAMPLE_BODY_JSON)

        await client.make_request(SAMPLE_URL)

        assert not session.closed
