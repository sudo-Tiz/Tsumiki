import json
import ssl
from urllib.error import HTTPError
import urllib.request

from loguru import logger

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService:
    """This class provides weather information for a given city."""

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
            hourly_weather = data["weather"][0]["hourly"]

            return {
                "location": location.capitalize(),
                "current": current_weather,  # the current weather information
                "hourly": hourly_weather,  # the data for the next 24 hours in tri-hourly intervals
            }

        except HTTPError as e:
            if e.code == 404:
                print("Error: City not found. Try a different city.")
        except Exception as e:
            print(f"Error: {e}")
            return None
