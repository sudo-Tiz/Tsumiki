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

    def __init__(self, **kwargs):
        super().__init__(
            name="panel-eventbox",
            **kwargs,
        )

    # self.connect("enter-notify-event", lambda *_:
    # self.children[0].add_style_class("widget_hover"))


class ButtonWidget(Button):
    """A container for button widgets."""

    def __init__(self, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )
        from utils.config import widget_config

        widget_style = widget_config["options"]["widget_style"]

        self.add_style_class(widget_style)
