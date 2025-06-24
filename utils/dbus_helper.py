from gi.repository import Gio, GLib


class GioDBusHelper:
    """A helper class for interacting with D-Bus using the Gio library."""

    def __init__(
        self,
        bus_name,
        object_path,
        interface_name,
        bus_type=Gio.BusType.SYSTEM,
    ):
        self.bus_name = bus_name
        self.object_path = object_path
        self.interface_name = interface_name

        self.bus = Gio.bus_get_sync(bus_type, None)

        self.proxy = Gio.DBusProxy.new_sync(
            self.bus,
            Gio.DBusProxyFlags.NONE,
            None,
            self.bus_name,
            self.object_path,
            self.interface_name,
            None,
        )

    def call_method(
        self,
        method_name,
        parameters=None,
        timeout=-1,
    ):
        if parameters is None:
            parameters = GLib.Variant("()", ())
        result = self.bus.call_sync(
            self.bus_name,
            self.object_path,
            self.interface_name,
            method_name,
            parameters,
            None,
            Gio.DBusCallFlags.NONE,
            timeout,
            None,
        )
        return result.unpack()

    def listen_signal(self, sender, member, callback):
        """Register a signal listener (conn, sender, path, iface, signal, parameters)"""
        self.bus.signal_subscribe(
            sender,
            self.interface_name,
            member,
            self.object_path,
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=callback,
        )

    def get_property(self, property_name):
        """Gets a D-Bus property using the standard D-Bus Properties interface."""
        result = self.call_method(
            "Get",
            GLib.Variant("(ss)", (self.interface_name, property_name)),
        )
        return result[0]  # It's a variant inside a variant

    def set_property(self, property_name, value_variant):
        """Sets a D-Bus property using the standard D-Bus Properties interface."""
        return self.call_method(
            method_name="Set",
            parameters=GLib.Variant(
                "(ssv)", (self.interface_name, property_name, value_variant)
            ),
        )
