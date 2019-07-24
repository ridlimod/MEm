import pymel.core as pym


def copyUV(src, tgt):
    pym.polyTransfer(tgt, ch=False, ao=src)
    pym.bakePartialHistory(tgt, prePostDeformers=True)


def copyUVs(itersrc, nsdest):
    i = 0
    for oM in itersrc:
        tgtNodeName = "{0}:{1}".format(nsdest, oM.name(stripNamespace=1))
        try:
            tgt = pym.PyNode(tgtNodeName)
        except pym.MayaNodeError:
            tgt = None
        if tgt:
            print "transfering UVs", oM.name(), "to", tgt.name()
            copyUV(oM, tgt)
            i += 1
        else:
            print "not found", tgtNodeName
    print "transfered", i, "uvs"


def copyMat(src, tgt):
    shp = src.listRelatives(type="shape")[0]
    SE = shp.listConnections(type="shadingEngine", et=True, d=True)[0]
    tgtShape = tgt.listRelatives(shapes=True)[0]
    if SE:
        pym.sets(SE, e=True, forceElement=tgtShape)


def copyMats(itersrc, nsdest):
    i = 0
    j = 0
    for obj in itersrc:
        tgtName = "{0}:{1}".format(nsdest, obj.name(stripNamespace=True))
        try:
            tgt = pym.PyNode(tgtName)
        except pym.MayaNodeError:
            tgt = None
        if tgt:
            print "copying Mats", obj.name(), "to", tgt.name()
            copyMat(obj, tgt)
            i += 1
        else:
            print "not found", tgtName
            j += 1
    print "copied", i, "materials"
    print "not found", j, "objects"
