import threading
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from loguru import logger


from services.weather import WeatherInfo
from shared.popup import PopupWindow
from utils.config import BarConfig
from utils.functions import text_icon


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def __init__(
        self,
    ):
        super().__init__(name="weather-menu", orientation="vertical")

        self.upper = CenterBox(
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=Image(
                    name="weather-icon",
                    icon_name="weather-showers",
                ),
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=[
                    Label(
                        label="Fetching weather...",
                        style_classes="panel-text",
                    )
                ],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[],
            ),
        )
        self.children = self.upper


class Weather(EventBox):
    """A widget to display the current weather."""

    def __init__(
        self,
        config: BarConfig,
    ):
        # Initialize the Box with specific name and style
        super().__init__()

        self.config = config["weather"]

        self.box = Box(
            name="weather",
            style_classes="panel-box",
        )

        self.children = self.box

        self.weather_menu = PopupWindow(
            transition_duration=350,
            anchor="top-right",
            transition_type="slide-down",
            child=WeatherMenu(),
            enable_inhibitor=True,
        )
        self.connect("button-press-event", lambda _: self.weather_menu.toggle_popup())

        self.weather_icon = text_icon(icon="", size="15px")

        self.weather_label = Label(
            label="Fetching weather...",
            style_classes="panel-text",
        )
        self.box.children = (self.weather_icon, self.weather_label)

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(self.config["interval"], self.update_label, initial_call=True)

    def update_label(self):
        weather_thread = threading.Thread(
            target=self.fetch_weather_in_thread,
            args=(self.config["location"],),
        )
        weather_thread.start()
        # Continue running the main program (non-blocking)
        logger.info(
            "[Weather] Weather information is being fetched in a separate thread...",
        )

    # This function will run the weather fetch in a separate thread
    def fetch_weather_in_thread(self, city: str):
        weather = WeatherInfo()
        res = weather.simple_weather_info(city)
        # Update the label with the weather icon and temperature

        print(res["temperature"], res["icon"])
        self.weather_label.set_label(res["temperature"])
        self.weather_icon.set_label(res["icon"])

        # Update the tooltip with the city and weather condition if enabled
        if self.config["enable_tooltip"]:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))
        return True
