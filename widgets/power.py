from typing import Literal

from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.widget import Widget

from shared.popup import PopupWindow
from utils.config import BarConfig

POWER_BUTTONS = [
    {"name": "lock", "label": "Lock"},
    {"name": "logout", "label": "Logout"},
    {"name": "suspend", "label": "Suspend"},
    {"name": "hibernate", "label": "Hibernate"},
    {"name": "shutdown", "label": "Shutdown"},
    {"name": "reboot", "label": "Reboot"},
]


class PowerControlButtons(Button):
    """A widget to show power options."""

    def __init__(self, name, label, size, **kwargs):
        (
            super().__init__(
                orientation="v",
                name="power-control-button",
                on_clicked=lambda button: self.on_button_press(pressed_button=name),
                child=Box(
                    orientation="v",
                    children=[
                        Image(
                            image_file=get_relative_path(f"../assets/icons/{name}.png"),
                            size=size,
                        ),
                        Label(label=label),
                    ],
                ),
            ),
        )

    def on_button_press(
        self,
        pressed_button: Literal[
            "lock",
            "logout",
            "suspend",
            "hibernate",
            "shutdown",
            "reboot",
        ],
    ):
        print(pressed_button)
        match pressed_button:
            case "shutdown":
                exec_shell_command_async("systemctl poweroff")
            case "reboot":
                exec_shell_command_async("systemctl reboot")
            case "hibernate":
                exec_shell_command_async("systemctl hibernate")
            case "suspend":
                exec_shell_command_async("systemctl suspend")
            case "lock":
                exec_shell_command_async("loginctl lock-session")
            case "logout":
                exec_shell_command_async("loginctl terminate-user $USER")


class PowerMenuPopup(PopupWindow):
    """A popup window to show power options."""

    def __init__(self):
        self.selected_operation: (
            Literal[
                "lock",
                "logout",
                "suspend",
                "hibernate" "shutdown",
                "reboot",
            ]
            | None
        ) = None

        self.box_name = "power-menu"
        self.button_name = "power-control-button"
        self.icon_size = 100

        self.menu = Box(
            name=self.box_name,
            orientation="v",
            children=[
                Box(
                    orientation="h",
                    children=[
                        PowerControlButtons(
                            name=value["name"],
                            label=value["label"],
                            size=self.icon_size,
                        )
                        for value in POWER_BUTTONS[0:3]
                    ],
                ),
                Box(
                    orientation="h",
                    children=[
                        PowerControlButtons(
                            name=value["name"],
                            label=value["label"],
                            size=self.icon_size,
                        )
                        for value in POWER_BUTTONS[3:]
                    ],
                ),
            ],
        )

        super().__init__(
            transition_type="crossfade",
            child=self.menu,
            anchor="center",
            keyboard_mode="on-demand",
        )

    def set_action_buttons_focus(self, can_focus: bool):
        for child in self.menu.children[0]:
            child: Widget = child
            child.set_can_focus(can_focus)

    def do_confirm(self):
        match self.selected_operation:
            case "shutdown":
                exec_shell_command_async("systemctl poweroff")
            case "reboot":
                exec_shell_command_async("systemctl reboot")
            case "hibernate":
                exec_shell_command_async("systemctl hibernate")
            case "suspend":
                exec_shell_command_async("systemctl suspend")
            case "lock":
                exec_shell_command_async("loginctl lock-session")
            case "logout":
                exec_shell_command_async("loginctl terminate-user $USER")
        self.toggle_popup()

    def toggle_popup(self, monitor: bool = False):
        self.selected_operation = None
        self.set_action_buttons_focus(True)
        return super().toggle_popup()


class PowerButton(Button):
    """A widget to power off the system."""

    def __init__(self, config: BarConfig, icon="", **kwargs):
        super().__init__(name="power", style_classes="panel-button", **kwargs)
        self.set_label(icon)

        self.connect("clicked", lambda *_: PowerMenuPopup().toggle_popup())
