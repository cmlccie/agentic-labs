#!/usr/bin/env python3
"""Weather Agent - chat with a local LLM server.

Requires a running local LLM server. Start one with:
    uv run agentic-labs local-llm
"""

from datetime import date, datetime, timedelta
from typing import Any, List, Literal, Optional
from zoneinfo import ZoneInfo

import requests
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

BASE_URL = "http://127.0.0.1:1234/v1"
API_KEY = "lite-llm"
MODEL = "openai/gpt-oss-20b"

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

SYSTEM_PROMPT = """
You are a helpful assistant that provides weather forecasts based on user queries.

- Use the provided tools to identify the specific location and date range for the user's
  weather forecast request.
- If the user does not specify a location, ask for clarification.
- If the user does not specify a date range, provide the forecast for the current day.
"""

# --------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------

provider = OpenAIProvider(base_url=BASE_URL, api_key=API_KEY)
model = OpenAIChatModel(MODEL, provider=provider)

agent = Agent(model, system_prompt=SYSTEM_PROMPT)


# -----------------------------------------------------------------------------
# Agent Dynamic System Prompt Injection
# -----------------------------------------------------------------------------


@agent.system_prompt()
def add_date_info() -> str:
    """Add current date information to the system prompt.

    Weather forecasts are available for 16 days, including today. Add dates and days
    of the week to the system prompt to help the agent provide accurate forecasts.
    """
    # Date Info Format: Thursday, December 25, 2025 (2025-12-25)

    today = date.today()
    date_info = [
        (today + timedelta(days=i)).strftime("%A, %B %d, %Y (%Y-%m-%d)")
        for i in range(16)
    ]

    return f"""\n## Date Information

    - Today is {today.strftime("%A, %B %d, %Y (%Y-%m-%d)")}.
    - Weather forecasts are available for the following dates:
      - {"\n  - ".join(date_info)}
    """


# --------------------------------------------------------------------------------------
# Agent Tools
# --------------------------------------------------------------------------------------

WeatherVariables = Literal[
    "cloud_cover_max",
    "cloud_cover_mean",
    "cloud_cover_min",
    "precipitation_hours",
    "precipitation_probability_max",
    "precipitation_sum",
    "rain_sum",
    "relative_humidity_2m_max",
    "relative_humidity_2m_mean",
    "relative_humidity_2m_min",
    "showers_sum",
    "snowfall_sum",
    "sunrise",
    "sunset",
    "temperature_2m_max",
    "temperature_2m_min",
    "wind_gusts_10m_max",
    "wind_gusts_10m_min",
    "wind_speed_10m_max",
    "wind_speed_10m_min",
]

PrecipitationUnit = Literal["mm", "inch"]

TemperatureUnit = Literal["celsius", "fahrenheit"]

TimeFormat = Literal["iso8601", "unixtime"]

WindSpeedUnit = Literal["kmh", "mph", "ms", "kn"]


# -----------------------------------------------------------------------------
# Get Weather Forecast
# -----------------------------------------------------------------------------


@agent.tool()
def get_weather_forecast(
    ctx: RunContext,
    latitude: float,
    longitude: float,
    timezone: str = "auto",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    weather_variables: Optional[List[WeatherVariables]] = None,
    time_format: TimeFormat = "iso8601",
    temperature_unit: TemperatureUnit = "fahrenheit",
    precipitation_unit: PrecipitationUnit = "inch",
    wind_speed_unit: WindSpeedUnit = "mph",
) -> dict[str, Any]:
    """Get the weather forecast for the provided coordinates.

    Includes sunrise and sunset times; minimum, maximum, and mean temperatures (in Fahrenheit);
    rain, showers, and snowfall precipitation (in inches);
    precipitation probability (in percentage).

    Default daily variables include:
        - cloud_cover_mean
        - precipitation_probability_max
        - precipitation_sum
        - temperature_2m_max
        - temperature_2m_min

    Args:
        latitude: Coordinate latitude in degrees.
        longitude: Coordinate longitude in degrees.
        timezone: Timezone for the forecast (e.g. 'America/New_York', default is "auto").
        start_date: Start date in ISO8601 (YYYY-MM-DD) format for the forecast (default is today).
        end_date: End date in ISO8601 (YYYY-MM-DD) format for the forecast (default is today).
        daily: Set of daily weather variables to include (default is a predefined set).

    Returns:
        dict[str, Any]: The weather forecast data including requested daily variables.
    """
    # Get today's date in the specified timezone
    if timezone == "auto":
        today = datetime.now().date().isoformat()
    else:
        try:
            tz = ZoneInfo(timezone)
            today = datetime.now(tz).date().isoformat()
        except Exception:
            # Fallback to local time if timezone is invalid
            today = datetime.now().date().isoformat()

    start_date = start_date or today
    end_date = end_date or today

    print(
        f"Fetching weather forecast for coordinates ({latitude}, {longitude}) from {start_date} to {end_date} with timezone '{timezone}'..."
    )

    weather_variables = (
        list(set(weather_variables))
        if weather_variables
        else [
            "cloud_cover_mean",
            "precipitation_probability_max",
            "precipitation_sum",
            "relative_humidity_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
        ]
    )

    request_parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(weather_variables),
        "timeformat": time_format,
        "temperature_unit": temperature_unit,
        "precipitation_unit": precipitation_unit,
        "wind_speed_unit": wind_speed_unit,
    }

    response = requests.get(OPEN_METEO_FORECAST_URL, params=request_parameters)

    try:
        response.raise_for_status()
        weather_data = response.json()
    except Exception as e:
        weather_data = {"error": f"Failed to fetch weather data: {str(e)}"}

    return weather_data


# --------------------------------------------------------------------------------------
# Get Locations
# --------------------------------------------------------------------------------------


@agent.tool()
def get_locations(
    ctx: RunContext,
    name: str,
    country_code: Optional[str] = None,
    count: int = 10,
) -> dict[str, Any]:
    """Get location information.

    Args:
        location_name: Name of the location (e.g., city name).
        country_code: Optional ISO-3166-1 alpha2 country code to narrow down the search (e.g., 'US' for the United States).

    Returns:
        dict[str, Any]: A dictionary containing location information.
    """
    print(f"Fetching location data for '{name}' with country code '{country_code}'...")

    request_parameters = {
        "name": name,
        "count": count,
        "language": "en",
        "format": "json",
    }

    if country_code is not None:
        request_parameters["countryCode"] = country_code

    response = requests.get(OPEN_METEO_GEOCODING_URL, params=request_parameters)

    try:
        response.raise_for_status()
        location_data = response.json()
    except Exception as e:
        location_data = {"error": f"Failed to fetch location data: {str(e)}"}

    return location_data


# --------------------------------------------------------------------------------------
# Main: Agent CLI
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    agent.to_cli_sync(prog_name="weather-agent")
