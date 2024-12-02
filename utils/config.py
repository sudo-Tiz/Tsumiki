from typing import List, TypedDict

from utils.functions import read_config

# Define the TypedDict types for various configurations


# Layout configuration for different sections of the bar
class Layout(TypedDict):
    """Configuration for Window"""

    left: List[str]
    middle: List[str]
    right: List[str]


# Configuration for HyprSunset
class HyprSunset(TypedDict):
    """Configuration for Window"""

    temperature: str
    enabled_icon: str
    disabled_icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool


# Configuration for HyprIdle
class HyprIdle(TypedDict):
    """Configuration for Window"""

    enabled_icon: str
    disabled_icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool


# Configuration for Battery
class Battery(TypedDict):
    """Configuration for Window"""

    enable_label: bool
    enable_tooltip: bool
    interval: int


# Configuration for CPU
class Cpu(TypedDict):
    """Configuration for Window"""

    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


# Configuration for Memory
class Memory(TypedDict):
    """Configuration for Window"""

    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


# Configuration for Storage
class Storage(TypedDict):
    """Configuration for Window"""

    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


# Configuration for Workspaces
class Workspaces(TypedDict):
    """Configuration for Window"""

    count: int


# Configuration for Window
class Window(TypedDict):
    """Configuration for Window"""

    length: int
    enable_icon: bool


# Configuration for Updates
class Updates(TypedDict):
    """Configuration for Updates"""

    os: str
    icon: str
    icon_size: str


# Configuration for Weather
class Weather(TypedDict):
    """Configuration for Window"""

    location: str


# Main configuration that includes all other configurations
class Config(TypedDict):
    """Main configuration"""

    layout: Layout
    hyprsunset: HyprSunset
    hypridle: HyprIdle
    battery: Battery
    cpu: Cpu
    memory: Memory
    storage: Storage
    workspaces: Workspaces
    window: Window
    updates: Updates
    weather: Weather


# Read the configuration from the JSON file
parsed_data = read_config()

# Now, `parsed_data` is a Python dictionary
# You can access individual items like this:
layout = parsed_data["layout"]
hyprsunset = parsed_data["hyprsunset"]
hypridle = parsed_data["hypridle"]
battery = parsed_data["battery"]
cpu = parsed_data["cpu"]
memory = parsed_data["memory"]
storage = parsed_data["storage"]
workspaces = parsed_data["workspaces"]
window = parsed_data["window"]
updates = parsed_data["updates"]
weather = parsed_data["weather"]

# Optionally, cast the parsed data to match our TypedDict using type hints
config: Config = parsed_data
