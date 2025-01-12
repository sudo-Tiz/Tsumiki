from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate

from shared.widget_container import BoxWidget
from utils.widget_config import BarConfig


class LanguageWidget(BoxWidget):
    """A widget to display the current language."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="language", **kwargs)

        self.config = widget_config["language"]

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config["truncation_size"],
                suffix="",
            ),
        )
        ## TODO: add tool tip

        self.children = self.lang
