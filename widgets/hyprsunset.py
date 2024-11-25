from shared.buttontoggle import CommandSwitcher
from fabric.widgets.button import Button


# This class represents a button widget for controlling the hyprsunset command
class HyprSunset(Button):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        # Store the configuration for hyprsunset
        self.config = config["hyprsunset"]
        # Set the command to adjust the screen temperature
        self.command = f"hyprsunset -t {self.config['temperature']}"

    def create(self):
        # Create a CommandSwitcher to toggle the hyprsunset command
        return CommandSwitcher(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hyprsunset",
        )
