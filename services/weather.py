import urllib.request


# This class provides weather information for a given city
class WeatherInfo:
    def simple_weather_info(self, city: str):
        try:
            # Construct the URL for fetching weather information
            url = f"http://wttr.in/{city.capitalize()}?format='%l,%c,%t,%C'"
            contents = urllib.request.urlopen(url).read().decode("utf-8")

            # Parse the weather information
            data = str(contents).split(",")
            return {
                "city": data[0].strip(),
                "icon": data[1].strip(),
                "temperature": data[2].strip(),
                "condition": data[3].strip(),
            }
        except Exception as e:
            # Handle any errors that occur during the request
            return {"error": str(e)}
