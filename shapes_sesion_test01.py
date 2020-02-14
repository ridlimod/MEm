from MEm.shapes import shapes; reload(shapes)
import maya.cmds as mc

shapes.clear()
shapes.connect()
"""
cutKey -cl -t ":" -f ":" -at "eyebrow_L_frown" -at "eyebrow_L_up" -at "eyebrow_L_down" -at "eyebrow_R_frown" -at "eyebrow_R_up" -at "eyebrow_R_down" BODY_BS;

"""
pym.cutKey("EYEBROW_L_BS", at="eyebrow_L_down", cl=True)
mc.cutKey("EYEBROW_L_BS", at="eyebrow_L_up", cl=True)

from MEm import offgrp
reload(offgrp)

offgrp.lockAll()

import MEm.shapes.shapes as SHP; reload(SHP)
SHP.CleanShapes()

oSHP = SHP.Shapes("EYELID_DOWN_L")
oSHP.mirrorShapes("EYELID_DOWN_R")
oSHP.extractShapes()
oSHP.insertShapes("EYELID_DOWN_L", "EYELID_DOWN_L_BS_grp")

sel = pym.ls(sl=1, type="transform")
pym.blendShape(*sel)

bsn = pym.ls(sl=1)[0]
bsn.getTarget(index=1)
dir(bsn.weight[0])
bsn.weight[0].getAlias()
dir(bsn)
help(bsn.getTarget)

bsn.listAttr()
dir(bsn.attributeAliasList)
dir(bsn.inputTarget[0])
bsn.weight[0].set(0.0)

help(pym.duplicate)
help(pym.makeIdentity)

import pymel.core as pym
dir(pym.workspace)
pym.sceneName()
sel = pym.ls(sl=1, type="transform")
pym.blendShape(*sel)

for n in pym.ls(sl=1, type="transform"):
    name = n.name().replace("L", "R")
    pym.duplicate(n, n=name)


bsN = pym.ls(sl=1)[0]
bsN.type()
