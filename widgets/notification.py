from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from shared.popover import PopOverWindow
from utils.functions import text_icon
from utils.widget_config import BarConfig
from utils.icons import common_text_icons


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


class NotificationWidget(Box):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        self.config = widget_config["notification"]
        super().__init__(
            name="notification-button", style_classes="panel-button", **kwargs
        )

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            margin="10px 10px 10px 10px",
            orientation="v",
            child=(WeatherMenu(data={"temperature": "25", "icon": "󰖑"})),
            visible=False,
            all_visible=False,
        )

        btn = Button(
            label="Notification",
            on_clicked=lambda _: popup.set_visible(not popup.get_visible()),
        )
        popup.set_pointing_to(btn)

        self.add(btn)
