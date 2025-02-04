import os

from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label

import utils.functions as helpers
from services import audio_service, bluetooth_service, network_service
from services.brightness import Brightness
from services.mpris import MprisPlayerManager
from shared.cicrle_image import CircleImage
from shared.pop_over import PopOverWindow
from shared.submenu import QuickSubToggle
from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig
from utils.widget_utils import (
    get_audio_icon_name,
    get_brightness_icon_name,
    psutil_fabricator,
    text_icon,
)
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

        user_image = (
            get_relative_path("../../assets/images/no_image.jpg")
            if not os.path.exists(os.path.expandvars("$HOME/.face"))
            else os.path.expandvars("$HOME/.face")
        )

        user_label = Label(label="User", v_align="center", h_align="start")

        uptime_label = Label(
            label=helpers.uptime(),
            style_classes="uptime",
            v_align="center",
            h_align="start",
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
                        style_classes="user-box",
                        orientation="h",
                        spacing=8,
                        children=(
                            CircleImage(
                                image_file=user_image,
                                size=70,
                            ),
                            info_box,
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
                user_label.set_label(
                    f"{helpers.get_distro_icon()} {value.get('user')}"
                ),
                uptime_label.set_label(f" {value.get('uptime')}"),
            ),
        )


class QuickSettingsButtonWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="quick-settings-button", **kwargs)

        self.config = widget_config["quick_settings"]

        self.audio = audio_service
        # Initialize the audio service
        self.brightness_service = Brightness().get_initial()

        self.audio.connect("notify::speaker", self.on_speaker_changed)
        self.brightness_service.connect("screen", self.on_brightness_changed)

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(QuickSettingsMenu(config=self.config),),
            visible=False,
            all_visible=False,
        )

        self.audio_icon = text_icon(
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

        self.brightness_icon = text_icon(
            "󰃠",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        popup.set_pointing_to(self)

        self.children = Box(
            children=(
                wifi_icon,
                self.audio_icon,
                self.brightness_icon,
            )
        )
        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio.speaker:
            return

        self.audio.speaker.connect("notify::volume", self.update_volume)
        self.update_volume()

    def update_volume(self, *_):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)

            self.audio_icon.set_text(
                get_audio_icon_name(volume, self.audio.speaker.muted)["text_icon"]
            )

    def on_brightness_changed(self, *_):
        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )
        self.brightness_icon.set_text(
            get_brightness_icon_name(normalized_brightness)["text_icon"]
        )
