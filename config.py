from typing import TypedDict, List

from utils import read_config


# Define the TypedDict types as shown previously
class Layout(TypedDict):
    left: List[str]
    middle: List[str]
    right: List[str]


class HyprSunset(TypedDict):
    temperature: str
    enabled_icon: str
    disabled_icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool


class HyprIdle(TypedDict):
    enabled_icon: str
    disabled_icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool


class Battery(TypedDict):
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Cpu(TypedDict):
    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Memory(TypedDict):
    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Storage(TypedDict):
    icon: str
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Workspaces(TypedDict):
    count: int


class Window(TypedDict):
    length: int


class Updates(TypedDict):
    os: str
    icon: str
    icon_size: str


class Weather(TypedDict):
    location: str


class Config(TypedDict):
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
