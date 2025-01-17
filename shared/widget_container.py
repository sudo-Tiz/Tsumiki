from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox


class BoxWidget(Box):
    """A container for box widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            spacing=4,
            style_classes="panel-box",
            **kwargs,
        )


class EventBoxWidget(EventBox):
    """A container for box widgets."""

    def __init__(self, children, **kwargs):
        super().__init__(
            **kwargs,
        )

        self.box = Box(
            spacing=4,
            style_classes="panel-box",
            children=children,
        )
        self.children = (self.box,)




class ButtonWidget(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )
