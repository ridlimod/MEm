import pymel.core as pym


def sign(ctl, signature="MEm", RollRockRig=False):
    ctl = pym.PyNode(ctl)
    attrbs = {
        "rigtype": (signature, "string"),
        "RollRockRig": (RollRockRig, "bool")
    }
    for key in attrbs:
        val, type = attrbs[key]
        if not ctl.hasAttr(key):
            ctl.addAttr(key, type=type)
        ctl.attr(key).set(val)
