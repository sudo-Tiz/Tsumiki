import threading

from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from loguru import logger

from services import WeatherInfo
from shared import PopupWindow
from utils.functions import text_icon
from utils.icons import common_text_icons
from utils.widget_config import BarConfig


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, data: dict):
        super().__init__(name="weather-menu")

        self.weather_container = Box(
            orientation="h", spacing=4, name="weather-container"
        )

        self.upper = CenterBox(
            name="weather-upper",
            start_children=Box(
                name="start-container",
                v_align="center",
                h_align="center",
                children=text_icon(
                    icon=data["icon"],
                    size="40px",
                ),
            ),
            center_children=Box(
                name="center-container",
                v_align="center",
                h_align="center",
                children=[
                    Label(
                        style_classes="temperature",
                        label=f"{data["temperature"]}°C",
                    ),
                    text_icon(
                        icon=common_text_icons["thermometer"],
                        size="20px",
                    ),
                ],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[],
            ),
        )

        self.bottom = Box()
        self.weather_container.add(self.upper)

        self.add(self.weather_container)


class WeatherWidget(EventBox):
    """A widget to display the current weather."""

    def __init__(
        self,
        widget_config: BarConfig,
    ):
        # Initialize the Box with specific name and style
        super().__init__()

        # Set the widget as not ready until the weather information is fetched
        self.is_ready = False

        self.config = widget_config["weather"]

        self.box = Box(
            name="weather",
            style_classes="panel-box",
        )

        self.children = self.box

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
            daemon=True,
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

        self.weather_label.set_label(f"{res['temperature']}°C")
        self.weather_icon.set_label(res["icon"])

        self.weather_menu = PopupWindow(
            transition_duration=350,
            anchor="top-right",
            transition_type="slide-down",
            child=WeatherMenu(res),
            enable_inhibitor=True,
        )
        self.connect("button-press-event", lambda *_: self.weather_menu.toggle_popup())

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))
        return True
