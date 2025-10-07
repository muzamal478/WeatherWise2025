import requests
import sys
import argparse
from tabulate import tabulate
from colorama import init, Fore, Style
import matplotlib.pyplot as plt
import datetime
import pytz
import os
from dotenv import load_dotenv

# Initialize colorama for colored terminal output
init()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/"
HISTORY_FILE = "data/search_history.txt"

def validate_api_key():
    """Validate the API key."""
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print(Fore.RED + "Error: Invalid or missing API key. Set a valid key in .env file." + Style.RESET_ALL)
        print("Get a key from: https://openweathermap.org/api")
        sys.exit(1)

def load_search_history():
    """Load the last 5 cities from search_history.txt."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return f.read().splitlines()[-5:]
        return []
    except Exception as e:
        print(Fore.RED + f"Error loading history: {e}" + Style.RESET_ALL)
        return []

def save_search_history(city):
    """Append a city to search_history.txt."""
    try:
        os.makedirs("data", exist_ok=True)
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(city + "\n")
    except Exception as e:
        print(Fore.RED + f"Error saving history: {e}" + Style.RESET_ALL)

def clear_search_history():
    """Clear search_history.txt."""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            print(Fore.GREEN + "Search history cleared!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error clearing history: {e}" + Style.RESET_ALL)

def fetch_weather(city):
    """Fetch current weather data for a city."""
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
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
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(Fore.RED + f"Error: Unauthorized API key for {city}. Please check your API key in .env." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error fetching weather for {city}: {e}" + Style.RESET_ALL)
        return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching weather for {city}: {e}" + Style.RESET_ALL)
        return None

def fetch_forecast(city):
    """Fetch 3-day forecast for a city."""
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        daily_data = []
        for forecast in data["list"][:24:8]:  # Every 24 hours (3 days)
            date = datetime.datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
            daily_data.append({
                "date": date,
                "temp": forecast["main"]["temp"],
                "condition": forecast["weather"][0]["description"]
            })
        return daily_data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(Fore.RED + f"Error: Unauthorized API key for {city}. Please check your API key in .env." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error fetching forecast for {city}: {e}" + Style.RESET_ALL)
        return []
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching forecast for {city}: {e}" + Style.RESET_ALL)
        return []

def check_weather_alerts(city):
    """Check for extreme weather conditions."""
    forecast = fetch_forecast(city)
    alerts = []
    for day in forecast:
        condition = day["condition"].lower()
        if any(extreme in condition for extreme in ["rain", "storm", "snow", "high wind"]):
            alerts.append(f"Warning: {condition.capitalize()} expected on {day['date']} in {city}. Stay safe!")
    return alerts

def plot_weather(data, cities, metric):
    """Plot temperature or humidity for multiple cities."""
    plt.figure(figsize=(8, 5))
    for city_data in data:
        dates = [d["date"] for d in city_data["forecast"]]
        values = [d[metric] for d in city_data["forecast"]]
        plt.plot(dates, values, marker="o", label=city_data["city"])
    plt.title(f"{metric.capitalize()} Over 3 Days")
    plt.xlabel("Date")
    plt.ylabel(metric.capitalize())
    plt.legend()
    plt.grid(True)
    plt.savefig(f"screenshots/{metric}_graph.png", dpi=300, bbox_inches="tight")
    plt.show()

def display_weather(cities, show_graph=False):
    """Display weather data for multiple cities."""
    validate_api_key()
    all_data = []
    for city in cities:
        save_search_history(city)
        weather = fetch_weather(city)
        if weather:
            forecast = fetch_forecast(city)
            alerts = check_weather_alerts(city)
            all_data.append({"city": weather["city"], "weather": weather, "forecast": forecast, "alerts": alerts})
    
    for data in all_data:
        print(Fore.CYAN + f"\nWeatherWise: {data['city']}" + Style.RESET_ALL)
        weather_table = [
            ["Temperature", f"{data['weather']['temp']}°C"],
            ["Humidity", f"{data['weather']['humidity']}%"],
            ["Condition", data['weather']['condition'].capitalize()],
            ["Wind Speed", f"{data['weather']['wind']} m/s"],
            ["Local Time", data['weather']['local_time']]
        ]
        print(tabulate(weather_table, headers=["Current Weather", ""], tablefmt="fancy_grid"))
        
        forecast_table = [[f["date"], f"{f['temp']}°C", f["condition"].capitalize()] for f in data["forecast"]]
        print("\n3-Day Forecast:")
        print(tabulate(forecast_table, headers=["Date", "Avg Temp", "Condition"], tablefmt="fancy_grid"))
        
        for alert in data["alerts"]:
            print(Fore.RED + alert + Style.RESET_ALL)
    
    if show_graph and all_data:
        plot_weather(all_data, cities, "temp")
        plot_weather(all_data, cities, "humidity")
    
    # Save multi-city output to file with plain format to avoid Unicode issues
    os.makedirs("screenshots", exist_ok=True)
    try:
        with open("screenshots/multi_city_output.txt", "w", encoding="utf-8") as f:
            for data in all_data:
                f.write(f"WeatherWise: {data['city']}\n")
                f.write(tabulate(weather_table, headers=["Current Weather", ""], tablefmt="plain") + "\n")
                f.write("3-Day Forecast:\n")
                f.write(tabulate(forecast_table, headers=["Date", "Avg Temp", "Condition"], tablefmt="plain") + "\n")
                for alert in data["alerts"]:
                    f.write(alert + "\n")
    except Exception as e:
        print(Fore.RED + f"Error saving output to file: {e}" + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description="WeatherWise CLI App")
    parser.add_argument("cities", nargs="?", default="London", help="Comma-separated city names (e.g., London,Paris)")
    parser.add_argument("--graph", action="store_true", help="Show temperature/humidity graphs")
    parser.add_argument("--history", action="store_true", help="Show search history")
    parser.add_argument("--clear-history", action="store_true", help="Clear search history")
    args = parser.parse_args()

    if args.clear_history:
        clear_search_history()
        return
    
    if args.history:
        history = load_search_history()
        if history:
            print(Fore.YELLOW + "Recent Searches (Last 5):" + Style.RESET_ALL)
            print("\n".join(history))
        else:
            print(Fore.YELLOW + "No search history found." + Style.RESET_ALL)
        return

    cities = [city.strip() for city in args.cities.split(",")]
    display_weather(cities, args.graph)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting WeatherWise..." + Style.RESET_ALL)
        sys.exit(0)