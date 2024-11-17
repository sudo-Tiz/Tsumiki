from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.hyprland.widgets import Language, ActiveWindow, Workspaces, WorkspaceButton
from fabric.utils import FormattedString, bulk_replace, get_relative_path, truncate

from utils import read_config
from widgets import player
from widgets.battery import BatteryLabel
from widgets.paneltoggle import CommandSwitcher
from widgets.stats import Cpu, Memory, Storage
from widgets.updates import Updates
from widgets.volume import AUDIO_WIDGET, VolumeWidget

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
        self.workspaces = Workspaces(
            name="workspaces",
            spacing=4,
            buttons=[WorkspaceButton(id=i, label=str(i)) for i in range(1, 8)],
            buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=str(ws_id)),
        )
        self.active_window = ActiveWindow(
            name="hyprland-window",
            formatter=FormattedString(
                " {'Desktop' if not win_title else truncate(win_title, 42)}",
                truncate=truncate,
            ),
        )

        self.language = Language(
            formatter=FormattedString(
                "{replace_lang(language)}",
                replace_lang=lambda lang: bulk_replace(
                    lang,
                    (r".*Eng.*", r".*Ar.*"),
                    ("ENG", "ARA"),
                    regex=True,
                ),
            ),
            name="hyprland-window",
        )
        self.date_time = DateTime(name="date-time")
        self.system_tray = SystemTray(name="system-tray", spacing=4)

        hypersunset_config = config["hyprsunset"]
        hyperidle_config = config["hypridle"]
        battery_config = config["battery"]
        cpu_config = config["cpu"]
        updates_config = config["updates"]

        self.hyprsunset = CommandSwitcher(
            command=f"hyprsunset -t {hypersunset_config["temperature"]}",
            enabled_icon=hypersunset_config["enabled_icon"],
            disabled_icon=hypersunset_config["disabled_icon"],
            enable_label=hypersunset_config["enable_label"],
            enable_tooltip=hypersunset_config["enable_tooltip"],
        )
        self.hypridle = CommandSwitcher(
            command="hypridle",
            enabled_icon=hyperidle_config["enabled_icon"],
            disabled_icon=hyperidle_config["disabled_icon"],
            enable_label=hyperidle_config["enable_label"],
            enable_tooltip=hyperidle_config["enable_tooltip"],
        )

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
        self.player = player()
        self.updates = Updates(os=updates_config["os"])

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=[
                    self.workspaces,
                    self.active_window,
                ],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=[self.date_time,self.player],
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
