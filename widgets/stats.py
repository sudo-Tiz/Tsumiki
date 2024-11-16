from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
)
from utils import NerdIcon
import psutil


class Cpu(Box):
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

        self.interval = interval

        self.cpu_icon = NerdIcon(icon, size="12px")

        self.children = self.cpu_icon
        self.cpu_level_label = Label()

        if self.enable_label:
            self.children = (self.cpu_icon, self.cpu_level_label)

        invoke_repeater(self.interval, self.update_progress_bars)

    def update_progress_bars(self):
        self.cpu_level_label.set_label(f"{psutil.cpu_percent()}%")
        return True
