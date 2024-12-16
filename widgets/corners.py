from fabric.widgets.box import Box
from fabric.widgets.shapes import Corner
from fabric.widgets.wayland import WaylandWindow


class ScreenCorners(WaylandWindow):
    """A widget to display the corners of the screen."""

    def __init__(self):
        super().__init__(
            layer="top",
            anchor="top left bottom right",
            pass_through=True,
            child=Box(
                orientation="vertical",
                children=[
                    Box(
                        children=[
                            self.make_corner("top-left"),
                            Box(h_expand=True),
                            self.make_corner("top-right"),
                        ]
                    ),
                    Box(v_expand=True),
                    Box(
                        children=[
                            self.make_corner("bottom-left"),
                            Box(h_expand=True),
                            self.make_corner("bottom-right"),
                        ]
                    ),
                ],
            ),
        )

    def make_corner(self, orientation) -> Box:
        return Box(
            h_expand=False,
            v_expand=False,
            name="panel-corner",
            children=Corner(
                orientation=orientation,  # type: ignore
                size=15,
            ),
        )
