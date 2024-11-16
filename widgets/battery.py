import psutil

from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from utils import NerdIcon, format_time


class BatteryLabel(Box):
    ICONS_CHARGING = [
        "󰂆",  # 10
        "󰂆",
        "󰂇",
        "󰂇",
        "󰂈",
        "󰢝",
        "󰂉",
        "󰢞",
        "󰂊",
        "󰂋",
        "󰂅",
    ]
    ICONS_NOT_CHARGING = [
        "󰂃",  # 0
        "󰁺",  # 10
        "󰁻",
        "󰁼",
        "󰁽",
        "󰁾",
        "󰁿",
        "󰂀",
        "󰂁",
        "󰂂",
        "󰁹",
    ]

    def __init__(
        self, enable_label: bool | None = None, enable_tooltip: bool | None = None
    ):
        super().__init__(name="battery")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        invoke_repeater(2000, self.update_battery_status, initial_call=True)

    def update_battery_status(self):
        battery = psutil.sensors_battery()

        if battery is None:
            self.hide()
            return

        battery_percent = round(battery.percent) if battery else 0.0

        battery_label = Label(label=f"{battery_percent}%")

        is_charging = battery.power_plugged if battery else False
        icons = self.ICONS_CHARGING if is_charging else self.ICONS_NOT_CHARGING

        index = min(max(battery_percent // 10, 0), 10)
        battery_icon = NerdIcon(icons[index], size="16px")

        self.children = battery_icon

        if self.enable_label and self.enable_label is not None:
            self.children = (battery_icon, battery_label)

        ## fix this to display time left for charging
        if not is_charging:
            self.set_tooltip_text(format_time(battery.secsleft))

        return True
