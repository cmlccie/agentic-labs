"""LLM Functions."""

from typing import Optional

import requests

# --------------------------------------------------------------------------------------
# Get Weather
# --------------------------------------------------------------------------------------


def get_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params,
    )
    response.raise_for_status()

    data = response.json()

    return data["current"]["temperature_2m"]


# --------------------------------------------------------------------------------------
# Get Coordinates
# --------------------------------------------------------------------------------------


def get_coordinates(location_name: str, country_code: Optional[str] = None):
    params = {
        "name": location_name,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    if country_code is not None:
        params["countryCode"] = country_code

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params=params,
    )
    response.raise_for_status()

    data = response.json()

    return {
        "name": data["results"][0]["name"],
        "country": data["results"][0]["country"],
        "latitude": data["results"][0]["latitude"],
        "longitude": data["results"][0]["longitude"],
    }
