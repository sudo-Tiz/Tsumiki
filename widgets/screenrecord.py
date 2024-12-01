from fabric import Fabricator
from fabric.utils import exec_shell_command, get_relative_path
from fabric.widgets.button import Button

# TODO: on button click enable/disable recording


class ScreenRecord(Button):
    """A widget to control the screen recording."""

    def __init__(self, **kwargs):
        super().__init__(name="screen-recorder", style_classes="panel-box", **kwargs)
        screen_record_info = Fabricator(
            poll_from=exec_shell_command(
                get_relative_path("../assets/scripts/screen_record.sh status"),
            ).strip("\n"),
            stream=True,
        )

        screen_record_info.connect(
            "changed",
            lambda _, value: (self.get_status(value)),
        )

    def get_status(self, value):
        status: str = value["status"]
        self.set_tooltip_text(status.capitalize())

        if status == "recording":
            self.set_label("󰻂")
        else:
            self.set_label("")
