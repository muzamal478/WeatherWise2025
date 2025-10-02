# Weather API Research Findings

## Overview
Researched weather APIs to select the best for the WeatherWise CLI app. Evaluated OpenWeatherMap, WeatherAPI, and AccuWeather based on documentation, free tier, and data coverage.

## APIs Evaluated
1. **OpenWeatherMap**:
   - **Pros**: Free tier (2,000 calls/day), clear documentation, supports current weather and 5-day forecast, JSON format.
   - **Cons**: Limited calls in free tier, requires API key.
   - **Endpoints**: `weather` (current), `forecast` (5-day).
2. **WeatherAPI**:
   - **Pros**: Free tier, simple API, astronomy data included.
   - **Cons**: Fewer calls (1,000/day), less detailed forecast.
3. **AccuWeather**:
   - **Pros**: Detailed data, location-based search.
   - **Cons**: Limited free tier, complex setup.

## Decision
Chose **OpenWeatherMap** for:
- Free tier sufficient for project (2,000 calls/day).
- Comprehensive endpoints: current weather (`/weather`), 3-day forecast (`/forecast`).
- Easy-to-parse JSON responses.
- Extensive documentation: [https://openweathermap.org/api](https://openweathermap.org/api).

## Next Steps
- Use API key for testing endpoints.
- Implement `weather.py` with city search and data display.