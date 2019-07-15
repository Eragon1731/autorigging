import maya.cmds as mc
import Utils

CTRL_SCALE = 1

def buildFKChain(fk_joints=None, ctrl_scale=CTRL_SCALE, keyword="fk", createXtra_grp=False):

    if fk_joints is None:
        fk_joints = mc.ls(sl=True)

    grps, names = createControllers(selected=fk_joints, ctrl_scale=ctrl_scale, keyword=keyword, createXtra_grp=createXtra_grp)

    print "names: ",names
    for i in range(1,len(grps)):
        mc.parent(grps[i], names[i-1])


    return names

def createControllers(selected=None, ctrl_scale=CTRL_SCALE, keyword="fk", createXtra_grp=False):

    #get all selected
    if selected is None:
        selected = mc.ls(sl=True)

    print "selected: ", selected

    #check if is a bnd joint
    currlist = [x for x in selected if keyword in x]

    ctrlnames = []
    grpnames = []

    print "currlist: "
    #creating controllers
    for i in range(len(currlist)):
        #get new names
        ctrlname = Utils.changeSuffix(currlist[i], keyword, "ctrl", "_")
        grpname = Utils.changeSuffix(currlist[i], keyword,"grp", "_")
        orientname = Utils.changeSuffix(currlist[i], keyword, "oct", "_")
        
        #joint position
        jnt_pos = mc.xform(currlist[i], q=True, translation=True, ws=True)

        #create and place controller
        ctrl = mc.circle(n=ctrlname, r=ctrl_scale, normal= (1,0,0))[0]
        grp = mc.group(ctrl, n=grpname)

        if createXtra_grp:
            grp = mc.group(grp, name=grpname + "_outerGrp")

        mc.move(jnt_pos[0], jnt_pos[1], jnt_pos[2], grp, a=True)
        ctrl_cvs = mc.ls(ctrlname + ".cv[*]")
        mc.scale(ctrl_scale, ctrl_scale, ctrl_scale, ctrl_cvs)

        #orient constraint
        tempconstraint = mc.orientConstraint(currlist[i], grp, mo=0)
        mc.delete(tempconstraint)
        mc.orientConstraint(ctrl, selected[i], mo=1, name=orientname)

        #get all names
        ctrlnames.append(ctrlname)
        print "ctrlnames: ", ctrlnames
        grpnames.append(grpname)


    return grpnames, ctrlnames
