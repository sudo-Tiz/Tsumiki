from fabric import Fabricator
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.utils import exec_shell_command, bulk_connect

from icons import ICONS

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


class Mpris(EventBox):
    def __init__(
        self,
        length=30,
        enable_tooltip=True,
    ):
        super().__init__(name="mpris", style_classes="bar-box")
        self.enable_tooltip = enable_tooltip

        self.label = Label(label="Nothing playing", style_classes="bar-button-label")
        self.text_icon = Label(label=ICONS["play"], style="padding: 0 10px;")

        self.revealer = Revealer(
            name="player-info-revealer",
            transition_type="slide-right",
            transition_duration=300,
            child=self.label,
            reveal_child=False,
        )

        self.revealer.set_reveal_child(True)

        self.box = Box(children=[self.text_icon, self.revealer])

        self.children = self.box
        self.length = length

        bulk_connect(
            self,
            {
                # "enter-notify-event": lambda *_: (
                #     self.revealer.set_reveal_child(True)
                #     if not self.revealer.get_reveal_child()
                #     else None
                # ),
                # "leave-notify-event": lambda *_: self.revealer.set_reveal_child(False)
                # if self.revealer.get_reveal_child()
                # else None,
                "button-press-event": lambda *_: self.play_pause(),
            },
        )

        playerInfo.connect(
            "changed",
            lambda _, value: (self.get_current(value)),
        )

    def get_current(self, value):
        info = value["info"] if len(value["info"]) < 30 else value["info"][:30]
        status = value["status"]

        if status == "Playing":
            self.set_visible(True)
            self.text_icon.set_label(ICONS["pause"])
            self.label.set_label(info)

        elif status == "Paused":
            self.set_visible(True)
            self.text_icon.set_label(ICONS["play"])
            self.label.set_label(info)

        else:
            self.set_visible(False)

        return True

    def play_pause(self, *_):
        exec_shell_command("playerctl play-pause")
