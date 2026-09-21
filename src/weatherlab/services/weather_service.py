from weatherlab.clients.geocoding_client import GeocodingClient
from weatherlab.clients.weather_client import WeatherClient
from weatherlab.models.weather import WeatherReport


class WeatherService:
    def __init__(
        self,
        geocoding_client: GeocodingClient | None = None,
        weather_client: WeatherClient | None = None,
    ):
        self.geocoding_client = (
            geocoding_client or GeocodingClient()
        )

        self.weather_client = (
            weather_client or WeatherClient()
        )

    def get_weather(self, city: str) -> WeatherReport:
        location = self.geocoding_client.search(city)

        current, hourly, daily = self.weather_client.get_forecast(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone,
        )

        return WeatherReport(
            location=location,
            current=current,
            hourly=hourly,
            daily=daily,
        )