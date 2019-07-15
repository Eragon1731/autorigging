import maya.cmds as mc
import auto_rig.Utils

bnd_jnts = mc.ls("*bnd*")

for i in range(len(bnd_jnts)):
    bnd_jnt = bnd_jnts[i]
    jnt_jnt = auto_rig.Utils.changeSuffix(jntname=bnd_jnt, currsuffix="bnd", suffix="jnt", separator="_")
    
    if mc.objExists(jnt_jnt):
        mc.pointConstraint(jnt_jnt, bnd_jnt, mo=True)
        mc.orientConstraint(jnt_jnt, bnd_jnt, mo=True)
    else:
        print "skipping ", jnt_jnt
        
       