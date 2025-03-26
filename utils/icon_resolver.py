import json
import os
import re

from gi.repository import GLib, Gtk
from loguru import logger

from .colors import Colors
from .constants import APP_CACHE_DIRECTORY

ICON_CACHE_FILE = APP_CACHE_DIRECTORY + "/icons.json"


class IconResolver:
    """A class to resolve icons for applications."""

    instance = None

    @staticmethod
    def get_default():
        if IconResolver.instance is None:
            IconResolver.instance = IconResolver()

        return IconResolver.instance

    def __init__(self):
        if os.path.exists(ICON_CACHE_FILE):
            with open(ICON_CACHE_FILE) as file:
                try:
                    self._icon_dict = json.load(file)
                except json.JSONDecodeError:
                    logger.info(
                        f"{Colors.INFO}[ICONS] Cache file does not exist or corrupted."
                    )
        else:
            self._icon_dict = {}

    def get_icon_name(self, app_id: str):
        if app_id in self._icon_dict:
            return self._icon_dict[app_id]
        new_icon = self._compositor_find_icon(app_id)
        logger.info(
            f"[ICONS] found new icon: '{new_icon}' for app id: '{app_id}', storing."
        )
        self._store_new_icon(app_id, new_icon)
        return new_icon

    def get_icon_pixbuf(self, app_id: str, size: int = 16):
        icon_name = self.get_icon_name(app_id)
        try:
            return Gtk.IconTheme.get_default().load_icon(
                icon_name,
                size,
                Gtk.IconLookupFlags.FORCE_SIZE,
            )
        except GLib.GError:
            return None

    def _store_new_icon(self, app_id: str, icon: str):
        self._icon_dict[app_id] = icon
        with open(ICON_CACHE_FILE, "w") as f:
            json.dump(self._icon_dict, f, indent=4, ensure_ascii=False)
            f.close()

    def _get_icon_from_desktop_file(self, desktop_file_path: str):
        with open(desktop_file_path) as f:
            for line in f.readlines():
                if "Icon=" in line:
                    return "".join(line[5:].split())
            return "application-x-symbolic"

    def _get_desktop_file(self, app_id: str) -> str | None:
        data_dirs = GLib.get_system_data_dirs()
        for data_dir in data_dirs:
            data_dir = data_dir + "/applications/"
            if os.path.exists(data_dir):
                # Do name resolving here

                files = os.listdir(data_dir)
                matching = [
                    s for s in files if "".join(app_id.lower().split()) in s.lower()
                ]
                if matching:
                    return data_dir + matching[0]

                for word in list(filter(None, re.split(r"-|\.|_|\s", app_id))):
                    matching = [s for s in files if word.lower() in s.lower()]
                    if matching:
                        return data_dir + matching[0]

        return None

    def _compositor_find_icon(self, app_id: str):
        if Gtk.IconTheme.get_default().has_icon(app_id):
            return app_id
        if Gtk.IconTheme.get_default().has_icon(app_id + "-desktop"):
            return app_id + "-desktop"
        desktop_file = self._get_desktop_file(app_id)
        return (
            self._get_icon_from_desktop_file(desktop_file)
            if desktop_file
            else "application-x-symbolic"
        )
