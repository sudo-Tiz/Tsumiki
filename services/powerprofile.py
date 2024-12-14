import dbus

# Connect to the system bus
bus = dbus.SystemBus()

# Get the PowerProfiles object
power_profiles = bus.get_object(
    "org.freedesktop.UPower.PowerProfiles", "/org/freedesktop/UPower/PowerProfiles"
)

# Get the Properties interface for this object
properties_interface = dbus.Interface(power_profiles, "org.freedesktop.DBus.Properties")

# Access the ActiveProfile property correctly using the 'Get' method
active_profile = properties_interface.Get(
    "org.freedesktop.UPower.PowerProfiles", "ActiveProfile"
)
