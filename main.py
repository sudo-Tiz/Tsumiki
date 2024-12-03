import setproctitle
from fabric import Application
from fabric.utils import exec_shell_command, get_relative_path, monitor_file
from loguru import logger

from modules.bar import StatusBar
from modules.notifications import NotificationPopup
from modules.osd import OSDContainer


def compile_apply_style(app: Application):
    logger.info("[Main] Compiling CSS")
    exec_shell_command("sass styles/main.scss dist/main.css")
    logger.info("[Main] CSS applied")
    app.set_stylesheet_from_file(get_relative_path("dist/main.css"))


APPLICATION_NAME = "fabricpanel"

if __name__ == "__main__":
    # Create the status bar
    bar = StatusBar()
    notifications = NotificationPopup()
    system_overlay = OSDContainer()

    # Initialize the application with the status bar
    app = Application(APPLICATION_NAME, bar, notifications, system_overlay)

    setproctitle.setproctitle(APPLICATION_NAME)

    # Monitor styles folder for changes
    main_css_file = monitor_file(get_relative_path("styles"))
    main_css_file.connect("changed", lambda *_: compile_apply_style(app))

    compile_apply_style(app)

    # Run the application
    app.run()
