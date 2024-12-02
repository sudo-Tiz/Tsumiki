from fabric.utils import exec_shell_command, exec_shell_command_async, invoke_repeater
from fabric.widgets.button import Button


class CommandSwitcher(Button):
    """A button widget to toggle a command. Useful for making services with two states."""

    def __init__(
        self,
        command: str,
        enabled_icon: str,
        disabled_icon: str,
        name: str,
        enable_label=True,
        enable_tooltip=True,
        interval: int = 2000,
        **kwargs,
    ):
        self.command = command
        self.command_without_args = self.command.split(" ")[0]  # command without args

        super().__init__(
            style_classes="bar-button",
            name=name,
            **kwargs,
        )

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip

        self.connect("clicked", self.toggle)
        invoke_repeater(interval, self.update, initial_call=True)

    def is_active(self, *_):
        return (
            exec_shell_command(
                f"bash -c 'pgrep -x {self.command_without_args} > /dev/null && echo yes || echo no'",
            ).strip()
            == "yes"
        )

    def cat_icon(self, icon: str, text: str):
        return f"{icon} {text}"

    def toggle(self, *_):
        if self.is_active():
            exec_shell_command(f"pkill {self.command_without_args}")
        else:
            exec_shell_command_async(f"bash -c '{self.command}&'", lambda *_: None)
        return self.update()

    def update(self, *_):
        if self.enable_label:
            self.set_label(
                self.cat_icon(
                    icon=self.enabled_icon if self.is_active() else self.disabled_icon,
                    text="On" if self.is_active() else "Off",
                ),
            )
        else:
            self.set_label(
                self.cat_icon(
                    icon=self.enabled_icon if self.is_active() else self.disabled_icon,
                    text="",
                ),
            )

        if self.enable_tooltip:
            self.set_tooltip_text(
                f"{self.command_without_args} enabled"
                if self.is_active()
                else f"{self.command_without_args} disabled",
            )
        return True
