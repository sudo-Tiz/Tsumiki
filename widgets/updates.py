import os
from pathlib import PurePath
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
    exec_shell_command
)
from utils import NerdIcon



class Updates(Box):
    def __init__(
        self,
        icon: str = "",
        interval: int = 2000,
        enable_label: bool = True,
        enable_tooltip: bool = True,
    ):
        super().__init__(name="cpu")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.icon = NerdIcon(icon, size="12px")

        self.children = self.icon
        self.update_level_label = Label()

        invoke_repeater(interval, self.update, initial_call=True)

    def update(self):
        if self.enable_label:
            self.children = (self.icon, self.update_level_label)

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../services/update.sh')


        ## TODO: make this async
        self.update_level_label.set_label(exec_shell_command(f"{filename} -arch").strip("\n"))
        return True