import maya.cmds as mc
import Utils


def buildIKLimb(ik_joints, ik_ctrl, pv_ctrl, constrain_last_jnt = True):
    'create ik handle and connect to ik controllers'

    ik_handlename = ik_joints[0] + "h"
    ik_handle = mc.ikHandle(sj=ik_joints[0], ee=ik_joints[2], name=ik_handlename)[0]
    mc.poleVectorConstraint(pv_ctrl, ik_handle)
    if constrain_last_jnt:
        mc.pointConstraint(ik_ctrl, ik_handle, mo=True)
        mc.orientConstraint(ik_ctrl, ik_joints[2], mo=True)


