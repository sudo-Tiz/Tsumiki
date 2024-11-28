from venv import logger
from fabric.widgets.eventbox import EventBox
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.box import Box

AUDIO_WIDGET = True

if AUDIO_WIDGET is True:
    try:
        from fabric.audio.service import Audio
    except Exception as e:
        logger.error(f"Error: {e}")
        AUDIO_WIDGET = False


# This class represents a widget that displays and controls the volume
class VolumeWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(name="volume", style_classes="bar-box", **kwargs)
        # Initialize the audio service
        self.audio = Audio()
        # Create a circular progress bar to display the volume level
        self.progress_bar = CircularProgressBar(
            name="volume-progress-bar", pie=True, size=24
        )
        # Create an event box to handle scroll events for volume control
        self.event_box = EventBox(
            events="scroll",
            child=Overlay(
                child=self.progress_bar,
                overlays=Label(
                    label="",
                    style="margin: 0px 6px 0px 0px; font-size: 12px",  # to center the icon glyph
                ),
            ),
        )
        # Connect the audio service to update the progress bar on volume change
        self.audio.connect("notify::speaker", self.on_speaker_changed)
        # Connect the event box to handle scroll events
        self.event_box.connect("scroll-event", self.on_scroll)
        # Add the event box as a child
        self.add(self.event_box)

    def on_scroll(self, _, event):
        # Adjust the volume based on the scroll direction
        match event.direction:
            case 0:
                self.audio.speaker.volume += 8
            case 1:
                self.audio.speaker.volume -= 8
        return

    def on_speaker_changed(self, *_):
        # Update the progress bar value based on the speaker volume
        if not self.audio.speaker:
            return
        self.progress_bar.value = self.audio.speaker.volume / 100
        self.audio.speaker.bind(
            "volume", "value", self.progress_bar, lambda _, v: v / 100
        )
        return
