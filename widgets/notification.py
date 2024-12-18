
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from utils.functions import text_icon
from utils.widget_config import BarConfig
import gi
from gi.repository import Gtk

gi.require_version("Gtk", "3.0")


class NotificationWidget(Box):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, **kwargs):

        self.config = widget_config["notification"]
        super().__init__(name="notification-button", style_classes="panel-button", **kwargs)

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(Gtk.ModelButton(label="Item 1"), False, True, 10)
        vbox.pack_start(Gtk.Label(label="Item 2"), False, True, 10)
        vbox.show_all()
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)


        button = Gtk.MenuButton(label="Click Me", popover=self.popover)
        self.children = (button)




