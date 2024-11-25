from fabric import Application
from fabric.utils import get_relative_path

from bar import StatusBar


if __name__ == "__main__":
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("styles/main.css"))

    app.run()
