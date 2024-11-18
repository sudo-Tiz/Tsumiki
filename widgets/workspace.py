from fabric.hyprland.widgets import (
    WorkspaceButton,
    Workspaces,
)
from fabric.widgets.box import Box


class WorkSpaceBox(Box):
    def __init__(self, ws_count=8, **kwargs):
        super().__init__(name="workspaces-box", **kwargs)

        self.workspace = Workspaces(
            name="workspaces",
            spacing=4,
            buttons=[
                WorkspaceButton(id=i, label=str(i)) for i in range(1, ws_count + 1)
            ],
            buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=str(ws_id)),
        )

        self.children = self.workspace
