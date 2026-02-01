"""xsmeteo - High-performance, strictly typed Python wrapper for Open-Meteo API."""

from __future__ import annotations

from xsmeteo.client import AsyncXSMeteo, XSMeteo
from xsmeteo.core import (
    DEFAULT_RATE_LIMITS,
    ENDPOINTS,
    APIEndpoints,
    RateLimitConfig,
    RateLimiter,
)
from xsmeteo.exceptions import (
    DecodeError,
    HTTPError,
    RateLimitError,
    RequestError,
    XSMeteoError,
)
from xsmeteo.models import (
    AirQualityResponse,
    BaseStruct,
    ClimateResponse,
    ElevationResponse,
    EnsembleResponse,
    FloodResponse,
    ForecastResponse,
    GeocodingResponse,
    GeocodingResult,
    HistoricalResponse,
    MarineResponse,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit,
)

__version__ = "0.1.1"

__all__ = [
    "DEFAULT_RATE_LIMITS",
    "ENDPOINTS",
    "APIEndpoints",
    "AirQualityResponse",
    "AsyncXSMeteo",
    "BaseStruct",
    "ClimateResponse",
    "DecodeError",
    "ElevationResponse",
    "EnsembleResponse",
    "FloodResponse",
    "ForecastResponse",
    "GeocodingResponse",
    "GeocodingResult",
    "HTTPError",
    "HistoricalResponse",
    "MarineResponse",
    "PrecipitationUnit",
    "RateLimitConfig",
    "RateLimitError",
    "RateLimiter",
    "RequestError",
    "TemperatureUnit",
    "TimeFormat",
    "WindSpeedUnit",
    "XSMeteo",
    "XSMeteoError",
]
