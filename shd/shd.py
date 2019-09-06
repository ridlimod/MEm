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
    shps = src.listRelatives(type="shape")
    if shps:
        shp = shps[0]
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


"""WIP COPIED FROM SESSION"""
def fixOverrideMat():
    lambertSE = pym.PyNode("initialShadingGroup")
    for obj in pym.ls(sl=1):
        shps = obj.listRelatives(shapes=True)
        if shps:
            shp = shps[0]
            SEs = shp.listConnections(type="shadingEngine", et=True, d=True)
            if SEs and len(SEs) == 1:
                SE = SEs[0]
                print "Cleaning", shp, "with", SE
                pym.sets(lambertSE, e=True, forceElement=shp.faces)
                pym.sets(SE, e=True, forceElement=shp.faces)


"""WIP COPIED FROM SESSION"""
def copyMatsToCache():
    for obj in pym.ls(sl=1, dag=1, type="transform"):
        shapes = obj.listRelatives(shapes=True)
        if shapes:
            shp = shapes[0]
            if obj.isVisible() and shp.isVisible() and shp.type()=="mesh":
                print obj.name(), obj.isVisible()
                tgtname = obj.name(stripNamespace=True)
                search = "|".join(map(lambda x: "caches:" + x, tgtname.split("|")))
                print "SEARCHING for:", search
                tgts = pym.ls(search)
                if tgts:
                    tgt = tgts[0]
                    print "FOUND:", tgt.name()
                    shd.copyMat(obj, tgt)


"""WIP COPIED FROM SESSION"""
def connectColorAndBump(shd1, shd2):
    bColor, bBump = None, None
    for node in pym.listHistory(shd1):
        if (
            node.type() == "file"
            and "basecolor" in node.name().lower()
        ):
            bColor = node
        if node.type() == "bump2d":
            bBump = node
        if bColor and bBump:
            break
    if bColor:
        bColor.outColor.connect(shd2.baseColor)
    if bBump:
        bBump.outNormal.connect(shd2.normalCamera)


def fixViewportShd():
    for obj in pym.selected():
        shps = obj.listRelatives(shapes=True)
        if shps:
            shp = shps[0]
            for se in shp.listSets(t=1):
                sS = se.surfaceShader.listConnections()
                aiSS = se.aiSurfaceShader.listConnections()
                if sS:
                    sS = sS[0]
                    baseColorN = sS.baseColor.listConnections()
                    if baseColorN:
                        baseColorN = baseColorN[0]
                        if not baseColorN.type() == "file":
                            print "Correct!"
                            sS.outColor.connect(se.aiSurfaceShader)
                            nSS = pym.duplicate(sS)[0]
                            nSS.rename(sS.name()[:-3] + "PRV")
                            nSS.outColor.connect(se.surfaceShader, force=True)
                            connectColorAndBump(sS, nSS)


""" Not used now, force bump type from filename
files = bBump.listHistory(type="file")
bI = bBump.bumpInterp.get()
if any(
    map(
        lambda x: "normal" in x.name().lower(), files
    )
) and bI != 1:
    bBump.bumpInterp.set(1)
elif any(
    map(
        lambda x: "bump" in x.name().lower(), files
    )
) and bI != 0:
    bBump.bumpInterp.set(0)
"""                                # bBump.bumpDepth.set(1)


def checkBumps(fix=False):
    sel = []
    for b2 in pym.ls(type="bump2d"):
        files = b2.listHistory(type="file")
        bI = b2.bumpInterp.get()
        if files:
            if any(
                map(lambda x: "normal" in x.name().lower(), files)
            ) and bI != 1:
                print "Wrong normal:", b2
                sel.append(b2)
                if fix:
                    b2.bumpInterp.set(1)

            if any(
                map(lambda x: "bump" in x.name().lower(), files)
            ) and bI != 0:
                print "Wrong bump:", b2
                sel.append(b2)
                if fix:
                    b2.bumpInterp.set(0)
    return sel


def getMeshNode(obj):
    obj = pym.PyNode(obj)
    if obj.type() == "transform":
        shps = obj.listRelatives(shapes=True)
        print shps
        if shps:
            obj = shps[0]
            print obj
            return obj
    if obj.type == "mesh":
        return obj
    return None


def copyMMAT(src, tgt):
    src = getMeshNode(src)
    tgt = getMeshNode(tgt)
    assert src and tgt, "select to mesh objects"
    for sg in src.listSets(t=1):
        for memb in sg.members():
            if type(memb) == pym.general.MeshFace:
                if memb.node() == src:
                    indx = memb.indices()
                    if indx:
                        pym.sets(sg, forceElement=tgt.faces[indx])
            elif type(memb) == pym.nodetypes.Mesh and memb == src:
                pym.sets(sg, forceElement=tgt)
