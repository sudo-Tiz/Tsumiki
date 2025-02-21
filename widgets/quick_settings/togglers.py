from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.cache_notification import NotificationCacheService
from shared.button_toggle import CommandSwitcher
from shared.widget_container import HoverButton


class QuickSettingToggler(CommandSwitcher):
    """A button widget to toggle a command."""

    def __init__(self, command, name, enabled_icon, disabled_icon, **kwargs):
        super().__init__(
            command,
            enabled_icon,
            disabled_icon,
            name,
            label=True,
            tooltip=False,
            interval=1000,
            style_classes="quicksettings-toggler",
            **kwargs,
        )


class HyprIdleQuickSetting(QuickSettingToggler):
    """A button to toggle the hyper idle mode."""

    def __init__(self, **kwargs):
        super().__init__(
            command="hypridle",
            enabled_icon="",
            disabled_icon="",
            name="quicksettings-togglebutton",
        )


class HyprSunsetQuickSetting(QuickSettingToggler):
    """A button to toggle the hyper idle mode."""

    def __init__(self, **kwargs):
        super().__init__(
            command="hyprsunset -t 2800k",
            enabled_icon="󱩌",
            disabled_icon="󰛨",
            name="quicksettings-togglebutton",
        )


class NotificationQuickSetting(HoverButton):
    """A button to toggle the notification."""

    def __init__(self):
        super().__init__(
            name="quicksettings-togglebutton",
            style_classes="quicksettings-toggler",
        )

        self.cache_notification_service = NotificationCacheService().get_initial()
        self.notification_label = Label(
            label="Noisy",
            style_classes="panel-text",
        )
        self.notification_icon = Image(
            icon_name="notifications-symbolic",
            icon_size=16,
            style_classes="panel-icon",
        )

        self.children = Box(
            orientation="h",
            spacing=10,
            style="padding: 5px;",
            children=(
                self.notification_icon,
                self.notification_label,
            ),
        )

        self.cache_notification_service.connect(
            "dnd", lambda _, value, *args: self.toggle_notification(value)
        )

        self.connect("clicked", self.on_click)

        self.toggle_notification(self.cache_notification_service.dont_disturb)

    def on_click(self, *args):
        """Toggle the notification."""
        self.cache_notification_service.dont_disturb = (
            not self.cache_notification_service.dont_disturb
        )

    def toggle_notification(self, value: bool):
        """Toggle the notification."""

        if value:
            self.notification_label.set_label("Quiet")
            self.notification_icon.set_from_icon_name(
                "notifications-disabled-symbolic", 16
            )
            self.remove_style_class("active")
        else:
            self.notification_label.set_label("Noisy")
            self.notification_icon.set_from_icon_name("notifications-symbolic", 16)
            self.add_style_class("active")
