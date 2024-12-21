import time

from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GLib

from shared.calendar import GtkCalendar
from shared.popover import PopOverWindow
from shared.separator import GtkSeparator
from shared.switch import Switch
from utils.icons import icons
from utils.widget_config import BarConfig


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(self):
        super().__init__(name="datemenu", orientation="h")

        GLib.timeout_add(1000, self.update_clock)

        self.clock_label = Label(
            "10:00",
            style_classes="clock",
        )

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

        notif_header = Box(
            style_classes="header",
            orientation="h",
            children=(
                Label("Do Not Disturb"),
                Switch(
                    name="notification-switch",
                    active=True,
                ),
            ),
        )

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

        date_column = Box(
            style_classes="date-column",
            orientation="v",
            children=(
                Box(
                    style_classes="clock-box",
                    orientation="v",
                    children=(self.clock_label),
                ),
                Box(
                    style_classes="calendar",
                    children=(
                        GtkCalendar(
                            h_expand=True,
                        ),
                    ),
                ),
            ),
        )

        notif_header.pack_end(
            EventBox(
                child=Box(
                    style_classes="header-action",
                    children=(
                        Label("Clear"),
                        Image(icon_name=icons["notifications"]["noisy"], icon_size=13),
                    ),
                )
            ),
            False,
            False,
            0,
        )

        self.children = (
            notification_colum,
            GtkSeparator(),
            date_column,
        )

    def update_clock(self):
        self.clock_label.set_text(time.strftime("%H:%M"))
        return True


class DateTimeWidget(EventBox):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", **kwargs)
        self.config = widget_config["notification"]
        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(DateNotificationMenu()),
            visible=False,
            all_visible=False,
        )

        self.connect(
            "button-press-event", lambda *_: popup.set_visible(not popup.get_visible())
        )

        popup.set_pointing_to(self)

        self.children = Box(
            style_classes="panel-box",
            children=(
                Image(
                    icon_name=icons["notifications"]["noisy"],
                    icon_size=14,
                    style="margin-right: 5px;",
                ),
                DateTime("%H:%M"),
            ),
        )
