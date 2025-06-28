from fabric.utils import exec_shell_command_async, get_relative_path
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.widget_utils import nerd_font_icon


class ScreenShotWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, **kwargs):
        super().__init__(name="screenshot", **kwargs)


        self.box.children = nerd_font_icon(
            self.config["icon"],
            props={"style_classes": "panel-font-icon"},
        )

        if self.config.get("label", True):
            self.box.add(Label(label="screenshot", style_classes="panel-text"))

        if self.config.get("tooltip", False):
            self.set_tooltip_text("Screen Shot")

        self.connect("clicked", self.handle_click)

    def lazy_init(self):
        if not self.initialized:
            self.script_file = get_relative_path("../assets/scripts/screenshot.sh")
            self.initialized = True

    def handle_click(self, *_):
        """Take a screenshot."""
        self.lazy_init()

        command = f"{self.script_file} area {self.config['path']}"

        if self.config.get("annotation", True):
            command += " --annotate"

        exec_shell_command_async(command, lambda *_: None)
