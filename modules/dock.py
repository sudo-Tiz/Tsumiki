import gi
from fabric.utils import get_desktop_applications
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.revealer import Revealer
from fabric.widgets.separator import Separator
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import Glace

from shared.popoverv1 import PopupWindow
from utils.icon_resolver import IconResolver
from utils.monitors import HyprlandWithMonitors

gi.require_version("Glace", "0.1")


class AppBar(Box):
    """A simple app bar widget for the dock."""

    def __init__(self, parent: Window):
        self.client_buttons = {}
        self._parent = parent

        self._all_apps = get_desktop_applications()
        self.app_identifiers = self._build_app_identifiers_map()

        self.config = parent.config

        self.icon_size = self.config.get("icon_size", 30)
        self.preview_size = self.config.get("preview_size", [40, 50])

        super().__init__(
            spacing=10,
            name="app-bar",
            style_classes=["window-basic", "sleek-border"],
            children=[
                Button(
                    image=Image(
                        icon_name="view-app-grid-symbolic",
                        icon_size=self.icon_size,
                    ),
                    on_button_press_event=lambda *_: print(
                        self._parent.get_application().actions["toggle-appmenu"][0]()
                    ),
                )
            ],
        )
        self.icon_resolver = IconResolver()
        self._manager = Glace.Manager()
        self._manager.connect("client-added", self.on_client_added)
        self._preview_image = Image()
        self._hyp = HyprlandWithMonitors()

        for item in self.config.get("pinned_apps", []):
            app = self.find_app(item)

            if app:
                self.add(
                    Button(
                        style_classes=["buttons-basic"],
                        image=Image(
                            pixbuf=app.get_icon_pixbuf(self.icon_size),
                        ),
                        tooltip_text=app.display_name or app.name
                        if self.config.get("tooltip", True)
                        else None,
                        on_clicked=lambda *_, app=app: app.launch(),
                    )
                )

        self.add(Separator())

        self.popup_revealer = Revealer(
            child=Box(
                children=self._preview_image,
                style_classes=["window-basic", "sleek-border"],
            ),
            transition_type="crossfade",
            transition_duration=400,
        )

        self.popup = PopupWindow(
            parent,
            child=self.popup_revealer,
            margin="0px 0px 80px 0px",
            visible=False,
        )

        self.popup_revealer.connect(
            "notify::child-revealed",
            lambda *_: self.popup.set_visible(False)
            if not self.popup_revealer.child_revealed
            else None,
        )

    def update_preview_image(self, client, client_button: Button):
        self.popup.set_pointing_to(client_button)

        def capture_callback(pbuf, _):
            self._preview_image.set_from_pixbuf(
                pbuf.scale_simple(self.preview_size[0], self.preview_size[1], 2)
            )
            self.popup.set_visible(True)
            self.popup_revealer.reveal()

        self._manager.capture_client(
            client=client,
            overlay_cursor=False,
            callback=capture_callback,
            user_data=None,
        )

    def _build_app_identifiers_map(self):
        identifiers = {}
        for app in self._all_apps:
            if app.name:
                identifiers[app.name.lower()] = app
            if app.display_name:
                identifiers[app.display_name.lower()] = app
            if app.window_class:
                identifiers[app.window_class.lower()] = app
            if app.executable:
                identifiers[app.executable.split("/")[-1].lower()] = app
            if app.command_line:
                identifiers[app.command_line.split()[0].split("/")[-1].lower()] = app
        return identifiers

    def find_app(self, app_identifier):
        if not app_identifier:
            return None
        if isinstance(app_identifier, dict):
            for key in [
                "window_class",
                "executable",
                "command_line",
                "name",
                "display_name",
            ]:
                if app_identifier.get(key):
                    app = self.find_app_by_key(app_identifier[key])
                    if app:
                        return app
            return None
        return self.find_app_by_key(app_identifier)

    def find_app_by_key(self, key_value):
        if not key_value:
            return None
        normalized_id = str(key_value).lower()
        if normalized_id in self.app_identifiers:
            return self.app_identifiers[normalized_id]
        for app in self._all_apps:
            if app.name and normalized_id in app.name.lower():
                return app
            if app.display_name and normalized_id in app.display_name.lower():
                return app
            if app.window_class and normalized_id in app.window_class.lower():
                return app
            if app.executable and normalized_id in app.executable.lower():
                return app
            if app.command_line and normalized_id in app.command_line.lower():
                return app
        return None

    def on_client_added(self, _, client: Glace.Client):
        client_image = Image()

        client_button = Button(
            style_classes=["buttons-basic", "buttons-transition"],
            image=client_image,
            on_button_press_event=lambda _, event: client.activate()
            if event.button == 1
            else None,
            on_enter_notify_event=lambda *_: self.update_preview_image(
                client, client_button
            ),
            on_leave_notify_event=lambda *_: self.popup_revealer.unreveal(),
        )
        self.client_buttons[client.get_id()] = client_button

        client.connect(
            "notify::app-id",
            lambda *_: client_image.set_from_pixbuf(
                self.icon_resolver.get_icon_pixbuf(client.get_app_id(), self.icon_size)
            ),
        )

        client.connect(
            "notify::app-id",
            lambda *_: client_button.set_tooltip_window(
                Window(
                    child=Box(style="min-height: 50px; min-width: 50px;"),
                    visible=False,
                    all_visible=False,
                )
            ),
        )

        client.connect(
            "notify::activated",
            lambda *_: client_button.add_style_class("active")
            if client.get_activated()
            else client_button.remove_style_class("active"),
        )

        client.connect("close", lambda *_: self.remove(client_button))
        self.add(client_button)


class Dock(Window):
    """A dock for applications."""

    def __init__(self, config):
        self.config = config["modules"]["dock"]
        super().__init__(
            layer=self.config.get("layer", "top"),
            anchor=self.config.get("anchor", "bottom-center"),
        )
        self.revealer = Revealer(
            child=Box(children=[AppBar(self)], style="padding: 20px 50px 5px 50px;"),
            transition_duration=500,
            transition_type="slide-up",
        )
        self.children = EventBox(
            events=["enter-notify", "leave-notify"],
            child=Box(style="min-height: 1px", children=self.revealer),
            on_enter_notify_event=lambda *_: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *_: self.revealer.set_reveal_child(False),
        )
