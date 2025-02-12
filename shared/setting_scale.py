from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scale import Scale


class SettingScale(Box):
    """A widget to display a scale for quick settings."""

    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        start_value: float = 50,
        icon_name: str = "package-x-generic-symbolic",
        pixel_size: int = 20,
        label=True,
        **kwargs,
    ):
        super().__init__(
            name="setting-scale",
            children=Box(spacing=5, h_expand=True),
            **kwargs,
        )
        self.pixel_size = pixel_size
        self.icon = Image(
            icon_name=icon_name, icon_size=self.pixel_size, style_classes="panel-icon"
        )
        self.icon_button = Button(image=self.icon, style_classes="panel-button")

        self.scale = Scale(
            marks=None,
            min_value=min,
            max_value=max,
            name="dashboard-slider",
            value=start_value,
            h_expand=True,
            increments=(1, 1),
        )

        self.label = Label(
            label=f"{start_value}%", name="setting-scale-label", visible=label
        )

        self.scale.connect(
            "change-value",
            lambda _, __, moved_pos: self.label.set_label(f"{round(moved_pos)}%"),
        )

        self.children = (self.icon_button, self.scale, self.label)
