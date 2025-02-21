from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.power_profile import PowerProfiles
from shared.submenu import QuickSubMenu, QuickSubToggle


class PowerProfileItem(Button):
    """A button to display the power profile."""

    def __init__(
        self,
        key,
        profile,
        active,
        **kwargs,
    ):
        super().__init__(
            style_classes="submenu-button power-profile",
            **kwargs,
        )
        self.profile = profile

        self.power_profile_service = PowerProfiles().get_initial()

        self.children = (
            Box(
                orientation="h",
                spacing=10,
                children=(
                    Image(
                        icon_name=profile["icon_name"],
                        icon_size=18,
                    ),
                    Label(
                        label=profile["name"],
                        style_classes="submenu-item-label",
                    ),
                ),
            ),
        )

        self.connect(
            "button-press-event",
            lambda *_: self.power_profile_service.set_power_profile(key),
        )
        self.set_active(key, active)

    def set_active(self, key, active):
        self.children.pop().add_style_class(f"{'active' if key == active else ''}")


class PowerProfileSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = PowerProfiles().get_initial()

        self.profiles = self.client.power_profiles
        self.active = self.client.get_current_profile()

        self.child = [
            PowerProfileItem(key=key, profile=profile, active=self.active)
            for key, profile in self.profiles.items()
        ]

        self.scan_button = Button(
            style="background-color: transparent",
        )

        super().__init__(
            title="Power profiles",
            title_icon="power-profile-power-saver-symbolic",
            scan_button=self.scan_button,
            child=Box(orientation="v", children=self.child, spacing=8),
            **kwargs,
        )


class PowerProfileToggle(QuickSubToggle):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon="power-profile-power-saver-symbolic",
            action_label="Power Saver",
            submenu=submenu,
            **kwargs,
        )
        self.client = PowerProfiles().get_initial()
        self.update_action_button()
        self.set_active_style(True)
        self.action_button.set_sensitive(False)

        self.client.connect(
            "profile",
            self.update_action_button,
        )

    def unslug(self, text):
        return " ".join(word.capitalize() for word in text.split("-"))

    def update_action_button(self, *_):
        self.active_pfl = self.client.get_current_profile()

        icon = self.client.get_profile_icon(self.active_pfl)

        self.action_icon.set_from_icon_name(icon, 18)
        self.set_action_label(self.unslug(self.active_pfl))
