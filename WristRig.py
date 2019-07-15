import maya.cmds as mc
import FKChain
import re

def getAttrName(jnt):

    print "full name of jnt for attr name: ", jnt
    tempname = jnt.split("_")[-1]
    attrname = re.sub("[0-9]", "", tempname)
    attrname += "_curl"

    print "this is the attr name: ", attrname
    return attrname


def buildWrist(wrist_ctrl=None, wrist_jnt=None, fingeramount=5, rot_ax="Y"):

    """Build the wrist setup for joints and finger controllers"""
    selection = mc.ls(sl=True)

    if not selection and (not wrist_jnt or not wrist_ctrl):
        print "Please select the wrist joint then the wrist controller"
        return
    if not wrist_ctrl:
        wrist_ctrl = selection[1]
    if not wrist_jnt:
        wrist_jnt = selection[0]

    mc.parentConstraint(wrist_jnt, wrist_ctrl, mo=True)

    finger_jnts = mc.listRelatives(wrist_jnt, allDescendents=True)
    numfinger_jnts = len(finger_jnts)/fingeramount

    print "fingeramount: ", fingeramount
    for i in range(fingeramount):

        singlefinger_jnts = finger_jnts[(numfinger_jnts * i): numfinger_jnts * (i+1)]
        singlefinger_jnts.reverse()
        singlefinger_jnts.pop()
        attrname = getAttrName(singlefinger_jnts[0])
        mc.addAttr(wrist_ctrl, longName=attrname, attributeType="float", keyable=True)

        print "singlefinger_jnts ", singlefinger_jnts

        fk_ctrls = FKChain.buildFKChain(fk_joints=singlefinger_jnts, ctrl_scale=0.5, keyword="jnt", createXtra_grp=True)

        print "FK Controllers: ", fk_ctrls

        outergrp = ""

        for j, fk in enumerate(fk_ctrls):
            ctrlgrp = mc.listRelatives(fk, parent=True)[0]

            if j == 0:
                temp = mc.listRelatives(ctrlgrp, parent=True)[0]
                outergrp = temp
            mc.connectAttr("%s.%s"%(wrist_ctrl, attrname), "%s.rotate%s"%(ctrlgrp, rot_ax))

        print "outer grp", outergrp
        print "wrist_ctrl", wrist_ctrl

        mc.parent(outergrp, wrist_ctrl)


# connect the wrist to the ik and fk joints
def connectWrist (fk_joint, ik_joint, wrist_joint, ikfk_attr):
    wristconstraint = mc.parentConstraint(ik_joint, fk_joint, wrist_joint, mo=True)
    mc.connectAttr(ikfk_attr, wristconstraint + "."+ik_joint+"WO")
    reversenode = mc.createNode("reverse")
    mc.connectAttr(ikfk_attr, reversenode, ".inputX")
    mc.connectAttr(reversenode + ".outputX", wristconstraint + "." + fk_joint + "W1")
