import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Create a window and a button
window = Gtk.Window(title="GTK Button Sensitivity Example")
button = Gtk.Button(label="Click Me")

# Load the CSS stylesheet
css_provider = Gtk.CssProvider()
css = """
GtkButton:sensitive {
    background-color: #4CAF50;
    color: white;
    border: 2px solid #388E3C;
}

GtkButton:insensitive {
    background-color: #B0BEC5;
    color: #607D8B;
    border: 2px solid #90A4AE;
}
"""
css_provider.load_from_data(css.encode('utf-8'))

# Apply the CSS to the screen
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Add the button to the window
window.add(button)

# Initially disable the button to see the "insensitive" style
button.set_sensitive(False)

# Show the window
window.show_all()

# Start the GTK main loop
Gtk.main()
