# WeatherWise CLI App Feature Plan

## Basic Features
1. **Search by City Name**:
   - Input: User enters city name via CLI (e.g., `python weather.py London`).
   - Action: Query OpenWeatherMap `/weather` endpoint.

2. **Current Weather**:
   - Display: Temperature (°C), humidity (%), weather condition (e.g., Clear), wind speed (m/s).
   - Format: Tabular output using `tabulate`, colored with `colorama`.

3. **3-Day Forecast**:
   - Display: Daily summary (date, avg temperature, condition) for next 3 days.
   - Action: Query `/forecast` endpoint, aggregate data.

## Implementation Plan
- **Week 2**:
  - Fetch current weather data using `requests`.
  - Parse JSON for temperature, humidity, condition, wind.
  - Format output with `tabulate` and `colorama`.
  - Fetch and summarize 3-day forecast.
  
- **Week 3**: Add error handling (e.g., invalid city, API errors), unit conversion (°C/°F).

## Expected Output Example
```
WeatherWise: London
+-------------------+----------------+
| Current Weather   |                |
+-------------------+----------------+
| Temperature       | 15°C           |
| Humidity          | 70%            |
| Condition         | Partly Cloudy  |
| Wind Speed        | 5 m/s          |
+-------------------+----------------+

3-Day Forecast:
+------------+-------------+----------------+
| Date       | Avg Temp    | Condition      |
+------------+-------------+----------------+
| 2025-10-07 | 14°C        | Rain           |
| 2025-10-08 | 16°C        | Clear          |
| 2025-10-09 | 13°C        | Cloudy         |
+------------+-------------+----------------+
```