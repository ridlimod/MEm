### Align Controls

import MEm.chan.srt as srt; reload(srt)
import MEm.xform.obj as oXF; reload(oXF)


csrt = srt.srt
for ofg in pym.ls(sl=1, dag=1):
    if ofg.name().endswith("_offgrp"):
        jntref = ofg.name().rsplit("_",1)[0] + "_def"
        try:
            jnt = pym.PyNode(jntref)
        except:
            jnt = None
        if jnt is not None:
            print "match", ofg.name(), " with", jntref
            csrt.lockAttrs(ofg, False)
            csrt.keyAttrs(ofg, True)
            prnt = ofg.getParent()
            pym.parent(ofg, w=1, a=1)
            oXF.copyTM(jnt, ofg)
            pym.parent(ofg, prnt, a=1)
            csrt.lockAttrs(ofg, True)
            csrt.keyAttrs(ofg, False)
