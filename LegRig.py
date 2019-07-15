import maya.cmds as mc
import LimbRig


def buildLeg(selected=None, ikfk_attr=None):
    if selected is None:
        selected = mc.ls(sl=True)
    LimbRig.buildLimbs(selected=selected, constrain_last_jnt=False, ikfk_attr=ikfk_attr)

