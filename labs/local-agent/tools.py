"""Weather Agent Tools."""

import logging
from typing import Optional

import requests

# --------------------------------------------------------------------------------------
# Get Weather
# --------------------------------------------------------------------------------------


def get_weather(latitude: float, longitude: float):
    """Get today's weather forecast for the provided coordinates."""

    logging.info(f"Getting weather for coordinates: {latitude}, {longitude}")

    params = {
        "forecast_days": 1,
        "timezone": "auto",
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "sunrise",
            "sunset",
            "temperature_2m_min",
            "temperature_2m_max",
            "temperature_2m_mean",
            "rain_sum",
            "showers_sum",
            "snowfall_sum",
            "precipitation_probability_max",
        ],
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params,
    )
    response.raise_for_status()

    data = response.json()

    weather_data = {
        "sunrise": data["daily"]["sunrise"][0],
        "sunset": data["daily"]["sunset"][0],
        "temperature_min": data["daily"]["temperature_2m_min"][0],
        "temperature_max": data["daily"]["temperature_2m_max"][0],
        "temperature_mean": data["daily"]["temperature_2m_mean"][0],
        "rain": data["daily"]["rain_sum"][0],
        "showers": data["daily"]["showers_sum"][0],
        "snowfall": data["daily"]["snowfall_sum"][0],
        "precipitation_probability": data["daily"]["precipitation_probability_max"][0],
    }

    logging.info(f"Weather data retrieved: {weather_data}")
    return weather_data


GET_WEATHER_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get today's weather forecast for the provided coordinates, including:"
        " sunrise and sunset times; minimum, maximum, and mean temperatures (in Fahrenheit);"
        " rain, showers, and snowfall precipitation (in inches);"
        " precipitation probability (in percentage).",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Coordinate latitude in degrees.",
                },
                "longitude": {
                    "type": "number",
                    "description": "Coordinate longitude in degrees.",
                },
            },
        },
        "required": ["latitude", "longitude"],
    },
}

# --------------------------------------------------------------------------------------
# Get Coordinates
# --------------------------------------------------------------------------------------


def get_coordinates(location_name: str, country_code: Optional[str] = None):
    """Get the longitude and latitude coordinates for a location."""

    logging.info(
        f"Getting coordinates for location: {location_name!r}, country code: {country_code!r}"
    )

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

    location_data = {
        "name": data["results"][0]["name"],
        "country": data["results"][0]["country"],
        "latitude": data["results"][0]["latitude"],
        "longitude": data["results"][0]["longitude"],
    }

    logging.info(f"Coordinates retrieved: {location_data}")

    return location_data


GET_COORDINATES_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "get_coordinates",
        "description": "Get the longitude and latitude coordinates for a location.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "location_name": {
                    "type": "string",
                    "description": "Location city (e.g. Berlin).",
                },
                "country_code": {
                    "type": "string",
                    "description": "ISO-3166-1 alpha2 country code (e.g. DE).",
                },
            },
        },
        "required": ["location_name"],
    },
}

# -------------------------------------------------------------------------------------------------
# Module Exports
# -------------------------------------------------------------------------------------------------

tools = [
    GET_WEATHER_DESCRIPTION,
    GET_COORDINATES_DESCRIPTION,
]

functions = {
    "get_weather": get_weather,
    "get_coordinates": get_coordinates,
}
