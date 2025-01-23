from services import audio_service
from shared.setting_scale import SettingScale


class AudioSlider(SettingScale):
    """A widget to display a scale for audio settings."""

    def __init__(self):
        self.client = audio_service
        super().__init__(min=0, max=100, icon_name="audio-volume-high-symbolic")
        self.scale.connect("change-value", self.on_scale_move)
        self.client.connect("speaker-changed", self.on_speaker_change)
        self.icon_button.connect("clicked", self.on_button_click)

    def on_scale_move(self, _, __, moved_pos):
        self.client.speaker.volume = moved_pos

    def on_speaker_change(self, *args):
        self.scale.set_sensitive(not audio_service.speaker.muted)
        self.scale.set_value(audio_service.speaker.volume)

    def on_button_click(self, *_):
        self.client.speaker.muted = not self.client.speaker.muted
