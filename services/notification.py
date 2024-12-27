import json
import os
from typing import List

from fabric.core.service import Service
from fabric.notifications import Notification
from loguru import logger

from utils.colors import Colors
from utils.config import NOTIFICATION_CACHE_FILE


class NotificationCacheService(Service):
    """A service to manage the notifications."""

    def __init__(self):
        self._count = 0
        self._notifications = []
        self.is_paused = False

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

        if self.is_paused:
            return

        # Append the new notification to the list
        self._notifications.append(data)

        # Serialize the notifications
        serialized_data = [Notification.serialize(data) for data in self._notifications]

        # Check if the cache file exists and read existing data
        if os.path.exists(NOTIFICATION_CACHE_FILE):
            with open(NOTIFICATION_CACHE_FILE, "r") as f:
                try:
                    # Load existing data if the file is not empty
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []  # If the file is empty or malformed
        else:
            existing_data = []

        # Combine existing and new notifications
        existing_data.extend(serialized_data)

        # Write the updated data back to the cache file
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(existing_data, f, indent=2)

        logger.info(f"{Colors.INFO}[Notifocation] Notification cached successfully.")

    @property
    def notifications(self) -> List[Notification]:
        """Return the notifications."""
        return self._notifications

    @property
    def count(self) -> int:
        """Return the count of notifications."""
        return self._count

    @property
    def is_paused(self) -> bool:
        """Return the pause status."""
        return self._is_paused

    @is_paused.setter
    def is_paused(self, value: bool):
        """Set the pause status."""
        self._is_paused = value
