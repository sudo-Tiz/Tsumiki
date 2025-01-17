from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate

from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig
from fabric.widgets.box import Box


class LanguageWidget(ButtonWidget):
    """A widget to display the current language."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="language", **kwargs)

        self.config = widget_config["language"]

        self.box = Box()
        self.children = (self.box,)

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config["truncation_size"],
                suffix="",
            ),
        )
        self.box.children = (self.lang,)
