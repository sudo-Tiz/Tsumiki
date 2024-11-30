from fabric import Application
from fabric.utils import get_relative_path, monitor_file

from loguru import logger

from modules.bar import StatusBar
from modules.notifications import NotificationsPopup
from modules.osd import OSDContainer

def apply_style(app: Application):
    logger.info("[Main] CSS applied")
    app.set_stylesheet_from_file(get_relative_path("styles/main.css"))


if __name__ == "__main__":
    # Create the status bar
    bar = StatusBar()
    notifications = NotificationsPopup()
    system_overlay = OSDContainer()


    # Initialize the application with the status bar
    app = Application("fabric-bar", bar, notifications)

    # Monitor main.css file for changes
    main_css_file = monitor_file(get_relative_path("styles"))
    main_css_file.connect("changed", lambda *args: apply_style(app))

    apply_style(app)

    # Run the application
    app.run()
