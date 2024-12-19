from typing import List, TypedDict

from utils.functions import read_config

# Default poll interval for widgets that need not be updated frequently
high_poll_interval = 1000 * 60 * 10  # 10 minutes

# Default configuration values
DEFAULT_CONFIG = {
    "theme": {
        "name": "catpuccin-frappe",
    },
    "layout": {
        "left_section": ["workspaces", "window_title"],
        "middle_section": ["datetime"],
        "right_section": [
            "updates",
            "battery",
            "bluetooth",
            "system_tray",
            "power",
        ],
    },
    "notification": {"icon_size": "12px", "tooltip": True,"icon": "",},
    "hypr_sunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "interval": 2000,
        "label": True,
        "tooltip": True,
    },
    "hypr_idle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "interval": 2000,
        "label": True,
        "tooltip": True,
    },
    "battery": {
        "label": True,
        "tooltip": True,
        "interval": 2000,
        "hide_label_when_full": True,
    },
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "interval": 2000,
        "label": True,
        "tooltip": True,
    },
    "memory": {
        "icon": "",
        "interval": 2000,
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "storage": {
        "icon": "󰋊",
        "interval": 2000,
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
    },
    "workspaces": {
        "count": 8,
        "occupied": True,
        "ignored": [],
        "reverse_scroll": False,
        "empty_scroll": False,
    },
    "window_title": {
        "enable_icon": True,
        "truncation": True,
        "truncation_size": 50,
    },
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "icon_size": "14px",
        "interval": high_poll_interval,
        "tooltip": True,
        "label": True,
    },
    "keyboard": {
        "icon": "󰌌",
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
    },
    "bluetooth": {
        "icon_size": 22,
        "label": True,
        "tooltip": True,
    },
    "volume": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "brightness": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "mpris": {
        "length": 30,
        "tooltip": True,
    },
    "language": {"length": 3},
    "task_bar": {"icon_size": 22},
    "system_tray": {"icon_size": 22, "ignore": []},
    "power": {"icon": "󰐥", "icon_size": "18px", "tooltip": True},
    "theme_switcher": {
        "icon": "",
        "icon_size": "14px",
        "silent": True,  # Whether to show a notification when the theme is changed
    },
}


class BaseConfig(TypedDict):
    """Common configuration for some sections"""

    icon_size: str
    label: bool
    tooltip: bool
    interval: int


class Layout(TypedDict):
    """ayout configuration for different sections of the bar"""

    left: List[str]
    middle: List[str]
    right: List[str]


class PowerButton(TypedDict):
    """Configuration for power button"""

    icon: str
    icon_size: int
    tooltip: bool


class HyprSunset(TypedDict, BaseConfig):
    """Configuration for hyprsunset"""

    temperature: str
    enabled_icon: str
    disabled_icon: str


class TaskBar(TypedDict):
    """Configuration for taskbar"""

    icon_size: int


class SystemTray(TypedDict):
    """Configuration for system tray"""

    icon_size: int
    ignore: List[str]


class HyprIdle(TypedDict, BaseConfig):
    """Configuration for hypridle"""

    enabled_icon: str
    disabled_icon: str


class Battery(TypedDict):
    """Configuration for battery"""

    label: bool
    tooltip: bool
    hide_label_when_full: bool
    interval: int


class Theme(TypedDict):
    """Configuration for battery"""

    name: str


class Cpu(TypedDict, BaseConfig):
    """Configuration for Cpu"""

    icon: str


class Mpris(TypedDict, BaseConfig):
    """Configuration for bar mpris"""

    length: int


class Memory(TypedDict, BaseConfig):
    """Configuration for window"""

    icon: str


class Storage(TypedDict, BaseConfig):
    """Configuration for storage"""

    icon: str


class Workspaces(TypedDict):
    """Configuration for Workspaces"""

    count: int
    occupied: bool
    ignored: List[int]


class WindowTitle(TypedDict):
    """Configuration for Window"""

    length: int
    enable_icon: bool
    truncation: bool
    truncation_size: int


class Updates(TypedDict, BaseConfig):
    """Configuration for updates"""

    os: str
    icon: str


class BlueTooth(TypedDict):
    """Configuration for bluetooth"""

    label: bool
    tooltip: bool
    icon_size: int


class Weather(TypedDict):
    """Configuration for weather"""

    location: str
    interval: int
    tooltip: bool
    label: bool


class Keyboard(TypedDict, BaseConfig):
    """Configuration for keyboard"""

    icon: str


class Notification(TypedDict, BaseConfig):
    """Configuration for keyboard"""

    icon: str
    icon_size: str


class ThemeSwitcher(TypedDict, BaseConfig):
    """Configuration for keyboard"""

    icon: str


class Language(TypedDict):
    """Configuration for language"""

    length: int


class Volume(TypedDict, BaseConfig):
    """Configuration for volume"""

    step_size: int


class Brightness(TypedDict, BaseConfig):
    """Configuration for brightness"""

    step_size: int


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    bluetooth: BlueTooth
    cpu: Cpu
    hypr_sunset: HyprSunset
    hypr_idle: HyprIdle
    keyboard: Keyboard
    language: Language
    theme: Theme
    theme_switcher: ThemeSwitcher
    layout: Layout
    memory: Memory
    notifications: Notification
    mpris: Mpris
    storage: Storage
    system_tray: SystemTray
    task_bar: TaskBar
    updates: Updates
    power: PowerButton
    volume: Volume
    brightness: Brightness
    workspaces: Workspaces
    window_title: WindowTitle
    weather: Weather


# Read the configuration from the JSON file
parsed_data = read_config()


# Merge the parsed data with the default configuration
def merge_defaults(data: dict, defaults: dict):
    return {**defaults, **data}


# Now, `parsed_data` is a Python dictionary
# You can access individual items like this:
layout = parsed_data["layout"]


for key, value in parsed_data.items():
    if key in DEFAULT_CONFIG:
        parsed_data[key] = merge_defaults(value, DEFAULT_CONFIG[key])


## TODO: validate the name of widget is within the dict

# Optionally, cast the parsed data to match our TypedDict using type hints
widget_config: BarConfig = parsed_data
