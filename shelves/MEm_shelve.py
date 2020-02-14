import pymel.core as pym
import MEm.jnt.tools
reload(MEm.jnt.tools)
import MEm.jnt.tools as mj

sel = pym.ls(selection=True)
objs, ref = sel[:-1],sel[-1]

for obj in objs:
    mj.createCtlAt(ref, obj)
