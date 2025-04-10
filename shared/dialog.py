from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from .pop_up import PopupWindow


class Dialog(PopupWindow):
    """A dialog box to display a message."""

    def __init__(
        self,
        title: str,
        body: str,
        command: str,
        **kwargs,
    ):
        self.wrapper = Box(orientation="v", name="dialog-wrapper")

        self.title = Label(h_align="center", name="dialog-title", label=title.upper())

        self.body = Label(h_align="center", name="dialog-body", label=body)

        self.buttons = Box(
            orientation="h",
            name="dialog-buttons-box",
            v_align="center",
            h_align="center",
        )

        self.ok_btn = Button(label="OK", name="dialog-button")
        self.cancel_btn = Button(label="Cancel", name="dialog-button")

        self.buttons.children = (self.ok_btn, self.cancel_btn)

        self.ok_btn.connect(
            "clicked", lambda *_: exec_shell_command_async(command, lambda *_: None)
        )
        self.cancel_btn.connect("clicked", lambda *_: self.destroy())

        self.wrapper.children = (self.title, self.body, self.buttons)

        super().__init__(
            name="dialog",
            transition_type="crossfade",
            child=self.wrapper,
            anchor="center",
            keyboard_mode="on-demand",
            **kwargs,
        )
