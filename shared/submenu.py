from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.widget import Widget

from .animator import Animator
from .circle_image import CircleImage
from .widget_container import HoverButton


class ScanButton(HoverButton):
    """A button to start a scan action."""

    def __init__(self, **kwargs):
        super().__init__(name="scan-button", style_classes="submenu-button", **kwargs)

        self.scan_image = CircleImage(
            image_file=get_relative_path("../assets/icons/png/refresh.png"),
            size=20,
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

        self.set_image(self.scan_image)

    def play_animation(self):
        self.scan_animator.play()

    def stop_animation(self):
        self.scan_animator.stop()


class QuickSubMenu(Box):
    """A widget to display a submenu for quick settings."""

    def __init__(
        self,
        scan_button: Button,
        child: Widget | None,
        title: str | None = None,
        title_icon: str | None = None,
        **kwargs,
    ):
        self.title = title
        self.title_icon = title_icon
        self.child = child

        super().__init__(visible=False, **kwargs)
        self.revealer_child = Box(orientation="v", name="submenu")

        self.submenu_title_box = self.make_submenu_title_box()

        self.scan_button = scan_button

        self.revealer_child.add(
            self.submenu_title_box
        ) if self.submenu_title_box else None
        self.revealer_child.add(self.child) if child else None

        self.revealer = Revealer(
            child=self.revealer_child,
            transition_type="slide-down",
            transition_duration=600,
            h_expand=True,
        )
        self.revealer.connect(
            "notify::child-revealed",
            lambda rev, _: self.set_visible(rev.get_reveal_child()),
        )

        self.add(self.revealer)

    def make_submenu_title_box(self) -> Box | None:
        submenu_box = Box(spacing=4, style_classes="submenu-title-box")

        if not self.title_icon and not self.title:
            return None
        if self.title_icon:
            submenu_box.add(Image(icon_name=self.title_icon, icon_size=18))
        if self.title:
            submenu_box.add(
                Label(style_classes="submenu-title-label", label=self.title)
            )

        submenu_box.pack_end(
            self.scan_button,
            False,
            False,
            0,
        )

        return submenu_box

    def do_reveal(self, visible: bool):
        self.set_visible(True)
        self.revealer.set_reveal_child(visible)

    def toggle_reveal(self) -> bool:
        self.set_visible(True)
        self.revealer.set_reveal_child(not self.revealer.get_reveal_child())
        return self.revealer.get_reveal_child()
