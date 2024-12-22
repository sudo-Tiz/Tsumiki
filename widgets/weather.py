from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from shared.popover import PopOverWindow
from utils.functions import text_icon
from utils.widget_config import BarConfig
from services import weather_service

import gi

from gi.repository import Gtk

gi.require_version("Gtk", "3.0")


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def __init__(self):
        super().__init__(
            style_classes="weather-box", orientation="v", h_expand=True, spacing=5
        )

        title_box = Box(style_classes="weather-header-box")

        self.title_label = Label(
            style_classes="weather-header",
            h_align="start",
            h_expand=True,
            v_align="end",
            label="Weather Forecast",
        )

        self.title_location = Label(
            style_classes="weather-header location",
            v_align="end",
            h_align="end",
            label="Location",
        )
        title_box.children = (self.title_label, self.title_location)

        self.forecast_box = Gtk.Grid(
            row_spacing=10,
            column_spacing=20,
        )

        # show next 5 hours forecast
        for col in range(5):
            time = Label(
                style_classes="weather-forecast-time", label="12:00", h_align="center"
            )
            icon = Image(
                icon_name="weather-clear-symbolic",
                icon_size=64,
                h_align="center",
                h_expand=True,
                style_classes="weather-forecast-icon",
            )

            temp = Label(
                style_classes="weather-forecast-temp", label="17", h_align="center"
            )
            self.forecast_box.attach(time, col, 0, 1, 1)
            self.forecast_box.attach(icon, col, 1, 1, 1)
            self.forecast_box.attach(temp, col, 2, 1, 1)

        self.children = (
            title_box,
            self.forecast_box,
        )

        self.forecast_box.show()


class WeatherWidget(Button):
    """A widget to display the current weather."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
    ):
        # Initialize the Box with specific name and style
        super().__init__()

        # TODO: cache the weather data
        self.is_data_ready = True

        self.config = widget_config["weather"]

        self.box = Box(
            name="weather",
            style_classes="panel-box",
        )

        self.children = self.box

        self.weather_icon = text_icon(icon="", size="15px")

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(WeatherMenu()),
            visible=False,
            all_visible=False,
        )

        self.weather_label = Label(
            label="Fetching weather...",
            style_classes="panel-text",
        )
        self.box.children = (self.weather_icon, self.weather_label)

        popup.set_pointing_to(self)

        self.connect(
            "clicked",
            lambda *_: self.is_data_ready
            and popup.set_visible(not popup.get_visible()),
        )

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(self.config["interval"], self.update_label, initial_call=False)

    # This function will run the weather fetch in a separate thread
    def update_label(self):
        res = weather_service.simple_weather_info(self.config["location"])
        # Update the label with the weather icon and temperature

        self.weather_label.set_label(f"{res['temperature']}°C")
        self.weather_icon.set_label(res["icon"])

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))
        return True
