from fabric.widgets.entry import Entry
from gi.repository import Gdk, Gtk


class TagEntry(Gtk.Box):
    def __init__(self, available_tags=None, **kwargs):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_spacing(2)

        # List of available tags
        self.available_tags = available_tags or [
            "python",
            "gtk",
            "programming",
            "ui",
            "linux",
        ]

        # Track created tags
        self.tags = []

        # Create the active entry
        self.entry = Entry(**kwargs)
        self.entry.set_hexpand(True)
        self.entry.connect("key-press-event", self.on_key_press)
        self.entry.connect("changed", self.on_text_changed)

        # Add entry to the box
        self.pack_start(self.entry, True, True, 0)
        self.show_all()

    def on_text_changed(self, entry):
        text = entry.get_text().strip()
        if text in self.available_tags:
            entry.get_style_context().add_class("tag-match")
        else:
            entry.get_style_context().remove_class("tag-match")

    def on_key_press(self, entry, event):
        keyval = event.keyval

        # Handle Enter key
        if keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
            text = entry.get_text().strip()
            if text and text in self.available_tags:
                self.create_tag(text)
                entry.set_text("")
                return True

        # Handle backspace
        elif keyval == Gdk.KEY_BackSpace:
            if entry.get_text() == "" and self.tags:
                # Remove the last tag
                self.remove_last_tag()
                return True

        return False

    def create_tag(self, text):
        # Create a tag button
        tag_box = Gtk.EventBox()
        tag_box.connect("button-press-event", self.on_tag_clicked)
        tag_box.tag_text = text

        # Container for the tag content
        tag_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        tag_container.set_spacing(4)

        # Tag label
        label = Gtk.Label(label=text)

        # Apply styling
        context = tag_box.get_style_context()
        context.add_class("tag")

        # Pack widgets
        tag_container.pack_start(label, False, False, 4)
        tag_box.add(tag_container)

        # Insert the tag before the entry
        position = len(self.get_children()) - 1  # Position before the entry
        self.pack_start(tag_box, False, False, 0)
        self.reorder_child(tag_box, position)

        # Store the tag
        self.tags.append(tag_box)

        self.show_all()

    def remove_last_tag(self):
        if self.tags:
            last_tag = self.tags.pop()
            self.remove(last_tag)

    def on_tag_clicked(self, widget, event):
        if event.button == 1 and event.type == Gdk.EventType.BUTTON_PRESS:
            # Remove the clicked tag
            self.tags.remove(widget)
            self.remove(widget)
            self.entry.grab_focus()

    def get_tags(self):
        return [tag.tag_text for tag in self.tags]


class TagInputDemo(Gtk.Window):
    def __init__(self):
        super().__init__(title="Tag Input Demo")
        self.set_default_size(400, 100)
        self.set_border_width(10)

        # Load CSS
        self.load_css()

        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Instructions
        instruction = Gtk.Label()
        instruction.set_markup(
            "<b>Available tags:</b> python, gtk, programming, ui, linux"
        )
        instruction.set_halign(Gtk.Align.START)
        vbox.pack_start(instruction, False, False, 0)

        # Create tag entry
        self.tag_entry = TagEntry()
        vbox.pack_start(self.tag_entry, False, False, 0)

        # Button to get tags
        button = Gtk.Button(label="Get Tags")
        button.connect("clicked", self.on_get_tags_clicked)
        vbox.pack_start(button, False, False, 0)

        # Result label
        self.result_label = Gtk.Label(label="")
        self.result_label.set_halign(Gtk.Align.START)
        vbox.pack_start(self.result_label, False, False, 0)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .tag {
            background-color: #3498db;
            border-radius: 4px;
            color: white;
            padding: 2px;
        }

        .tag-match {
            background-color: #e8f4fc;
        }
        """
        css_provider.load_from_data(css.encode())

        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_get_tags_clicked(self, button):
        tags = self.tag_entry.get_tags()
        if tags:
            self.result_label.set_text(f"Selected tags: {', '.join(tags)}")
        else:
            self.result_label.set_text("No tags selected")
