import time

import gi
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import Gtk

from shared.popover import PopOverWindow
from utils.functions import uptime
from utils.icons import icons
from utils.widget_config import BarConfig

gi.require_version("Gtk", "3.0")


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(self):
        super().__init__(name="datemenu", orientation="h")

        self.clock_label = Label(
            label=time.strftime("%H:%M"),
            style_classes="clock",
        )

        self.uptime = Label(style_classes="uptime", label=uptime())

        invoke_repeater(1000, self.update_lables, initial_call=True)

        # Placeholder for when there are no notifications
        placeholder = Box(
            style_classes="placeholder",
            orientation="v",
            h_align="center",
            v_align="center",
            v_expand=True,
            h_expand=True,
            visible=True,  # visible if no notifications
            children=(
                Image(
                    icon_name=icons["notifications"]["silent"],
                    icon_size=64,
                    style="margin-bottom: 10px;",
                ),
                Label("Your inbox is empty"),
            ),
        )

        # Header for the notification column
        dnd_switch = Gtk.Switch(
            name="notification-switch",
            active=True,
            valign=Gtk.Align.CENTER,
            visible=True,
        )

        notif_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label("Do Not Disturb"), dnd_switch),
        )

        clear_button = Button(
            name="clear-button",
            v_align="center",
            child=Box(
                children=(
                    Label("Clear"),
                    Image(
                        icon_name=icons["notifications"]["noisy"],
                        icon_size=13,
                        name="clear-icon",
                    ),
                )
            ),
        )

        notif_header.pack_end(
            clear_button,
            False,
            False,
            0,
        )

        # Notification body column
        notification_colum = Box(
            name="notification-column",
            orientation="v",
            children=(
                notif_header,
                ScrolledWindow(
                    v_expand=True,
                    style_classes="notification-scrollable",
                    h_scrollbar_policy="never",
                    child=Box(children=(placeholder)),
                ),
            ),
        )

        # Date and time column

        date_column = Box(
            style_classes="date-column",
            orientation="v",
            children=(
                Box(
                    style_classes="clock-box",
                    orientation="v",
                    children=(self.clock_label, self.uptime),
                ),
                Box(
                    style_classes="calendar",
                    children=(
                        Gtk.Calendar(
                            visible=True,
                            hexpand=True,
                            halign=Gtk.Align.CENTER,
                        )
                    ),
                ),
            ),
        )

        self.children = (
            notification_colum,
            Gtk.Separator(
                visible=True,
            ),
            date_column,
        )

    def update_lables(self):
        self.clock_label.set_text(time.strftime("%H:%M"))
        self.uptime.set_text(uptime())
        return True


class DateTimeWidget(Box):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", style_classes="panel-box", **kwargs)
        self.config = widget_config["date_time"]
        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(DateNotificationMenu()),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.children = DateTime(
            self.config["format"],
            on_clicked=lambda *_: popup.set_visible(not popup.get_visible()),
        )
