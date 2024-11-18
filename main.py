from fabric import Application
from fabric.utils import get_relative_path
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window

from utils import read_config
from widgets.battery import BatteryLabel
from widgets.hypridle import HyprIdle
from widgets.hyprsunset import HyprSunset
from widgets.language import LanguageBox
from widgets.mpris import Mpris
from widgets.stats import Cpu, Memory, Storage
from widgets.updates import Updates
from widgets.volume import AUDIO_WIDGET, VolumeWidget
from widgets.window import WindowBox
from widgets.workspace import WorkSpaceBox

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
        self.workspaces = WorkSpaceBox()

        self.active_window = WindowBox()

        self.language = LanguageBox()

        self.date_time = DateTime(name="date-time")
        self.system_tray = SystemTray(name="system-tray", spacing=4)

        battery_config = config["battery"]
        cpu_config = config["cpu"]
        updates_config = config["updates"]
        updates_config = config["updates"]

        self.hyprsunset = HyprSunset(config=config).create()
        self.hypridle = HyprIdle(config=config).create()

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
        )
        self.status_container.add(VolumeWidget()) if AUDIO_WIDGET is True else None

        self.battery = BatteryLabel(
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

        self.memory = Memory()
        self.storage = Storage()
        self.player = Mpris()
        self.updates = Updates(os=updates_config["os"])

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=[self.workspaces, self.active_window, self.language],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=[self.date_time, self.player],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.cpu,
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


if __name__ == "__main__":
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("main.css"))

    app.run()
