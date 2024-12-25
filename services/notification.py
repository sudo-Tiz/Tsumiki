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

    def read_notifications(self) -> List[Notification]:
        """Read the notifications from the notifications file."""
        notifications = []
        try:
            with open(NOTIFICATION_CACHE_FILE, "r") as file:
                for line in file:
                    notification = json.loads(line)
                    notifications.append(notification)
                    self._count += 1
                    return notifications
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
