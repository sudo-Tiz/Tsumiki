from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox

from services.mpris import MprisPlayerManager
from shared.pop_over import PopOverWindow
from shared.separator import Separator
from shared.widget_container import ButtonWidget
from utils.functions import text_icon
from utils.widget_settings import BarConfig
from widgets.dashboard.player import PlayerBoxStack

from .sliders.audio import AudioSlider
from .sliders.brightness import BrightnessSlider


class DashBoardMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, **kwargs):
        super().__init__(
            name="dashboard-menu", orientation="v", all_visible=True, **kwargs
        )

        box = CenterBox(
            orientation="v",
            start_children=Box(
                orientation="v",
                spacing=10,
                style_classes="slider-box",
                children=(
                    AudioSlider(),
                    BrightnessSlider(),
                    Separator(),
                ),
            ),
            center_children=PlayerBoxStack(mpris_manager=MprisPlayerManager()),
        )

        self.add(box)


class DashBoardWidget(ButtonWidget):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", **kwargs)

        self.config = widget_config["date_time"]

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(DashBoardMenu()),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.children = text_icon(
            "󰃠",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
