import pymel.core as pym


jntDrawStyle = {
    "None": 2,
    "Bone": 0,
    "Multi": 1
}


ncTypes = {
    "transform": "tm",
    "joint": "jnt",
    "locator": "loc",
    "nurbsCurve": "cv"
}


def setDrawStyle(jnt, drawStyle=jntDrawStyle["Bone"]):
    jnt.drawStyle.set(drawStyle)


def renameChain(jnt, namepattern, indxs, step=1):
    for jnt in pym.ls(jnt, dag=True, type="joint"):
        newname = namepattern.format(**indxs)
        pym.rename(jnt, newname)
        for key in indxs:
            indxs[key] += step


def createFKControlChain(start, end=None, p="world"):
    head = "_".join(start.name().split("_")[:-1])
    name = "{0}_{1}".format(head, "offgrp")
    ctlname = "{0}_fk_control".format(head)
    node = pym.createNode("transform", n=name)
    pym.parent(node, start, r=True)

    if p == "world":
        pym.parent(node, w=True, a=True)
    else:
        pym.parent(node, p, a=True)

    ctl = pym.createNode("transform", n=ctlname, p=node)

    if end is None or start != end:
        for child in start.getChildren(type="transform"):
            createFKControlChain(child, end, p=ctl.name())


def getJnt(ctl):
    if ctl.type() != "transform":
        ctl = ctl.getParent()
    jntname = "_".join(ctl.name().split("_")[0:3])+"_def"
    try:
        jnt = pym.PyNode(jntname)
    except pym.MayaNodeError as e:
        print "skip node:", jntname, e
        return
    return jnt


def getCtl(jnt, ctltype=""):
    if ctltype != "":
        ctlid = "_".join([ctltype, "control"])
    else:
        ctlid = "control"

    ctlname = pym.PyNode("_".join(jnt.name().split("_")[0:-1])+"_"+ctlid)
    print ctlname
    try:
        ctl = pym.PyNode(ctlname)
    except pym.MayaNodeError as e:
        print "skip node:", ctlname, e
        return
    return ctl


def addCtlRefShape(ref, ctl):
    refShapes = ref.listRelatives(shapes=True)
    i = 1
    for shape in refShapes:
        pym.parent(shape, ctl, r=True, s=True, add=True)
        i += 1


def rmCtlShape(ctl):
    for shape in ctl.listRelatives(shapes=True):
        pym.parent(shape, rm=True, s=True)


def replaceCtlRefShape(ref, ctl):
    rmCtlShape(ctl)
    addCtlRefShape(ref, ctl)


def uninstanceCtlShape(ctl):
    i = 1
    for shape in ctl.listRelatives(shapes=True):
        id, x, side, func = ctl.name().split("_", 3)
        shapename = "_".join(
            [
                id,
                "{0}{1:0>2}".format(x, i),
                side,
                func,
                "shp"]
        )
        shape.duplicate(name=shapename, addShape=True)[0]
        pym.parent(shape, rm=True, s=True)
        i += 1


def createCtlAt(ref, tm):
    offgrp = pym.createNode("transform", n="new_offgrp", p=tm)
    pym.parent(offgrp, a=True, w=True)
    ctl = pym.createNode("transform", n="new_control", p=offgrp)
    addCtlRefShape(ref, ctl)


def ctlColor(color):
    dColor = {
        blue: 6,
        red: 13,
        green: 14,
        yellow: 17
    }

    if color not in dColor:
        icolor = 1
    else:
        icolor = dColor[color]

    sel = (obj for obj in pym.ls(selection=True, dag=True) if obj.name().endswith("_control"))
    for s in sel:
        for shape in s.listRelatives(shapes=True):
            shape.overrideEnabled.set(0)
        s.overrideEnabled.set(1)
        s.overrideColor.set(icolor)
