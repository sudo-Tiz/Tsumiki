from services.brightness import Brightness
from shared.setting_scale import SettingSlider
from utils.icons import icons


class BrightnessSlider(SettingSlider):
    """A widget to display a scale for brightness settings."""

    def __init__(
        self,
    ):
        self.client = Brightness().get_initial()
        super().__init__(
            pixel_size=20,
            icon_name=icons["brightness"]["screen"],
        )

        if self.client.screen_brightness == -1:
            self.destroy()
            return

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            self.client.connect("screen", self.on_brightness_change)

    def on_scale_move(self, _, __, moved_pos):
        self.client.screen_brightness = moved_pos

    def on_brightness_change(self, service: Brightness, _):
        self.scale.set_value(service.screen_brightness)
        self.scale.set_tooltip_text(f"{round(service.screen_brightness)}%")
