import gi
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from shared.popover import PopOverWindow
from utils.icons import icons
from utils.widget_config import BarConfig

gi.require_version("Gtk", "3.0")


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(self):
        super().__init__(name="notification-menu")

        notif_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label(label="Notifications"),),
        )

        notif_header.pack_end(
            Box(
                style_classes="header-actions",
                children=(
                    Label(label="Clear"),
                    Button(
                        name="clear-btn",
                        image=Image(
                            icon_name=icons["notifications"]["noisy"], icon_size=14
                        ),
                    ),
                ),
            ),
            False,
            False,
            0,
        )
        self.add(notif_header)


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
            margin="10px 10px 10px 10px",
            orientation="v",
            child=(DateNotificationMenu()),
            visible=False,
            all_visible=False,
        )

        btn = Button(
            image=Image(icon_name=icons["notifications"]["noisy"], icon_size=14),
            on_clicked=lambda _: popup.set_visible(not popup.get_visible()),
        )
        popup.set_pointing_to(btn)

        self.add(btn)
