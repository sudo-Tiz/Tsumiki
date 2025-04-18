import json
import os
import ssl
import time
import urllib.request
from urllib.error import HTTPError

from loguru import logger

from utils import Colors
from utils.constants import WEATHER_CACHE_FILE

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService:
    """This class provides weather information for a given city."""

    instance = None

    @staticmethod
    def get_default():
        if WeatherService.instance is None:
            WeatherService.instance = WeatherService()

        return WeatherService.instance

    def simple_weather_info(self, location: str):
        try:
            url = ""
            # Construct the URL for fetching weather information
            if location != "":
                encoded_location = urllib.parse.quote_plus(location.capitalize())

                url = f"http://wttr.in/{encoded_location}?format=j1"
            else:
                url = "http://wttr.in/?format=j1"

            logger.info(f"[Weather] Fetching weather information from {url}")
            contents = (
                urllib.request.urlopen(url, context=context, timeout=10)
                .read()
                .decode("utf-8")
            )

            # Parse the weather information
            data = json.loads(contents)

            current_weather = data["current_condition"][0]
            weather = data["weather"][0]
            hourly_weather = weather["hourly"]
            location = data["nearest_area"][0]["areaName"][0]["value"]

            return {
                "location": location.capitalize(),
                "current": current_weather,  # the current weather information
                "hourly": hourly_weather,  # tri-hourly data for the next 24 hours
                "astronomy": weather["astronomy"][0],  # the sunrise and sunset times
            }

        except HTTPError as e:
            if e.code == 404:
                logger.error(
                    f"{Colors.ERROR}Error: City not found. Try a different city."
                )
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_weather(self, location: str):
        # Check if cache exists and is fresh
        if os.path.exists(WEATHER_CACHE_FILE):
            last_modified = os.path.getmtime(WEATHER_CACHE_FILE)
            logger.info(
                f"{Colors.INFO} reading weather from cache file {WEATHER_CACHE_FILE}"
            )
            if time.time() - last_modified < 86400:  # 24 hours
                with open(WEATHER_CACHE_FILE, "r") as f:
                    return json.load(f)

        logger.info(
            f"{Colors.INFO}Cache file {WEATHER_CACHE_FILE} does not exist or is stale. "
            f"Fetching new data."
        )
        weather = self.simple_weather_info(location)
        if weather is None:
            return None
        # Save the weather data to the cache file
        with open(WEATHER_CACHE_FILE, "w") as f:
            json.dump(weather, f)

        return weather
