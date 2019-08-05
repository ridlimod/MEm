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
    confl = multFNdiffCS()
    for filecnf in confl:
        print "FILE:", filecnf
        for fileNode in confl[filecnf]:
            print "\t", fileNode.name(), fileNode.colorSpace.get()
