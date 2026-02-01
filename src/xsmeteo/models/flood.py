from __future__ import annotations

from xsmeteo.models.base import BaseStruct


class FloodResponse(BaseStruct, forbid_unknown_fields=False):
    """Response from the Flood API."""

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int | None = None
    timezone: str | None = None
    timezone_abbreviation: str | None = None
    daily_units: dict[str, str] | None = None
    daily: dict[str, list[float | int | str | None]] | None = None
