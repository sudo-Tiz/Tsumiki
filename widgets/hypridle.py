from fabric.widgets.button import Button

from shared.buttontoggle import CommandSwitcher


# This class represents a button widget for controlling the hypridle command
class HyprIdle(Button):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        # Store the configuration for hypridle
        self.config = config["hypridle"]
        # Set the command to hypridle
        self.command = "hypridle"

    def create(self):
        # Create a CommandSwitcher to toggle the hypridle command
        return CommandSwitcher(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hypridle",
        )
