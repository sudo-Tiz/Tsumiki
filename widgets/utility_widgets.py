import gi
from fabric.widgets.box import Box
from gi.repository import Gtk

from utils.widget_config import BarConfig

gi.require_version("GtkLayerShell", "0.1")
gi.require_version("Gtk", "3.0")


class SpacingWidget(Box):
    """A simple widget to add spacing between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="spacing", **kwargs)
        self.config = widget_config["spacing"]
        self.set_style(f"min-width: {self.config['size']}px;")


class DividerWidget(Box):
    """A simple widget to add a divider between widgets."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="divider", **kwargs)

        self.children = Box(
            children=(
                Gtk.Separator(orientation=Gtk.Orientation.VERTICAL, visible=True),
            )
        )
