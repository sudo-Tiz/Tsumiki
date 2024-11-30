from typing import cast
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.revealer import Revealer
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.wayland import WaylandWindow
from fabric.notifications import Notifications, Notification
from fabric.utils import invoke_repeater, bulk_connect

from gi.repository import GdkPixbuf

from utils.functions import check_icon_exists

NOTIFICATION_WIDTH = 360
NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_TIMEOUT = 100 * 1000  # 10 seconds


class NotificationPopupWidget(EventBox):
    def __init__(self, notification: Notification, **kwargs):
        super().__init__(
            **kwargs,
        )

        notif_box = Box(
            name="notification",
            spacing=8,
            orientation="v",
            size=(NOTIFICATION_WIDTH, -1),
        )

        self.children = notif_box

        self._notification = notification

        header_container = Box(spacing=12, orientation="h")

        header_container.children = (
            self.get_icon(notification.app_icon),
            Label(
                str(
                    self._notification.summary
                    if self._notification.summary
                    else notification.app_name
                ),
                h_align="start",
                style="font-weight: 900;",
            ),
        )

        header_container.pack_end(
            Box(
                children=(
                    Button(
                        image=Image(
                            icon_name=check_icon_exists("close-symbolic","window-close-symbolic"),
                            icon_size=16,
                        ),
                        style_classes="close-button",
                        v_align="center",
                        h_align="end",
                        on_clicked=lambda *_: self._notification.close(),
                    ),
                )
            ),
            False,
            False,
            0,
        )

        body_container = Box(spacing=4, orientation="h")

        # Use provided image if available, otherwise use "notification-symbolic" icon
        if image_pixbuf := self._notification.image_pixbuf:
            body_container.add(
                Image(
                    pixbuf=image_pixbuf.scale_simple(
                        NOTIFICATION_IMAGE_SIZE,
                        NOTIFICATION_IMAGE_SIZE,
                        GdkPixbuf.InterpType.BILINEAR,
                    )
                )
            )

        body_container.add(
            Box(
                spacing=4,
                orientation="v",
                children=[
                    Label(
                        label=self._notification.body,
                        line_wrap="word-char",
                        v_align="start",
                        h_align="start",
                    )
                    .build()
                    .add_style_class("body")
                    .unwrap(),
                ],
                h_expand=True,
                v_expand=True,
            )
        )

        notif_box.add(header_container)
        notif_box.add(body_container)

        self.actions_revealer = Revealer(
            transition_type="slide_down", reveal_child=False, transition_duration=300
        )

        if actions := self._notification.actions:
            self.actions_revealer.children = Box(
                spacing=4,
                orientation="h",
                children=[
                    Button(
                        h_expand=True,
                        v_expand=True,
                        label=action.label,
                        on_clicked=lambda *_, action=action: action.invoke(),
                    )
                    for action in actions
                ],
            )

        notif_box.add(self.actions_revealer)

        bulk_connect(
            self,
            {
                "enter-notify-event": lambda *_: (
                    self.actions_revealer.set_reveal_child(True),
                    notif_box.add_style_class("shadow"),
                ),
                "leave-notify-event": lambda *_: (
                    self.actions_revealer.set_reveal_child(False)
                ),
            },
        )

        # destroy this widget once the notification is closed

        self._notification.connect(
            "closed",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.destroy(),
            ),
        )

        # automatically close the notification after the timeout period
        invoke_repeater(
            NOTIFICATION_TIMEOUT,
            lambda: self._notification.close("expired"),
            initial_call=False,
        )

    def get_icon(self, app_icon) -> Image:
        match app_icon:
            case str(x) if "file://" in x:
                return Image(
                    name="notification-icon",
                    image_file=app_icon[7:],
                    size=24,
                )
            case str(x) if len(x) > 0 and "/" == x[0]:
                return Image(
                    name="notification-icon",
                    image_file=app_icon,
                    size=24,
                )
            case _:
                return Image(
                    name="notification-icon",
                    icon_name=app_icon if app_icon else "dialog-information-symbolic",
                    size=24,
                )


class NotificationsPopup(WaylandWindow):
    def __init__(self, **kwargs):
        super().__init__(
            margin="8px 8px 8px 8px",
            anchor="top right",
            child=Box(
                size=2,  # so it's not ignored by the compositor
                spacing=4,
                orientation="v",
            ).build(
                lambda viewport, _: Notifications(
                    on_notification_added=lambda notifs_service, nid: viewport.add(
                        NotificationPopupWidget(
                            cast(
                                Notification,
                                notifs_service.get_notification_from_id(nid),
                            )
                        )
                    )
                )
            ),
            visible=True,
            all_visible=True,
            **kwargs,
        )
