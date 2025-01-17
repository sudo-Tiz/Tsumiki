import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ColorChangeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hover to Change Color")

        self.set_default_size(400, 400)

        # Create a GtkEventBox
        event_box = Gtk.EventBox()

        # Set a custom CSS class for the GtkEventBox
        event_box.get_style_context().add_class("my-event-box")

        # Create a GtkBox (container)
        box = Gtk.Box(spacing=6)
        box.set_border_width(10)

        # Add a label to the box
        label = Gtk.Label(label="Hover over this box")
        box.pack_start(label, True, True, 0)

        # Add the GtkBox as the child of the GtkEventBox
        event_box.add(box)

        # Add the event box to the window
        self.add(event_box)

        # Load and apply CSS styles
        self.apply_css()

    def apply_css(self):
        # Create a CssProvider and load CSS styles
        css_provider = Gtk.CssProvider()
        css = """
        GtkEventBox.my-event-box:hover GtkBox {
            background-color: red;
            color: white;
        }

        GtkBox {
            background-color: white;
        }
        """
        css_provider.load_from_data(css.encode())

        # Apply the CSS to the window
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


# Create the window and run the application
win = ColorChangeWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
