import maya.cmds as cmds

class JointHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_selected_joints(hierarchy=False, all_joints=False):
        """Get selected joints, optionally including hierarchy or all scene joints.
        :param hierarchy: Whether to include joints in the hierarchy.
        :param all_joints: Whether to include all joints in the scene.
        :return: A list of selected joints.
        """

        if all_joints:
            return cmds.ls(type="joint") or []

        selected_joints = cmds.ls(selection=True, type="joint") or []
        if hierarchy and selected_joints:
            descendants = cmds.listRelatives(selected_joints, allDescendents=True, type="joint") or []
            selected_joints.extend(descendants)

        return selected_joints

    @staticmethod
    def freeze_joint_orientation(joints_to_orient):
        """
        Freezes the joint orientation by zeroing out the joint orient
        and baking the new rotation into the joint.

        :param joints_to_orient: The name of the joint to freeze.
        """
        cmds.joint(joints_to_orient, edit=True, zeroScaleOrient=True)
        cmds.makeIdentity(joints_to_orient, apply=True, translate=False, rotate=True, scale=False, normal=0)


class ColorHelper:

    def __init__(self):
        pass