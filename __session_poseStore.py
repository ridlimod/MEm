# Pose Store Test

import pymel.core as pym

poses = {}

posestore={}
for ctl in pym.ls(sl=1, type="transform"):
    print ctl.name()
    posestore[ctl.name()] = {
        "t": list(ctl.translate.get()),
        "r": list(ctl.rotate.get()),
        "s": list(ctl.scale.get())
    }

posestore
poses["mouth"] = posestore

poses

mpose = poses["mouth"]
for ctlname in mpose:
    ctl = pym.PyNode(ctlname)
    t = mpose[ctlname]["t"]
    r = mpose[ctlname]["r"]
    s = mpose[ctlname]["s"]
    for attr, tm in [("translate", t), ("rotate", r), ("scale", s)]:
        for axis, i in [("X", 0), ("Y", 1), ("Z", 2)]:
            attrName = attr + axis
            print attrName
            try:
                ctl.setAttr(attrName, tm[i])
            except:
                pass

# import json
# with open("poseLib.json", "w") as fh:
#    json.dump(poses, fh, indent=4)
