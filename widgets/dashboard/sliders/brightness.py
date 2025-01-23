from services.brightness import Brightness
from shared.setting_scale import SettingScale


class BrightnessSlider(SettingScale):
    """A widget to display a scale for brightness settings."""

    def __init__(
        self,
    ):
        self.client = Brightness().get_initial()
        super().__init__(
            min=0,
            max=self.client.max_screen if self.client.max_screen != -1 else 0,
            start_value=self.client.screen_brightness,
            pixel_size=24,
            icon_name="display-brightness-symbolic",
        )

        if self.client.screen_brightness == -1:
            self.destroy()
            return

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            self.client.connect("notify::screen-brightness", self.on_brightness_change)

    def on_scale_move(self, _, __, moved_pos):
        self.client.screen_brightness = moved_pos

    def on_brightness_change(self, service: Brightness, _):
        self.scale.set_value(service.screen_brightness)
