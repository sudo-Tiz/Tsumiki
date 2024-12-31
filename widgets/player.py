import gi

from fabric.widgets.box import Box
from fabric.widgets.scale import Scale
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import Gtk, Gdk
gi.require_version("Gtk", "3.0")


# Constants for icon names
FALLBACK_ICON = "audio-x-generic-symbolic"
PLAY_ICON = "media-playback-start-symbolic"
PAUSE_ICON = "media-playback-pause-symbolic"
PREV_ICON = "media-skip-backward-symbolic"
NEXT_ICON = "media-skip-forward-symbolic"


# Helper function to format length as mm:ss
def length_str(length):
    min = int(length // 60)
    sec = int(length % 60)
    return f"{min}:{sec:02}"


# Player class (converted from the original function)
class Player(Box):
    def __init__(self, player):
        super().__init__(orientation="vertical")

        self.player = player

        # Cover Image
        img = Image(
            image_file=player.get_cover_path(), size=17, h_expand=True, v_expand=True
        )

        # Track Title
        title = Label(label=player.get_track_title(), line_wrap=True)

        # Artist(s)
        artist = Label(label=", ".join(player.get_track_artists()), line_wrap=True)

        # Position Slider
        position_slider = Scale(
            Gtk.Orientation.HORIZONTAL, 0, 1, 0.01
        )
        position_slider.set_draw_value(False)
        position_slider.set_sensitive(player.get_length() > 0)
        position_slider.connect("value-changed", self.on_position_slider_changed)

        # Position Label
        position_label = Label()
        self.update_position_label(position_label)

        # Length Label
        length_label = Label(
            label=length_str(player.get_length()), h_align=Gtk.Align.END
        )

        # Icon (Entry-based)
        icon = Gtk.Image.new_from_icon_name(player.get_icon_name(), Gtk.IconSize.MENU)
        icon.set_halign(Gtk.Align.END)
        icon.set_vexpand(True)

        # Play/Pause Button
        play_pause_button = Button()
        play_pause_button.connect("clicked", self.on_play_pause_clicked)
        play_pause_button.set_child(
            Gtk.Image.new_from_icon_name(PLAY_ICON, Gtk.IconSize.BUTTON)
        )

        # Previous Button
        prev_button = Button()
        prev_button.connect("clicked", self.on_prev_clicked)
        prev_button.set_child(
            Image(icon_name=PREV_ICON, icon_size=16)
        )

        # Next Button
        next_button = Button()
        next_button.connect("clicked", self.on_next_clicked)
        next_button.set_child(
            Image(icon_name=NEXT_ICON, icon_size=16)
        )

        # Arrange elements into boxes
        player_box = Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        player_box.pack_start(title, False, False, 0)
        player_box.pack_start(artist, False, False, 0)
        player_box.pack_start(position_slider, False, False, 0)
        player_box.pack_start(position_label, False, False, 0)
        player_box.pack_start(length_label, False, False, 0)

        control_box = Box(spacing=6)
        control_box.pack_start(prev_button, False, False, 0)
        control_box.pack_start(play_pause_button, False, False, 0)
        control_box.pack_start(next_button, False, False, 0)

        player_box.pack_start(control_box, False, False, 0)

        self.add(player_box)

    def on_position_slider_changed(self, slider):
        value = slider.get_value()
        self.player.set_position(value * self.player.get_length())

    def on_play_pause_clicked(self, button):
        self.player.play_pause()

    def on_prev_clicked(self, button):
        self.player.previous()

    def on_next_clicked(self, button):
        self.player.next()

    def update_position_label(self, label):
        label.set_label(length_str(self.player.get_position()))


class Media(Box):
    def __init__(self, players):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.players = players

        # Create player widgets based on the list of players
        for player in self.players:
            player_widget = Player(player)
            self.pack_start(player_widget, False, False, 0)

