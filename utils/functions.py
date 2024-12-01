import datetime
import json
from typing import Literal

import gi
import psutil
from fabric.utils import get_relative_path
from fabric.widgets.label import Label

from utils.icons import DISTRO_ICONS

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk


# Function to read the configuration file
def read_config():
    with open(get_relative_path("../config.json"), "r") as file:
        # Load JSON data into a Python dictionary
        data = json.load(file)
    return data


# Function to create a text icon label
def text_icon(icon: str, size: str = "24px", props: dict = None):
    label_props = {
        "label": str(icon),  # Directly use the provided icon name
        "name": "nerd-icon",
        "style": f"font-size: {size}; ",  # Set font family for Material Icons
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

    return bytes / (1024**multiplier)


# Function to get the system uptime
def uptime():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")


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
    icon = next((icon for id, icon in DISTRO_ICONS if id == distro_id), None)

    # Return the found icon or default to '' if not found
    return icon if icon else ""
