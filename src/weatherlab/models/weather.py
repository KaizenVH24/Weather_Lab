from datetime import datetime

from pydantic import BaseModel


class CurrentWeather(BaseModel):
    time: datetime
    temperature: float
    temperature_unit: str
    humidity: float | None = None
    wind_speed: float | None = None
    precipitation: float | None = None
    weather_code: int | None = None


class DailyForecast(BaseModel):
    date: datetime
    temperature_max: float
    temperature_min: float
    precipitation_probability: float | None = None
    weather_code: int | None = None


class WeatherReport(BaseModel):
    location: "Location"
    current: CurrentWeather
    daily: list[DailyForecast] = []


from .location import Location