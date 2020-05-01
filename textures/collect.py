import pymel.core as pym


def copyAlltoAsset(assetMaps):
    assetMaps = pym.Path(assetMaps)
    for fn in pym.ls(type="file"):
        ftn = pym.Path(fn.fileTextureName.get())
        if pym.Path(ftn).parent != assetMaps:
            tgt = assetMaps / ftn.basename()
            if not tgt.exists():
                print "copy:", ftn, "to:", assetMaps
                pym.Path.copy(ftn, assetMaps)


def diffCS(lFN):
    ref = None
    for node in lFN:
        if ref is None:
            ref = node.colorSpace.get()
        else:
            cmp = node.colorSpace.get()
            if cmp != ref:
                return True
    return False


def multFNdiffCS():
    fileNodes = {}
    for fn in pym.ls(type="file"):
        ftn = pym.Path(fn.fileTextureName.get())
        if ftn in fileNodes:
            fileNodes[ftn].append(fn)
        else:
            fileNodes[ftn] = [fn]

    multFN = filter(lambda x: diffCS(fileNodes[x]), fileNodes)
    filteredDict = {}
    for fn in multFN:
        filteredDict[fn] = fileNodes[fn]

    return filteredDict


def conflictTextures():
    sel = []
    confl = multFNdiffCS()
    for filecnf in confl:
        print "FILE:", filecnf
        for fileNode in confl[filecnf]:
            sel.append(fileNode)
            print "\t", fileNode.name(), fileNode.colorSpace.get()
    return sel


def getFilesByCS(*colorspaces):
    for fn in pym.ls(type="file"):
        cs = fn.colorSpace.get()
        if cs in colorspaces:
            yield fn


def getFilesWithUnusualCS():
    for fn in pym.ls(type="file"):
        cs = fn.colorSpace.get()
        print fn, cs
        if not any(map(lambda x: cs == ACES_colorSpace[x], ACES_colorSpace)):
            yield fn


ACES_colorSpace = {
    "srgb": u'Utility - sRGB - Texture',
    "raw": u'Utility - Raw',
    "p3-d60": u'Output - P3-D60'
}
