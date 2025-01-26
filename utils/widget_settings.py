from typing import List, Literal, TypedDict

# Define the type
Layer = Literal["background", "bottom", "top", "overlay"]

# Common configuration fields that will be reused
BaseConfig = TypedDict(
    "BaseConfig", {"icon_size": str, "label": bool, "tooltip": bool, "interval": int}
)

# Layout configuration
Layout = TypedDict(
    "Layout", {"left": List[str], "middle": List[str], "right": List[str]}
)

# Power button configuration
PowerButton = TypedDict("PowerButton", {"icon": str, "icon_size": int, "tooltip": bool})

# HyprSunset configuration
HyprSunset = TypedDict(
    "HyprSunset",
    {
        **BaseConfig.__annotations__,
        "temperature": str,
        "enabled_icon": str,
        "disabled_icon": str,
    },
)

# TaskBar configuration
TaskBar = TypedDict("TaskBar", {"icon_size": int})

# SystemTray configuration
SystemTray = TypedDict("SystemTray", {"icon_size": int, "ignored": List[str]})

# HyprIdle configuration
HyprIdle = TypedDict(
    "HyprIdle",
    {**BaseConfig.__annotations__, "enabled_icon": str, "disabled_icon": str},
)

# Battery configuration
Battery = TypedDict(
    "Battery",
    {
        "label": bool,
        "tooltip": bool,
        "full_battery_level": int,
        "hide_label_when_full": bool,
    },
)

# Theme configuration
Theme = TypedDict("Theme", {"name": str})

# ClickCounter configuration
ClickCounter = TypedDict("ClickCounter", {"count": int})

# StopWatch configuration
StopWatch = TypedDict(
    "StopWatch", {"stopped_icon": str, "running_icon": str, "icon_size": str}
)


# Bar configuration
Options = TypedDict(
    "Options",
    {
        "screen_corners": bool,
        "check_updates": bool,
        "location": str,
        "layer": str,
        "widget_style": str,
    },
)

# Cpu configuration
Cpu = TypedDict("Cpu", {**BaseConfig.__annotations__, "icon": str})

# Mpris configuration
Mpris = TypedDict("Mpris", {**BaseConfig.__annotations__, "truncation_size": int})

# Memory configuration
Memory = TypedDict("Memory", {**BaseConfig.__annotations__, "icon": str})

# Storage configuration
Storage = TypedDict("Storage", {**BaseConfig.__annotations__, "icon": str})

# Workspaces configuration
Workspaces = TypedDict(
    "Workspaces",
    {"count": int, "occupied": bool, "ignored": List[int], "icon_map": dict},
)

# WindowTitle configuration
WindowTitle = TypedDict(
    "WindowTitle",
    {
        "enable_icon": bool,
        "truncation": bool,
        "truncation_size": int,
        "title_map": any,
    },
)

# Updates configuration
Updates = TypedDict("Updates", {**BaseConfig.__annotations__, "os": str, "icon": str})

# Bluetooth configuration
BlueTooth = TypedDict("BlueTooth", {"label": bool, "tooltip": bool, "icon_size": int})

# Weather configuration
Weather = TypedDict(
    "Weather",
    {
        "detect_location": bool,
        "location": str,
        "interval": int,
        "tooltip": bool,
        "label": bool,
    },
)

# Keyboard configuration
Keyboard = TypedDict("Keyboard", {**BaseConfig.__annotations__, "icon": str})

# MicroPhone configuration
MicroPhone = TypedDict("MicroPhone", {**BaseConfig.__annotations__})


Cava = TypedDict("Cava", {"bars": int})

# DateTimeMenu configuration
DateTimeMenu = TypedDict("DateTimeMenu", {"format": str, "notification_count": bool})

# ThemeSwitcher configuration
ThemeSwitcher = TypedDict("ThemeSwitcher", {**BaseConfig.__annotations__, "icon": str})

# Spacing configuration
Spacing = TypedDict("Spacing", {"size": int})

# Divider configuration
Divider = TypedDict("Divider", {"size": int})

# Language configuration
Language = TypedDict("Language", {"truncation_size": int})

# Volume configuration
Volume = TypedDict("Volume", {**BaseConfig.__annotations__, "step_size": int})

# Brightness configuration
Brightness = TypedDict("Brightness", {**BaseConfig.__annotations__, "step_size": int})


# Notification configuration
Notification = TypedDict(
    "Notification",
    {"ignored": List[str], "timeout": int, "anchor": str, "auto_dismiss": bool},
)

# Recording configuration
Recording = TypedDict("Recording", {"path": str, "icon_size": int, "tooltip": bool})


# OSD configuration
OSD = TypedDict(
    "Osd", {"enabled": bool, "timeout": int, "anchor": str, "show_label": bool}
)


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    bluetooth: BlueTooth
    brightness: Brightness
    cava: Cava
    click_counter: ClickCounter
    cpu: Cpu
    date_time: DateTimeMenu
    divider: Divider
    hypr_idle: HyprIdle
    hypr_sunset: HyprSunset
    keyboard: Keyboard
    language: Language
    layout: Layout
    memory: Memory
    microphone: MicroPhone
    mpris: Mpris
    notification: Notification
    options: Options
    osd: OSD
    power: PowerButton
    recorder: Recording
    spacing: Spacing
    stop_watch: StopWatch
    storage: Storage
    system_tray: SystemTray
    task_bar: TaskBar
    theme: Theme
    theme_switcher: ThemeSwitcher
    updates: Updates
    volume: Volume
    weather: Weather
    window_title: WindowTitle
    workspaces: Workspaces
