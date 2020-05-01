BaseCtl = pym.PyNode("featherHeadBase_01_c_fk_control")

for dctl in pym.ls(sl=1, dag=1, type="transform"):
    namep = dctl.name().split("_")
    id = namep[0]
    part = namep[1]
    side = namep[2]
    use = "_".join(namep[3:])
    print id, part, side, use
    if use == "driver_offgrp":
        continue
    if use == "driver_driven_offgrp":
        if part == "01":
            BaseCtl.rotate.connect(dctl.rotate)
        else:
            headOG = "_".join([id, part, side, "offgrp"])
            headOG = pym.PyNode(headOG)
            print "Ret:", headOG.name(), dctl.name()
            pym.parentConstraint(headOG, dctl)
    elif use == "driver_control" and part != "09":
        headDvn = "_".join([id, part, side, "driven", "offgrp"])
        headDvn = pym.PyNode(headDvn)
        print "Start:", dctl.name(), headDvn.name()
        pym.parentConstraint(dctl, headDvn)
        if part == "01":
            i = 2
            j = 5
        elif part == "05":
            i = 6
            j = 12
        else:
            continue
        print "Rot:", headDvn.name(), i, j
        for iPart in xrange(i, j):
            headNext = "_".join([id, "{0:0>2}".format(iPart), side, "driven", "offgrp"])
            headNext = pym.PyNode(headNext)
            print headDvn.name(), headNext.name()
            headDvn.rotate.connect(headNext.rotate)
            headDvn = headNext

# create driven transform grp con controls
import pymel.core as pym
from MEm.xform import obj as oTM

iter = (ctl for ctl in pym.ls(sl=1, dag=1, type="transform") if ctl.name().endswith("control"))

for ctl in iter:
    name = ctl.name()
    ctlP = ctl.getParent()
    if not "_driven_" in ctlP.name():
        fieldName = name.split("_")
        driveName = "_".join(fieldName[:-1]) + "_driven_offgrp"
        dTM = pym.createNode("transform", n=driveName, p=ctlP)
        pym.parent(ctl, dTM)
