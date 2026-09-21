from datetime import datetime

import requests

from weatherlab.models.weather import (
    CurrentWeather,
    DailyForecast,
    HourlyForecast,
)


class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        timezone: str = "auto",
    ) -> tuple[
        CurrentWeather,
        list[HourlyForecast],
        list[DailyForecast],
    ]:

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
            "hourly": (
                "temperature_2m,"
                "precipitation_probability,"
                "precipitation,"
                "weather_code"
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

        # -------------------------
        # Current weather
        # -------------------------

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

        # -------------------------
        # Hourly forecast
        # -------------------------

        hourly = data["hourly"]

        hourly_forecasts = []

        for index, time in enumerate(hourly["time"]):
            hourly_forecasts.append(
                HourlyForecast(
                    time=datetime.fromisoformat(time),
                    temperature=hourly["temperature_2m"][index],
                    precipitation_probability=(
                        hourly["precipitation_probability"][index]
                    ),
                    precipitation=hourly["precipitation"][index],
                    weather_code=hourly["weather_code"][index],
                )
            )

        # -------------------------
        # Daily forecast
        # -------------------------

        daily = data["daily"]

        daily_forecasts = []

        for index, forecast_date in enumerate(daily["time"]):
            daily_forecasts.append(
                DailyForecast(
                    date=forecast_date,
                    temperature_max=daily["temperature_2m_max"][index],
                    temperature_min=daily["temperature_2m_min"][index],
                    precipitation_probability=(
                        daily["precipitation_probability_max"][index]
                    ),
                    weather_code=daily["weather_code"][index],
                )
            )

        return (
            current_weather,
            hourly_forecasts,
            daily_forecasts,
        )