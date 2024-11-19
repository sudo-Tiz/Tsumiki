from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
)
from services.weather import WeatherInfo


class Weather(Box):
    def __init__(
        self,
        city: str,
        interval: int = 60000,
        enable_tooltip=True,
    ):
        super().__init__(name="weather", style_classes="bar-box")
        self.enable_tooltip = enable_tooltip
        self.city = city

        self.weather_service = WeatherInfo()

        self.weather_label = Label(label="weather", style_classes="bar-button-label")
        self.children = self.weather_label

        invoke_repeater(interval, self.update_label, initial_call=True)

    def update_label(self):
        res = self.weather_service.simple_weather_info(city=self.city)
        self.weather_label.set_label(f"{res["icon"]} {res["temperature"]}")

        if self.enable_tooltip:
            self.set_tooltip_text(f"{res["city"]}, {res["condition"]}".strip("'"))
        return True
