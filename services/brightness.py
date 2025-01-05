import os
import subprocess

from fabric.core.service import Property, Service, Signal
from fabric.utils import exec_shell_command, monitor_file
from gi.repository import GLib
from loguru import logger

import utils.functions as helpers
from utils.colors import Colors


# Helper function to execute brightnessctl asynchronously
def exec_brightnessctl_async(args: str):
    # Executes brightnessctl command asynchronously, ensuring no resource leaks.

    if not helpers.executable_exists("brightnessctl"):
        logger.error(f"{Colors.ERROR}Command brightnessctl not found")

    try:
        # Use subprocess.Popen to run the command without blocking
        process = subprocess.Popen(
            f"brightnessctl {args}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for the process to complete
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(
                f"{Colors.ERROR}Error executing brightnessctl: {stderr.decode().strip()}"
            )
        else:
            logger.debug(
                f"{Colors.INFO}brightnessctl output: {stdout.decode().strip()}",
            )  # Optional: Log the output
    except Exception as e:
        logger.exception(f"Exception in exec_brightnessctl_async: {e}")


# Discover screen backlight device
screen_device = exec_shell_command(
    "bash -c 'ls -w1 /sys/class/backlight | head -1'"
).strip("\n")



class Brightness(Service):
    """Service to manage screen brightness levels."""

    instance = None

    @staticmethod
    def get_initial():
        if Brightness.instance is None:
            Brightness.instance = Brightness()

        return Brightness.instance

    @Signal
    def screen(self, value: int) -> None:
        """Signal emitted when screen brightness changes."""
        # Implement as needed for your application

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not screen_device:
            logger.error(f"{Colors.ERROR}No screen backlight device found")

        # Path for screen backlight control
        self.screen_backlight_path = f"/sys/class/backlight/{screen_device}"

        # Initialize maximum brightness level
        self.max_screen = self._read_max_brightness(self.screen_backlight_path)

        # Monitor screen brightness file
        self.screen_monitor = monitor_file(f"{self.screen_backlight_path}/brightness")

        self.screen_monitor.connect(
            "changed",
            lambda _, file, *args: self.emit(
                "screen",
                round(int(file.load_bytes()[0].get_data())),
            ),
        )

        # Log the initialization of the service
        logger.info(
            f"{Colors.INFO}Brightness service initialized for device: {screen_device}"
        )

    def _read_max_brightness(self, path: str) -> int:
        # Reads the maximum brightness value from the specified path.
        max_brightness_path = os.path.join(path, "max_brightness")
        if os.path.exists(max_brightness_path):
            with open(max_brightness_path) as f:
                return int(f.read().strip())
        return -1  # Return -1 if file doesn't exist, indicating an error.

    @Property(int, "read-write")
    def screen_brightness(self) -> int:
        # Property to get or set the screen brightness.
        brightness_path = os.path.join(self.screen_backlight_path, "brightness")
        if os.path.exists(brightness_path):
            with open(brightness_path) as f:
                return int(f.read().strip())
        logger.warning(
            f"{Colors.WARNING}Brightness file does not exist: {brightness_path}"
        )
        return -1  # Return -1 if file doesn't exist, indicating error.

    @screen_brightness.setter
    def screen_brightness(self, value: int):
        # Setter for screen brightness property.
        if not (0 <= value <= self.max_screen):
            value = max(0, min(value, self.max_screen))

        try:
            exec_brightnessctl_async(f"--device '{screen_device}' set {value}")
            self.emit("screen", int((value / self.max_screen) * 100))
            logger.info(
                f"{Colors.INFO}Set screen brightness to {value} (out of {self.max_screen})"
            )
        except GLib.Error as e:
            logger.error(f"{Colors.ERROR}Error setting screen brightness: {e.message}")
        except Exception as e:
            logger.exception(f"Unexpected error setting screen brightness: {e}")
