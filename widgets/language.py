from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box

from utils.widget_config import BarConfig


class LanguageWidget(Box):
    """A widget to display the current language."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(name="language", style_classes="panel-box", **kwargs)

        self.config = widget_config["language"]

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config["length"],
                suffix="",
            ),
        )
        ## TODO: add tool tip

        self.children = self.lang
