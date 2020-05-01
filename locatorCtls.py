import MEm.jnt.tools as jnt; reload(jnt)
import MEm.xform.obj
import pymel.core as pym

root = pym.ls(sl=1)[0]
jnt.createFKControlChain(root, control="ctlr", ctltype="locator")
locsize = 0.5
for loc in pym.ls(sl=1, dag=True, type="locator"):
    ctlTM = loc.getParent()
    jntSysName = "_".join(ctlTM.name().split("_")[0:3]) + "_sys"
    jntO = pym.PyNode(jntSysName)
    pym.parentConstraint(ctlTM, jntO)
