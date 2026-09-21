from datetime import date, datetime

from pydantic import BaseModel, Field

from .location import Location


class CurrentWeather(BaseModel):
    time: datetime
    temperature: float
    temperature_unit: str
    humidity: float | None = None
    wind_speed: float | None = None
    precipitation: float | None = None
    weather_code: int | None = None


class HourlyForecast(BaseModel):
    time: datetime
    temperature: float
    precipitation_probability: float | None = None
    precipitation: float | None = None
    weather_code: int | None = None


class DailyForecast(BaseModel):
    date: date
    temperature_max: float
    temperature_min: float
    precipitation_probability: float | None = None
    weather_code: int | None = None


class WeatherReport(BaseModel):
    location: Location
    current: CurrentWeather
    hourly: list[HourlyForecast] = Field(default_factory=list)
    daily: list[DailyForecast] = Field(default_factory=list)