import time

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import GLib

from shared.calendar import GtkCalendar
from shared.popover import PopOverWindow
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
            style_classes="notification-column",
            orientation="v",
            children=(notif_header,),
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

        self.add(notification_colum)
        self.add(date_column)

    def update_clock(self):
        self.clock_label.set_text(time.strftime("%H:%M"))
        return True


class NotificationWidget(Box):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        self.config = widget_config["notification"]
        super().__init__(
            name="notification-button", style_classes="panel-button", **kwargs
        )

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(DateNotificationMenu()),
            visible=False,
            all_visible=False,
        )

        btn = Button(
            style_classes="notification-button",
            image=Image(icon_name=icons["notifications"]["noisy"], icon_size=14),
            on_clicked=lambda _: popup.set_visible(not popup.get_visible()),
        )
        popup.set_pointing_to(btn)

        self.add(btn)
