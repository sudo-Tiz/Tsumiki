from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.functions import text_icon
from utils.widget_settings import BarConfig

MIC_ON_ICON = "󰍬"
MIC_OFF_ICON = "󰍭"


class MicrophoneIndicatorWidget(ButtonWidget):
    """A widget to display the current microphone status."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(**kwargs)

        self.config = widget_config["microphone"]

        self.box = Box()
        self.children = (self.box,)

        self.icon = text_icon(
            icon=MIC_OFF_ICON,
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.mic_label = Label(
            label="",
            style_classes="panel-text",
            visible=False,
        )

        self.audio_service.connect("microphone_changed", self.update_status)
        self.update_status()

        self.box.children = (self.icon, self.mic_label)

    def update_status(self, *_):
        current_microphone = self.audio_service.microphone

        if current_microphone:
            is_muted = current_microphone.muted
            self.icon.set_label(MIC_OFF_ICON if is_muted else MIC_ON_ICON)

            # Update the label  if enabled
            if self.config["label"]:
                self.mic_label.set_label("Off" if is_muted else "On")
                self.mic_label.show()

            if self.config["tooltip"]:
                self.set_tooltip_text(
                    "Microphone is muted" if is_muted else "Microphone is on"
                )

            self.icon.set_visible(True)
        else:
            self.icon.set_visible(False)

        return True
