import requests
from datetime import datetime, timedelta
import os

CACHE_FILE = "weather_cache.txt"

# Example location
LATITUDE = 48.1486   # Bratislava
LONGITUDE = 17.1077


def get_date_from_user():
    user_input = input("Enter date (YYYY-MM-DD) or press Enter for tomorrow: ").strip()

    if user_input == "":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        # Validate format
        datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None


def load_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            for line in f:
                date, value = line.strip().split(",")
                cache[date] = float(value)
    return cache


def save_to_cache(date, value):
    with open(CACHE_FILE, "a") as f:
        f.write(f"{date},{value}\n")


def fetch_weather(date):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        f"&daily=precipitation_sum"
        f"&timezone=Europe%2FLondon"
        f"&start_date={date}"
        f"&end_date={date}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        precipitation = data.get("daily", {}).get("precipitation_sum", [])

        if not precipitation:
            return None

        return precipitation[0]

    except Exception as e:
        print("Error fetching weather:", e)
        return None


def interpret_result(value):
    if value is None or value < 0:
        print("I don't know")
    elif value == 0.0:
        print("It will not rain")
    else:
        print(f"It will rain (precipitation: {value})")


def main():
    date = None

    while date is None:
        date = get_date_from_user()

    cache = load_cache()

    if date in cache:
        print("Loaded from cache.")
        result = cache[date]
    else:
        print("Fetching from API...")
        result = fetch_weather(date)
        if result is not None:
            save_to_cache(date, result)

    interpret_result(result)


if __name__ == "__main__":
    main()