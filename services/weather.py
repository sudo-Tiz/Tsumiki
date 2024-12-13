import json
import ssl
import urllib.request

from utils.icons import WEATHER_TEXT_ICONS

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherInfo:
    """This class provides weather information for a given city."""

    def simple_weather_info(self, city: str):
        try:
            # Construct the URL for fetching weather information
            url = f"https://wttr.in/{city.capitalize()}?format=j1"
            contents = (
                urllib.request.urlopen(url, context=context).read().decode("utf-8")
            )

            # Parse the weather information
            data = json.loads(contents)

            current_weather = data["current_condition"][0]
            hourly_weather = data["weather"][0]["hourly"]

            return {
                "city": city,
                "icon": WEATHER_TEXT_ICONS[current_weather["weatherCode"]]["icon"],
                "temperature": current_weather["FeelsLikeC"],
                "condition": current_weather["weatherDesc"][0]["value"],
                "hourly": hourly_weather,
            }

        except Exception as e:
            # Handle any errors that occur during the request
            return {"error": str(e)}
