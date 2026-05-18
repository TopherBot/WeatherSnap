#!/usr/bin/env python3

"""weather_snap.py

A tiny CLI that fetches current weather for a given city using the OpenWeatherMap API.

Usage:
    export OPENWEATHER_API_KEY=your_api_key
    python weather_snap.py <city_name>
"""

import os
import sys
import argparse
import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str, api_key: str) -> dict:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        sys.stderr.write(f"Error contacting OpenWeatherMap: {exc}\n")
        sys.exit(1)

def format_output(data: dict) -> str:
    name = data.get("name", "Unknown")
    weather = data.get("weather", [{}])[0].get("description", "N/A").title()
    temp = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind = data.get("wind", {}).get("speed", "N/A")
    return (
        f"Weather for {name}:\n"
        f"  Condition : {weather}\n"
        f"  Temperature: {temp}°C\n"
        f"  Humidity   : {humidity}%\n"
        f"  Wind Speed : {wind} m/s\n"
    )

def main():
    parser = argparse.ArgumentParser(description="Fetch current weather for a city.")
    parser.add_argument("city", help="Name of the city to query")
    args = parser.parse_args()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        sys.stderr.write("Error: OPENWEATHER_API_KEY environment variable not set.\n")
        sys.exit(1)

    data = fetch_weather(args.city, api_key)
    print(format_output(data))

if __name__ == "__main__":
    main()
