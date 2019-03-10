from MEm.chan.srt import srt
import pymel.core as pym


def deepControls(obj, tgt):
    if obj.name().endswith("_control"):
        print obj.name()
        offname = "_".join(obj.name().split("_")[:-1]) + "_offgrp"
        ctlparent = obj.getParent()
        offgrp = pym.createNode("transform", n=offname)
        pym.parent(offgrp, ctlparent, r=1)
        pym.parent(offgrp, tgt, a=1)
        ctlname = "_".join(obj.name().split("_")[:-1]) + "_side_control"
        sideCtl = pym.createNode("transform", p=offgrp, n=ctlname)
        attrState = srt.getState(obj)

        srt.lockAttrs(obj, False)
        srt.keyAttrs(obj, True)

        pym.parentConstraint(ctlparent, offgrp, mo=1)
        pym.parentConstraint(sideCtl, obj)

        srt.setState(sideCtl, attrState)

        for child in obj.getChildren():
            deepControls(child, sideCtl)
    else:
        for child in obj.getChildren():
            deepControls(child, tgt)
