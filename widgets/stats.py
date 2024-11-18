from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import (
    invoke_repeater,
)
from utils import TextIcon, convert_bytes
import psutil


class Cpu(Box):
    def __init__(
        self,
        icon: str = "",
        icon_size="12px",
        interval: int = 2000,
        enable_label=True,
        enable_tooltip=True,
    ):
        super().__init__(name="cpu")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.text_icon = TextIcon(
            icon, size=icon_size, props={"style_classes": "bar-text-icon"}
        )
        self.children = self.text_icon
        self.cpu_level_label = Label(label="0%", style_classes="bar-button-label")

        invoke_repeater(interval, self.update_label, initial_call=True)

    def update_label(self):
        if self.enable_label:
            self.cpu_level_label.set_label(f"{psutil.cpu_percent()}%")
            self.children = (self.text_icon, self.cpu_level_label)

        return True


class Memory(Box):
    def __init__(
        self,
        icon: str = "",
        icon_size="12px",
        interval: int = 2000,
        enable_label=True,
        enable_tooltip=True,
    ):
        super().__init__(name="memory")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.icon = TextIcon(
            icon, size=icon_size, props={"style_classes": "bar-text-icon"}
        )
        self.children = self.icon
        self.memory_level_label = Label(label="0%", style_classes="bar-button-label")

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


class Storage(Box):
    def __init__(
        self,
        icon: str = "󰋊",
        icon_size="14px",
        interval: int = 2000,
        enable_label=True,
        enable_tooltip=True,
    ):
        super().__init__(name="storage")
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.icon = TextIcon(
            icon, size=icon_size, props={"style_classes": "bar-text-icon"}
        )

        self.children = self.icon
        self.storage_level_label = Label(label="0", style_classes="bar-button-label")

        invoke_repeater(interval, self.update_values, initial_call=True)

    def update_values(self):
        self.disk = psutil.disk_usage("/")
        if self.enable_label:
            self.storage_level_label.set_label(f"{self.get_used()}GB")
            self.children = (self.icon, self.storage_level_label)

        if self.enable_tooltip:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n {self.get_used()}GB/{self.get_total()}GB"
            )

        return True

    def get_used(self):
        return f"{format(convert_bytes(self.disk.used, "gb"),".1f")}"

    def get_total(self):
        return f"{format(convert_bytes(self.disk.total, "gb"),".1f")}"
