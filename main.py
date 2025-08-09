from PySide6 import QtWidgets

from ui.widgets import CustomDialog
from core.logic import cmds
from tools.orient_tool import OrientToolWidget
from tools.colorizer_tool import ColorizerToolWidget

class MAKS_ToolsWidget(CustomDialog):
    """A tool for colorizing shape nodes in Maya."""
    OBJECT_NAME = "MAKS_ToolsWidget"

    def __init__(self):
        super().__init__()
        self.setObjectName(self.OBJECT_NAME)
        self.orient_tool_widget = None
        self.colorizer_tool_widget = None


        self.setup_ui("MAKS Tools")

    def create_widgets(self):
        """Create all the widgets for the UI."""
        self.orient_tool_widget = OrientToolWidget()
        self.colorizer_tool_widget = ColorizerToolWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.orient_tool_widget, "Orient Tool")
        self.tab_widget.addTab(self.colorizer_tool_widget, "Colorizer Tool")


    def create_layout(self):
        """Create the layouts and arrange widgets."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def create_connections(self):
        """Connect widget signals to slots."""
        self.tab_widget.currentChanged.connect(self.on_current_index_changed)

    def on_current_index_changed(self, index):
        """Handle the current tab index change."""
        if index == 0:
            self.orient_tool_widget.setup_ui()
        elif index == 1:
            self.colorizer_tool_widget.setup_ui()


if __name__ == "__main__":
    workspace_control_name = f"{MAKS_ToolsWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = MAKS_ToolsWidget()
    orient_tool.show(dockable=True)