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
        self.all_notifications = self.do_read_notifications()
        self._count = len(self.all_notifications)

        self.deserialized_notifications = []
        self._dont_disturb = False

    def do_read_notifications(self):
        # Check if the cache file exists and read existing data
        if os.path.exists(NOTIFICATION_CACHE_FILE):
            with open(NOTIFICATION_CACHE_FILE, "r") as file:
                try:
                    # Load existing data if the file is not empty
                    existing_data = json.load(file)
                except (json.JSONDecodeError, KeyError, ValueError, IndexError) as e:
                    logger.error(f"{Colors.INFO}[Notification]", e)
                    existing_data = []  # If the file is empty or malformed
        else:
            existing_data = []
        return existing_data

    def remove_notification(self, id: int):
        """Remove the notification of given id."""
        item = next((p for p in self.all_notifications if p["id"] == id), None)
        index = self.all_notifications.index(item)

        self.write_notifications(self.all_notifications)

        self.all_notifications.pop(index)
        self._count -= 1
        self.emit("notification_count", self._count)

        # Emit clear_all signal if there are no notifications left
        if self._count == 0:
            self.emit("clear_all", True)

    def cache_notification(self, data: Notification):
        """Cache the notification."""

        existing_data = self.all_notifications

        serialized_data = data.serialize()
        serialized_data.update({"id": self._count + 1})

        # Append the new notification to the existing data
        existing_data.append(serialized_data)

        # Write the updated data back to the cache file
        self.write_notifications(existing_data)

        self._count += 1
        self.all_notifications = existing_data
        self.emit("notification_count", self._count)

    def clear_all_notifications(self):
        """Empty the notifications."""
        self._notifications = []
        self._count = 0

        # Write the updated data back to the cache file
        self.write_notifications(self._notifications)
        self.emit("clear_all", True)
        self.emit("notification_count", self._count)

    def write_notifications(self, data):
        """Write the notifications to the cache file."""
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"{Colors.INFO}[Notification] Notifications written successfully.")

    def get_deserialized(self) -> List[Notification]:
        """Return the notifications."""
        if len(self.deserialized_notifications) <= 0:
            self.deserialized_notifications = [
                Notification.deserialize(data) for data in self._notifications
            ]
        return self.deserialized_notifications
