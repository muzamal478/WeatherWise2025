# WeatherWise CLI App - Week 3 Implementation
# Author: Muzamil Asghar
# Date: October 14, 2025
# Description: Enhanced CLI app with async API calls, rich visualizations, user configs,
# data exports, subcommands, and testing.

import asyncio
import aiohttp
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import pandas as pd
import datetime
import pytz
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
import requests_cache
import json

# Initialize rich console
console = Console()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/"
HISTORY_FILE = "data/search_history.txt"
CONFIG_FILE = "config.yaml"
EXPORT_DIR = "exports"

# Weather condition icons
WEATHER_ICONS = {
    "clear": "☀️", "clouds": "☁️", "rain": "🌧️", "storm": "🌩️", "snow": "❄️"
}

def load_config():
    """Load user configuration from config.yaml."""
    default_config = {"default_city": "London", "units": "metric", "last_api_key": None}
    try:
        if Path(CONFIG_FILE).exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or default_config
                return config
        return default_config
    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/red]")
        return default_config

def save_config(config):
    """Save user configuration to config.yaml."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f)
    except Exception as e:
        console.print(f"[red]Error saving config: {e}[/red]")

def reset_config():
    """Reset config.yaml to default."""
    default_config = {"default_city": "London", "units": "metric", "last_api_key": None}
    save_config(default_config)
    console.print("[green]Configuration reset to default![/green]")

def load_search_history():
    """Load the last 5 cities from search_history.txt."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return f.read().splitlines()[-5:]
        return []
    except Exception as e:
        console.print(f"[red]Error loading history: {e}[/red]")
        return []

def save_search_history(city):
    """Append a city to search_history.txt."""
    try:
        os.makedirs("data", exist_ok=True)
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(city + "\n")
    except Exception as e:
        console.print(f"[red]Error saving history: {e}[/red]")

def clear_search_history():
    """Clear search_history.txt."""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            console.print("[green]Search history cleared![/green]")
    except Exception as e:
        console.print(f"[red]Error clearing history: {e}[/red]")

async def fetch_weather(city, session, units="metric"):
    """Fetch current weather data asynchronously for a city."""
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units={units}"
    try:
        async with session.get(url, timeout=5) as response:
            response.raise_for_status()
            data = await response.json()
            timezone_offset = data["timezone"]  # Seconds from UTC
            local_time = datetime.datetime.now(pytz.UTC) + datetime.timedelta(seconds=timezone_offset)
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind": data["wind"]["speed"],
                "local_time": local_time.strftime("%Y-%m-%d %H:%M")
            }
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            console.print(f"[red]Unauthorized API key for {city}. Check .env.[/red]")
        else:
            console.print(f"[red]Error fetching weather for {city}: {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Error fetching weather for {city}: {e}[/red]")
        return None

async def fetch_forecast(city, session, units="metric"):
    """Fetch 3-day forecast asynchronously for a city."""
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units={units}"
    try:
        async with session.get(url, timeout=5) as response:
            response.raise_for_status()
            data = await response.json()
            daily_data = []
            for forecast in data["list"][:24:8]:  # Every 24 hours (3 days)
                date = datetime.datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
                daily_data.append({
                    "date": date,
                    "temp": forecast["main"]["temp"],
                    "condition": forecast["weather"][0]["description"]
                })
            return daily_data
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            console.print(f"[red]Unauthorized API key for {city}. Check .env.[/red]")
        else:
            console.print(f"[red]Error fetching forecast for {city}: {e}[/red]")
        return []
    except Exception as e:
        console.print(f"[red]Error fetching forecast for {city}: {e}[/red]")
        return []

def check_weather_alerts(forecast):
    """Check for extreme weather conditions."""
    alerts = []
    for day in forecast:
        condition = day["condition"].lower()
        if any(extreme in condition for extreme in ["rain", "storm", "snow", "high wind"]):
            alerts.append(f"Warning: {condition.capitalize()} expected on {day['date']}. Stay safe!")
    return alerts

def plot_weather(data, metric, units):
    """Plot temperature or humidity for multiple cities."""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 5))
    for city_data in data:
        dates = [d["date"] for d in city_data["forecast"]]
        values = [d[metric] for d in city_data["forecast"]]
        plt.plot(dates, values, marker="o", label=city_data["city"])
    plt.title(f"{metric.capitalize()} Over 3 Days ({'°C' if units == 'metric' else '°F'})")
    plt.xlabel("Date")
    plt.ylabel(metric.capitalize())
    plt.legend()
    plt.grid(True)
    plt.savefig(f"screenshots/{metric}_graph.png", dpi=300, bbox_inches="tight")
    plt.show()

def export_weather_data(all_data, export_type, filename):
    """Export weather data to CSV or JSON using pandas."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filepath = Path(EXPORT_DIR) / filename
    data_list = []
    for data in all_data:
        for forecast in data["forecast"]:
            data_list.append({
                "city": data["city"],
                "date": forecast["date"],
                "temperature": forecast["temp"],
                "humidity": data["weather"]["humidity"],
                "condition": forecast["condition"]
            })
    df = pd.DataFrame(data_list)
    try:
        if export_type == "csv":
            df.to_csv(filepath, index=False, encoding="utf-8")
            console.print(f"[green]Exported to {filepath}[/green]")
        elif export_type == "json":
            df.to_json(filepath, orient="records", lines=True)
            console.print(f"[green]Exported to {filepath}[/green]")
    except Exception as e:
        console.print(f"[red]Error exporting data: {e}[/red]")

def generate_summary(all_data, units):
    """Generate a summary report of weather data."""
    data_list = []
    for data in all_data:
        temps = [f["temp"] for f in data["forecast"]]
        data_list.append({
            "city": data["city"],
            "avg_temp": sum(temps) / len(temps) if temps else 0,
            "avg_humidity": data["weather"]["humidity"]
        })
    df = pd.DataFrame(data_list)
    table = Table(title="Weather Summary")
    table.add_column("City", style="cyan")
    table.add_column("Avg Temp", style="magenta")
    table.add_column("Avg Humidity", style="green")
    for _, row in df.iterrows():
        table.add_row(row["city"], f"{row['avg_temp']:.2f}{'°C' if units == 'metric' else '°F'}", f"{row['avg_humidity']}%")
    console.print(table)
    try:
        with open("screenshots/summary_report.txt", "w", encoding="utf-8") as f:
            f.write(str(table))
        console.print("[green]Summary saved to screenshots/summary_report.txt[/green]")
    except Exception as e:
        console.print(f"[red]Error saving summary: {e}[/red]")

async def display_weather(cities, units="metric", show_graph=False, export_type=None, export_file=None, summary=False):
    """Display weather data for multiple cities with progress bar."""
    validate_api_key()
    all_data = []
    requests_cache.install_cache("weather_cache", backend="sqlite", expire_after=3600)
    
    async with aiohttp.ClientSession() as session:
        with Progress() as progress:
            task = progress.add_task("[cyan]Fetching weather data...", total=len(cities) * 2)
            for city in cities:
                save_search_history(city)
                weather_task = fetch_weather(city, session, units)
                forecast_task = fetch_forecast(city, session, units)
                weather, forecast = await asyncio.gather(weather_task, forecast_task)
                progress.advance(task)
                if weather:
                    alerts = check_weather_alerts(forecast)
                    all_data.append({"city": weather["city"], "weather": weather, "forecast": forecast, "alerts": alerts})
                progress.advance(task)
    
    for data in all_data:
        # Current weather table
        table = Table(title=f"WeatherWise: {data['city']}", title_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        condition = data["weather"]["condition"].lower()
        icon = next((icon for key, icon in WEATHER_ICONS.items() if key in condition), "🌍")
        table.add_row("Temperature", f"{data['weather']['temp']}{'°C' if units == 'metric' else '°F'}")
        table.add_row("Humidity", f"{data['weather']['humidity']}%")
        table.add_row("Condition", f"{icon} {data['weather']['condition'].capitalize()}")
        table.add_row("Wind Speed", f"{data['weather']['wind']} m/s")
        table.add_row("Local Time", data["weather"]["local_time"])
        console.print(table)
        
        # Forecast table
        forecast_table = Table(title="3-Day Forecast")
        forecast_table.add_column("Date", style="cyan")
        forecast_table.add_column("Avg Temp", style="magenta")
        forecast_table.add_column("Condition", style="green")
        for f in data["forecast"]:
            condition = f["condition"].lower()
            icon = next((icon for key, icon in WEATHER_ICONS.items() if key in condition), "🌍")
            forecast_table.add_row(f["date"], f"{f['temp']}{'°C' if units == 'metric' else '°F'}", f"{icon} {f['condition'].capitalize()}")
        console.print(forecast_table)
        
        # Alerts
        for alert in data["alerts"]:
            console.print(f"[red]{alert}[/red]")
    
    if export_type and export_file and all_data:
        export_weather_data(all_data, export_type, export_file)
    
    if summary and all_data:
        generate_summary(all_data, units)
    
    if show_graph and all_data:
        plot_weather(all_data, "temp", units)
        plot_weather(all_data, "humidity", units)

def validate_api_key():
    """Validate the API key."""
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        console.print("[red]Error: Invalid or missing API key. Set a valid key in .env file.[/red]")
        console.print("Get a key from: https://openweathermap.org/api")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="WeatherWise CLI App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch weather data")
    fetch_parser.add_argument("cities", nargs="?", default=load_config()["default_city"], help="Comma-separated city names")
    fetch_parser.add_argument("--graph", action="store_true", help="Show graphs")
    fetch_parser.add_argument("--units", choices=["metric", "imperial"], default=load_config()["units"], help="Temperature units")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export weather data")
    export_parser.add_argument("cities", nargs="?", default=load_config()["default_city"], help="Comma-separated city names")
    export_parser.add_argument("--type", choices=["csv", "json"], required=True, help="Export format")
    export_parser.add_argument("--file", required=True, help="Export filename")
    export_parser.add_argument("--units", choices=["metric", "imperial"], default=load_config()["units"], help="Temperature units")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Generate weather summary")
    summary_parser.add_argument("cities", nargs="?", default=load_config()["default_city"], help="Comma-separated city names")
    summary_parser.add_argument("--units", choices=["metric", "imperial"], default=load_config()["units"], help="Temperature units")

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--default-city", help="Set default city")
    config_parser.add_argument("--units", choices=["metric", "imperial"], help="Set temperature units")
    config_parser.add_argument("--reset", action="store_true", help="Reset configuration")

    # History command
    history_parser = subparsers.add_parser("history", help="Show search history")
    history_parser.add_argument("--clear", action="store_true", help="Clear search history")

    args = parser.parse_args()

    config = load_config()

    if args.command == "config":
        if args.reset:
            reset_config()
            return
        if args.default_city or args.units:
            config["default_city"] = args.default_city or config["default_city"]
            config["units"] = args.units or config["units"]
            save_config(config)
            console.print("[green]Configuration updated![/green]")
        else:
            console.print("[yellow]Current configuration:[/yellow]")
            console.print(config)
        return

    if args.command == "history":
        if args.clear:
            clear_search_history()
        else:
            history = load_search_history()
            if history:
                console.print("[yellow]Recent Searches (Last 5):[/yellow]")
                for city in history:
                    console.print(city)
            else:
                console.print("[yellow]No search history found.[/yellow]")
        return

    cities = [city.strip() for city in args.cities.split(",")]
    if not cities or not args.cities.strip():
        console.print("[red]Error: At least one city is required.[/red]")
        sys.exit(1)

    asyncio.run(display_weather(
        cities,
        units=args.units,
        show_graph=args.graph if hasattr(args, "graph") else False,
        export_type=args.type if hasattr(args, "type") else None,
        export_file=args.file if hasattr(args, "file") else None,
        summary=args.command == "summary"
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]Exiting WeatherWise...[/red]")
        sys.exit(0)