from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from utils.widget_config import widget_config
from widgets import (
    Battery,
    BlueToothWidget,
    BrightnessWidget,
    CpuWidget,
    DateTimeWidget,
    HyprIdleWidget,
    HyprSunsetWidget,
    KeyboardLayoutWidget,
    LanguageWidget,
    MemoryWidget,
    Mpris,
    PowerButton,
    StorageWidget,
    SystemTray,
    TaskBarWidget,
    ThemeSwitcherWidget,
    UpdatesWidget,
    VolumeWidget,
    WeatherWidget,
    WindowTitleWidget,
    WorkSpacesWidget,
)
from widgets.notification import NotificationWidget


class StatusBar(Window):
    """A widget to display the status bar panel."""

    def __init__(
        self,
    ):
        super().__init__(
            name="panel",
            layer="top",
            anchor="left top right",
            pass_through=False,
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.widgets_list = {
            # Workspaces: Displays the list of workspaces or desktops
            "workspaces": WorkSpacesWidget,
            "system_tray": SystemTray,
            "notification": NotificationWidget,
            "task_bar": TaskBarWidget,
            "bluetooth": BlueToothWidget,
            "keyboard": KeyboardLayoutWidget,
            "brightness": BrightnessWidget,
            "power": PowerButton,
            # WindowTitle: Shows the title of the current window
            "window_title": WindowTitleWidget,
            # LanguageBox: Displays the current language selection
            "language": LanguageWidget,
            # DateTime: Displays the current date and time
            "datetime": DateTimeWidget,
            "volume": VolumeWidget,
            # HyprSunset: Provides information about the sunset time based on location
            "hypr_sunset": HyprSunsetWidget,
            # # HyprIdle: Shows the idle time for the system
            "hypr_idle": HyprIdleWidget,
            # Battery: Displays the battery status with optional label and tooltip
            "battery": Battery,
            # Cpu: Displays CPU usage information with optional label and tooltip
            "cpu": CpuWidget,
            # # ClickCounter: Tracks the number of clicks on a widget or component
            # "click_counter": ClickCounter(),
            # Memory: Displays the system's memory usage
            "memory": MemoryWidget,
            # Storage: Shows the system's storage usage (e.g., disk space)
            "storage": StorageWidget,
            # Weather: Displays the weather for a given city (e.g., Kathmandu)
            "weather": WeatherWidget,
            # Mpris: Displays information about the current media player status
            "mpris": Mpris,
            # Updates: Shows available system updates based on the OS
            "updates": UpdatesWidget,
            "theme_switcher": ThemeSwitcherWidget,
        }

        layout = self.make_layout()

        self.children = CenterBox(
            name="panel-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=layout["left_section"],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=layout["middle_section"],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=layout["right_section"],
            ),
        )

        self.show_all()

    def make_layout(self):
        """assigns the three sections their respective widgets"""

        layout = {"left_section": [], "middle_section": [], "right_section": []}

        for key in layout:
            layout[key].extend(
                self.widgets_list[widget](widget_config, bar=self)
                for widget in widget_config["layout"][key]
            )

        return layout
