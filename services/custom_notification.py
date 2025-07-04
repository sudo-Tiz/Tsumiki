import json
import os
import threading
from typing import List

from fabric import Signal
from fabric.notifications import Notification, Notifications
from loguru import logger

from utils.colors import Colors
from utils.constants import (
    NOTIFICATION_CACHE_FILE,
)
from utils.functions import write_json_file


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
        return len(self.all_notifications)

    @property
    def dont_disturb(self) -> bool:
        """Return the pause status."""
        return self._dont_disturb

    @dont_disturb.setter
    def dont_disturb(self, value: bool):
        """Set the pause status."""
        self._dont_disturb = value
        self.emit("dnd", value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self.all_notifications = []
        self._count = 0  # Will be updated to highest ID when loading
        self.deserialized_notifications = []
        self._dont_disturb = False
        self._load_notifications()

    # Load notifications from the cache file
    def _load_notifications(self):
        """Read notifications from the cache file."""
        if os.path.exists(NOTIFICATION_CACHE_FILE):
            try:
                with open(NOTIFICATION_CACHE_FILE, "r") as file:
                    notifications = json.load(file)

                    notifications.reverse()

                def validate_with_id(notification):
                    """Helper to validate and return ID if valid."""
                    try:
                        self._deserialize_notification(notification)
                        return (True, notification, notification.get("id", 0))
                    except Exception as e:
                        msg = f"[Notification] Invalid: {str(e)[:50]}"
                        logger.exception(f"{Colors.INFO}{msg}")
                        return (False, None, 0)

                # Validate all notifications at once
                results = [validate_with_id(n) for n in notifications]

                # Process results and find highest ID
                valid_notifications = []
                highest_id = self._count  # Start with current count
                for is_valid, notification, notification_id in results:
                    if is_valid:
                        valid_notifications.append(notification)
                        highest_id = max(highest_id, notification_id)

                self.all_notifications = valid_notifications
                self._count = highest_id  # Update to highest ID seen
                write_json_file(self.all_notifications, NOTIFICATION_CACHE_FILE)
                logger.info(
                    f"{Colors.INFO}[Notification] Notifications written successfully."
                )

            except (json.JSONDecodeError, KeyError, ValueError, IndexError) as e:
                logger.exception(f"{Colors.INFO}[Notification] {e}")
                self.all_notifications = []
                self._count = 0

    # Remove a notification by ID, ensuring thread safety
    def remove_notification(self, id: int):
        with self._lock:
            item = next((p for p in self.all_notifications if p["id"] == id), None)
            if item:
                self.all_notifications.remove(item)
                self._persist_and_emit()

                if len(self.all_notifications) == 0:
                    self.emit("clear_all", True)

    # Cache a notification, ensuring thread safety
    def cache_notification(self, widget_config, data: Notification, max_count: int):
        with self._lock:
            self._cleanup_invalid_notifications()
            new_notification = self._create_serialized_notification(data)
            self._enforce_per_app_limit(widget_config, new_notification, max_count)
            self.all_notifications.append(new_notification)
            self._enforce_global_limit(max_count)
            self._persist_and_emit()

    def _cleanup_invalid_notifications(self):
        """Remove any invalid notifications."""

        def validate_with_id(notification):
            """Helper to validate and return result with ID."""
            try:
                self._deserialize_notification(notification)
                return (True, notification, None)
            except Exception as e:
                msg = f"[Notification] Removing invalid: {str(e)[:50]}"
                logger.debug(msg)
                return (False, None, notification.get("id", 0))

        # Validate all notifications at once
        results = [validate_with_id(n) for n in self.all_notifications]

        # Process results
        valid_notifications = []
        invalid_count = 0
        for is_valid, notification, invalid_id in results:
            if is_valid:
                valid_notifications.append(notification)
            else:
                invalid_count += 1
                self.emit("notification-closed", invalid_id, "dismissed-by-limit")

        if invalid_count > 0:
            self.all_notifications = valid_notifications
            self._persist_and_emit()

            logger.info(
                f"{Colors.INFO}[Notification] Notifications written successfully."
            )

    def _create_serialized_notification(self, data: Notification) -> dict:
        """Generate a new notification with a unique ID."""
        self._count += 1
        serialized = data.serialize()
        serialized.update(
            {
                "id": self._count,
                "app_name": data.app_name,
            }
        )
        return serialized

    def _enforce_global_limit(self, max_count: int):
        """Remove oldest notifications if total count exceeds global limit."""
        while len(self.all_notifications) > max_count:
            oldest = self.all_notifications.pop(0)
            self.emit("notification-closed", oldest["id"], "dismissed-by-limit")

    def _enforce_per_app_limit(
        self, widget_config, new_notification: dict, max_count: int
    ):
        """Ensure per-app limits are respected."""
        app_name = new_notification["app_name"]
        per_app_limits = widget_config.get("notification", {}).get("per_app_limits", {})
        app_limit = per_app_limits.get(app_name, max_count)

        app_notifications = [
            n for n in self.all_notifications if n["app_name"] == app_name
        ]

        if len(app_notifications) >= app_limit:
            app_notifications.sort(key=lambda x: x["id"])  # Oldest first
            to_remove = len(app_notifications) - app_limit + 1
            for old in app_notifications[:to_remove]:
                self.all_notifications.remove(old)
                self.emit("notification-closed", old["id"], "dismissed-by-limit")

    def _deserialize_notification(self, notification):
        """Deserialize a notification."""
        return Notification.deserialize(notification)

    def _persist_and_emit(self):
        """Persist notifications and emit relevant signals."""
        write_json_file(self.all_notifications, NOTIFICATION_CACHE_FILE)
        self.emit("notification_count", len(self.all_notifications))

    def clear_all_notifications(self):
        """Empty the notifications."""
        logger.info("[Notification] Clearing all notifications")

        # Clear notifications but preserve the highest ID we've seen
        highest_id = self._count

        self.all_notifications = []

        self._persist_and_emit()

        logger.info(f"{Colors.INFO}[Notification] Notifications written successfully.")

        self.emit("clear_all", True)

        # Restore the ID counter so new notifications get unique IDs
        self._count = highest_id

    def get_deserialized(self) -> List[Notification]:
        """Return the notifications."""

        def deserialize_with_id(notification):
            """Helper to deserialize and return result with ID."""
            try:
                return (self._deserialize_notification(notification), None)
            except Exception as e:
                msg = f"[Notification] Deserialize failed: {str(e)[:50]}"
                logger.exception(f"{Colors.INFO}{msg}")
                return (None, notification.get("id"))

        # Process all notifications at once
        results = [
            deserialize_with_id(notification) for notification in self.all_notifications
        ]

        # Split into successful and failed
        deserialized = []
        invalid_ids = []
        for result, error_id in results:
            if result is not None:
                deserialized.append(result)
            elif error_id is not None:
                invalid_ids.append(error_id)

        # Clean up invalid notifications
        for invalid_id in invalid_ids:
            self.remove_notification(invalid_id)

        return deserialized
