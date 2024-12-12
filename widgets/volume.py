from venv import logger

from fabric.widgets.box import Box
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

from utils.config import BarConfig
from utils.functions import get_audio_icon_name, text_icon

AUDIO_WIDGET = True

if AUDIO_WIDGET is True:
    try:
        from fabric.audio.service import Audio
    except Exception as e:
        logger.error(f"Error: {e}")
        AUDIO_WIDGET = False


# TODO: handle mute and unmute events


class VolumeWidget(EventBox):
    """a widget that displays and controls the volume."""

    def __init__(self, config: BarConfig, **kwargs):
        super().__init__(events=["scroll", "smooth-scroll"], **kwargs)

        self.change_volume_by = 5

        # Initialize the audio service
        self.audio = Audio()

        self.config = config["volume"]

        # Create a circular progress bar to display the volume level
        self.progress_bar = CircularProgressBar(
            name="volume-progress-bar",
            pie=True,
            size=24,
        )

        self.volume_label = Label(style_classes="panel-label", visible=False)

        self.icon = text_icon(
            icon="",
            size=self.config["icon_size"],
            props={
                "style_classes": "volume-icon",
            },
        )

        # Create an event box to handle scroll events for volume control
        self.box = Box(
            spacing=4,
            name="volume",
            style_classes="panel-box",
            children=(
                Overlay(child=self.progress_bar, overlays=self.icon),
                self.volume_label,
            ),
        )
        # Connect the audio service to update the progress bar on volume change
        self.audio.connect("notify::speaker", self.on_speaker_changed)
        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

        # Add the event box as a child
        self.add(self.box)

    def on_scroll(self, _, event):
        # Adjust the volume based on the scroll direction

        val_y = event.delta_y

        if val_y > 0:
            self.audio.speaker.volume += self.change_volume_by
        else:
            self.audio.speaker.volume -= self.change_volume_by

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio.speaker:
            return

        if self.config["enable_tooltip"]:
            self.set_tooltip_text(self.audio.speaker.description)

        self.audio.speaker.connect("notify::volume", self.update_volume)
        self.update_volume()

    def toggle_mute(self):
        current_stream = self.audio_service.speaker
        if current_stream:
            current_stream.muted = not current_stream.muted

    def update_volume(self, *_):
        if self.audio.speaker:
            volume = round(self.audio.speaker.volume)
            self.progress_bar.set_value(volume / 100)

        if self.config["enable_label"]:
            self.volume_label.show()
            self.volume_label.set_text(f"{volume}%")

        self.icon.set_text(
            get_audio_icon_name(volume, self.audio.speaker.muted)["text_icon"]
        )
