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
            icon_name=icons.icons["recorder"]["recording"],
            icon_size=self.config["icon_size"],
        )
        self.recording_idle_image = Image(
            icon_name="media-stop-symbolic",
            icon_size=self.config["icon_size"],
        )

        self.set_image(self.recording_idle_image)
        recorder_service = ScreenRecorder(widget_config)

        recorder_service.connect("recording", self.update_ui)

        self.connect(
            "clicked",
            lambda _: recorder_service.screencast_stop()
            if self.is_recording
            else recorder_service.screencast_start(fullscreen=True),
        )

    def update_ui(self, _, is_recording: bool):
        print(is_recording)
        if is_recording:
            self.set_image(self.recording_ongoing_image)
            self.is_recording = True
        else:
            self.set_image(self.recording_ongoing_image)
            self.is_recording = True
