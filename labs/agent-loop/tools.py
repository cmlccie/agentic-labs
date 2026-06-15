"""Weather Agent Tools."""

import logging
from typing import Optional

import requests

# --------------------------------------------------------------------------------------
# Get Weather
# --------------------------------------------------------------------------------------


def get_weather(latitude: float, longitude: float):
    """Get today's weather forecast for the provided coordinates.

    Includes sunrise and sunset times; minimum, maximum, and mean temperatures (in Fahrenheit);
    rain, showers, and snowfall precipitation (in inches);
    precipitation probability (in percentage).

    Args:
        latitude: Coordinate latitude in degrees.
        longitude: Coordinate longitude in degrees.

    Returns:
        Weather data including sunrise, sunset, temperatures, and precipitation.
    """

    logging.info(f"Tool Call:    get_weather({latitude=!r}, {longitude=!r})")

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

    logging.info(
        f"Tool Result:  get_weather({latitude=!r}, {longitude=!r}) -> {weather_data}"
    )
    return weather_data


# --------------------------------------------------------------------------------------
# Get Coordinates
# --------------------------------------------------------------------------------------


def get_coordinates(location_name: str, country_code: Optional[str] = None):
    """Get the longitude and latitude coordinates for a location.

    Args:
        location_name: Name of the location (e.g., city name).
        country_code: ISO-3166-1 alpha2 country code (e.g., "DE" for Germany).

    Returns:
        A dictionary containing the location name, country, latitude, and longitude.
    """

    logging.info(
        f"Tool Call:    get_coordinates({location_name=!r}, {country_code=!r})"
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

    logging.info(
        f"Tool Result:  get_coordinates({location_name=!r}, {country_code=!r}) -> {location_data}"
    )

    return location_data
