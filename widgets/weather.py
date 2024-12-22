from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from shared.popover import PopOverWindow
from utils.functions import text_icon
from utils.widget_config import BarConfig
from utils.icons import weather_text_icons_v2
from services import weather_service

import gi

from gi.repository import Gtk, GLib

gi.require_version("Gtk", "3.0")


class WeatherMenu(Box):
    """A menu to display the weather information."""

    # wttr.in time are in 300,400...2100 format , we need to convert it to 3:00, 4:00...21:00
    def format_wttr_time(self, time: str):
        time_value = int(int(time) / 100)
        return f"{time_value}:00" if time_value > 9 else f"0{time_value}:00"

    def __init__(self, data):
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

        hourly_forecast = data["hourly"][3:8]

        # show next 5 hours forecast
        for col in range(5):
            time = Label(
                style_classes="weather-forecast-time",
                label=f"{self.format_wttr_time(hourly_forecast[col]["time"])}",
                h_align="center",
            )
            icon = Image(
                icon_name=weather_text_icons_v2[hourly_forecast[col]["weatherCode"]][
                    "image"
                ],
                icon_size=64,
                h_align="center",
                h_expand=True,
                style_classes="weather-forecast-icon",
            )

            temp = Label(
                style_classes="weather-forecast-temp",
                label=f"{hourly_forecast[col]["tempC"]}°C",
                h_align="center",
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

        self.config = widget_config["weather"]

        self.bar = bar

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
        # Create a background thread to fetch weather data
        GLib.Thread.new("thread", self.fetch_weather, None)
        return True

    def fetch_weather(self, _data):
        res = weather_service.simple_weather_info(self.config["location"])

        GLib.idle_add(self.update_ui, res)
        return False

    def update_ui(self, res):
        # Update the label with the weather icon and temperature in the main thread
        self.weather_label.set_label(f"{res['temperature']}°C")
        self.weather_icon.set_label(res["icon"])

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))

        popup = PopOverWindow(
            parent=self.bar,
            name="popup",
            child=(WeatherMenu(data=res)),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
