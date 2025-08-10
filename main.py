"""MAKS Tools: a collection of Maya utilities with a dockable UI.

This entry-point module assembles the available tools (Orienter, Colorizer) into
one tabbed window that can be docked inside Autodesk Maya.
"""

from PySide6 import QtWidgets

from ui.widgets import CustomDialog
from tools.orienter import OrienterWidget
from tools.colorizer import ColorizerWidget

import maya.cmds as cmds


class MainToolsWidget(CustomDialog):
    """The main host window for the MAKS tools suite (Orienter + Colorizer)."""

    OBJECT_NAME = "MAKS Tools"

    def __init__(self):
        """Construct the tabbed tools window and initialize child tools."""
        super().__init__()
        self.setObjectName(self.OBJECT_NAME)

        self.orient_tool_widget = None
        self.colorizer_tool_widget = None

        self.tab_widget = None

        self.setup_ui()

    def create_widgets(self):
        """Create tool widgets and the tab container."""
        self.orient_tool_widget = OrienterWidget()
        self.colorizer_tool_widget = ColorizerWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.orient_tool_widget, "Orienter")
        self.tab_widget.addTab(self.colorizer_tool_widget, "Colorizer")

    def create_layout(self):
        """Create the layouts and arrange widgets."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def create_connections(self):
        """Connect widget signals to slots (reserved for future use)."""
        pass

    def on_current_index_changed(self, index):
        """Handle the current tab index change (reserved)."""
        pass


if __name__ == "__main__":
    workspace_control_name = f"{MainToolsWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = MainToolsWidget()
    orient_tool.show(dockable=True)