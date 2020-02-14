import pymel.core as pym
import os

DeltaMush_Attrs = [
    "envelope",
    "smoothingIterations",
    "smoothingStep",
    "inwardConstraint",
    "outwardConstraint",
    "distanceWeight",
    "pinBorderVertices",
    "displacement",
    "scale"
]


def reset(obj):
    obj = pym.PyNode(obj)
    dmN = pym.listHistory(obj, type="deltaMush")[0]
    scenePath = os.path.dirname(pym.sceneName())
    if scenePath == "":
        scenePath = pym.workspace.path
    fileName = os.path.basename(pym.sceneName())
    wmPath = os.path.join(
        scenePath,
        "_deformer_wm"
    ).replace("\\", "/")

    if not os.path.exists(wmPath):
        os.makedirs(wmPath)

    partName = obj.name()
    if ":" in partName:
        partName = partName.split(":")[-1]
    assetName = fileName.split("_")[0]
    wmName = "deltaMush_{0}_{1}.xml".format(partName, assetName)
    pym.deformerWeights(wmName, export=True, path=wmPath, deformer=dmN)
    dmAttrs = {}
    for attr in DeltaMush_Attrs:
        val = dmN.getAttr(attr)
        dmAttrs[attr] = val
    dmN.setGeometry([obj], rm=True)
    pym.delete(dmN)

    if obj.namespace() != '':
        dmNewName = "{0}:{1}_{2}_deltaMush".format(
            obj.namespace(), partName, assetName
        )
    else:
        dmNewName = "{0}_{1}_deltaMush".format(partName, assetName)

    dmN = pym.deltaMush(obj, n=dmNewName)
    for attr in dmAttrs:
        dmN.setAttr(attr, dmAttrs[attr])
    pym.deformerWeights(wmName, im=True, path=wmPath, deformer=dmN)


def connectScale(obj, ctl):
    obj = pym.PyNode(obj)
    ctl = pym.PyNode(ctl)
    dmN = pym.listHistory(obj, type="deltaMush")[0]
    try:
        ctl.scale.connect(dmN.scale)
    except Exception as e:
        print "ERROR:", e
