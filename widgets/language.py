from fabric.hyprland.widgets import Language
from fabric.widgets.box import Box

from fabric.utils import FormattedString, bulk_replace


class LanguageBox(Box):
    def __init__(self, **kwargs):
        super().__init__(name="language-box", **kwargs)

        self.lang = Language(
            name="language",
            formatter=FormattedString(
                "{replace_lang(language)}",
                replace_lang=lambda lang: bulk_replace(
                    lang,
                    (r".*Eng.*", r".*Ar.*"),
                    ("ENG", "ARA"),
                    regex=True,
                ),
            ),
        )

        self.children = self.lang
