from fabric import Application
from fabric.utils import get_relative_path

from bar import StatusBar


if __name__ == "__main__":
    # Create the status bar
    bar = StatusBar()
    # Initialize the application with the status bar
    app = Application("bar", bar)
    # Set the stylesheet for the application
    app.set_stylesheet_from_file(get_relative_path("styles/main.css"))

    # Run the application
    app.run()
