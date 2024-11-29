import json
from typing import Literal
from fabric.widgets.label import Label
import psutil
import datetime
from fabric.utils import get_relative_path
import math


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


def get_relative_time(param_time, get_real_time):
    value = ""

    diff = (get_real_time() * 0.000001) - param_time
    secs = diff / 60
    hours = secs / 60
    days = hours / 24

    if secs < 1:
        value = "Just now"  # Consider more specific wording, "Now" is a bit unclear
    elif secs >= 1 and hours < 1:
        # 1m - 1h
        val = math.floor(secs)
        value = f"{val} minute"
        if val > 1:
            value += "s"
        value += " ago"
    elif hours >= 1 and hours < 24:
        # 1h - 24h
        val = math.floor(hours)
        value = f"{val} hour"
        if val > 1:
            value += "s"
        value += " ago"
    else:
        # Days
        val = math.floor(days)
        value = f"{val} day"
        if val > 1:
            value += "s"
        value += " ago"

    return value
