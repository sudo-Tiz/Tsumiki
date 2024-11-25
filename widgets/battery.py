import math

import psutil
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from utils.utils import format_time


class Battery(Box):
    def __init__(
        self,
        interval: int = 2000,
        enable_label=True,
        enable_tooltip=True,
    ):
        # Initialize the Box with specific name and style
        super().__init__(name="battery", style_classes="bar-box")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        # Set up a repeater to call the update_battery_status method at specified intervals
        invoke_repeater(interval, self.update_battery_status, initial_call=True)

    def update_battery_status(self):
        # Get the battery status
        battery = psutil.sensors_battery()

        if battery is None:
            self.hide()
            return

        battery_percent = round(battery.percent) if battery else 0

        battery_label = Label(
            label=f"{battery_percent}%", style_classes="bar-button-label"
        )

        is_charging = battery.power_plugged if battery else False

        battery_icon = Image(
            icon_name=self.get_icon_name(
                battery_percent=battery_percent, is_charging=is_charging
            ),
            icon_size=14,
        )

        self.children = battery_icon

        # Update the label with the battery percentage if enabled
        if self.enable_label:
            self.children = (battery_icon, battery_label)

        # Update the tooltip with the battery status details if enabled
        if self.enable_tooltip:
            if battery_percent == 100:
                self.set_tooltip_text("Full")
            elif is_charging and battery_percent < 100:
                self.set_tooltip_text(f"Time to full: {format_time(battery.secsleft)}")
            else:
                self.set_tooltip_text(f"Time to empty: {format_time(battery.secsleft)}")

        return True

    def get_icon_name(self, battery_percent: int, is_charging: bool):
        # Determine the icon name based on the battery percentage and charging status
        if battery_percent == 100:
            return "battery-level-100-charged-symbolic"

        return f"battery-level-{math.floor(battery_percent/10) * 10}{'-charging' if is_charging else''}-symbolic"
