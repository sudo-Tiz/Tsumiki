from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from loguru import logger

from services.mpris import MprisPlayer, MprisPlayerManager
from utils.config import BarConfig
from utils.icons import ICONS


class Mpris(EventBox):
    """A widget to control the MPRIS."""

    def __init__(
        self,
        config: BarConfig,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(name="mpris")
        self.config = config["mpris"]

        # Services
        self.mpris_manager = MprisPlayerManager()

        for player in self.mpris_manager.players:
            logger.info(
                f"[PLAYER MANAGER] player found: {player.get_property('player-name')}",
            )
            self.player = MprisPlayer(player)

        self.player.connect("notify::metadata", self.get_current)
        self.player.connect("notify::playback-status", self.get_playback_status)

        self.label = Label(label="Nothing playing", style_classes="panel-text")
        self.text_icon = Label(label=ICONS["playing"], style="padding: 0 5px;")

        self.revealer = Revealer(
            name="mpris-revealer",
            transition_type="slide-right",
            transition_duration=300,
            child=self.label,
            reveal_child=False,
        )

        self.revealer.set_reveal_child(True)

        self.box = Box(
            style_classes="panel-box",
            children=[self.text_icon, self.revealer],
        )

        self.children = self.box

        # Connect the button press event to the play_pause method
        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: self.play_pause(),
            },
        )

    def get_current(self, *_):
        # Get the current player info and status
        metadata = self.player.metadata

        bar_label = metadata["xesam:title"]

        trucated_info = (
            bar_label if len(bar_label) < self.config["length"] else bar_label[:30]
        )

        self.label.set_label(trucated_info)

        if self.config["enable_tooltip"]:
            self.set_tooltip_text(bar_label)

    def get_playback_status(self, *_):
        status = self.player.playback_status.lower()
        if status == "playing":
            self.text_icon.set_label(ICONS["paused"])
        else:
            self.text_icon.set_label(ICONS["playing"])

    def play_pause(self, *_):
        # Toggle play/pause using playerctl
        self.player.play_pause()
