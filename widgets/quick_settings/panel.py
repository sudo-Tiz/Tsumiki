from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label

from services import bluetooth_service, network_service, wifi
from services.mpris import MprisPlayerManager
from shared.cicrle_image import CircleImage
from shared.pop_over import PopOverWindow
from shared.submenu import QuickSubToggle
from shared.widget_container import ButtonWidget
from utils.functions import uptime
from utils.widget_settings import BarConfig
from utils.widget_utils import psutil_fabricator, text_icon
from widgets.player import PlayerBoxStack
from widgets.quick_settings.sliders.mic import MicrophoneSlider
from widgets.quick_settings.submenu.bluetooth import BluetoothSubMenu, BluetoothToggle
from widgets.quick_settings.submenu.wifi import WifiSubMenu, WifiToggle

from .sliders.audio import AudioSlider
from .sliders.brightness import BrightnessSlider


class QuickSettingsButtonBox(Box):
    """A box to display the quick settings buttons."""

    def __init__(self, **kwargs):
        super().__init__(
            orientation="v",
            spacing=4,
            h_align="start",
            v_align="start",
            h_expand=True,
            v_expand=True,
            **kwargs,
        )
        self.buttons = Box(
            orientation="h", spacing=4, h_align="center", v_align="center"
        )
        self.active_submenu = None

        # Bluetooth
        self.bluetooth_toggle = BluetoothToggle(
            submenu=BluetoothSubMenu(bluetooth_service),
            client=bluetooth_service,
        )

        # Wifi
        self.wifi_toggle = WifiToggle(
            submenu=WifiSubMenu(network_service),
            client=network_service,
        )

        self.buttons.add(self.wifi_toggle)
        self.buttons.add(self.bluetooth_toggle)

        self.wifi_toggle.connect("reveal-clicked", self.set_active_submenu)
        self.bluetooth_toggle.connect("reveal-clicked", self.set_active_submenu)

        self.add(self.buttons)
        self.add(self.wifi_toggle.submenu)
        self.add(self.bluetooth_toggle.submenu)

    def set_active_submenu(self, btn: QuickSubToggle):
        if btn.submenu != self.active_submenu and self.active_submenu is not None:
            self.active_submenu.do_reveal(False)

        self.active_submenu = btn.submenu
        self.active_submenu.toggle_reveal() if self.active_submenu else None


class QuickSettingsMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, config, **kwargs):
        super().__init__(
            name="quicksettings-menu", orientation="v", all_visible=True, **kwargs
        )

        self.config = config

        user_label = Label(label="User", v_align="center", h_align="start")

        uptime_label = Label(
            label=uptime(), style_classes="uptime", v_align="center", h_align="start"
        )

        info_box = Box(
            orientation="v",
            children=(user_label, uptime_label),
            spacing=8,
            style_classes="info-box",
        )

        box = CenterBox(
            orientation="v",
            start_children=Box(
                orientation="v",
                spacing=10,
                v_align="center",
                children=(
                    Box(
                        Box(
                            style_classes="user-box",
                            orientation="h",
                            spacing=8,
                            children=(
                                CircleImage(
                                    image_file=get_relative_path(
                                        "../../assets/images/no_image.jpg"
                                    ),
                                    size=70,
                                ),
                                info_box,
                            ),
                        ),
                    )
                ),
            ),
            center_children=Box(
                orientation="v",
                spacing=10,
                style_classes="slider-box",
                children=(BrightnessSlider(), AudioSlider(), MicrophoneSlider()),
            ),
            end_children=(
                PlayerBoxStack(MprisPlayerManager(), config=self.config["media"])
            ),
        )

        self.add(box)

        psutil_fabricator.connect(
            "changed",
            lambda _, value: (
                user_label.set_label(value.get("user")),
                uptime_label.set_label(value.get("uptime")),
            ),
        )


class QuickSettingsButtonWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="quick-settings-button", **kwargs)

        self.config = widget_config["quick_settings"]

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(QuickSettingsMenu(config=self.config),),
            visible=False,
            all_visible=False,
        )

        audio_icon = text_icon(
            "",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        wifi_icon = text_icon(
            "󰤨",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        brightness_icon = text_icon(
            "󰃠",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        popup.set_pointing_to(self)

        self.children = Box(
            children=(
                wifi_icon,
                audio_icon,
                brightness_icon,
            )
        )
        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
