import json
import os
import re

import gi
from gi.repository import GLib, Gtk
from loguru import logger

from utils.config import APP_CACHE_DIRECTORY

gi.require_version("Gtk", "3.0")

ICON_CACHE_FILE = APP_CACHE_DIRECTORY + "/icons.json"


class IconResolver:
    """A class to resolve icons for applications."""

    def __init__(self):
        if os.path.exists(ICON_CACHE_FILE):
            with open(ICON_CACHE_FILE) as f:
                try:
                    self._icon_dict = json.load(f)
                except json.JSONDecodeError:
                    logger.info("[ICONS] Cache file does not exist or is corrupted")
        else:
            self._icon_dict = {}

    def get_icon(self, app_id: str):
        if app_id in self._icon_dict:
            return self._icon_dict[app_id]
        new_icon = self._compositor_find_icon(app_id)
        logger.info(
            f"[ICONS] found new icon: '{new_icon}' for app id: '{app_id}', storing..."
        )
        self._store_new_icon(app_id, new_icon)
        return new_icon

    def _store_new_icon(self, app_id: str, icon: str):
        self._icon_dict[app_id] = icon
        with open(ICON_CACHE_FILE, "w") as f:
            json.dump(self._icon_dict, f)
            f.close()

    def _get_icon_from_desktop_file(self, desktop_file_path: str):
        # TODO: get icon in the [Desktop Entry] section only
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
