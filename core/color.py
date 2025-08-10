import maya.cmds as cmds
import maya.OpenMaya as om

class ColorHelper:

    MAX_OVERRIDE_COLORS = 32

    @classmethod
    def get_shape_nodes(cls):
        selection = cmds.ls(selection=True)
        if not selection:
            return None

        shapes = []
        for node in selection:
            shapes.extend(cmds.listRelatives(node, shapes=True))

        return shapes

    @classmethod
    def override_color(cls, color_index):
        """
        Enables drawing overrides on the selected nodes and
        sets the override color
        """
        if color_index >= cls.MAX_OVERRIDE_COLORS or color_index < 0:
            om.MGlobal.displayError("Color index out-of-range (must be between 0-31)")
            return False

        shapes = cls.get_shape_nodes()
        if not shapes:
            om.MGlobal.displayError("No shape nodes selected")
            return False

        for shape in shapes:
            try:
                cmds.setAttr(f"{shape}.overrideEnabled", True)
                cmds.setAttr(f"{shape}.overrideColor", color_index)
            except RuntimeError:
                om.MGlobal.displayWarning("Failed to override color: {0}".format(shape))
        return None

    @classmethod
    def use_defaults(cls):
        """
        Disables drawing overrides on the selected nodes
        """
        shapes = cls.get_shape_nodes()
        if not shapes:
            om.MGlobal.displayWarning("No shapes nodes selected")
            return False

        for shape in shapes:
            try:
                cmds.setAttr(f"{shape}.overrideEnabled", False)
            except RuntimeError:
                om.MGlobal.displayWarning(f"Failed to restore defaults: {shape}")
        return None


