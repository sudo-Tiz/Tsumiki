
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.label import Label

class Player(Box):
    """A widget to display the player information."""
    def __init__(self):
        super().__init__(orientation="v", spacing=4, v_align="start", h_expand=True, style_classes="widget-player")

       
        self.album_art_box = Box(spacing=12)
        self.album_art = Image(icon_name="audio-x-generic-symbolic", icon_size=16, style_classes="widget-player-album-art")
        self.album_art_box.pack_start(self.album_art, False, True, 0)

        self.text_box = Box(orientation="v", spacing=4)
        self.title_label = Label(label="Title", h_align="start", v_align="start",style_classes="widget-player-title")


        self.subtitle_label = Label(label="Subtitle", h_align="start", v_align="start",style_classes="widget-player-subtitle")
        self.text_box.pack_start(self.title_label, False, True, 0)
        self.text_box.pack_start(self.subtitle_label, False, True, 0)

        self.album_art_box.pack_start(self.text_box, False, True, 0)
        self.pack_start(self.album_art_box, False, True, 0)

        # Second child: Control buttons (Shuffle, Prev, Play/Pause, Next, Repeat)
        self.control_box = Box(spacing=6, homogeneous=True, h_align="center")

        self.button_shuffle = self.create_button("media-playlist-shuffle-symbolic", "button_shuffle_img")
        self.button_prev = self.create_button("media-seek-backward-symbolic", "button_prev_img")
        self.button_play_pause = self.create_button("media-playback-pause-symbolic", "button_play_pause_img")
        self.button_next = self.create_button("media-seek-forward-symbolic", "button_next_img")
        self.button_repeat = self.create_button("media-playlist-repeat-symbolic", "button_repeat_img")

        self.control_box.pack_start(self.button_shuffle, True, True, 0)
        self.control_box.pack_start(self.button_prev, True, True, 0)
        self.control_box.pack_start(self.button_play_pause, True, True, 0)
        self.control_box.pack_start(self.button_next, True, True, 0)
        self.control_box.pack_start(self.button_repeat, True, True, 0)

        self.pack_start(self.control_box, False, True, 2)

    def create_button(self, icon_name, img_id):
        button = Button(style_classes=["circular", "image-button", "flat"])
        image = Image(icon_name=icon_name, icon_size=20, name=img_id)
        button.add(image)
        return button

