from pydantic import BaseModel


class Location(BaseModel):
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str