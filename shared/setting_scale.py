from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.scale import Scale


class SettingScale(Box):
    """A widget to display a scale for quick settings."""

    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        start_value: float = 50,
        icon_name: str = "package-x-generic-symbolic",
        pixel_size: int = 22,
        **kwargs,
    ):
        super().__init__(
            name="setting-scale",
            children=Box(spacing=5, h_expand=True),
            **kwargs,
        )
        self.pixel_size = pixel_size
        self.icon = Image(icon_name=icon_name, icon_size=self.pixel_size)
        self.icon_button = Button(image=self.icon, name="panel-button")

        self.scale = Scale(
            min_value=min,
            max_value=max,
            name="dashboard-slider",
            value=start_value,
            h_expand=True,
        )

        self.children = (self.icon_button, self.scale)
