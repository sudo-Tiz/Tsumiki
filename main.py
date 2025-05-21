import traceback
from typing import Literal

import setproctitle
from fabric import Application
from fabric.utils import cooldown, exec_shell_command, get_relative_path, monitor_file
from gi.repository import GLib, Gtk
from loguru import logger

import utils.functions as helpers
from modules import StatusBar
from utils import (
    APP_CACHE_DIRECTORY,
    APPLICATION_NAME,
    Colors,
    widget_config,
)

# Manually map log levels to readable names
LOG_LEVEL_NAMES = {
    GLib.LogLevelFlags.LEVEL_ERROR: "ERROR",
    GLib.LogLevelFlags.LEVEL_CRITICAL: "CRITICAL",
    GLib.LogLevelFlags.LEVEL_WARNING: "WARNING",
    GLib.LogLevelFlags.LEVEL_MESSAGE: "MESSAGE",
    GLib.LogLevelFlags.LEVEL_INFO: "INFO",
    GLib.LogLevelFlags.LEVEL_DEBUG: "DEBUG",
}


def log_handler(domain, level, message):
    level_name = LOG_LEVEL_NAMES.get(
        GLib.LogLevelFlags(
            level & ~GLib.LogLevelFlags.FLAG_FATAL & ~GLib.LogLevelFlags.FLAG_RECURSION
        ),
        f"UNKNOWN({level})",
    )
    print(f"\n[{domain or 'Default'}] {level_name}: {message}")
    traceback.print_stack()


# Set log levels
log_levels = (
    GLib.LogLevelFlags.LEVEL_ERROR
    | GLib.LogLevelFlags.LEVEL_CRITICAL
    | GLib.LogLevelFlags.LEVEL_WARNING
    | GLib.LogLevelFlags.LEVEL_MESSAGE
    | GLib.LogLevelFlags.LEVEL_INFO
    | GLib.LogLevelFlags.LEVEL_DEBUG
)

# Common GTK/GLib log domains
domains = [None, "Gtk", "GLib", "GLib-GObject", "Gdk", "Pango"]

for domain in domains:
    GLib.log_set_handler(domain, log_levels, log_handler)


@cooldown(2)
@helpers.run_in_thread
def process_and_apply_css(app: Application):
    helpers.check_executable_exists("sass")
    logger.info(f"{Colors.INFO}[Main] Compiling CSS")
    output = exec_shell_command("sass styles/main.scss dist/main.css --no-source-map")

    if output == "":
        logger.info(f"{Colors.INFO}[Main] CSS applied")
        app.set_stylesheet_from_file(get_relative_path("dist/main.css"))
    else:
        logger.error(f"{Colors.ERROR}[Main]Failed to compile sass!")
        logger.error(f"{Colors.ERROR}[Main] {output}")
        app.set_stylesheet_from_string("")


general_options = widget_config["general"]
module_options = widget_config["modules"]


if not general_options["debug"]:
    for log in [
        "fabric",
        "widgets",
        "utils",
        "utils.config",
        "modules",
        "services",
    ]:
        logger.disable(log)


if __name__ == "__main__":
    helpers.ensure_directory(APP_CACHE_DIRECTORY)

    # Create the status bar
    bar = StatusBar(widget_config)

    windows = [bar]

    if module_options["app_launcher"]["enabled"]:
        from modules import AppLauncher

        app_launcher = AppLauncher(widget_config)
        windows.append(app_launcher)

    if module_options["notification"]["enabled"]:
        from modules import NotificationPopup

        windows.append(NotificationPopup(widget_config))

    if module_options["screen_corners"]["enabled"]:
        from modules import ScreenCorners

        screen_corners = ScreenCorners(widget_config)

        windows.append(screen_corners)

    if module_options["dock"]["enabled"]:
        from modules.dock import Dock

        dock = Dock(widget_config)

        windows.append(dock)

    if module_options["desktop_clock"]["enabled"]:
        from modules import DesktopClock

        desktop_clock = DesktopClock(widget_config)

        windows.append(desktop_clock)

    if module_options["osd"]["enabled"]:
        from modules import OSDContainer

        windows.append(OSDContainer(widget_config))

    @Application.action("toggle")
    def toggle(
        item: Literal["bar", "desktop_clock", "dock", "screen_corners", "app_launcher"],
    ):
        """Toggle the visibility of the specified item."""
        match item:
            case "bar":
                bar.toggle()
            case "desktop_clock":
                desktop_clock.toggle()
            case "dock":
                dock.toggle()
            case "screen_corners":
                screen_corners.toggle()
            case "app_launcher":
                app_launcher.toggle()
            case _:
                logger.error(
                    f"{Colors.ERROR}[Main] Invalid item '{item}' specified for toggle."
                    "Valid options are: bar, desktop_clock, dock, screen_corners, app_launcher."  # noqa: E501
                )

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, windows=windows)

    helpers.copy_theme(widget_config["theme"]["name"])

    # Set custom `-symbolic.svg` icons' dir
    icon_theme = Gtk.IconTheme.get_default()
    icons_dir = get_relative_path("./assets/icons/svg/gtk")
    icon_theme.append_search_path(icons_dir)

    # Monitor styles folder for changes
    if general_options["debug"]:
        main_css_file = monitor_file(get_relative_path("styles"))
        common_css_file = monitor_file(get_relative_path("styles/common"))
        main_css_file.connect("changed", lambda *_: process_and_apply_css(app))
        common_css_file.connect("changed", lambda *_: process_and_apply_css(app))
    else:
        process_and_apply_css(app)

    setproctitle.setproctitle(APPLICATION_NAME)

    # Run the application
    app.run()
