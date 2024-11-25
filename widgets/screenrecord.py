from fabric import Fabricator
from fabric.widgets.button import Button
from fabric.utils import exec_shell_command, get_relative_path

screenRecordInfo = Fabricator(
    poll_from=lambda: {
        "status": str(
            exec_shell_command(
                get_relative_path("../assets/scripts/screen_record.sh status")
            ).strip("\n")
        )
    },
    interval=1000,
)


## TODO: on button click enable/disable recording


class ScreenRecord(Button):
    def __init__(self, **kwargs):
        super().__init__(name="screen-recorder", style_classes="bar-box")

        screenRecordInfo.connect(
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
