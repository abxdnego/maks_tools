from PySide6 import QtWidgets, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as om
import maya.cmds as cmds


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, color="#FFFFFF"):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.set_color(color)

    def set_color(self, color):
        self.setStyleSheet("QLabel { background-color: %s; "
                           "color: #000000; "
                           "border-radius: 2px; "
                           "font-weight: bold;}"
                           % color)

class CustomSpinBox(QtWidgets.QDoubleSpinBox):

    MIN_WIDTH = 40
    DEFAULT_VALUE = 45
    STEP_VALUE = 15
    MINIMUM_VALUE, MAXIMUM_VALUE = -360, 360

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip("Rotation increment in degrees")
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.setValue(self.DEFAULT_VALUE)
        self.setDecimals(2)
        self.setRange(self.MINIMUM_VALUE, self.MAXIMUM_VALUE)
        self.setSingleStep(self.STEP_VALUE)
        self.setMinimumWidth(self.MIN_WIDTH)

class CustomPushButton(QtWidgets.QPushButton):
    BUTTON_HEIGHT = 40

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(self.BUTTON_HEIGHT)

class CustomDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    
    OBJECT_NAME = "CustomDialog"

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = cls()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show(dockable=True)
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
    
    def __init__(self, parent=None):
        super().__init__(parent)

    def create_widgets(self):
        pass

    def create_layout(self):
        pass

    def create_connections(self):
        pass

    def setup_ui(self):
        """Set up the UI elements."""
        self.setWindowTitle(self.OBJECT_NAME)
        self.setMinimumWidth(self.sizeHint().width())
        self.create_widgets()
        self.create_layout()
        self.create_connections()


    def keyPressEvent(self, e):
        pass
