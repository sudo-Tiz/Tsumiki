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

        cpu_icon = NerdIcon(icon, size="12px")

        self.children = cpu_icon
        self.cpu_level_label = Label()


        if self.enable_label:
            self.children = (cpu_icon, self.cpu_level_label)

        invoke_repeater(interval, self.update_label)

    def update_label(self):
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
        super().__init__(name="cpu")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        memory_icon = NerdIcon(icon, size="12px")

        self.children = memory_icon
        self.memory_level_label = Label()

        self.set_tooltip_text = f"󰾆 {psutil.virtual_memory().percent}"


        if self.enable_label:
            self.children = (memory_icon, self.memory_level_label)

        invoke_repeater(interval, self.update_label)

    def update_label(self):
        self.memory_level_label.set_label(f"{format(convert_bytes(psutil.virtual_memory().used, "gb"),".1f")}")
        return True
