## IK SYS
import MEm.fkik as fkik; reload(fkik)
import pymel.core as pym


fkik.birdsys['attr']
attrRef = "leg_s_attributesShape"
ctlIkRef = "foot_s_ik_control"
ctlFKRef = "foot_s_fk_control"


for side in ["_l_", "_r_"]:
    attrName = attrRef.replace("_s_", side)
    ctlik_name = ctlIkRef.replace("_s_", side)
    ctlfk_name = ctlFKRef.replace("_s_", side)

    locShape = pym.createNode('locator', n=attrName)
    tm = locShape.getParent()

    for attr in locShape.listAttr():
        sShortAttrName = attr.shortName()
        if sShortAttrName != "FKIK":
            if attr.isInChannelBox():
                attr.showInChannelBox(False)

    locShape.addAttr("FKIK", type="float", max=1.0, min=0.0)
    locShape.FKIK.setKeyable(True)
    locShape.FKIK.setLocked(False)
    locShape.visibility.get()
    locShape.visibility.set(False)

    ctlfk = pym.PyNode(ctlfk_name)
    ctlik = pym.PyNode(ctlik_name)
    pym.parent(locShape, ctlfk, shape=True, r=True, add=True)
    pym.parent(locShape, ctlik, shape=True, r=True, add=True)

    pym.delete(tm)


"""
input2D[1].input2Dx --> _l_
input2D[1].input2Dy --> _r_
output2Dx --> _l_
output2Dy --> _r_
"""
subNode = pym.shadingNode("plusMinusAverage", n="IKFK", asUtility=True)
subNode.operation.set(2)
for side, chan in [("_l_", "x"), ("_r_", "y")]:
    attrName = attrRef.replace("_s_", side)
    locShape = pym.PyNode(attrName)
    subNode.setAttr("input2D[0].input2D{0}".format(chan), 1.0)
    locShape.FKIK.connect(subNode.attr("input2D[1].input2D{0}".format(chan)))


"""
Constraints
"""
constraints = [
    ("foot_s_ik_control", "ankle_01_s_def", "FKIK", "orientConstraint"),
    ("foot_s_ik_control", "leg_s_ikh_sys", None, "pointConstraint"),
    ("leg_01_s_ik_sys", "leg_01_s_def", "FKIK", "orientConstraint"),
    ("leg_02_s_ik_sys", "leg_02_s_def", "FKIK", "orientConstraint"),
    ("leg_01_s_fk_sys", "leg_01_s_def", "IKFK", "orientConstraint"),
    ("leg_02_s_fk_sys", "leg_02_s_def", "IKFK", "orientConstraint"),
    ("foot_s_fk_control", "ankle_01_s_def", "IKFK", "orientConstraint"),
    ("upperleg_s_fk_control", "leg_01_s_fk_sys", None, "orientConstraint"),
    ("lowerleg_s_fk_control", "leg_02_s_fk_sys", None, "orientConstraint"),
]

for source, target, w, type in constraints:
    for side, chan in [("_l_", "x"), ("_r_", "y")]:
        src = source.replace("_s_", side)
        tgt = target.replace("_s_", side)
        print "constraint:", type, "src:", src, "tgt:", tgt,
        if w:
            print "weighted:", w, chan
        else:
            print ""


import maya.cmds as mc
oC = getattr(pym, "orientConstraint")
c = oC("foot_l_fk_control", "ankle_01_l_def")


mc.orientConstraint("ankle_01_l_def", q=True, wal=True)
mc.orientConstraint("ankle_01_l_def", q=True, tl=True)
c.listAttr()
wAttr = c.attr("foot_l_fk_control" + "W1")
dir(wAttr)
wAttr.getAlias()
wAttr.name(includeNode=False)
locShape.FKIK.connect(wAttr)
subNode.output2Dx.connect(wAttr)
tl = oC("ankle_01_l_def", q=True, tl=True)
wal = oC("ankle_01_l_def", q=True, wal=True)
dW = dict(zip(tl, wal))
dW
pym.ls('ankle_01_l_def.foot_l_ik_controlW0')

for source, target, w, type in constraints:
    for side, chan in [("_l_", "x"), ("_r_", "y")]:
        src = source.replace("_s_", side)
        tgt = target.replace("_s_", side)
        print "constraint:", type, "src:", src, "tgt:", tgt,
        if w:
            print "weighted:", w, chan
        else:
            print ""
        fC = getattr(pym, type)
        mFC = getattr(mc, type)
        if src not int oC(tgt, q=True, tl=True):
            print "New"
            oC = fC(src, tgt)

for source, target, w, type in constraints:
    for side, chan in [("_l_", "x"), ("_r_", "y")]:
        src = source.replace("_s_", side)
        tgt = target.replace("_s_", side)
        fkik = attrRef.replace("_s_", side)
        fkik = pym.PyNode(fkik).attr("FKIK")
        ikfk = pym.PyNode("IKFK").attr("output2D" + chan)
        fC = getattr(pym, type)
        mFC = getattr(mc, type)
        tl = mFC(tgt, q=True, tl=True)
        wal = mFC(tgt, q=True, wal=True)
        dW = dict(zip(tl, wal))
        oC = mFC(tgt, q=True, n=True)
        if w == "IKFK":
            print "connect:", ikfk, "to:", dW[src]
            if not pym.isConnected(ikfk, ".".join([oC, dW[src]])):
                print "New"
                pym.connectAttr(ikfk, ".".join([oC, dW[src]]))
        elif w == "FKIK":
            print "connect:", fkik, "to:", dW[src]
            if not pym.isConnected(fkik, ".".join([oC, dW[src]])):
                print "New"
                pym.connectAttr(fkik, ".".join([oC, dW[src]]))


""" Vis connections """
conns = [
    ("FKIK", "foot_s_ik_control_shp.visibility"),
    ("FKIK", "polevectorLeg_s_control_shp.visibility"),
    ("IKFK", "foot_s_fk_control_shp.visibility"),
    ("IKFK", "lowerleg_s_fk_control_shp.visibility"),
    ("IKFK", "upperleg_s_fk_control_shp.visibility")
]

for side, chan in [("_l_", "x"), ("_r_", "y")]:
    fkik = attrRef.replace("_s_", side)
    fkik = pym.PyNode(fkik).attr("FKIK")
    ikfk = pym.PyNode("IKFK").attr("output2D" + chan)
    for con, attr in conns:
        attr = attr.replace("_s_", side)
        if con == "FKIK":
            print "connect:", fkik, "to:", attr
            if not pym.isConnected(fkik, attr):
                print "New"
                pym.connectAttr(fkik, attr)
        elif con == "IKFK":
            print "connect:", ikfk, "to:", attr
            if not pym.isConnected(ikfk, attr):
                print "New"
                pym.connectAttr(ikfk, attr)
