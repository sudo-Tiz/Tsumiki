import psutil
from fabric.utils import invoke_repeater
from fabric.widgets.label import Label

import utils.functions as helpers
from shared.widget_container import BoxWidget
from utils.icons import common_text_icons
from utils.widget_config import BarConfig


class CpuWidget(BoxWidget):
    """A widget to display the current CPU usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="cpu",
            **kwargs,
        )

        self.config = widget_config["cpu"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.cpu_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.children = (self.text_icon, self.cpu_level)

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(self.config["interval"], self.update_label, initial_call=True)

    def update_label(self):
        # Update the label with the current CPU usage if enabled
        if self.config["label"]:
            self.cpu_level_label.show()
            self.cpu_level_label.set_label(f"{psutil.cpu_percent()}%")

        return True


class MemoryWidget(BoxWidget):
    """A widget to display the current memory usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="memory",
            **kwargs,
        )

        self.config = widget_config["memory"]

        # Create a TextIcon with the specified icon and size
        self.icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )
        self.memory_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.children = (self.icon, self.memory_level_label)

        # Set up a repeater to call the update_values method at specified intervals
        invoke_repeater(self.config["interval"], self.update_values, initial_call=True)

    def update_values(self):
        # Get the current memory usage
        self.used_memory = psutil.virtual_memory().used
        self.total_memory = psutil.virtual_memory().total
        self.percent_used = psutil.virtual_memory().percent

        # Update the label with the used memory if enabled
        if self.config["label"]:
            self.memory_level_label.set_label(self.get_used())
            self.memory_level_label.show()

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {psutil.virtual_memory().percent}%\n{common_text_icons['memory']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return f"{format(helpers.convert_bytes(self.used_memory, 'gb'),'.1f')}"

    def get_total(self):
        return f"{format(helpers.convert_bytes(self.total_memory, 'gb'),'.1f')}"


class StorageWidget(BoxWidget):
    """A widget to display the current storage usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="storage",
            **kwargs,
        )
        self.config = widget_config["storage"]

        # Create a TextIcon with the specified icon and size
        self.icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.storage_level_label = Label(
            label="0", style_classes="panel-text", visible=False
        )

        self.children = (self.icon, self.storage_level_label)

        # Set up a repeater to call the update_values method at specified intervals
        invoke_repeater(self.config["interval"], self.update_values, initial_call=True)

    def update_values(self):
        # Get the current disk usage
        self.disk = psutil.disk_usage("/")

        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.storage_level_label.set_label(f"{self.get_used()}")
            self.storage_level_label.show()

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n{common_text_icons['storage']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return f"{format(helpers.convert_bytes(self.disk.used, 'gb'),'.1f')}"

    def get_total(self):
        return f"{format(helpers.convert_bytes(self.disk.total, 'gb'),'.1f')}"
