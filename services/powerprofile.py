import gi
from fabric import Service
from gi.repository import Gio, GLib

gi.require_version("Gio", "2.0")
gi.require_version("GObject", "2.0")


class PowerProfiles(Service):
    """Service to interact with the PowerProfiles service."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self.power_profiles = {
            "performance": {
                "name": "Performance",
                "icon_name": "power-profile-performance-symbolic",
            },
            "balanced": {
                "name": "Balanced",
                "icon_name": "power-profile-balanced-symbolic",
            },
            "power-saver": {
                "name": "Power Saver",
                "icon_name": "power-profile-power-saver-symbolic",
            },
        }

        # Constants
        bus_name = "net.hadess.PowerProfiles"
        object_path = "/net/hadess/PowerProfiles"

        self.proxy = Gio.DBusProxy.new_sync(
            Gio.bus_get_sync(Gio.BusType.SYSTEM, None),
            Gio.DBusProxyFlags.NONE,
            None,
            bus_name,
            object_path,
            "net.hadess.PowerProfiles",
            None,
        )
        self.proxy.connect(
            "g-properties-changed",
            lambda proxy, changed, invalidated: print(
                "Properties changed:", changed["ActiveProfile"]
            ),
        )

    def get_active_profile(self):
        return self.power_profiles[self.proxy.get_cached_property("ActiveProfile")]

    def set_active_profile(self, profile):
        self.proxy.call_sync(
            "SetProfile", GLib.Variant("s", profile), Gio.DBusCallFlags.NONE, -1, None
        )
