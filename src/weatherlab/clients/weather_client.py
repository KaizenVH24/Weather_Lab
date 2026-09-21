from datetime import datetime

import requests

from weatherlab.models.weather import CurrentWeather, DailyForecast


class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        timezone: str = "auto",
    ) -> tuple[CurrentWeather, list[DailyForecast]]:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "timezone": timezone,
            "forecast_days": 7,
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]
        current_units = data["current_units"]

        current_weather = CurrentWeather(
            time=datetime.fromisoformat(current["time"]),
            temperature=current["temperature_2m"],
            temperature_unit=current_units["temperature_2m"],
            humidity=current.get("relative_humidity_2m"),
            wind_speed=current.get("wind_speed_10m"),
            precipitation=current.get("precipitation"),
            weather_code=current.get("weather_code"),
        )

        daily = data["daily"]

        forecasts = []

        for index, date in enumerate(daily["time"]):
            forecasts.append(
                DailyForecast(
                    date=datetime.fromisoformat(date),
                    temperature_max=daily["temperature_2m_max"][index],
                    temperature_min=daily["temperature_2m_min"][index],
                    precipitation_probability=(
                        daily["precipitation_probability_max"][index]
                    ),
                    weather_code=daily["weather_code"][index],
                )
            )

        return current_weather, forecasts