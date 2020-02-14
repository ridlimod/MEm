import pymel.core as pym
from MEm.xform import obj as oTM
reload(oTM)

def fixOrientation(jnt):
    name = jnt.name()
    sName = name.split("_")
    ctlName = "_".join(sName[:-1]) + "_control"
    offName = "_".join(sName[:-1]) + "_offgrp"
    oOff = pym.PyNode(offName)
    oCtl = pym.PyNode(ctlName)
    oParent = oOff.getParent()
    world = False
    if not oParent:
        world=True
    children = oCtl.getChildren(type="transform")
    if not world:
        print oParent.name()
    else:
        print "world"
    print children

    pym.parent(oCtl, w=1, a=1)
    pym.parent(oOff, w=1, a=1)

    oTM.copyTM(jnt, oOff)
    pym.parent(oCtl, oOff, a=1)
    pym.makeIdentity(oCtl, apply=True, translate=True, rotate=True, scale=True)

    if not world:
        pym.parent(oOff, oParent, a=1)
    for child in children:
        pym.parent(child, oCtl, a=1)


oS = pym.ls(sl=1, type="joint")
for o in oS:
    print o.name()
    fixOrientation(o)
