from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
)
from utils import NerdIcon, convert_bytes
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

        self.icon = NerdIcon(icon, size="12px")

        self.children = self.icon
        self.cpu_level_label = Label()

        invoke_repeater(interval, self.update_label, initial_call=True)

    def update_label(self):
        if self.enable_label:
            self.children = (self.icon, self.cpu_level_label)

        self.cpu_level_label.set_label(f"{psutil.cpu_percent()}%")
        return True


class Memory(Box):
    def __init__(
        self,
        icon: str = "",
        interval: int = 2000,
        enable_label: bool = True,
        enable_tooltip: bool = True,
    ):
        super().__init__(name="memory")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.icon = NerdIcon(icon, size="12px")

        self.children = self.icon
        self.memory_level_label = Label()

        invoke_repeater(interval, self.update_values, initial_call=True)

    def update_values(self):
        self.used_memory = psutil.virtual_memory().used
        self.total_memory = psutil.virtual_memory().total
        self.percent_used = psutil.virtual_memory().percent

        if self.enable_label:
            self.memory_level_label.set_label(self.get_used())
            self.children = (self.icon, self.memory_level_label)

        if self.enable_tooltip:
            self.set_tooltip_text(
                f"󰾆 {psutil.virtual_memory().percent}%\n {self.get_used()}GB/{self.get_total()}GB"
            )

        return True

    def get_used(self):
        return f"{format(convert_bytes(self.used_memory, "gb"),".1f")}"

    def get_total(self):
        return f"{format(convert_bytes(self.total_memory, "gb"),".1f")}"
