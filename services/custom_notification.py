import json
import os
from typing import List

from fabric import Signal
from fabric.notifications import Notification, Notifications
from loguru import logger

from utils.colors import Colors
from utils.constants import NOTIFICATION_CACHE_FILE


class CustomNotifications(Notifications):
    """A service to manage the notifications."""

    @Signal
    def clear_all(self, value: bool) -> None:
        """Signal emitted when notifications are emptied."""
        # Implement as needed for your application

    @Signal
    def notification_count(self, value: int) -> None:
        """Signal emitted when a new notification is added."""
        # Implement as needed for your application

    @Signal
    def dnd(self, value: bool) -> None:
        """Signal emitted when dnd is toggled."""
        # Implement as needed for your application

    @property
    def count(self) -> int:
        """Return the count of notifications."""
        return self._count

    @property
    def dont_disturb(self) -> bool:
        """Return the pause status."""
        return self._dont_disturb

    @dont_disturb.setter
    def dont_disturb(self, value: bool):
        """Set the pause status."""
        self._dont_disturb = value
        self.emit("dnd", value)

    def __init__(self, **kwargs):
        super().__init__()
        self.all_notifications = self._read_notifications()
        self._count = len(self.all_notifications)
        self.deserialized_notifications = []
        self._dont_disturb = False

    def _read_notifications(self):
        """Read notifications from the cache file."""
        if os.path.exists(NOTIFICATION_CACHE_FILE):
            try:
                with open(NOTIFICATION_CACHE_FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, KeyError, ValueError, IndexError) as e:
                logger.error(f"{Colors.INFO}[Notification] {e}")
        return []

    def remove_notification(self, id: int):
        """Remove the notification of given id."""
        item = next((p for p in self.all_notifications if p["id"] == id), None)
        if item:
            self.all_notifications.remove(item)
            self._count -= 1
            self._write_notifications(self.all_notifications)
            self.emit("notification_count", self._count)

            # Emit clear_all signal if there are no notifications left
            if self._count == 0:
                self.emit("clear_all", True)

    def cache_notification(self, data: Notification, max_count: int):
        """Cache the notification."""
        serialized_data = data.serialize()
        serialized_data.update({"id": self._count + 1})
        self.all_notifications.append(serialized_data)

        # Remove the oldest notification if the count exceeds the max count
        if self._count > max_count:
            self.all_notifications.pop(0)

        self._count += 1
        self._write_notifications(self.all_notifications)
        self.emit("notification_count", self._count)

    def clear_all_notifications(self):
        """Empty the notifications."""
        self.all_notifications = []
        self._count = 0
        self._write_notifications(self.all_notifications)
        self.emit("clear_all", True)
        self.emit("notification_count", self._count)

    def _write_notifications(self, data):
        """Write the notifications to the cache file."""
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"{Colors.INFO}[Notification] Notifications written successfully.")

    def get_deserialized(self) -> List[Notification]:
        """Return the notifications."""
        if not self.deserialized_notifications:
            self.deserialized_notifications = [
                Notification.deserialize(data) for data in self.all_notifications
            ]
        return self.deserialized_notifications
