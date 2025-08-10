"""Colorizer tool: quickly set Maya shape override colors from a palette.

This module provides a dockable UI that lets you pick among Maya's 32 index
colors and apply them to the currently selected shapes. It also allows restoring
Maya defaults and resetting all meshes in the scene.
"""

from ui.widgets import CustomPushButton, CustomDialog, QtWidgets
from core.color import ColorHelper, cmds, om


class ColorizerWidget(CustomDialog):
    """Dockable UI for applying legacy index colors to selected shapes."""

    OBJECT_NAME = "Colorizer"

    def __init__(self, parent=None):
        """Construct the UI and set up an internal state."""
        super().__init__(parent)
        self.setObjectName(self.OBJECT_NAME)

        self.selected_index = -1
        self.color_buttons = []
        self.base_styles = []

        self.palette_widget = None
        self.grid_layout = None
        self.override_button = None
        self.default_button = None
        self.reset_all_button = None

        self.setup_ui()

    def create_widgets(self):
        """Create the palette grid and action buttons."""
        self.palette_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.palette_widget)
        self.grid_layout.setSpacing(2)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        columns = ColorHelper.MAX_OVERRIDE_COLORS // 4  # 16 columns, 2 rows
        color_swatch_size = 30

        for index in range(ColorHelper.MAX_OVERRIDE_COLORS):
            button = QtWidgets.QPushButton(self.palette_widget)
            button.setFlat(True)
            button.setFixedSize(color_swatch_size, color_swatch_size)

            if index == 0:
                color = [0.6, 0.6, 0.6]
            else:
                color = cmds.colorIndex(index, query=True)

            r = int(color[0] * 255)
            g = int(color[1] * 255)
            b = int(color[2] * 255)

            base_style = f"background-color: rgb({r}, {g}, {b}); border: none;"
            button.setStyleSheet(base_style)
            self.base_styles.append(base_style)

            button.clicked.connect(lambda checked=False, i=index: self.select_color(i))

            row = index // columns
            col = index % columns
            self.grid_layout.addWidget(button, row, col)

            self.color_buttons.append(button)

        self.override_button = CustomPushButton("Colorize")
        self.default_button = CustomPushButton("Set to Default")
        self.reset_all_button = CustomPushButton("Reset All")

    def create_layout(self):
        """Lay out the palette and action buttons."""

        shape_colorizer_action_btn_layout = QtWidgets.QHBoxLayout()
        shape_colorizer_action_btn_layout.addWidget(self.override_button)
        shape_colorizer_action_btn_layout.addWidget(self.default_button)

        shape_colorizer_layout = QtWidgets.QVBoxLayout()
        shape_colorizer_layout.addWidget(self.palette_widget)
        shape_colorizer_layout.addLayout(shape_colorizer_action_btn_layout)
        shape_colorizer_layout.addWidget(self.reset_all_button)

        shape_colorizer_grp = QtWidgets.QGroupBox("Shape Colorizer")
        shape_colorizer_grp.setLayout(shape_colorizer_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(shape_colorizer_grp)

        self.adjustSize()
        self.setFixedSize(self.size())

    def create_connections(self):
        """Connect button clicks to actions."""
        self.override_button.clicked.connect(self.override)
        self.default_button.clicked.connect(self.use_defaults)
        self.reset_all_button.clicked.connect(self.reset_all_colors)

    def select_color(self, index):
        """Set the currently selected color index and update button highlight."""
        self.selected_index = index
        # Highlight the selected button
        for i, btn in enumerate(self.color_buttons):
            if i == index:
                selected_style = self.base_styles[i].replace("border: none;", "border: 2px solid white;")
                btn.setStyleSheet(selected_style)
            else:
                btn.setStyleSheet(self.base_styles[i])

    def override(self):
        cmds.undoInfo(openChunk=True)
        """Apply the selected color index to currently selected shapes."""
        if self.selected_index != -1:
            ColorHelper.override_color(self.selected_index)
        cmds.undoInfo(closeChunk=True)

    def keyPressEvent(self, e):
        """Reserved for keyboard shortcut overrides (optional)."""
        pass

    @staticmethod
    def reset_all_colors():
        """Reset all mesh shapes in the scene to default override color state."""
        cmds.undoInfo(openChunk=True)
        shapes = cmds.ls(type="mesh")
        for shape in shapes:
            cmds.setAttr(f"{shape}.overrideEnabled", False)
            cmds.setAttr(f"{shape}.overrideRGBColors", False)
            cmds.setAttr(f"{shape}.overrideColorRGB", 0.0, 0.0, 0.0)
        cmds.undoInfo(closeChunk=True)

    @staticmethod
    def use_defaults():
        """Disable draw overrides on selected shapes, restoring Maya defaults.

        Returns:
            bool | None: False if nothing to operate on, otherwise None.
        """
        shapes = ColorHelper.get_shape_nodes()
        if not shapes:
            om.MGlobal.displayWarning("No shapes nodes selected")
            return False

        for shape in shapes:
            try:
                cmds.setAttr(f"{shape}.overrideEnabled", False)
            except RuntimeError:
                om.MGlobal.displayWarning(f"Failed to restore defaults: {shape}")
        return None

if __name__ == "__main__":
    workspace_control_name = f"{ColorizerWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = ColorizerWidget()
    orient_tool.show(dockable=True)