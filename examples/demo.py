"""
xsmeteo Demo Script
Run this script to see the library in action!
"""

from __future__ import annotations

import asyncio

from xsmeteo import AsyncXSMeteo, XSMeteo


def run_sync_demo() -> None:
    print("--- Synchronous Client Demo ---")
    with XSMeteo() as client:
        # 1. Forecast
        print("Fetching forecast for Berlin...")
        forecast = client.get_forecast(
            latitude=52.52,
            longitude=13.41,
            hourly=["temperature_2m", "rain"],
            timezone="auto",
        )
        if forecast.hourly:
            count = len(forecast.hourly["temperature_2m"])
            print(f"Success! Received forecast with {count} data points.")
            print(f"Current temp (approx): {forecast.hourly['temperature_2m'][0]}°C\n")

        # 2. Geocoding
        print("Searching for 'New York'...")
        search = client.search_locations(name="New York", count=1)
        if search.results:
            city = search.results[0]
            lat, lon = city.latitude, city.longitude
            print(f"Found: {city.name}, {city.country} ({lat:.2f}, {lon:.2f})\n")


async def run_async_demo() -> None:
    print("--- Asynchronous Client Demo ---")
    async with AsyncXSMeteo() as client:
        # 1. Historical Data
        print("Fetching historical data (yesterday)...")
        historical = await client.get_historical(
            latitude=52.52,
            longitude=13.41,
            start_date="2023-01-01",
            end_date="2023-01-02",
            hourly=["temperature_2m"],
        )
        if historical.hourly:
            count = len(historical.hourly["temperature_2m"])
            print(f"Success! Received {count} historical data points.\n")


def main() -> None:
    # Run Sync
    run_sync_demo()

    # Run Async
    asyncio.run(run_async_demo())


if __name__ == "__main__":
    main()
