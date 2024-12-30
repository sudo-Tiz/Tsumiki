from fabric.widgets.image import Image

from services.screenrecord import ScreenRecorder
from shared.widget_container import ButtonWidget
from utils import icons
from utils.widget_config import BarConfig


class Recorder(ButtonWidget):
    """A widget to record the system"""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="recorder", **kwargs)

        self.is_recording = False
        self.config = widget_config["recorder"]

        self.recording_ongoing_image = Image(
            h_align="center",
            v_align="center",
            icon_name=icons.icons["recorder"]["recording"],
            icon_size=self.config["icon_size"],
        )
        self.recording_idle_image = Image(
            icon_name=icons.icons["recorder"]["stopped"],
            icon_size=self.config["icon_size"],
            h_align="center",
            v_align="center",
        )

        self.set_image(self.recording_idle_image)
        if self.config["tooltip"]:
            self.set_tooltip_text("Recording stopped")

        recorder_service = ScreenRecorder(widget_config)

        recorder_service.connect("recording", self.update_ui)

        self.connect(
            "clicked",
            lambda _: recorder_service.screencast_stop()
            if self.is_recording
            else recorder_service.screencast_start(),
        )

    def update_ui(self, _, is_recording: bool):
        if is_recording:
            self.set_image(self.recording_ongoing_image)
            self.is_recording = True
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording started")
        else:
            self.set_image(self.recording_idle_image)
            self.is_recording = False
            if self.config["tooltip"]:
                self.set_tooltip_text("Recording stopped")
