from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box


class LanguageBox(Box):
    def __init__(self, length=3, **kwargs):
        super().__init__(name="language", style_classes="panel-box", **kwargs)

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=length,
                suffix="",
            ),
        )
        ## Todo: add tool tip

        self.children = self.lang
