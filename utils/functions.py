import datetime
import json
import os
import shutil
import subprocess
from typing import Literal

import gi
import psutil
from fabric.utils import get_relative_path
from fabric.widgets.label import Label
from gi.repository import GLib, Gtk
from loguru import logger

from utils.config import APP_CACHE_DIRECTORY
import utils.icons as icons
from utils.colors import Colors

gi.require_version("Gtk", "3.0")


class ExecutableNotFoundError(ImportError):
    """Raised when an executable is not found."""

    def __init__(self, executable_name: str):
        super().__init__(
            f"{Colors.FAIL}Executable {executable_name} not found. Please install it using your package manager."
        )


# Function to get the system icon theme
def copy_theme(theme: str):
    destination_file = get_relative_path("../styles/theme.scss")
    source_file = get_relative_path(f"../styles/themes/{theme}.scss")

    if not os.path.exists(source_file):
        logger.warning(
            f"{Colors.WARNING}Warning: The theme file '{theme}.scss' was not found. Using default theme."
        )
        source_file = get_relative_path("../styles/themes/catpuccin-mocha.scss")

    try:
        with open(source_file, "r") as source_file:
            content = source_file.read()

        # Open the destination file in write mode
        with open(destination_file, "w") as destination_file:
            destination_file.write(content)
            logger.info(f"{Colors.OKBLUE}[THEME] '{theme}' applied successfully.")

    except FileNotFoundError:
        logger.error(
            f"{Colors.FAIL}Error: The theme file '{source_file}' was not found."
        )
        exit(1)


# Function to read the configuration file
def read_config():
    with open(get_relative_path("../config.json")) as file:
        # Load JSON data into a Python dictionary
        data = json.load(file)
    return data


# Function to create a text icon label
def text_icon(icon: str, size: str = "16px", props=None):
    label_props = {
        "label": str(icon),  # Directly use the provided icon name
        "name": "nerd-icon",
        "style": f"font-size: {size}; ",
        "h_align": "center",  # Align horizontally
        "v_align": "center",  # Align vertically
    }

    if props:
        label_props.update(props)

    return Label(**label_props)


# Function to format time in hours and minutes
def format_time(secs: int):
    mm, _ = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d h %02d min" % (hh, mm)


# Function to convert bytes to kilobytes, megabytes, or gigabytes
def convert_bytes(bytes: int, to: Literal["kb", "mb", "gb"]):
    multiplier = 1

    if to == "mb":
        multiplier = 2
    elif to == "gb":
        multiplier = 3

    return f"{bytes / (1024**multiplier)}{to.upper()}"


# Function to get the system uptime
def uptime():
    boot_time = psutil.boot_time()
    now = datetime.datetime.now()

    diff = now.timestamp() - boot_time

    # Convert the difference in seconds to hours and minutes
    hours, remainder = divmod(diff, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{int(hours):02}:{int(minutes):02}"


# Function to convert seconds to miliseconds
def convert_seconds_to_miliseconds(seconds: int):
    return seconds * 1000


# Function to check if an icon exists, otherwise use a fallback icon
def check_icon_exists(icon_name: str, fallback_icon: str) -> str:
    if Gtk.IconTheme.get_default().has_icon(icon_name):
        return icon_name
    return fallback_icon


# Function to get the distro icon
def get_distro_icon():
    distro_id = GLib.get_os_info("ID")
    # Search for the icon in the list
    icon = next((icon for id, icon in icons.distro_text_icons if id == distro_id), None)

    # Return the found icon or default to '' if not found
    return icon if icon else ""


# Function to check if an executable exists
def executable_exists(executable_name):
    executable_path = shutil.which(executable_name)
    return bool(executable_path)


# Function to get the brightness icons
def get_brightness_icon_name(level: int) -> dict[Literal["icon_text", "icon"], str]:
    if level <= 0:
        return {
            "text_icon": icons.brightness_text_icons["off"],
            "icon": "display-brightness-off-symbolic",
        }

    if level > 0 and level < 32:
        return {
            "text_icon": icons.brightness_text_icons["low"],
            "icon": "display-brightness-low-symbolic",
        }
    if level > 32 and level < 66:
        return {
            "text_icon": icons.brightness_text_icons["medium"],
            "icon": "display-brightness-medium-symbolic",
        }
    if level >= 66 and level <= 100:
        return {
            "text_icon": icons.icons.brightness_text_icons["high"],
            "icon": "display-brightness-high-symbolic",
        }


# Function to get the volume icons
def get_audio_icon_name(
    volume: int, is_muted: bool
) -> dict[Literal["icon_text", "icon"], str]:
    if volume <= 0 or is_muted:
        return
    if volume > 0 and volume < 32:
        return {
            "text_icon": icons.volume_text_icons["low"],
            "icon": "audio-volume-low-symbolic",
        }
    if volume > 32 and volume < 66:
        return {
            "text_icon": icons.volume_text_icons["medium"],
            "icon": "audio-volume-medium-symbolic",
        }
    if volume >= 66 and volume <= 100:
        return {
            "text_icon": icons.volume_text_icons["high"],
            "icon": "audio-volume-high-symbolic",
        }
    else:
        return {
            "text_icon": icons.volume_text_icons["overamplified"],
            "icon": "audio-volume-overamplified-symbolic",
        }


def send_notification(
    title, message, urgency="normal", timeout=0, icon=None, category=None, hint=None
):
    """
    Send a notification using the notify-send command with customizable parameters.

    :param title: The title of the notification
    :param message: The message content of the notification
    :param urgency: The urgency level (low, normal, critical)
    :param timeout: The timeout in milliseconds (0 means no timeout)
    :param icon: The path to an icon image (optional)
    :param category: The category of the notification (optional)
    :param hint: Extra hints as a dictionary (optional)
    """
    command = ["notify-send"]

    # Add title and message
    command.append(title)
    command.append(message)

    # Add urgency if specified
    if urgency in ["low", "normal", "critical"]:
        command.extend(["-u", urgency])

    # Add timeout if specified
    if timeout > 0:
        command.extend(["-t", str(timeout)])

    # Add icon if specified
    if icon:
        command.extend(["-i", icon])

    # Add category if specified
    if category:
        command.extend(["--category", category])

    # Add hints (if any)
    if hint:
        for key, value in hint.items():
            command.extend([f"--hint={key}={value}"])

    # Send the notification
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"{Colors.FAIL}Error sending notification: {e}")


# Function to get the percentage of a value
def convert_to_percent(
    current: int | float, max: int | float, is_int=True
) -> int | float:
    if is_int:
        return int((current / max) * 100)
    else:
        return (current / max) * 100


# Function to ensure the cache directory exists
def ensure_cache_dir_exists():
    if not os.path.exists(APP_CACHE_DIRECTORY):
        os.makedirs(APP_CACHE_DIRECTORY)
