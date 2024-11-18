from fabric.hyprland.widgets import (
    ActiveWindow,
)
from fabric.widgets.box import Box

from fabric.utils import FormattedString, truncate


class WindowBox(Box):
    def __init__(self, **kwargs):
        super().__init__(name="window-box", **kwargs)

        self.window = ActiveWindow(
            name="window",
            formatter=FormattedString(
                " {'Desktop' if not win_title else truncate(win_title, 30)}",
                truncate=truncate,
            ),
        )

        self.children = self.window
