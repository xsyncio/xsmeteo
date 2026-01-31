from __future__ import annotations

from typing import TYPE_CHECKING, cast
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from xsmeteo.client.async_client import AsyncXSMeteo
from xsmeteo.exceptions import DecodeError, HTTPError
from xsmeteo.models.forecast import ForecastResponse
from xsmeteo.models.historical import HistoricalResponse

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture
async def client() -> AsyncGenerator[AsyncXSMeteo, None]:
    async with AsyncXSMeteo() as client:
        # Mock the internal httpx client
        client._client = AsyncMock(spec=httpx.AsyncClient)
        yield client


@pytest.mark.asyncio
async def test_get_forecast_success(client: AsyncXSMeteo) -> None:
    # Arrange
    # Use a comprehensive JSON response covering all fields in ForecastResponse
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = (
        b"{"
        b'"latitude": 52.52,'
        b'"longitude": 13.41,'
        b'"generationtime_ms": 2.2,'
        b'"utc_offset_seconds": 3600,'
        b'"timezone": "Europe/Berlin",'
        b'"timezone_abbreviation": "CET",'
        b'"elevation": 38.0,'
        b'"current_units": {"time": "iso8601", "temperature_2m": "C"},'
        b'"current": {"time": "2023-01-01T12:00", "temperature_2m": 12.5},'
        b'"hourly_units": {"time": "iso8601", "temperature_2m": "C", "rain": "mm"},'
        b'"hourly": {'
        b'  "time": ["2023-01-01T00:00", "2023-01-01T01:00"],'
        b'  "temperature_2m": [10.5, 9.8],'
        b'  "rain": [0.0, 0.2]'
        b"},"
        b'"daily_units": {"time": "iso8601", "temperature_2m_max": "C"},'
        b'"daily": {'
        b'  "time": ["2023-01-01"],'
        b'  "temperature_2m_max": [15.2]'
        b"}"
        b"}"
    )
    cast("AsyncMock", client._client.get).return_value = mock_response

    # Act
    result = await client.get_forecast(
        latitude=52.52,
        longitude=13.41,
        current=["temperature_2m"],
        hourly=["temperature_2m", "rain"],
        daily=["temperature_2m_max"],
    )

    # Assert
    assert isinstance(result, ForecastResponse)

    # 1. Verify Metadata
    assert result.latitude == 52.52
    assert result.longitude == 13.41
    assert result.generationtime_ms == 2.2
    assert result.utc_offset_seconds == 3600
    assert result.timezone == "Europe/Berlin"
    assert result.timezone_abbreviation == "CET"
    assert result.elevation == 38.0

    # 2. Verify Current Data (Dynamic Dict)
    assert result.current is not None
    assert result.current["time"] == "2023-01-01T12:00"
    assert result.current["temperature_2m"] == 12.5
    assert result.current_units is not None
    assert result.current_units["temperature_2m"] == "C"

    # 3. Verify Hourly Data (Dynamic Dict with list values)
    assert result.hourly is not None
    # Check lists length
    assert len(result.hourly["time"]) == 2
    assert result.hourly["temperature_2m"] == [10.5, 9.8]
    assert result.hourly["rain"] == [0.0, 0.2]
    # Check units
    assert result.hourly_units is not None
    assert result.hourly_units["temperature_2m"] == "C"
    assert result.hourly_units["rain"] == "mm"

    # 4. Verify Daily Data (Dynamic Dict with list values)
    assert result.daily is not None
    assert result.daily["time"] == ["2023-01-01"]
    assert result.daily["temperature_2m_max"] == [15.2]
    assert result.daily_units is not None
    assert result.daily_units["temperature_2m_max"] == "C"

    cast("AsyncMock", client._client.get).assert_called_once()


@pytest.mark.asyncio
async def test_get_historical_success(client: AsyncXSMeteo) -> None:
    # Arrange
    # Use a comprehensive JSON response
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = (
        b"{"
        b'"latitude": 52.52,'
        b'"longitude": 13.41,'
        b'"generationtime_ms": 2.2,'
        b'"utc_offset_seconds": 3600,'
        b'"timezone": "Europe/Berlin",'
        b'"timezone_abbreviation": "CET",'
        b'"elevation": 38.0,'
        b'"daily_units": {"time": "iso8601", "temperature_2m_max": "C"},'
        b'"daily": {'
        b'  "time": ["2022-01-01"],'
        b'  "temperature_2m_max": [15.0]'
        b"}"
        b"}"
    )
    cast("AsyncMock", client._client.get).return_value = mock_response

    # Act
    result = await client.get_historical(
        latitude=52.52,
        longitude=13.41,
        start_date="2022-01-01",
        end_date="2022-01-02",
        daily=["temperature_2m_max"],
    )

    # Assert
    assert isinstance(result, HistoricalResponse)
    assert result.latitude == 52.52
    assert result.longitude == 13.41
    assert result.generationtime_ms == 2.2
    assert result.utc_offset_seconds == 3600
    assert result.timezone == "Europe/Berlin"
    assert result.timezone_abbreviation == "CET"
    assert result.elevation == 38.0

    # Verify dynamic field access
    assert result.daily is not None
    assert result.daily["time"] == ["2022-01-01"]
    assert result.daily["temperature_2m_max"] == [15.0]
    assert result.daily_units is not None
    assert result.daily_units["temperature_2m_max"] == "C"

    cast("AsyncMock", client._client.get).assert_called_once()


@pytest.mark.asyncio
async def test_get_forecast_http_error(client: AsyncXSMeteo) -> None:
    # Arrange
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.content = b'{"error": true, "reason": "Invalid parameters"}'
    mock_response.text = '{"error": true, "reason": "Invalid parameters"}'
    cast("AsyncMock", client._client.get).return_value = mock_response

    # Act & Assert
    with pytest.raises(HTTPError) as exc_info:
        await client.get_forecast(latitude=52.52, longitude=13.41)

    assert str(exc_info.value) == "400: Invalid parameters"
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_get_forecast_decode_error(client: AsyncXSMeteo) -> None:
    # Arrange
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = b"invalid json"
    cast("AsyncMock", client._client.get).return_value = mock_response

    # Act & Assert
    with pytest.raises(DecodeError):
        await client.get_forecast(latitude=52.52, longitude=13.41)


@pytest.mark.asyncio
async def test_search_locations_success(client: AsyncXSMeteo) -> None:
    # Arrange
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.content = (
        b'{"results": [{"id": 1, "name": "Berlin", "latitude": 52.52, "longitude": 13.41}]}'
    )
    cast("AsyncMock", client._client.get).return_value = mock_response

    # Act
    result = await client.search_locations(name="Berlin")

    # Assert
    assert result.results is not None
    assert len(result.results) == 1
    assert result.results[0].name == "Berlin"
