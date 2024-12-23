import json
from operator import le
import time

import gi
from fabric.utils import exec_shell_command, get_relative_path, invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import GLib, Gtk

from services import weather_service
from shared.popover import PopOverWindow
from utils.functions import convert_seconds_to_miliseconds, text_icon
from utils.icons import weather_text_icons, weather_text_icons_v2
from utils.widget_config import BarConfig

gi.require_version("Gtk", "3.0")


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, data):
        super().__init__(
            style_classes="weather-box", orientation="v", h_expand=True, spacing=5
        )

        # Get the current weather
        current_weather = data["current"]

        # Get the hourly forecast
        hourly_forecast = data["hourly"]

        self.weather_icons_dir = get_relative_path("../assets/icons/weather")

        title_box = CenterBox(
            style_classes="weather-header-box",
            start_children=(
                Box(
                    v_align="start",
                    children=(
                        Image(
                            image_file=f"{self.weather_icons_dir}/{weather_text_icons_v2[current_weather["weatherCode"]]["image"]}.svg",
                            size=80,
                            v_align="start",
                        ),
                        Box(
                            orientation="v",
                            v_align="center",
                            children=(
                                Label(
                                    style_classes="condition",
                                    v_align="center",
                                    h_align="center",
                                    label=f"{current_weather["weatherDesc"][0]["value"]}",
                                ),
                                Label(
                                    style_classes="temperature",
                                    v_align="center",
                                    h_align="center",
                                    label=f"{current_weather['temp_C']}°C",
                                ),
                            ),
                        ),
                    ),
                )
            ),
            center_children=(
                Box(
                    name="weather-details",
                    orientation="v",
                    v_align="start",
                    spacing=10,
                    children=(
                        Label(
                            style_classes="windspeed",
                            v_align="center",
                            label=f"0 {current_weather['windspeedKmph']} mph",
                        ),
                        Label(
                            style_classes="humidity",
                            v_align="center",
                            label=f"󰖎 {current_weather['humidity']}%",
                        ),
                    ),
                )
            ),
            end_children=(
                Box(
                    orientation="v",
                    spacing=10,
                    v_align="start",
                    children=(
                        Label(
                            style_classes="location",
                            v_align="center",
                            h_align="center",
                            label=f"{data['location']}",
                        ),
                        Label(
                            style_classes="feels-like",
                            v_align="center",
                            h_align="center",
                            label=f"Feels Like {current_weather['FeelsLikeC']}°C",
                        ),
                    ),
                )
            ),
        )

        expander = Gtk.Expander(
            child=title_box,
            visible=True,
            expanded=True,
            name="weather-expander",
        )

        # Create a grid to display the hourly forecast

        self.forecast_box = Gtk.Grid(
            row_spacing=10,
            column_spacing=20,
            name="weather-grid",
            visible=True,
        )

        self.children = (
            expander,
            Gtk.Separator(
                orientation=Gtk.Orientation.HORIZONTAL,
                visible=True,
                name="weather-separator",
            ),
            self.forecast_box,
        )

        invoke_repeater(
            convert_seconds_to_miliseconds(3600),
            self.update_grid,
            hourly_forecast,
            initial_call=True,
        )

    def update_grid(self, hourly_forecast):
        current_time = int(time.strftime("%H00"))

        next_values = hourly_forecast[:4]

        if current_time > 1200:
            next_values = hourly_forecast[4:8]


        # show next 4 hours forecast
        for col in range(4):
            column_data = next_values[col]

            hour = Label(
                style_classes="weather-forecast-time",
                label=f"{self.convert_to_12hr_format(column_data["time"])}",
                h_align="center",
            )
            icon = Image(
                image_file=f"{self.weather_icons_dir}/{weather_text_icons_v2[column_data["weatherCode"]]["image"]}.svg",
                size=70,
                h_align="center",
                h_expand=True,
                style_classes="weather-forecast-icon",
            )

            temp = Label(
                style_classes="weather-forecast-temp",
                label=f"{column_data["tempC"]}°C",
                h_align="center",
            )
            self.forecast_box.attach(hour, col, 0, 1, 1)
            self.forecast_box.attach(icon, col, 1, 1, 1)
            self.forecast_box.attach(temp, col, 2, 1, 1)

    # wttr.in time are in 300,400...2100 format , we need to convert it to 3:00, 4:00...21:00
    def convert_to_12hr_format(self, time: str) -> str:
        time = int(time)
        hour = time // 100  # Get the hour (e.g., 1200 -> 12)
        minute = time % 100  # Get the minutes (e.g., 1200 -> 00)

        # Convert to 12-hour format
        period = "AM" if hour < 12 else "PM"

        # Adjust hour for 12-hour format
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        # Format the time as a string
        return f"{hour}:{minute:02d} {period}"


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

        self.weather_icon = text_icon(
            icon="",
            size="15px",
            props={
                "style_classes": "weather-bar-icon",
            },
        )

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
        if self.config["detect_location"]:
            self.config["location"] = json.loads(
                exec_shell_command("curl ipinfo.io").strip("\n")
            )["city"]

        res = weather_service.simple_weather_info(self.config["location"])

        GLib.idle_add(self.update_ui, res)
        return False

    def update_ui(self, res):
        # Update the label with the weather icon and temperature in the main thread
        current_weather = res["current"]
        text_icon = weather_text_icons[current_weather["weatherCode"]]["icon"]
        self.weather_label.set_label(f"{current_weather["FeelsLikeC"]}°C")
        self.weather_icon.set_label(text_icon)

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"{res['location']}, {current_weather["weatherDesc"][0]["value"]}"
            )

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
