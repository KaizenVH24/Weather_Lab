import requests

from weatherlab.models.location import Location


class GeocodingClient:
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def search(self, city: str) -> Location:
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            raise ValueError(f"Location not found: {city}")

        result = results[0]

        return Location(
            name=result["name"],
            country=result.get("country", "Unknown"),
            latitude=result["latitude"],
            longitude=result["longitude"],
            timezone=result.get("timezone", "UTC"),
        )