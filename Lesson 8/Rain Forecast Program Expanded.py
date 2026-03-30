import requests
from datetime import datetime, timedelta
import os


class WeatherForecast:
    def __init__(self, filename="weather_cache.txt"):
        self.filename = filename
        self.data = {}
        self._load()

        # Default location (Bratislava)
        self.latitude = 48.1486
        self.longitude = 17.1077

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    date, value = line.strip().split(",")
                    self.data[date] = float(value)

    def _save(self):
        with open(self.filename, "w") as f:
            for date, value in self.data.items():
                f.write(f"{date},{value}\n")

    def _fetch_from_api(self, date):
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.latitude}"
            f"&longitude={self.longitude}"
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
            print("API error:", e)
            return None

    # REQUIRED METHODS

    def __getitem__(self, date):
        # If already cached → return it
        if date in self.data:
            return self.data[date]

        # Otherwise fetch from API
        value = self._fetch_from_api(date)

        if value is not None:
            self.data[date] = value
            self._save()

        return value

    def __setitem__(self, date, value):
        self.data[date] = value
        self._save()

    def __iter__(self):
        return iter(self.data)

    def items(self):
        for date, value in self.data.items():
            yield (date, value)


# -------------------------
# MAIN PROGRAM (UPDATED)
# -------------------------

def get_date():
    user_input = input("Enter date (YYYY-MM-DD) or press Enter for tomorrow: ").strip()

    if user_input == "":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("Invalid format.")
        return None


def interpret(value):
    if value is None or value < 0:
        print("I don't know")
    elif value == 0.0:
        print("It will not rain")
    else:
        print(f"It will rain (precipitation: {value})")


def main():
    wf = WeatherForecast()

    date = None
    while date is None:
        date = get_date()

    result = wf[date]  #uses __getitem__
    interpret(result)

    print("\nSaved forecasts:")
    for d, v in wf.items():  #uses items()
        print(d, "->", v)


if __name__ == "__main__":
    main()