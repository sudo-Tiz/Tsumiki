from fabric.bluetooth import BluetoothClient
from fabric.widgets.box import Box
from fabric.widgets.image import Image

from utils.config import BarConfig


class Bluetooth(Box):
    """A widget to display the Bluetooth status."""

    def __init__(self,config: BarConfig, **kwargs):
        super().__init__(**kwargs, style_classes="panel-box")
        self.bluetooth_client = BluetoothClient()

        self.ICONS = {
            "off": "bluetooth-disabled",
            "on": "bluetooth-active",
            "paired": "bluetooth-paired",
        }

        self.bluetooth_icon = Image(
            icon_name=self.ICONS["off"],
            icon_size=24,
        )

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        self.update_bluetooth_status()

    def update_bluetooth_status(self, *args):
        icon = self.ICONS["on"] if self.bluetooth_client.enabled else self.ICONS["off"]

        if self.bluetooth_icon:
            self.remove(self.bluetooth_icon)

        self.bluetooth_icon.set_from_icon_name(icon)
        self.add(self.bluetooth_icon)

    def on_destroy(self):
        self.bluetooth_client.disconnect("changed", self.update_bluetooth_status)
