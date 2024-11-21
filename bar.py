from widgets.battery import Battery
from widgets.clickcounter import ClickCounter
from widgets.hypridle import HyprIdle
from widgets.hyprsunset import HyprSunset
from widgets.language import LanguageBox
from widgets.mpris import Mpris
from widgets.stats import Cpu, Memory, Storage
from widgets.updates import Updates
from widgets.volume import AUDIO_WIDGET, VolumeWidget
from widgets.weather import Weather
from widgets.window import WindowTitle
from widgets.workspace import WorkSpaces
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window

from utils import read_config


config = read_config()


class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            margin="10px 10px -2px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        layout = {"left_children": [], "center_children": [], "right_children": []}

        layout = config["layout"]
        battery_config = config["battery"]
        cpu_config = config["cpu"]
        updates_config = config["updates"]
        updates_config = config["updates"]

        widgets_list = {
            "workspaces": WorkSpaces(),
            "windowtitle": WindowTitle(),
            "language": LanguageBox(),
            "datetime": DateTime(name="date-time"),
            "systemtray": SystemTray(name="system-tray", spacing=4),
            "hyprsunset": HyprSunset(config=config).create(),
            "hypridle": HyprIdle(config=config).create(),
            "battery": Battery(
                enable_label=battery_config["enable_label"],
                enable_tooltip=battery_config["enable_tooltip"],
                interval=battery_config["interval"],
            ),
            "cpu": Cpu(
                icon=cpu_config["icon"],
                enable_label=cpu_config["enable_label"],
                enable_tooltip=cpu_config["enable_tooltip"],
                interval=cpu_config["interval"],
            ),
            "clickcounter": ClickCounter(),
            "memory": Memory(),
            "storage": Storage(),
            "weather": Weather("kathmandu"),
            "player": Mpris(),
            "updates": Updates(os=updates_config["os"]),
        }

        self.workspaces = WorkSpaces()

        self.window_title = WindowTitle()

        self.language = LanguageBox()

        self.date_time = DateTime(name="date-time")
        self.system_tray = SystemTray(name="system-tray", spacing=4)

        self.hyprsunset = HyprSunset(config=config).create()
        self.hypridle = HyprIdle(config=config).create()

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
        )
        self.status_container.add(VolumeWidget()) if AUDIO_WIDGET is True else None

        self.battery = Battery(
            enable_label=battery_config["enable_label"],
            enable_tooltip=battery_config["enable_tooltip"],
            interval=battery_config["interval"],
        )

        self.cpu = Cpu(
            icon=cpu_config["icon"],
            enable_label=cpu_config["enable_label"],
            enable_tooltip=cpu_config["enable_tooltip"],
            interval=cpu_config["interval"],
        )

        self.click_counter = ClickCounter()

        self.memory = Memory()
        self.storage = Storage()
        self.weather = Weather("kathmandu")
        self.player = Mpris()
        self.updates = Updates(os=updates_config["os"])

        layout["left_children"].extend(
            widgets_list[widget] for widget in layout["left"]
        )
        layout["center_children"].extend(
            widgets_list[widget] for widget in layout["left"]
        )

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=layout["left_children"],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=layout["right_children"],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.weather,
                    self.click_counter,
                    self.storage,
                    self.updates,
                    self.memory,
                    self.battery,
                    self.hypridle,
                    self.hyprsunset,
                    self.status_container,
                    self.system_tray,
                ],
            ),
        )

        self.show_all()
