from fabric import Fabricator
from fabric.widgets.label import Label
from fabric.widgets.button import Button
from fabric.widgets.box import Box
from fabric.utils import exec_shell_command

playerInfo = Fabricator(
    poll_from=lambda: {
        "status": str(exec_shell_command("playerctl status").strip("\n")),
        "info": str(
            exec_shell_command(
                'playerctl metadata --format "{{ title }} - {{ artist }}"'
            ).strip("\n")
        ),
    },
    interval=1000,
)


class Mpris(Box):
    def __init__(
        self,
        length=30,
        enable_tooltip=True,
    ):
        super().__init__(name="mpris")
        self.enable_tooltip = enable_tooltip

        self.label = Label(label="Nothing playing", style_classes="box-label")
        self.button = Button(label="", name="mpris-button")
        self.children = [self.button, self.label]
        self.length = length
        self.button.connect("clicked", self.play_pause)

        playerInfo.connect(
            "changed",
            lambda _, value: (self.get_current(value)),
        )

    def get_current(self, value):
        if value["status"] == "Playing":
            self.button.set_label("")
        elif value["status"] == "Paused":
            self.button.set_label("")
        self.label.set_label(value["info"])

    def play_pause(self, *_):
        exec_shell_command("playerctl play-pause")


## hide the whole thing when stopped. Show icon. Use fab
