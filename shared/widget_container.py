from fabric.widgets.box import Box


class WidgetContainer(Box):
    """A container for widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            name="widgets-container",
            spacing=4,
            orientation="h",
            style_classes="panel-box",
            **kwargs,
        )
