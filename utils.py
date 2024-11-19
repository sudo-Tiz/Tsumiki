import json
from typing import Literal
from fabric.widgets.label import Label
import psutil
import datetime


def read_config():
    with open("config.json", "r") as file:
        # Load JSON data into a Python dictionary
        data = json.load(file)
    return data


def TextIcon(icon: str, size: str = "24px", props: dict = None):
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


def format_time(secs: int):
    mm, _ = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d h %02d min" % (hh, mm)


def convert_bytes(bytes: int, to: Literal["kb", "mb", "gb"]):
    multiplier = 1

    if to == "mb":
        multiplier = 2
    elif to == "gb":
        multiplier = 3

    return bytes / (1024**multiplier)


def uptime():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")
