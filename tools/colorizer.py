from ui.widgets import CustomPushButton, CustomDialog, QtWidgets
from core.color import ColorHelper, cmds

class ColorizerWidget(CustomDialog):
    OBJECT_NAME = "Colorizer"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(self.OBJECT_NAME)

        self.selected_index = -1
        self.color_buttons = []
        self.base_styles = []

        self.palette_widget = None
        self.grid_layout = None
        self.override_button = None
        self.default_button = None

        self.setup_ui()

    def create_widgets(self):
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

        self.override_button = CustomPushButton("Override")
        self.default_button = CustomPushButton("Default")

    def create_layout(self):

        shape_colorizer_action_btn_layout = QtWidgets.QHBoxLayout()
        shape_colorizer_action_btn_layout.addWidget(self.override_button)
        shape_colorizer_action_btn_layout.addWidget(self.default_button)

        shape_colorizer_layout = QtWidgets.QVBoxLayout()
        shape_colorizer_layout.addWidget(self.palette_widget)
        shape_colorizer_layout.addLayout(shape_colorizer_action_btn_layout)

        shape_colorizer_grp = QtWidgets.QGroupBox("Shape Colorizer")
        shape_colorizer_grp.setLayout(shape_colorizer_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(shape_colorizer_grp)

        self.adjustSize()
        self.setFixedSize(self.size())


    def create_connections(self):
        self.override_button.clicked.connect(self.override)
        self.default_button.clicked.connect(self.use_default)

    def select_color(self, index):
        self.selected_index = index
        # Highlight the selected button
        for i, btn in enumerate(self.color_buttons):
            if i == index:
                selected_style = self.base_styles[i].replace("border: none;", "border: 2px solid white;")
                btn.setStyleSheet(selected_style)
            else:
                btn.setStyleSheet(self.base_styles[i])

    def override(self):
        if self.selected_index != -1:
            ColorHelper.override_color(self.selected_index)

    @staticmethod
    def use_default():
        ColorHelper.use_defaults()

    def keyPressEvent(self, e):
        pass


if __name__ == "__main__":
    workspace_control_name = f"{ColorizerWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = ColorizerWidget()
    orient_tool.show(dockable=True)