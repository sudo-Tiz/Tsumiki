from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import GLib, Gtk

from services import weather_service
from shared import LottieAnimationWidget, LottieAnimation, PopOverWindow
from utils.functions import convert_seconds_to_miliseconds, text_icon
from utils.icons import weather_text_icons, weather_text_icons_v2
from utils.widget_config import BarConfig


class Dashboard(Button):
    def __init__(self):
        super(self).__init__()
