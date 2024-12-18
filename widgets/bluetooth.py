from fabric.bluetooth import BluetoothClient
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

import utils.icons as icons
from utils.widget_config import BarConfig


class BlueToothWidget(Box):
    """A widget to display the Bluetooth status."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(**kwargs, style_classes="panel-box")
        self.bluetooth_client = BluetoothClient()

        self.icons = icons.icons["bluetooth"]

        self.icon_size = 14

        self.config = widget_config["bluetooth"]

        self.bluetooth_icon = Image(
            icon_name=self.icons["enabled"],
            icon_size=self.icon_size,
        )

        self.bt_label = Label(label="", visible=False, style_classes="panel-text")

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        self.update_bluetooth_status()

    def update_bluetooth_status(self, *args):
        bt_status = "on" if self.bluetooth_client.enabled else "off"

        icon = self.icons["enabled"] if bt_status == "on" else self.icons["disabled"]

        if self.bluetooth_icon:
            self.remove(self.bluetooth_icon)

        self.bluetooth_icon.set_from_icon_name(icon, icon_size=self.icon_size)
        self.children = (self.bluetooth_icon, self.bt_label)

        if self.config["label"]:
            self.bt_label.set_text(bt_status.capitalize())
            self.bt_label.show()

        if self.config["tooltip"]:
            self.set_tooltip_text(f"Bluetooth is {bt_status}")

    def on_destroy(self):
        self.bluetooth_client.disconnect("changed", self.update_bluetooth_status)
