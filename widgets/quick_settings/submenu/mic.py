from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import Gtk

from services import audio_service
from shared.animator import Animator
from shared.circle_image import CircleImage
from shared.submenu import QuickSubMenu
from shared.widget_container import HoverButton
from utils.icons import icons
from widgets.quick_settings.sliders.mic import MicrophoneSlider


class MicroPhoneSubMenu(QuickSubMenu):
    """A submenu to display mic controls."""

    def __init__(self, **kwargs):
        self.client = audio_service

        self.scan_image = CircleImage(
            image_file=get_relative_path("../../../assets/icons/refresh.png"),
            size=20,
        )

        # Create refresh button first since parent needs it
        self.scan_button = HoverButton(
            style_classes="submenu-button",
            name="scan-button",
            image=self.scan_image,
        )

        self.scan_animator = Animator(
            bezier_curve=(0, 0, 1, 1),
            duration=4,
            min_value=0,
            max_value=360,
            tick_widget=self,
            repeat=False,
            notify_value=lambda p, *_: self.scan_image.set_angle(p.value),
        )
        self.scan_button.connect("clicked", lambda _: self.update_apps())

        # Create app list container
        self.app_list = Gtk.ListBox(
            selection_mode=Gtk.SelectionMode.NONE, name="app-list"
        )
        self.app_list.get_style_context().add_class("menu")

        # Wrap in scrolled window
        self.child = ScrolledWindow(
            min_content_size=(-1, 100),
            max_content_size=(-1, 100),
            propagate_width=True,
            propagate_height=True,
            h_scrollbar_policy=Gtk.PolicyType.NEVER,
            child=self.app_list,
        )

        # Initialize parent with our components
        super().__init__(
            title="Microphones",
            title_icon=icons["audio"]["mic"]["high"],
            scan_button=self.scan_button,
            child=Box(orientation="v", children=[self.child]),
            **kwargs,
        )

        # Connect signals
        self.client.connect("changed", self.update_apps)
        self.update_apps()

    def update_apps(self, *args):
        """Update the list of applications with volume controls."""

        self.scan_animator.play()
        # Clear existing rows
        while row := self.app_list.get_row_at_index(0):
            self.app_list.remove(row)

        # Add applications
        for app in self.client.microphones:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("menu-item")

            # Main container
            box = Box(
                name="list-box-row",
                orientation="v",
                spacing=10,
                margin_start=6,
                margin_end=6,
                margin_top=3,
                margin_bottom=3,
            )

            # App name
            name_box = Box(orientation="h", spacing=12, h_expand=True)

            # App icon
            icon = Image(
                icon_name=app.icon_name or icons["audio"]["mic"]["high"],
                icon_size=16,
            )
            name_box.pack_start(icon, False, True, 0)

            # App name label
            name_label = Label(label=app.name, style_classes="submenu-item-label")
            name_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
            name_label.set_halign(Gtk.Align.START)
            name_label.set_tooltip_text(app.description or app.name)
            name_box.pack_start(name_label, True, True, 0)

            box.add(name_box)

            # Audio controls
            audio_box = Box(
                orientation="h",
                spacing=6,
                margin_start=24,  # Indent to align with app name
            )

            # Create audio slider for this app
            slider = MicrophoneSlider(app, show_chevron=False)
            audio_box.pack_start(slider, True, True, 0)

            box.add(audio_box)

            row.add(box)
            self.app_list.add(row)

        self.app_list.show_all()
