from fabric.bluetooth import BluetoothClient
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from utils.config import BarConfig


class BlueToothWidget(Box):
    """A widget to display the Bluetooth status."""

    def __init__(self, config: BarConfig, **kwargs):
        super().__init__(**kwargs, style_classes="panel-box")
        self.bluetooth_client = BluetoothClient()

        self.ICONS = {
            "off": "bluetooth-disabled",
            "on": "bluetooth-active",
            "paired": "bluetooth-paired",
        }

        self.config = config["bluetooth"]

        self.bluetooth_icon = Image(
            icon_name=self.ICONS["off"],
            icon_size=24,
        )

        self.bt_label = Label(label="",visible=False)

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        self.update_bluetooth_status()

    def update_bluetooth_status(self, *args):
        bt_status = "on" if self.bluetooth_client.enabled else "off"

        icon = self.ICONS[bt_status]

        if self.bluetooth_icon:
            self.remove(self.bluetooth_icon)

        self.bluetooth_icon.set_from_icon_name(icon)
        self.add(self.bluetooth_icon,self.bt_label)

        if self.config["enable_label"]:
            self.bt_label.set_text(bt_status.capitalize())
            self.bt_label.show()

        if self.config["enable_tooltip"]:
            self.set_tooltip_text(f"Bluetooth is {bt_status}")

    def on_destroy(self):
        self.bluetooth_client.disconnect("changed", self.update_bluetooth_status)
