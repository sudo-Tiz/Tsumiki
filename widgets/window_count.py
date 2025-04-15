import json

from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import bulk_connect
from fabric.widgets.label import Label
from loguru import logger

from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


class WindowCountWidget(ButtonWidget):
    """A widget to display windows in active workspace."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="window_count", **kwargs)
        self.config = widget_config["window_count"]

        self.connection = get_hyprland_connection()

        self.icon = text_icon(
            icon=self.config["icon"],
            props={"style_classes": "panel-icon"},
        )

        self.count_label = Label(label="0", style_classes="panel-text")

        self.box.children = (self.icon, self.count_label)

        bulk_connect(
            self.connection,
            {
                "event::workspace": lambda *_: self.get_window_count(),
                "event::focusedmon": lambda *_: self.get_window_count(),
                "event::openwindow": lambda *_: self.get_window_count(),
                "event::closewindow": lambda *_: self.get_window_count(),
                "event::movewindow": lambda *_: self.get_window_count(),
            },
        )

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.get_window_count(), logger.info(
            "[WindowCount] Connected to the hyprland socket"
        )

    def get_window_count(
        self,
    ):
        """Get the number of windows in the active workspace."""
        data = json.loads(
            str(self.connection.send_command("j/activeworkspace").reply.decode())
        )

        self.count_label.set_label(
            self.config["label_format"].format(count=data["windows"])
        )

        return (
            logger.info("[WindowCount] Could not find active windows for workspace")
            if not data
            else logger.info(
                f"[WindowCount] Set WindowCount for workspace: {data['id']}"
            )
        )
