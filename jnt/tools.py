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

def rename():
    pass


def chainInstance(jnt, objtype):
    for jnt in pym.ls(jnt, dag=True, type="joint"):
        name = "{0}_{1}".format(objtype, jnt.name())
        print "new obj:", name
        node = pym.createNode(objtype, n=name)
        if node.type() != "transform":
            node = node.getParent()
        pym.parent(node, jnt, r=True)
        pym.parent(node, w=True, a=True)


def chainInstanceR(jnt, objtype, p="world"):
    subname = "_".join(jnt.name().split("_")[:-1])
    name = "{0}_{1}".format(subname, ncTypes[objtype])
    print name
    ctlname = "{0}_control".format(subname)
    print ctlname
    node = pym.createNode(objtype, n=name)
    if node.type() != "transform":
        node = node.getParent()
    pym.parent(node, jnt, r=True)

    if p == "world":
        pym.parent(node, w=True, a=True)
    else:
        pym.parent(node, p, a=True)

    ctl = pym.createNode("transform", n=ctlname, p=node)

    for child in jnt.getChildren():
        if child.type() == "joint":
            chainInstanceR(child, objtype, p=ctl.name())


def chainCtlInstance(ref, jntList):
    for jnt in jntList:
        ctlname = pym.PyNode("_".join(jnt.name().split("_")[0:-1])+"_control")
        try:
            ctl = pym.PyNode(ctlname)
        except pym.MayaNodeError as e:
            print "skip node:", ctlname, e
            continue
        refInstance = ref.duplicate(name = "reftemp", ilf=True)
        refShapes = refInstance[0].listRelatives(shapes=True)
        i = 1
        for shape in refShapes:
            id, x, side, func = ctl.name().split("_")
            shapename = "_".join([id, "{0}{1:0>2}".format(x, i), side, "shp"])
            shape.rename(shapename)
            pym.parent(shape, ctl, r=True, s=True)
            i += 1
        pym.delete(refInstance)


def chainCtlInstanceR():
    base, ref = pym.ls(selection=True)
    baseCtl = pym.PyNode("_".join(base.name().split("_")[0:-1])+"_control")
    base.name(), baseCtl.name(), ref.name()
    for ctl in (ctl for ctl in pym.ls(baseCtl, dag=True, type="transform") if ctl.name().endswith("_control")):
        print ctl.name()
        i = 1
        refInstance = ref.duplicate(name = "reftemp", ilf=True)
        refShapes = refInstance[0].listRelatives(shapes=True)
        for shape in refShapes:
            id, x, side, func = ctl.name().split("_")
            shapename = "_".join([id, "{0}{1:0>2}".format(x, i), side, "shp"])
            shape.rename(shapename)
            pym.parent(shape, ctl, r=True, s=True)
            i += 1
        pym.delete(refInstance)
