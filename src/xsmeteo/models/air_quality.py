from __future__ import annotations


from xsmeteo.models.base import BaseStruct


class AirQualityResponse(BaseStruct, forbid_unknown_fields=False):
    """Response from the Air Quality API."""

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float | None = None
    hourly_units: dict[str, str] | None = None
    hourly: dict[str, list[float | int | str | None]] | None = None
    hal_hourly_units: dict[str, str] | None = (
        None  # Specific to AQ? Keeping generic naming if unsure
    )
    current_units: dict[str, str] | None = None
    current: dict[str, float | int | str] | None = None
