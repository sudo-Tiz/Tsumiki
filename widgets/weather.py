from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
)
from loguru import logger
from services.weather import WeatherInfo
import threading


class Weather(Box):
    def __init__(
        self,
        city: str,
        interval: int = 60000,
        enable_tooltip=True,
    ):
        # Initialize the Box with specific name and style
        super().__init__(name="weather", style_classes="bar-box")
        self.enable_tooltip = enable_tooltip
        self.city = city

        self.weather_label = Label(
            label="Fetching weather...", style_classes="bar-button-label"
        )
        self.children = self.weather_label

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(interval, self.update_label, initial_call=True)

    def update_label(self):
        weather_thread = threading.Thread(
            target=self.fetch_weather_in_thread, args=(self.city,)
        )
        weather_thread.start()
        # Continue running the main program (non-blocking)
        logger.info(
            "[Weather] Weather information is being fetched in a separate thread..."
        )

    # This function will run the weather fetch in a separate thread
    def fetch_weather_in_thread(self, city: str):
        weather = WeatherInfo()
        res = weather.simple_weather_info(city)
        # Update the label with the weather icon and temperature
        self.weather_label.set_label(f"{res['icon']} {res['temperature']}")

        # Update the tooltip with the city and weather condition if enabled
        if self.enable_tooltip:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))
        return True
