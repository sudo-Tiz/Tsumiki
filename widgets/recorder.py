from fabric.widgets.image import Image
from shared.widget_container import ButtonWidget
from utils import icons
from utils.widget_config import BarConfig


class Recorder(ButtonWidget):
    """A widget to record the system"""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="recorder", **kwargs)

        self.config = widget_config["recorder"]

        self.set_image(
            Image(icon_name=icons.icons["recorder"]["recording"], icon_size=16)
        )
