from __future__ import annotations

from xsmeteo.models.base import BaseStruct


class MarineResponse(BaseStruct, forbid_unknown_fields=False):
    """Response from the Marine Weather API."""

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float | None = None
    hourly_units: dict[str, str] | None = None
    hourly: dict[str, list[float | int | str | None]] | None = None
    daily_units: dict[str, str] | None = None
    daily: dict[str, list[float | int | str | None]] | None = None
