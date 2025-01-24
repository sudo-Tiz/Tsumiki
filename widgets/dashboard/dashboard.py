from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label

from services.mpris import MprisPlayerManager
from shared.cicrle_image import CircleImage
from shared.pop_over import PopOverWindow
from shared.widget_container import ButtonWidget
from utils.functions import psutil_fabricator, text_icon
from utils.widget_settings import BarConfig
from widgets.player import PlayerBoxStack

from .sliders.audio import AudioSlider
from .sliders.brightness import BrightnessSlider


class DashBoardMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, **kwargs):
        super().__init__(
            name="dashboard-menu", orientation="v", all_visible=True, **kwargs
        )

        user_label = Label(
            "User",
            style_classes="user_name",
        )

        box = CenterBox(
            orientation="v",
            start_children=Box(
                orientation="v",
                spacing=10,
                v_align="center",
                style_classes="user-box",
                children=(
                    Box(
                        orientation="h",
                        spacing=10,
                        children=(
                            CircleImage(
                                image_file=get_relative_path(
                                    "../../assets/images/no_image.jpg"
                                ),
                                size=70,
                            ),
                            user_label,
                        ),
                    ),
                    PlayerBoxStack(MprisPlayerManager()),
                ),
            ),
            center_children=Box(
                orientation="v",
                spacing=10,
                style_classes="slider-box",
                children=(AudioSlider(), BrightnessSlider()),
            ),
        )

        self.add(box)

        psutil_fabricator.connect(
            "changed",
            lambda _, value: user_label.set_label(value.get("user")[0]),
        )


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

        self.children = Box(
            children=(
                text_icon(
                    "󰤨",
                    props={
                        "style_classes": "panel-text-icon overlay-icon",
                    },
                ),
                text_icon(
                    "󰃠",
                    props={
                        "style_classes": "panel-text-icon overlay-icon",
                    },
                ),
                text_icon(
                    "",
                    props={
                        "style_classes": "panel-text-icon overlay-icon",
                    },
                ),
            )
        )
        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
