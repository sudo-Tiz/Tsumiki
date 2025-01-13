from fabric.widgets.box import Box
from fabric.widgets.button import Button


class BoxWidget(Box):
    """A container for box widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            spacing=4,
            style_classes="panel-box",
            **kwargs,
        )


class ButtonWidget(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-box",
            **kwargs,
        )
