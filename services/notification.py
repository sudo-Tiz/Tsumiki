import json
import os
from typing import List

from fabric.core.service import Service
from fabric.notifications import Notification
from loguru import logger

from utils.colors import Colors
from utils.constants import NOTIFICATION_CACHE_FILE


class NotificationCacheService(Service):
    """A service to manage the notifications."""

    instance = None

    @staticmethod
    def get_initial():
        if NotificationCacheService.instance is None:
            NotificationCacheService.instance = NotificationCacheService()

        return NotificationCacheService.instance

    def get_deserailized(self) -> List[Notification]:
        """Return the notifications."""
        if len(self.notifications) <= 0:
            self.notifications = [
                Notification.deserialize(data) for data in self._notifications
            ]
        return self.notifications

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

    def __init__(self):
        self._count = 0
        self._notifications = []
        self.notifications = []  # this is deserialized data
        self._dont_disturb = False
        self.do_read_notifications()

    def do_read_notifications(self) -> List[Notification]:
        """Read the notifications from the notifications file."""
        try:
            with open(NOTIFICATION_CACHE_FILE, "r") as file:
                self._notifications = json.load(file)
                self._count = len(self._notifications)
        except FileNotFoundError:
            return []

    def cache_notification(self, data):
        """Cache the notification."""

        # Append the new notification to the list
        self._notifications.append(data)

        # Serialize the notifications
        serialized_data = [Notification.serialize(data) for data in self._notifications]

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

        # Combine existing and new notifications
        existing_data.extend(serialized_data)

        # Write the updated data back to the cache file
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        logger.info(f"{Colors.INFO}[Notification] Notification cached successfully.")

    def clear_notifications(self):
        """Clear the notifications."""
        self._notifications = []
        self._count = 0

        # Write the updated data back to the cache file
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

        logger.info(f"{Colors.INFO}[Notification] Notifications cleared successfully.")
