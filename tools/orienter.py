"""Orienter tool: interactively orient Maya joints via a dockable UI.

This module defines OrienterWidget, a dockable PySide6 tool that helps artists
orient selected joints consistently. It supports:
- Aim/Up axis selection with auto-resolving conflicts
- World up direction and optional reverse
- Auto orient secondary axis using Maya's joint command
- Batch orientation on selected joints or across a hierarchy
- Manual local axis tweak and freezing
- Local axis display toggling for selection, hierarchy, or the entire scene
"""

from core.joint import JointHelper, cmds, om
from ui.widgets import CustomPushButton, CustomLabel, CustomSpinBox, CustomDialog, QtWidgets


class OrienterWidget(CustomDialog):
    """Dockable UI for orienting joints and adjusting their local axes."""
    OBJECT_NAME = "Orienter"

    def __init__(self):
        super().__init__()
        self.setObjectName(self.OBJECT_NAME)

        # --- Widget Variables ---
        self.target_selected_rb = None
        self.target_hierarchy_rb = None

        self.aim_x_rb = None
        self.aim_y_rb = None
        self.aim_z_rb = None
        self.aim_btn_grp = None

        self.up_x_rb = None
        self.up_y_rb = None
        self.up_z_rb = None
        self.up_btn_grp = None

        self.world_up_x_btn = None
        self.world_up_y_btn = None
        self.world_up_z_btn = None
        self.world_up_btn_grp = None
        self.world_up_reverse_cb = None

        self.auto_orient_up_axis_cb = None

        self.orient_joint_btn = None
        self.orient_joint_to_world_btn = None

        self.local_axis_tweak_x_label = None
        self.local_axis_tweak_y_label = None
        self.local_axis_tweak_z_label = None
        self.local_axis_tweak_x_sb = None
        self.local_axis_tweak_y_sb = None
        self.local_axis_tweak_z_sb = None

        self.local_axis_tweak_sub_x_btn = None
        self.local_axis_tweak_add_x_btn = None
        self.local_axis_tweak_sub_y_btn = None
        self.local_axis_tweak_add_y_btn = None
        self.local_axis_tweak_sub_z_btn = None
        self.local_axis_tweak_add_z_btn = None

        self.show_selected_local_axis_btn = None
        self.hide_selected_local_axis_btn = None
        self.show_hierarchy_local_axis_btn = None
        self.hide_hierarchy_local_axis_btn = None
        self.show_all_local_axis_btn = None
        self.hide_all_local_axis_btn = None

        self.setup_ui()

    def create_widgets(self):
        """Create all the widgets for the UI."""

        # --- Target Widgets ---
        self.target_hierarchy_rb = QtWidgets.QRadioButton("Hierarchy")
        self.target_hierarchy_rb.setChecked(True)
        self.target_selected_rb = QtWidgets.QRadioButton("Selected")

        # --- Aim Axis Widgets ---
        self.aim_x_rb = QtWidgets.QRadioButton("X")
        self.aim_x_rb.setChecked(True)
        self.aim_y_rb = QtWidgets.QRadioButton("Y")
        self.aim_z_rb = QtWidgets.QRadioButton("Z")

        self.aim_btn_grp = QtWidgets.QButtonGroup()
        self.aim_btn_grp.addButton(self.aim_x_rb)
        self.aim_btn_grp.addButton(self.aim_y_rb)
        self.aim_btn_grp.addButton(self.aim_z_rb)

        # --- Up Axis Widgets ---
        self.up_x_rb = QtWidgets.QRadioButton("X")
        self.up_y_rb = QtWidgets.QRadioButton("Y")
        self.up_y_rb.setChecked(True)
        self.up_z_rb = QtWidgets.QRadioButton("Z")

        self.up_btn_grp = QtWidgets.QButtonGroup()
        self.up_btn_grp.addButton(self.up_x_rb)
        self.up_btn_grp.addButton(self.up_y_rb)
        self.up_btn_grp.addButton(self.up_z_rb)

        # --- Up World Direction Widgets (Styled Push Buttons) ---
        self.world_up_x_btn = QtWidgets.QRadioButton("X")
        self.world_up_y_btn = QtWidgets.QRadioButton("Y")
        self.world_up_y_btn.setChecked(True)
        self.world_up_z_btn = QtWidgets.QRadioButton("Z")
        self.world_up_reverse_cb = QtWidgets.QCheckBox("Reverse")

        self.world_up_btn_grp = QtWidgets.QButtonGroup()
        self.world_up_btn_grp.addButton(self.world_up_x_btn)
        self.world_up_btn_grp.addButton(self.world_up_y_btn)
        self.world_up_btn_grp.addButton(self.world_up_z_btn)

        # --- Auto Orient Up Axis ---
        self.auto_orient_up_axis_cb = QtWidgets.QCheckBox("Auto Orient Up Axis")
        self.auto_orient_up_axis_cb.setChecked(True)
        self.auto_orient_up_axis_cb.setToolTip(
            "Guess the Up Axis based on the average Up Vector of the selected joints.")

        # --- Action Button ---
        self.orient_joint_btn = CustomPushButton("Orient Joints")
        self.orient_joint_to_world_btn = CustomPushButton("Orient Joints to World")

        # --- Local Axis Tweaks ---
        self.local_axis_tweak_x_label = CustomLabel("X", "#FF7474")
        self.local_axis_tweak_y_label = CustomLabel("Y", "#74FF74")
        self.local_axis_tweak_z_label = CustomLabel("Z", "#7474FF")
        self.local_axis_tweak_x_sb = CustomSpinBox()
        self.local_axis_tweak_y_sb = CustomSpinBox()
        self.local_axis_tweak_z_sb = CustomSpinBox()

        self.local_axis_tweak_sub_x_btn = CustomPushButton("-")
        self.local_axis_tweak_add_x_btn = CustomPushButton("+")
        self.local_axis_tweak_sub_y_btn = CustomPushButton("-")
        self.local_axis_tweak_add_y_btn = CustomPushButton("+")
        self.local_axis_tweak_sub_z_btn = CustomPushButton("-")
        self.local_axis_tweak_add_z_btn = CustomPushButton("+")

        # --- Local Axis Visibility ---
        self.show_selected_local_axis_btn = CustomPushButton("Show Selected")
        self.hide_selected_local_axis_btn = CustomPushButton("Hide Selected")
        self.show_hierarchy_local_axis_btn = CustomPushButton("Show Hierarchy")
        self.hide_hierarchy_local_axis_btn = CustomPushButton("Hide Hierarchy")
        self.show_all_local_axis_btn = CustomPushButton("Show All")
        self.hide_all_local_axis_btn = CustomPushButton("Hide All")

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

        up_layout = QtWidgets.QHBoxLayout()
        up_layout.addWidget(self.up_x_rb)
        up_layout.addWidget(self.up_y_rb)
        up_layout.addWidget(self.up_z_rb)
        up_layout.addStretch()

        world_up_layout = QtWidgets.QHBoxLayout()
        world_up_layout.addWidget(self.world_up_x_btn)
        world_up_layout.addWidget(self.world_up_y_btn)
        world_up_layout.addWidget(self.world_up_z_btn)
        world_up_layout.addStretch()
        world_up_layout.addWidget(self.world_up_reverse_cb)

        orientation_layout = QtWidgets.QFormLayout()
        orientation_layout.addRow("Target:", orientation_target_layout)
        orientation_separator = QtWidgets.QFrame()
        orientation_separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        orientation_separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        orientation_layout.addRow(orientation_separator)
        orientation_layout.addRow("Aim Axis:", aim_layout)
        orientation_layout.addRow("Up Axis:", up_layout)
        orientation_layout.addRow("World Up Dir:", world_up_layout)
        orientation_layout.addRow("", self.auto_orient_up_axis_cb)
        orientation_layout.addRow(self.orient_joint_btn)
        orientation_layout.addRow(self.orient_joint_to_world_btn)

        orientation_grp = QtWidgets.QGroupBox("Orientation Settings")
        orientation_grp.setLayout(orientation_layout)

        # --- Local Axis Tweaks ---

        local_axis_tweak_grid_layout = QtWidgets.QGridLayout()
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_x_label, 0, 0)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_y_label, 1, 0)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_z_label, 2, 0)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_x_sb, 0, 1)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_y_sb, 1, 1)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_z_sb, 2, 1)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_sub_x_btn, 0, 2)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_add_x_btn, 0, 3)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_sub_y_btn, 1, 2)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_add_y_btn, 1, 3)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_sub_z_btn, 2, 2)
        local_axis_tweak_grid_layout.addWidget(self.local_axis_tweak_add_z_btn, 2, 3)

        local_axis_tweak_grp = QtWidgets.QGroupBox("Local Axis Tweak")
        local_axis_tweak_grp.setLayout(local_axis_tweak_grid_layout)

        # --- Local Axis Visibility ---
        local_axis_visibility_layout = QtWidgets.QGridLayout()
        local_axis_visibility_layout.addWidget(self.show_selected_local_axis_btn, 0, 0)
        local_axis_visibility_layout.addWidget(self.hide_selected_local_axis_btn, 0, 1)
        local_axis_visibility_layout.addWidget(self.show_hierarchy_local_axis_btn, 1, 0)
        local_axis_visibility_layout.addWidget(self.hide_hierarchy_local_axis_btn, 1, 1)
        local_axis_visibility_layout.addWidget(self.show_all_local_axis_btn, 2, 0)
        local_axis_visibility_layout.addWidget(self.hide_all_local_axis_btn, 2, 1)

        visibility_grp = QtWidgets.QGroupBox("Local Axis Visibility")
        visibility_grp.setLayout(local_axis_visibility_layout)

        # --- Main Vertical Layout ---
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(orientation_grp)
        main_layout.addWidget(local_axis_tweak_grp)
        main_layout.addWidget(visibility_grp)

    def create_connections(self):
        """Connect widget signals to slots."""

        # --- Orientation Settings ---
        self.aim_x_rb.toggled.connect(self.handle_axis_orientation_toggle)
        self.aim_y_rb.toggled.connect(self.handle_axis_orientation_toggle)
        self.aim_z_rb.toggled.connect(self.handle_axis_orientation_toggle)
        self.up_x_rb.toggled.connect(self.handle_axis_orientation_toggle)
        self.up_y_rb.toggled.connect(self.handle_axis_orientation_toggle)
        self.up_z_rb.toggled.connect(self.handle_axis_orientation_toggle)

        self.orient_joint_btn.clicked.connect(lambda: self.orient_joints(reset_to_world=False))
        self.orient_joint_to_world_btn.clicked.connect(lambda: self.orient_joints(reset_to_world=True))

        # --- local axis tweaks ---
        self.local_axis_tweak_add_x_btn.clicked.connect(lambda: self.rotate_local_axis_joint("x", 1))
        self.local_axis_tweak_sub_x_btn.clicked.connect(lambda: self.rotate_local_axis_joint("x", -1))
        self.local_axis_tweak_add_y_btn.clicked.connect(lambda: self.rotate_local_axis_joint("y", 1))
        self.local_axis_tweak_sub_y_btn.clicked.connect(lambda: self.rotate_local_axis_joint("y", -1))
        self.local_axis_tweak_add_z_btn.clicked.connect(lambda: self.rotate_local_axis_joint("z", 1))
        self.local_axis_tweak_sub_z_btn.clicked.connect(lambda: self.rotate_local_axis_joint("z", -1))

        # --- Local Axis Visibility ---
        self.show_selected_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="selected", visible=True))
        self.hide_selected_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="selected", visible=False))

        self.show_hierarchy_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="hierarchy", visible=True))
        self.hide_hierarchy_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="hierarchy", visible=False))

        self.show_all_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="all", visible=True))
        self.hide_all_local_axis_btn.clicked.connect(
            lambda: self.toggle_local_axis_visibility(scope="all", visible=False))

    # ----------------------------------ORIENTATION SETTINGS-------------------------------------------------
    def get_axis_orientation_settings(self):
        """
        Get the axis orientation settings based on the current state of the widgets.
        :return str: The axis orientation settings to be used for joint's orientation.
        """

        aim_up_map = {
            ('X', 'Y'): 'xyz',
            ('X', 'Z'): 'xzy',
            ('Y', 'Z'): 'yzx',
            ('Y', 'X'): 'yxz',
            ('Z', 'X'): 'zxy',
            ('Z', 'Y'): 'zyx'
        }

        aim = self.aim_btn_grp.checkedButton().text()
        up = self.up_btn_grp.checkedButton().text()

        return aim_up_map.get((aim, up), '')

    def get_world_up_settings(self):
        """
        Get the world up settings based on the current state of the widgets.
        :return str: The world up axis direction in either positive or negative value.
        """

        for btn, axis in [(self.world_up_x_btn, 'x'),
                          (self.world_up_y_btn, 'y'),
                          (self.world_up_z_btn, 'z')]:
            if btn.isChecked():
                return axis + ('down' if self.world_up_reverse_cb.isChecked() else 'up')
        return 'none' + ('down' if self.world_up_reverse_cb.isChecked() else 'up')

    def handle_axis_orientation_toggle(self):
        """
        If Aim and Up axes are set to the same value, automatically
        adjust the other axis to prevent an invalid state.
        """
        sender = self.sender()

        self.disconnect_axis_signals()

        axis_cycle = {'X': 'Y', 'Y': 'Z', 'Z': 'X'}

        aim_axis = self.aim_btn_grp.checkedButton().text()
        up_axis = self.up_btn_grp.checkedButton().text()

        if aim_axis == up_axis:
            if sender in self.aim_btn_grp.buttons():
                new_up_axis = axis_cycle[up_axis]
                if new_up_axis == 'X':
                    self.up_x_rb.setChecked(True)
                elif new_up_axis == 'Y':
                    self.up_y_rb.setChecked(True)
                else:
                    self.up_z_rb.setChecked(True)
            else:
                new_aim_axis = axis_cycle[aim_axis]
                if new_aim_axis == 'X':
                    self.aim_x_rb.setChecked(True)
                elif new_aim_axis == 'Y':
                    self.aim_y_rb.setChecked(True)
                else:
                    self.aim_z_rb.setChecked(True)

        self.reconnect_axis_signals()

    def disconnect_axis_signals(self):
        """Disconnects all axis-toggled signals to prevent recursion."""
        for button in self.aim_btn_grp.buttons() + self.up_btn_grp.buttons():
            button.toggled.disconnect(self.handle_axis_orientation_toggle)

    def reconnect_axis_signals(self):
        """Reconnects all axis-toggled signals."""
        for button in self.aim_btn_grp.buttons() + self.up_btn_grp.buttons():
            button.toggled.connect(self.handle_axis_orientation_toggle)

    def orient_joints(self, reset_to_world=False):
        """
        Orients all selected joints based on the selected options.
        """
        cmds.undoInfo(openChunk=True)

        select_children = False
        if self.target_hierarchy_rb.isChecked():
            select_children = True

        auto_orient_enable = False
        orient_tip = False
        if self.auto_orient_up_axis_cb.isChecked():
            auto_orient_enable = True
        else:
            orient_tip = True

        if reset_to_world:
            axis_orientation_settings = 'none'
        else:
            axis_orientation_settings = self.get_axis_orientation_settings()

        selected_joints = JointHelper.get_joints(hierarchy=False)
        if not selected_joints:
            om.MGlobal.displayWarning("Please select one or more joints to orient.")
            cmds.undoInfo(closeChunk=True)
            return
        JointHelper.freeze_joint_orientation(selected_joints)

        try:
            if selected_joints:
                cmds.joint(selected_joints, edit=True,
                           orientJoint=axis_orientation_settings,
                           secondaryAxisOrient=self.get_world_up_settings(),
                           autoOrientSecondaryAxis=auto_orient_enable,
                           children=select_children,
                           zeroScaleOrient=True)
                if orient_tip:
                    joint_list = cmds.ls(selection=True, type='joint')
                    joint_tip = cmds.listRelatives(joint_list, allDescendents=True)[0]
                    cmds.setAttr(f"{joint_tip}.jointOrient", 0, 0, 0)
            else:
                om.MGlobal.displayWarning("Please select a joint.")
                cmds.undoInfo(closeChunk=True)
                return

        except RuntimeError as e:
            om.MGlobal.displayWarning(
                f"Orientation failed: {str(e)}. Select multiple joints or enable 'Auto Orient Up Axis'.")
            cmds.undoInfo(closeChunk=True)
            return
        finally:
            cmds.undoInfo(closeChunk=True)

    # ----------------------------------LOCAL AXIS TWEAKS-------------------------------------------------
    def rotate_local_axis_joint(self, axis, direction):
        """
        Rotates all selected joints around a specified local axis by a value.
        The new rotation is then frozen.

        Args:
            axis (str): The local axis to rotate around ('x', 'y', or 'z').
            direction (int): The direction of rotation (1 for adding, -1 for subtracting).
        """

        if self.target_hierarchy_rb.isChecked():
            selected_joints = JointHelper.get_joints(hierarchy=True)
        else:
            selected_joints = JointHelper.get_joints()

        if not selected_joints:
            om.MGlobal.displayWarning("Please select one or more joints to rotate.")
            return

        cmds.undoInfo(openChunk=True)

        try:
            apply_rotation = (0, 0, 0)
            if axis == "x":
                rotation_value = self.local_axis_tweak_x_sb.value()
                apply_rotation = (rotation_value * direction, 0, 0)
            elif axis == "y":
                rotation_value = self.local_axis_tweak_y_sb.value()
                apply_rotation = (0, rotation_value * direction, 0)
            elif axis == "z":
                rotation_value = self.local_axis_tweak_z_sb.value()
                apply_rotation = (0, 0, rotation_value * direction)

            for joint in selected_joints:
                cmds.xform(joint, relative=True, objectSpace=True, rotateAxis=apply_rotation)
                JointHelper.freeze_joint_orientation(joint)
        finally:
            cmds.undoInfo(closeChunk=True)

    # ----------------------------------JOINTS VISIBILITY-------------------------------------------------
    @staticmethod
    def toggle_local_axis_visibility(scope, visible):
        """
        Shows or hides the local axis of joints based on the specified scope.

        Args:
            scope (str): The scope of joints to affect ("selected", "hierarchy", or "all").
            visible (bool): The visibility state to set (True for show, False for hide).
        """
        cmds.undoInfo(stateWithoutFlush=False)

        joints_to_affect = []

        if scope == "selected":
            joints_to_affect = JointHelper.get_joints()
        elif scope == "hierarchy":
            joints_to_affect = JointHelper.get_joints(hierarchy=True)
        elif scope == "all":
            joints_to_affect = JointHelper.get_joints(all_joints=True)

        if not joints_to_affect:
            om.MGlobal.displayWarning("No joints selected.")
            return

        for joint in joints_to_affect:
            cmds.setAttr(f"{joint}.displayLocalAxis", visible)

        cmds.undoInfo(stateWithoutFlush=True)


if __name__ == "__main__":
    workspace_control_name = f"{OrienterWidget.OBJECT_NAME}WorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name)

    orient_tool = OrienterWidget()
    orient_tool.show(dockable=True)
