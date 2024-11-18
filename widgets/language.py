from fabric.hyprland.widgets import Language
from fabric.widgets.box import Box

from fabric.utils import FormattedString, truncate


class LanguageBox(Box):
    def __init__(self, length=3, **kwargs):
        super().__init__(name="language-box", **kwargs)

        self.lang = Language(
            name="language",
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=length,
                suffix="",
            ),
        )

        self.children = self.lang
