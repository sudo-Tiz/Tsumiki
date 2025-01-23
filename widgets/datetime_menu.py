import time
from typing import List

import gi
from fabric.notifications import Notification
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GdkPixbuf, Gtk

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from services.cache_notification import NotificationCacheService
from shared.custom_image import CustomImage
from shared.pop_over import PopOverWindow
from shared.separator import Separator
from shared.widget_container import ButtonWidget
from utils.functions import uptime
from utils.icons import icons
from utils.widget_settings import BarConfig

gi.require_version("Gtk", "3.0")


class DateMenuNotification(EventBox):
    """A widget to display a notification."""

    def __init__(
        self,
        index: int,
        notification: Notification,
        **kwargs,
    ):
        super().__init__(
            size=(constants.NOTIFICATION_WIDTH, -1),
            name="notification-eventbox",
            **kwargs,
        )

        self._notification = notification

        self._timeout_id = None

        self.notification_cache_service = NotificationCacheService().get_initial()

        self.notification_box = Box(
            spacing=8,
            name="notification",
            orientation="v",
        )

        if notification.urgency == 2:
            self.notification_box.add_style_class("critical")

        header_container = Box(
            spacing=8, orientation="h", style_classes="notification-header"
        )

        header_container.children = (
            helpers.get_icon(notification.app_icon, 25),
            Label(
                markup=helpers.escape_markup(
                    str(
                        self._notification.summary
                        if self._notification.summary
                        else notification.app_name,
                    )
                ),
                h_align="start",
                style_classes="summary",
                ellipsization="end",
            ),
        )
        close_button = Button(
            image=Image(
                icon_name=helpers.check_icon_exists(
                    "close-symbolic",
                    icons["ui"]["close"],
                ),
                icon_size=16,
            ),
            style_classes="close-button",
            on_clicked=lambda _: self.notification_cache_service.remove_notification(
                index
            ),
        )

        header_container.pack_end(
            Box(v_align="start", children=(close_button)),
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=4, orientation="h", style_classes="notification-body"
        )

        # Use provided image if available, otherwise use "notification-symbolic" icon
        if image_pixbuf := self._notification.image_pixbuf:
            body_container.add(
                Box(
                    v_expand=True,
                    v_align="center",
                    children=CustomImage(
                        pixbuf=image_pixbuf.scale_simple(
                            constants.NOTIFICATION_IMAGE_SIZE,
                            constants.NOTIFICATION_IMAGE_SIZE,
                            GdkPixbuf.InterpType.BILINEAR,
                        ),
                        style_classes="image",
                    ),
                )
            )

        body_container.add(
            Label(
                markup=helpers.escape_markup(self._notification.body),
                line_wrap="word-char",
                ellipsization="end",
                v_align="start",
                h_align="start",
                style_classes="body",
            ),
        )

        # Add the header, body, and actions to the notification box
        self.notification_box.children = (
            header_container,
            body_container,
        )

        # Add the notification box to the EventBox
        self.add(self.notification_box)


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            name="datemenu",
            orientation="h",
            **kwargs,
        )
        self.notification_cache_service = NotificationCacheService().get_initial()

        self.clock_label = Label(
            label=time.strftime("%H:%M"),
            style_classes="clock",
        )

        notifications: List[Notification] = (
            self.notification_cache_service.get_deserailized()
        )

        notifications_list = [
            DateMenuNotification(notification=val, index=index)
            for index, val in enumerate(notifications)
        ]

        self.notification_list_box = Box(
            orientation="v",
            h_align="center",
            spacing=8,
            h_expand=True,
            visible=len(notifications) > 0,
            children=notifications_list,
        )

        self.uptime = Label(style_classes="uptime", label=uptime())

        # Placeholder for when there are no notifications
        placeholder = Box(
            style_classes="placeholder",
            orientation="v",
            h_align="center",
            v_align="center",
            v_expand=True,
            h_expand=True,
            visible=len(notifications) == 0,  # visible if no notifications
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
        self.dnd_switch = Gtk.Switch(
            name="notification-switch",
            active=False,
            valign=Gtk.Align.CENTER,
            visible=True,
        )

        notif_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label("Do Not Disturb"), self.dnd_switch),
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

        clear_button.connect(
            "clicked", lambda _: self.notification_cache_service.clear_notifications()
        )

        notif_header.pack_end(
            clear_button,
            False,
            False,
            0,
        )

        # Notification body column
        notification_column = Box(
            name="notification-column",
            orientation="v",
            children=(
                notif_header,
                ScrolledWindow(
                    v_expand=True,
                    style_classes="notification-scrollable",
                    h_scrollbar_policy="never",
                    child=Box(children=(placeholder, self.notification_list_box)),
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
            notification_column,
            Separator(),
            date_column,
        )

        invoke_repeater(1000, self.update_labels, initial_call=True)
        notification_service.connect("notification-added", self.on_new_notification)
        self.notification_cache_service.connect("cleared", self.clear_notifications)

    def clear_notifications(self, *_):
        print("Cleared")

    def on_new_notification(self, fabric_notif, id):
        notification: Notification = fabric_notif.get_notification_from_id(id)
        self.notification_list_box.add(
            DateMenuNotification(
                notification=notification,
                index=len(self.notification_list_box.children) - 1,
            )
        )

    def update_labels(self):
        self.clock_label.set_text(time.strftime("%H:%M"))
        self.uptime.set_text(uptime())
        return True


class DateTimeWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", **kwargs)

        self.config = widget_config["date_time"]

        self.notification_cache_service = NotificationCacheService().get_initial()

        date_menu = DateNotificationMenu()

        popup = PopOverWindow(
            parent=bar,
            name="date-menu-popover",
            child=date_menu,
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.notof_indicator = Image(
            icon_name=icons["notifications"]["noisy"],
            icon_size=16,
        )

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )

        self.children = Box(
            spacing=10,
            v_align="center",
            children=(
                self.notof_indicator,
                DateTime(self.config["format"], name="date-time"),
            ),
        )
        date_menu.dnd_switch.connect("notify::active", self.on_dnd_switch)

    def on_dnd_switch(self, switch, _):
        """Handle the do not disturb switch."""
        if switch.get_active():
            self.notof_indicator.set_from_icon_name(
                icons["notifications"]["silent"], icon_size=16
            )
            self.notification_cache_service.dont_disturb = True

        else:
            self.notof_indicator.set_from_icon_name(
                icons["notifications"]["noisy"], icon_size=16
            )
            self.notification_cache_service.dont_disturb = False
