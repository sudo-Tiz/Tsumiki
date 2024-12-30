from fabric.utils import exec_shell_command, exec_shell_command_async, invoke_repeater

import utils.functions as helpers
from shared.widget_container import ButtonWidget


class CommandSwitcher(ButtonWidget):
    """A button widget to toggle a command. Useful for making services with two states."""

    def __init__(
        self,
        command: str,
        enabled_icon: str,
        disabled_icon: str,
        name: str,
        label=True,
        tooltip=True,
        interval: int = 2000,
        **kwargs,
    ):
        self.command = command
        self.command_without_args = self.command.split(" ")[0]  # command without args

        super().__init__(
            name=name,
            **kwargs,
        )

        if not helpers.executable_exists(self.command_without_args):
            raise helpers.ExecutableNotFoundError(self.command_without_args)

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.label = label
        self.tooltip = tooltip

        self.connect("clicked", self.toggle)
        invoke_repeater(interval, self.update, initial_call=True)

    def cat_icon(self, icon: str, text: str):
        return f"{icon} {text}"

    def toggle(self, *_):
        if helpers.is_app_running(self.command_without_args):
            exec_shell_command(f"pkill {self.command_without_args}")
        else:
            exec_shell_command_async(f"bash -c '{self.command}&'", lambda *_: None)
        return self.update()

    def update(self, *_):
        if self.label:
            self.set_label(
                self.cat_icon(
                    icon=self.enabled_icon
                    if helpers.is_app_running(self.command_without_args)
                    else self.disabled_icon,
                    text="On"
                    if helpers.is_app_running(self.command_without_args)
                    else "Off",
                ),
            )
        else:
            self.set_label(
                self.cat_icon(
                    icon=self.enabled_icon
                    if helpers.is_app_running(self.command_without_args)
                    else self.disabled_icon,
                    text="",
                ),
            )

        if self.tooltip:
            self.set_tooltip_text(
                f"{self.command_without_args} enabled"
                if helpers.is_app_running(self.command_without_args)
                else f"{self.command_without_args} disabled",
            )
        return True
