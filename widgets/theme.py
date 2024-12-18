import os

from fabric.utils import get_relative_path
from fabric.widgets.button import Button

from utils.functions import copy_theme, text_icon
from utils.widget_config import BarConfig


class ThemeSwitcherWidget(Button):
    """A widget to switch themes."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(name="theme_switcher", style_classes="panel-button", **kwargs)

        self.config = widget_config["theme_switcher"]

        theme_files = os.listdir(get_relative_path("../styles/themes"))

        # Remove the '.scss' part from each string in the list
        self.themes_list = [style.replace(".scss", "") for style in theme_files]

        self.current_theme = self.themes_list[0]

        self.children = text_icon(
            self.config["icon"],
            self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.connect("clicked", self.cycle_themes)

    def cycle_themes(self, *_):
        """Cycle through the themes."""
        copy_theme(self.current_theme)
        self.current_theme = self.themes_list[
            (self.themes_list.index(self.current_theme) + 1) % len(self.themes_list)
        ]
