import json
import ssl
import urllib.request
from urllib.error import HTTPError

from loguru import logger

from utils.colors import Colors

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService:
    """This class provides weather information for a given city."""

    instance = None

    @staticmethod
    def get_initial():
        if WeatherService.instance is None:
            WeatherService.instance = WeatherService()

        return WeatherService.instance

    def simple_weather_info(self, location: str):
        try:
            # Construct the URL for fetching weather information

            encoded_location = urllib.parse.quote_plus(location.capitalize())
            url = f"https://wttr.in/{encoded_location}?format=j1"

            logger.info(f"[Weather] Fetching weather information from {url}")
            contents = (
                urllib.request.urlopen(url, context=context).read().decode("utf-8")
            )

            # Parse the weather information
            data = json.loads(contents)

            current_weather = data["current_condition"][0]
            weather = data["weather"][0]
            hourly_weather = weather["hourly"]

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
        except Exception as e:
            print(f"Error: {e}")
            return None
