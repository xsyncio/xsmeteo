from __future__ import annotations


from xsmeteo.models.base import BaseStruct


class ClimateResponse(BaseStruct, forbid_unknown_fields=False):
    """Response from the Climate Change API."""

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    daily_units: dict[str, str] | None = None
    daily: dict[str, list[float | int | str | None]] | None = None
