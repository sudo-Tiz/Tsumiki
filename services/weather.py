import json
import ssl
import urllib.request

# Create an SSLContext that ignores certificate validation
context = ssl._create_unverified_context()


class WeatherService:
    """This class provides weather information for a given city."""

    def simple_weather_info(self, location: str):
        try:
            # Construct the URL for fetching weather information
            url = f"https://wttr.in/{location.capitalize()}?format=j1"
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

        except Exception as e:
            # Handle any errors that occur during the request
            return {"error": str(e)}
