from fabric.widgets.box import Box

from utils import BarConfig


class SpacingWidget(Box):
    """A simple widget to add spacing between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="spacing", **kwargs)


class DividerWidget(Box):
    """A simple widget to add a divider between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="divider", orientation="vertical", **kwargs)
