from shared.buttontoggle import CommandSwitcher
from fabric.widgets.button import Button


class HyprIdle(Button):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.config = config["hypridle"]

        self.command = "hypridle"

    def create(self):
        return CommandSwitcher(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hypridle",
        )
