import maya.cmds as mc
import Utils
import IKChain
import FKChain

CTRL_SCALE = 1

def setupJointChains(selected):
    ik_jnts = setupSingleChain(selected, suffix="ik")
    fk_jnts = setupSingleChain(selected, suffix="fk")

    return ik_jnts, fk_jnts

def setupSingleChain(selected, suffix):
    jntchains = mc.duplicate(selected, renameChildren=True)
    duplicatejnts = []

    for jnt in jntchains:
        newname = Utils.changeSuffix(jntname=jnt, currsuffix="jnt", suffix=suffix, separator="_")
        tempjnt = mc.rename(jnt, newname)
        duplicatejnts.append(tempjnt)

    return duplicatejnts

def buildLimbs(selected = None, constrain_last_jnt = False, ikfk_attr=None):

    'create two extra joints, renames them and build ik and fk structures'

    if not ikfk_attr:
        mc.warning("Please specify ikfk attr")
        return

    if not mc.objExists(ikfk_attr):
        mc.addAttr(ikfk_attr.split("."[0]), longName=ikfk_attr.split(".")[1], attributeType='float', min=0, max=1)
        mc.setAttr(ikfk_attr, k=True)

    if selected is None:
        selected = mc.ls(sl=True)

    if len(selected) != 3:
        mc.warning("Please select exactly 3 objs: the joint, ik controller and a pole vector controller")
        return

    joint = selected[0]
    jnt_childrenjoints = mc.listRelatives(joint, allDescendents=True)
    jnt_childrenjoints.reverse()
    jnt_joints = [joint] + jnt_childrenjoints
    ik_ctrl = selected[1]
    pv_ctrl = selected[2]

    'blend the chains'
    ik_jnts, fk_jnts = setupJointChains(joint)
    fk_ctrls = FKChain.buildFKChain(fk_joints=fk_jnts, ctrl_scale=CTRL_SCALE)
    IKChain.buildIKLimb(ik_joints=ik_jnts[:3], ik_ctrl=ik_ctrl, pv_ctrl=pv_ctrl, constrain_last_jnt=constrain_last_jnt)

    blendJointChains(ik_jnts, fk_jnts, jnt_joints, ikfk_attr)
    connectCtrlsVisibility([ik_ctrl, pv_ctrl], fk_ctrls, ikfk_attr)

def connectCtrlsVisibility(ik_ctrls, fk_ctrls, ikfk_attr):

    for fkc in fk_ctrls:
        mc.connectAttr(ikfk_attr, fkc + ".visibility")

    for ikc in ik_ctrls:
        reverse_node = mc.createNode("reverse")
        mc.connectAttr(ikfk_attr, reverse_node+".inputX")
        mc.connectAttr(reverse_node + ".outputX", ikc + ".visibility")


def blendJointChains(fk_jnts, ik_jnts, jnt_joints, ikfk_attr):

    'Blends ik and fk joints between the jnt joints structure'

    for i in range(len(jnt_joints)):
        blend_colors_node = mc.createNode("blendColors", name= jnt_joints[i][:-3] + "bcn")
        mc.connectAttr(ik_jnts[i] + ".rotate", blend_colors_node + ".color1")
        mc.connectAttr(fk_jnts[i] + ".rotate", blend_colors_node + ".color2")
        mc.connectAttr(blend_colors_node + ".output", jnt_joints[i] + ".rotate")
        mc.connectAttr(ikfk_attr, blend_colors_node + ".blender")
