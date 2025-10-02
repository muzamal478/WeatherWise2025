# WeatherWise CLI App - Week 1 Scaffold
# Author: Muzamil Asghar
# Date: October 2, 2025
# Description: Initial scaffold for a command-line weather app using OpenWeather API

import requests
import sys
from tabulate import tabulate
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# Placeholder for OpenWeatherMap API key
API_KEY = "940d5987b6ec97342b50fdb6f73eadc6"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/"

def main():
    print(Fore.CYAN + "Welcome to WeatherWise CLI App!" + Style.RESET_ALL)
    print("Week 1: This is a scaffold. Full functionality in Week 2.")
    print("Planned features: Search by city, current conditions, 3-day forecast.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting WeatherWise..." + Style.RESET_ALL)
        sys.exit(0)