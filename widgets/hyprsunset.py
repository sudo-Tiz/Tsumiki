from shared.buttontoggle import CommandSwitcher
from utils.config import BarConfig


class HyprSunsetWidget(CommandSwitcher):
    """A widget to control the hyprsunset command."""

    def __init__(self, config: BarConfig, **kwargs):
        # Store the configuration for hyprsunset
        self.config = config["hypr_sunset"]

        # Set the command to adjust the screen temperature
        self.command = f"hyprsunset -t {self.config['temperature']}"

        super().__init__(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hyprsunset",
            **kwargs,
        )
