# WeatherWise Unit and Integration Tests
# Author: Muzamil Asghar
# Date: October 14, 2025

import pytest
import asyncio
import aiohttp
from weather import fetch_weather, fetch_forecast, load_config, save_config, load_search_history, save_search_history, check_weather_alerts

@pytest.mark.asyncio
async def test_fetch_weather():
    async with aiohttp.ClientSession() as session:
        result = await fetch_weather("London", session, units="metric")
        assert result is not None
        assert "city" in result
        assert result["city"] == "London"

@pytest.mark.asyncio
async def test_fetch_forecast():
    async with aiohttp.ClientSession() as session:
        result = await fetch_forecast("London", session, units="metric")
        assert isinstance(result, list)
        assert len(result) <= 3

def test_load_config():
    config = load_config()
    assert config["default_city"] == "London"
    assert config["units"] == "metric"

def test_save_config():
    config = {"default_city": "London", "units": "imperial", "last_api_key": None}
    save_config(config)
    loaded = load_config()
    assert loaded["default_city"] == "London"
    assert loaded["units"] == "imperial"

def test_search_history():
    save_search_history("TestCity")
    history = load_search_history()
    assert "TestCity" in history

def test_check_weather_alerts():
    forecast = [{"date": "2025-10-15", "temp": 10, "condition": "rain"}]
    alerts = check_weather_alerts(forecast)
    assert len(alerts) == 1
    assert "rain" in alerts[0].lower()