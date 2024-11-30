from calendar import c
import time
from typing import Literal

from fabric.audio import Audio
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.widgets.revealer import Revealer
from fabric.widgets.image import Image
from fabric.widgets.scale import Scale, ScaleMark
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GLib, GObject
from services.brightness import Brightness
from utils.animator import Animator


class AnimatedScale(Scale):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animator = Animator(
            bezier_curve=(0.34, 1.56, 0.64, 1.0),
            duration=0.8,
            min_value=self.min_value,
            max_value=self.value,
            tick_widget=self,
            notify_value=lambda p, *_: self.set_value(p.value),
        )

    def animate_value(self, value: float):
        self.animator.pause()
        self.animator.min_value = self.value
        self.animator.max_value = value
        self.animator.play()


class BrightnessOSDContainer(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, orientation="h", spacing=12, name="osd-container")
        self.brightness_service = Brightness()
        self.level = Label()
        self.icon = self._create_icon("display-brightness-symbolic", 28)
        self.scale = self._create_brightness_scale()

        self.add(self.icon)
        self.add(self.scale)

        self.update_brightness()

        self.scale.connect("value-changed", lambda *_: self.update_brightness())
        self.brightness_service.connect("screen", self.on_brightness_changed)

    def _create_icon(self, icon_name: str, pixel_size: int) -> Image:
        icon = Image(icon_name=icon_name)
        icon.set_pixel_size(pixel_size)
        return icon

    def _create_brightness_scale(self) -> AnimatedScale:
        return AnimatedScale(
            marks=(ScaleMark(value=i) for i in range(1, 100, 10)),
            value=70,
            min_value=0,
            max_value=100,
            increments=(1, 1),
            orientation="h",
        )

    def update_brightness(self):
        current_brightness = self.brightness_service.screen_brightness
        if current_brightness != 0:
            normalized_brightness = (
                current_brightness / self.brightness_service.max_screen
            ) * 100
            self.scale.animate_value(normalized_brightness)
        print(current_brightness)
        self.update_icon(int(normalized_brightness))

    def update_icon(self, current_brightness):
        icon_name = self._get_brightness_icon_name(current_brightness)
        self.level.set_label(f"{current_brightness}%")
        self.icon.set_from_icon_name(icon_name)

    def on_brightness_changed(self, sender, value, *args):
        normalized_brightness = (value / self.brightness_service.max_screen) * 101
        self.scale.animate_value(normalized_brightness)

    def _get_brightness_icon_name(self, level: int) -> str:
        if level >= 66:
            return "display-brightness-high-symbolic"
        elif level < 32 and level > 0:
            return "display-brightness-medium-symbolic"
        elif level <= 1:
            return "display-brightness-off-symbolic"
        else:
            return "display-brightness-medium-symbolic"


class AudioOSDContainer(Box):
    __gsignals__ = {
        "volume-changed": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs, orientation="h", spacing=13, name="osd-container")
        self.audio = Audio()
        self.icon = self._create_icon("audio-volume-medium-symbolic", 28)
        self.level = Label(name="osd-level")
        self.scale = self._create_audio_scale()

        self.add(self.icon)
        self.add(self.scale)
        self.add(self.level)
        self.sync_with_audio()

        self.scale.connect("value-changed", self.on_volume_changed)
        self.audio.connect("notify::speaker", self.on_audio_speaker_changed)

    def _create_icon(self, icon_name: str, pixel_size: int) -> Image:
        icon = Image(icon_name=icon_name)
        icon.set_pixel_size(pixel_size)
        return icon

    def _create_audio_scale(self) -> AnimatedScale:
        return AnimatedScale(
            marks=(ScaleMark(value=i) for i in range(1, 100, 10)),
            value=70,
            min_value=0,
            max_value=100,
            increments=(1, 1),
            orientation="h",
        )

    def sync_with_audio(self):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)
            self.scale.set_value(volume)
            self.update_icon(volume)

    def on_volume_changed(self, *_):
        if self.audio.speaker:
            volume = self.scale.value
            if 0 <= volume <= 100:
                self.audio.speaker.set_volume(volume)
                self.update_icon(volume)
                self.emit("volume-changed")

    def on_audio_speaker_changed(self, *_):
        if self.audio.speaker:
            self.audio.speaker.connect("notify::volume", self.update_volume)
            self.update_volume()

    def update_volume(self, *_):
        if self.audio.speaker and not self.is_hovered():
            volume = round(self.audio.speaker.volume)
            self.scale.set_value(volume)
            self.update_icon(volume)

    def update_icon(self, volume):
        icon_name = self._get_audio_icon_name(volume)
        self.level.set_label(f"{volume}%")
        self.icon.set_from_icon_name(icon_name)

    def _get_audio_icon_name(self, volume: int) -> str:
        if volume >= 66:
            return "audio-volume-high-symbolic"
        elif volume < 32 and volume > 0:
            return "audio-volume-low-symbolic"
        elif volume <= 0:
            return "audio-volume-muted-symbolic"
        else:
            return "audio-volume-medium-symbolic"


class OSDContainer(Window):
    def __init__(
        self,
        anchor: str = "bottom center",
        timeout=1000,
        transition_duration=100,
        keyboard_mode: Literal["none", "exclusive", "on-demand"] = "on-demand",
        **kwargs,
    ):
        self.audio_container = AudioOSDContainer()
        self.brightness_container = BrightnessOSDContainer()

        self.timeout = timeout

        self.revealer = Revealer(
            name="osd-revealer",
            transition_type="slide-up",
            transition_duration=transition_duration,
            child_revealed=False,
        )

        self.main_box = Box(
            orientation="v",
            spacing=13,
            children=[self.revealer],
        )

        super().__init__(
            layer="overlay",
            anchor=anchor,
            child=self.main_box,
            visible=False,
            pass_through=True,
            keyboard_mode=keyboard_mode,
            **kwargs,
        )

        self.last_activity_time = time.time()

        self.audio_container.audio.connect("notify::speaker", self.show_audio)
        self.brightness_container.brightness_service.connect(
            "screen", self.show_brightness
        )
        self.audio_container.connect("volume-changed", self.show_audio)

        GLib.timeout_add(100, self.check_inactivity)

    def show_audio(self, *_):
        self.show_box(box_to_show="audio")
        self.reset_inactivity_timer()

    def show_brightness(self, *_):
        self.show_box(box_to_show="brightness")
        self.reset_inactivity_timer()

    def show_box(self, box_to_show: Literal["audio", "brightness"]):
        self.set_visible(True)
        if box_to_show == "audio":
            self.revealer.children = self.audio_container
        elif box_to_show == "brightness":
            self.revealer.children = self.brightness_container
        self.revealer.set_reveal_child(True)
        self.reset_inactivity_timer()

    def start_hide_timer(self):
        self.set_visible(False)

    def reset_inactivity_timer(self):
        self.last_activity_time = time.time()

    def check_inactivity(self):
        if time.time() - self.last_activity_time >= (self.timeout / 1000):
            self.start_hide_timer()
        return True
