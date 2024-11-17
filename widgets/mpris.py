from fabric.widgets.label import Label
from fabric.widgets.button import Button
from fabric.utils import invoke_repeater, exec_shell_command


class Mpris(Button):
    def __init__(
        self,
        length=30,
        enable_tooltip: bool = True,
    ):
        super().__init__(name="mpris")
        self.enable_tooltip = enable_tooltip

        self.label = Label(label="Nothing playing")
        self.children = [self.label]
        self.length = length
        self.connect("clicked", self.play_pause)

        invoke_repeater(1250, self.get_current)

    def get_current(self):
        self.details: str = exec_shell_command(
            'playerctl metadata --format "{{ title }} - {{ artist }}"'
        )

        if len(self.details) > 30:
            self.details = self.details[: self.length]

        self.label.set_label(f"{self.details}")

    def play_pause(self, *_):
        exec_shell_command("playerctl play-pause")


## hide the whole thing when stopped. Show icon. Use fab
