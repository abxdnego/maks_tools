from PySide6 import QtCore, QtWidgets
from shiboken6 import wrapInstance
import sys
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds

def maya_main_window():
    """Returns the Maya main window as a QMainWindow instance."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


class OrientTool(QtWidgets.QDialog):
    """A tool for orienting joints with additional utility features in Maya."""
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)

        self.setWindowTitle("MAKS Orient Tool")
        self.setFixedSize(300, 600)
        self.mac_window()

        # --- Member Variables ---
        self.target_selected_rb = None
        self.target_hierarchy_rb = None

        self.aim_x_rb = None
        self.aim_y_rb = None
        self.aim_z_rb = None
        self.aim_btn_grp = None
        self.aim_reverse_cb = None

        self.up_x_rb = None
        self.up_y_rb = None
        self.up_z_rb = None
        self.up_btn_grp = None
        self.up_reverse_cb = None

        self.up_dir_x_btn = None
        self.up_dir_y_btn = None
        self.up_dir_z_btn = None
        self.up_dir_btn_grp = None
        self.up_dir_reverse_cb = None

        self.orient_btn = None

        self.manual_tweak_x_sb = None
        self.manual_tweak_y_sb = None
        self.manual_tweak_z_sb = None

        self.manual_tweak_sub_x_btn = None
        self.manual_tweak_add_x_btn = None
        self.manual_tweak_sub_y_btn = None
        self.manual_tweak_add_y_btn = None
        self.manual_tweak_sub_z_btn = None
        self.manual_tweak_add_z_btn = None

        self.show_selected_local_axis_btn = None
        self.hide_selected_local_axis_btn = None
        self.show_hierarchy_local_axis_btn = None
        self.hide_hierarchy_local_axis_btn = None
        self.show_all_local_axis_btn = None
        self.hide_all_local_axis_btn = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all the widgets for the UI."""
        button_height = 40

        # --- Target Widgets ---
        self.target_hierarchy_rb = QtWidgets.QRadioButton("Hierarchy")
        self.target_hierarchy_rb.setChecked(True)
        self.target_selected_rb = QtWidgets.QRadioButton("Selected")

        # --- Aim Axis Widgets ---
        self.aim_x_rb = QtWidgets.QRadioButton("X")
        self.aim_x_rb.setChecked(True)
        self.aim_y_rb = QtWidgets.QRadioButton("Y")
        self.aim_z_rb = QtWidgets.QRadioButton("Z")
        self.aim_reverse_cb = QtWidgets.QCheckBox("Reverse")

        self.aim_btn_grp = QtWidgets.QButtonGroup()
        self.aim_btn_grp.addButton(self.aim_x_rb)
        self.aim_btn_grp.addButton(self.aim_y_rb)
        self.aim_btn_grp.addButton(self.aim_z_rb)

        # --- Up Axis Widgets ---
        self.up_x_rb = QtWidgets.QRadioButton("X")
        self.up_y_rb = QtWidgets.QRadioButton("Y")
        self.up_y_rb.setChecked(True)
        self.up_z_rb = QtWidgets.QRadioButton("Z")
        self.up_reverse_cb = QtWidgets.QCheckBox("Reverse")

        self.up_btn_grp = QtWidgets.QButtonGroup()
        self.up_btn_grp.addButton(self.up_x_rb)
        self.up_btn_grp.addButton(self.up_y_rb)
        self.up_btn_grp.addButton(self.up_z_rb)

        # --- Up World Direction Widgets (Styled Push Buttons) ---
        self.up_dir_x_btn = QtWidgets.QRadioButton("X")
        self.up_dir_y_btn = QtWidgets.QRadioButton("Y")
        self.up_dir_y_btn.setChecked(True)
        self.up_dir_z_btn = QtWidgets.QRadioButton("Z")
        self.up_dir_reverse_cb = QtWidgets.QCheckBox("Reverse")

        self.up_dir_btn_grp = QtWidgets.QButtonGroup()
        self.up_dir_btn_grp.addButton(self.up_dir_x_btn)
        self.up_dir_btn_grp.addButton(self.up_dir_y_btn)
        self.up_dir_btn_grp.addButton(self.up_dir_z_btn)

        # --- Auto Orient Up Axis ---
        self.auto_orient_up_axis_cb = QtWidgets.QCheckBox("Auto Orient Up Axis")
        self.auto_orient_up_axis_cb.setChecked(True)
        self.auto_orient_up_axis_cb.setToolTip("Guess the Up Axis based on the average Up Vector of the selected joints.")

        # --- Action Button ---
        self.orient_btn = QtWidgets.QPushButton("Orient Joints")
        self.orient_btn.setFixedHeight(button_height)

        # --- Manual Tweaks ---
        fixed_width = 55
        default_value = 45
        step_value = 15
        minimal_value, maximum_value = -360, 360
        self.manual_tweak_x_sb = QtWidgets.QDoubleSpinBox()
        self.manual_tweak_x_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.manual_tweak_x_sb.setValue(default_value)
        self.manual_tweak_x_sb.setRange(minimal_value, maximum_value)
        self.manual_tweak_x_sb.setSingleStep(step_value)
        self.manual_tweak_x_sb.setFixedWidth(fixed_width)
        self.manual_tweak_y_sb = QtWidgets.QDoubleSpinBox()
        self.manual_tweak_y_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.manual_tweak_y_sb.setValue(default_value)
        self.manual_tweak_y_sb.setRange(minimal_value, maximum_value)
        self.manual_tweak_y_sb.setSingleStep(step_value)
        self.manual_tweak_y_sb.setFixedWidth(fixed_width)
        self.manual_tweak_z_sb = QtWidgets.QDoubleSpinBox()
        self.manual_tweak_z_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.manual_tweak_z_sb.setValue(default_value)
        self.manual_tweak_z_sb.setRange(minimal_value, maximum_value)
        self.manual_tweak_z_sb.setSingleStep(step_value)
        self.manual_tweak_z_sb.setFixedWidth(fixed_width)

        self.manual_tweak_sub_x_btn = QtWidgets.QPushButton("-")
        self.manual_tweak_sub_x_btn.setFixedHeight(button_height)
        self.manual_tweak_add_x_btn = QtWidgets.QPushButton("+")
        self.manual_tweak_add_x_btn.setFixedHeight(button_height)
        self.manual_tweak_sub_y_btn = QtWidgets.QPushButton("-")
        self.manual_tweak_sub_y_btn.setFixedHeight(button_height)
        self.manual_tweak_add_y_btn = QtWidgets.QPushButton("+")
        self.manual_tweak_add_y_btn.setFixedHeight(button_height)
        self.manual_tweak_sub_z_btn = QtWidgets.QPushButton("-")
        self.manual_tweak_sub_z_btn.setFixedHeight(button_height)
        self.manual_tweak_add_z_btn = QtWidgets.QPushButton("+")
        self.manual_tweak_add_z_btn.setFixedHeight(button_height)

        # --- Local Axis Visibility ---
        self.show_selected_local_axis_btn = QtWidgets.QPushButton("Show Selected")
        self.show_selected_local_axis_btn.setFixedHeight(button_height)
        self.hide_selected_local_axis_btn = QtWidgets.QPushButton("Hide Selected")
        self.hide_selected_local_axis_btn.setFixedHeight(button_height)
        self.show_hierarchy_local_axis_btn = QtWidgets.QPushButton("Show Hierarchy")
        self.show_hierarchy_local_axis_btn.setFixedHeight(button_height)
        self.hide_hierarchy_local_axis_btn = QtWidgets.QPushButton("Hide Hierarchy")
        self.hide_hierarchy_local_axis_btn.setFixedHeight(button_height)
        self.show_all_local_axis_btn = QtWidgets.QPushButton("Show All")
        self.show_all_local_axis_btn.setFixedHeight(button_height)
        self.hide_all_local_axis_btn = QtWidgets.QPushButton("Hide All")
        self.hide_all_local_axis_btn.setFixedHeight(button_height)

    def create_layout(self):
        """Create the layouts and arrange widgets."""

        # --- Orientation Settings ---
        orientation_target_layout = QtWidgets.QHBoxLayout()
        orientation_target_layout.addWidget(self.target_hierarchy_rb)
        orientation_target_layout.addWidget(self.target_selected_rb)

        aim_layout = QtWidgets.QHBoxLayout()
        aim_layout.addWidget(self.aim_x_rb)
        aim_layout.addWidget(self.aim_y_rb)
        aim_layout.addWidget(self.aim_z_rb)
        aim_layout.addStretch()
        aim_layout.addWidget(self.aim_reverse_cb)

        up_layout = QtWidgets.QHBoxLayout()
        up_layout.addWidget(self.up_x_rb)
        up_layout.addWidget(self.up_y_rb)
        up_layout.addWidget(self.up_z_rb)
        up_layout.addStretch()
        up_layout.addWidget(self.up_reverse_cb)

        up_dir_layout = QtWidgets.QHBoxLayout()
        up_dir_layout.addWidget(self.up_dir_x_btn)
        up_dir_layout.addWidget(self.up_dir_y_btn)
        up_dir_layout.addWidget(self.up_dir_z_btn)
        up_dir_layout.addStretch()
        up_dir_layout.addWidget(self.up_dir_reverse_cb)

        orientation_layout = QtWidgets.QFormLayout()
        orientation_layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        orientation_layout.addRow("Target:", orientation_target_layout)
        orientation_separator = QtWidgets.QFrame()
        orientation_separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        orientation_separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        orientation_layout.addRow(orientation_separator)
        orientation_layout.addRow("Aim Axis:", aim_layout)
        orientation_layout.addRow("Up Axis:", up_layout)
        orientation_layout.addRow("Up World Dir:", up_dir_layout)
        orientation_layout.addRow("", self.auto_orient_up_axis_cb)

        orientation_grp = QtWidgets.QGroupBox("Orientation Settings")
        orientation_grp.setLayout(orientation_layout)

        # --- Manual Tweaks ---
        manual_tweak_x_layout = QtWidgets.QHBoxLayout()
        manual_tweak_x_layout.addWidget(QtWidgets.QLabel("X"))
        manual_tweak_x_layout.addWidget(self.manual_tweak_x_sb)
        manual_tweak_x_layout.addWidget(self.manual_tweak_sub_x_btn)
        manual_tweak_x_layout.addWidget(self.manual_tweak_add_x_btn)

        manual_tweak_y_layout = QtWidgets.QHBoxLayout()
        manual_tweak_y_layout.addWidget(QtWidgets.QLabel("Y"))
        manual_tweak_y_layout.addWidget(self.manual_tweak_y_sb)
        manual_tweak_y_layout.addWidget(self.manual_tweak_sub_y_btn)
        manual_tweak_y_layout.addWidget(self.manual_tweak_add_y_btn)

        manual_tweak_z_layout = QtWidgets.QHBoxLayout()
        manual_tweak_z_layout.addWidget(QtWidgets.QLabel("Z"))
        manual_tweak_z_layout.addWidget(self.manual_tweak_z_sb)
        manual_tweak_z_layout.addWidget(self.manual_tweak_sub_z_btn)
        manual_tweak_z_layout.addWidget(self.manual_tweak_add_z_btn)

        manual_tweak_vbox_layout = QtWidgets.QVBoxLayout()
        manual_tweak_vbox_layout.addLayout(manual_tweak_x_layout)
        manual_tweak_vbox_layout.addLayout(manual_tweak_y_layout)
        manual_tweak_vbox_layout.addLayout(manual_tweak_z_layout)

        manual_tweak_grp = QtWidgets.QGroupBox("Manual Tweak")
        manual_tweak_grp.setLayout(manual_tweak_vbox_layout)

        # --- Local Axis Visibility ---
        show_selected_layout = QtWidgets.QHBoxLayout()
        show_selected_layout.addWidget(self.show_selected_local_axis_btn)
        show_selected_layout.addWidget(self.hide_selected_local_axis_btn)

        show_hierarchy_layout = QtWidgets.QHBoxLayout()
        show_hierarchy_layout.addWidget(self.show_hierarchy_local_axis_btn)
        show_hierarchy_layout.addWidget(self.hide_hierarchy_local_axis_btn)

        show_all_layout = QtWidgets.QHBoxLayout()
        show_all_layout.addWidget(self.show_all_local_axis_btn)
        show_all_layout.addWidget(self.hide_all_local_axis_btn)

        local_axis_visibility_layout = QtWidgets.QVBoxLayout()
        local_axis_visibility_layout.addLayout(show_selected_layout)
        local_axis_visibility_layout.addLayout(show_hierarchy_layout)
        local_axis_visibility_layout.addLayout(show_all_layout)

        visibility_grp = QtWidgets.QGroupBox("Local Axis Visibility")
        visibility_grp.setLayout(local_axis_visibility_layout)

        # --- Main Vertical Layout ---
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(orientation_grp)
        main_layout.addWidget(self.orient_btn)
        main_layout.addWidget(manual_tweak_grp)
        main_layout.addWidget(visibility_grp)

    def create_connections(self):
        """Connect widget signals to slots."""
        self.aim_x_rb.toggled.connect(self.handle_axis_toggle)
        self.aim_y_rb.toggled.connect(self.handle_axis_toggle)
        self.aim_z_rb.toggled.connect(self.handle_axis_toggle)
        self.up_x_rb.toggled.connect(self.handle_axis_toggle)
        self.up_y_rb.toggled.connect(self.handle_axis_toggle)
        self.up_z_rb.toggled.connect(self.handle_axis_toggle)


        # --- Local Axis Visibility ---
        self.show_selected_local_axis_btn.clicked.connect(self.show_selected_local_axis)
        self.hide_selected_local_axis_btn.clicked.connect(self.hide_selected_local_axis)
        self.show_hierarchy_local_axis_btn.clicked.connect(self.show_hierarchy_local_axis)
        self.hide_hierarchy_local_axis_btn.clicked.connect(self.hide_hierarchy_local_axis)
        self.show_all_local_axis_btn.clicked.connect(self.show_all_local_axis)
        self.hide_all_local_axis_btn.clicked.connect(self.hide_all_local_axis)

    def handle_axis_toggle(self):
        """
        If Aim and Up axes are set to the same value, automatically
        adjust the other axis to prevent an invalid state.
        """
        sender = self.sender()
        if not sender or not sender.isChecked():
            return

        # Disconnect signals to prevent infinite recursion
        self.disconnect_axis_signals()

        axis_cycle = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}

        # Get the currently checked axis for both groups
        aim_axis = self.aim_btn_grp.checkedButton().text()
        up_axis = self.up_btn_grp.checkedButton().text()

        # If they match, we fix whichever group didn't trigger the change
        if aim_axis == up_axis:
            # If the sender is from the Aim group, cycle the Up axis
            if sender in self.aim_btn_grp.buttons():
                new_up_axis = axis_cycle[up_axis]
                if new_up_axis == 'X': self.up_x_rb.setChecked(True)
                elif new_up_axis == 'Y': self.up_y_rb.setChecked(True)
                else: self.up_z_rb.setChecked(True)
            # Otherwise, the sender is from the Up group, so cycle the Aim axis
            else:
                new_aim_axis = axis_cycle[aim_axis]
                if new_aim_axis == 'X': self.aim_x_rb.setChecked(True)
                elif new_aim_axis == 'Y': self.aim_y_rb.setChecked(True)
                else: self.aim_z_rb.setChecked(True)

        # Reconnect signals
        self.reconnect_axis_signals()

    def disconnect_axis_signals(self):
        """Disconnects all axis-toggled signals to prevent recursion."""
        for button in self.aim_btn_grp.buttons() + self.up_btn_grp.buttons():
            button.toggled.disconnect(self.handle_axis_toggle)

    def reconnect_axis_signals(self):
        """Reconnects all axis-toggled signals."""
        for button in self.aim_btn_grp.buttons() + self.up_btn_grp.buttons():
            button.toggled.connect(self.handle_axis_toggle)

    def mac_window(self):
        """Apply macOS-specific window flags."""
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.WindowType.Tool, True)



    # ----------------------------------LOGIC-------------------------------------------------
    @staticmethod
    def get_selected_joints(hierarchy=False, all_joints=False):
        """Get selected joints, optionally including hierarchy or all scene joints."""
        if all_joints:
            return cmds.ls(type="joint") or []

        selected_joints = cmds.ls(selection=True, type="joint") or []
        if hierarchy and selected_joints:
            descendants = cmds.listRelatives(selected_joints, allDescendents=True, type="joint") or []
            selected_joints.extend(descendants)

        return selected_joints


    # ----------------------------------ACTIONS-------------------------------------------------
    def show_selected_local_axis(self):
        """Show the local axis of the selected joints."""
        selected_joints = self.get_selected_joints()
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", True)

    def hide_selected_local_axis(self):
        """Hide the local axis of the selected joints."""
        selected_joints = self.get_selected_joints()
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", False)

    def show_hierarchy_local_axis(self):
        """Show the local axis of all joints in the hierarchy of the selected joints."""
        selected_joints = self.get_selected_joints(hierarchy=True)
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", True)

    def hide_hierarchy_local_axis(self):
        """Hide the local axis of all joints in the hierarchy of the selected joints."""
        selected_joints = self.get_selected_joints(hierarchy=True)
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", False)

    def show_all_local_axis(self):
        """Show the local axis of all joints in the current scene."""
        selected_joints = self.get_selected_joints(all_joints=True)
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", True)

    def hide_all_local_axis(self):
        """Hide the local axis of all joints in the current scene."""
        selected_joints = self.get_selected_joints(all_joints=True)
        for joint in selected_joints:
            cmds.setAttr(f"{joint}.displayLocalAxis", False)


if __name__ == "__main__":
    global orient_tool
    try:
        if "orient_tool" in globals():
            orient_tool.close()
            orient_tool.deleteLater()
    except (RuntimeError, NameError):
        pass

    orient_tool = OrientTool()
    orient_tool.show()
