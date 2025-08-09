from ui.widgets import CustomPushButton, CustomLabel, CustomSpinBox, CustomDialog, QtWidgets
from core.logic import ColorHelper, cmds, om

class ColorizerToolWidget(CustomDialog):
    """A tool for colorizing shape nodes in Maya."""
    OBJECT_NAME = "ColorizerToolWidget"

    def __init__(self):
        super().__init__()
        self.setObjectName(self.OBJECT_NAME)

        self.change_color_btn = None

        self.setup_ui("Colorizer Tool")


    def create_widgets(self):
        """Create all the widgets for the UI."""

        self.change_color_btn = CustomPushButton("Change Color")

    def create_layout(self):
        """Create the layouts and arrange widgets."""

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.change_color_btn)

    def create_connections(self):
        """Connect widget signals to slots."""

        self.change_color_btn.clicked.connect(lambda:self.override_color(9))

    def override_color(self, color_index):
        """Override the color of a node."""
        if color_index < 0 or color_index >= 32:
            om.MGlobal.displayError("Color index out of range.")
            return

        shapes = ColorHelper.get_shape_nodes()
        if not shapes:
            om.MGlobal.displayError("No shapes nodes selected.")
            return

        for shape in shapes:
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideColor", color_index)


if __name__ == "__main__":
    workspace_control_name = f"{ColorizerToolWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = ColorizerToolWidget()
    orient_tool.show(dockable=True)

