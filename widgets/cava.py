
from fabric import Fabricator
from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.widget_container import BoxWidget
from utils.widget_config import BarConfig


class CavaWidget(BoxWidget):
    """A widget to display the Cava audio visualizer."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="cava",**kwargs)

        label = Label()
        self.children= (
        Box(spacing=1, children=[label]).build(
        lambda box, _: Fabricator(
            poll_from=f"bash -c {get_relative_path('../assets/scripts/cava.sh')}",
            interval=0,
            stream=True,
            on_changed=lambda f, line: label.set_label(line),
        )
        )
        )
