import json
import os
from typing import List

from fabric.core.service import Service, Signal, Property
from fabric.notifications import (
    Notification,
)
from gi.repository import GLib

CACHE_DIR = GLib.get_user_cache_dir()

NOTIFICATIONS_CACHE_PATH = f"{CACHE_DIR}/notifications"
CACHE_FILE = f"{NOTIFICATIONS_CACHE_PATH}/notifications.json"


class NotificationCacheService(Service):
    """A service to manage the notifications."""

    def __init__(self):
        self._count = 0
        self._notifications: List[Notification] = self.read_notifications()


    @Signal
    def notification_added(self, notification: Notification) -> None:...

    @Property(str, flags="read-write")
    def notifications(self) -> str:
        return self._notifications

    @notifications.setter
    def notifications(self, data: Notification):
        self._notifications.append(data)
        self.notification_added(data)


    def read_notifications(self) -> List[Notification]:
        """Read the notifications from the notifications file."""
        notifications = []
        try:
            with open(CACHE_FILE, "r") as file:
                for line in file:
                    notification = json.loads(line)
                    notifications.append(notification)
                    self._count += 1
                    return notifications
        except FileNotFoundError:
            return []

    def cache_notification(self, fabric_notif, id):
        """Cache the notification."""
        data: Notification = fabric_notif.get_notification_from_id(id)

        self.notifications = data

        # Check if the directory exists, if not, create it
        if not os.path.exists(NOTIFICATIONS_CACHE_PATH):
            os.makedirs(NOTIFICATIONS_CACHE_PATH)

        serialzed_data = [Notification.serialize(data) for data in self._notifications]

        # Append to the file if it exists, or create it if it doesn't
        with open(CACHE_FILE, "a") as f:
            # Append content to the file
            f.write(json.dumps(serialzed_data, indent=2))
